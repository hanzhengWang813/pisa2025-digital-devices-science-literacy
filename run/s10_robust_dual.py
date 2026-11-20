# -*- coding: utf-8 -*-
"""
s10_robust_dual.py — 表5 稳健性检验：只报双通道（带标准误与显著性）
=====================================================================
论文摘要与结论的落脚点是双通道模型的两条链式效应：
  · 娱乐链  a1·d1·b3（X → 娱乐性使用 → 自我调节 → 科学素养）
  · 学习链  a2·d2·b3（X → 学习性使用 → 自我调节 → 科学素养）
  · 间接合计（双通道模型中五条间接路径之和）
表5 因此只报告这三个量，不再并列单通道结果（单通道点估计仍写入 json 备查，
字段名加 single_ 前缀，论文不引用）。

推断口径与 s7b_pv_models 完全一致，稳健性表因此可以标显著性：
  1) 对 PV1..PV10 各自估计同一方案（同一 est_parallel、同一标准化方式）
  2) 每个 PV 用 80 套 Fay-BRR 复制权重（ρ=0.5，factor=1/[H(1-ρ)²]=1/20）得 U_k
  3) Rubin 合并：T = Ū + (1+1/M)B，t 检验自由度按 Rubin 公式
例外：unweighted 方案不使用抽样权重，复制权重法对其不成立（无权重估计对每套
复制权重都相同，方差恒为 0），改用 500 次简单随机重抽样求 SE。

基准行（PV 分别估计 + Rubin 合并）与「似真值均值法」行直接取自
results/pv_mediation.json，与表3 同源。

产出：results/robustness_dual.json
  est/se/df/t/p/ci 均为长度 3 的列表，顺序 = [娱乐链, 学习链, 间接合计]
"""
import os, json
import numpy as np
import pandas as pd
from scipy import stats
import common2 as C
import s7b_pv_models as S

EXT = ["ST001D01T", "REPEAT", "ST022Q01TA", "ICTRES"]
PVS = ["PV%dSCIE" % i for i in range(1, 11)]
M = len(PVS)
NB = 500          # unweighted 方案的简单随机重抽样次数
IDX = [S.PAR_Q.index("ind_m1a_m2"), S.PAR_Q.index("ind_m1b_m2"), S.PAR_Q.index("ind_total")]


def pool_brr(d, x, m1a, m1b, m2, wcol, covs):
    """10 个 PV × 80 套复制权重 → Rubin 合并（只留三个链式量）。"""
    TH, UU = [], []
    for p in PVS:
        th = S.est_parallel(d, p, wcol, x=x, m1a=m1a, m1b=m1b, m2=m2, covs=covs)
        reps = []
        for rc in C.REPW:
            try:
                reps.append(S.est_parallel(d, p, rc, x=x, m1a=m1a, m1b=m1b, m2=m2, covs=covs))
            except Exception:
                continue
        reps = np.array(reps)
        TH.append(th)
        UU.append(C.BRR_FACTOR * np.nansum((reps - th) ** 2, axis=0))
    TH = np.array(TH)[:, IDX]
    UU = np.array(UU)[:, IDX]
    rb = S.rubin(TH, UU)
    return dict(est=[float(v) for v in rb["Q"]], se=[float(v) for v in rb["SE"]],
                df=[float(v) for v in rb["df"]], t=[float(v) for v in rb["t"]],
                p=[float(v) for v in rb["p"]],
                ci=[[float(a), float(b)] for a, b in zip(rb["ci_lo"], rb["ci_hi"])],
                per_pv_min=[float(np.nanmin(TH[:, i])) for i in range(3)],
                per_pv_max=[float(np.nanmax(TH[:, i])) for i in range(3)],
                method="fay_brr_rubin")


def boot_iid(d, x, m1a, m1b, m2, covs, rng):
    """无权重方案：简单随机重抽样（i.i.d. bootstrap），给出三个链式量的 SE。"""
    n = len(d)
    vals = np.empty((NB, 3))
    for i in range(NB):
        s = d.iloc[rng.integers(0, n, n)]
        vals[i] = S.est_parallel(s, S.YM, "__ones", x=x, m1a=m1a, m1b=m1b, m2=m2, covs=covs)[IDX]
    est = S.est_parallel(d, S.YM, "__ones", x=x, m1a=m1a, m1b=m1b, m2=m2, covs=covs)[IDX]
    se = np.nanstd(vals, axis=0, ddof=1)
    return dict(est=[float(v) for v in est], se=[float(v) for v in se],
                df=[float(n - 1)] * 3, t=[float(v) for v in est / se],
                p=[float(v) for v in 2 * stats.norm.sf(np.abs(est / se))],
                ci=[[float(a), float(b)] for a, b in zip(est - 1.96 * se, est + 1.96 * se)],
                method="iid_bootstrap_%d" % NB)


def run():
    df = C.load()
    pv = C.read_frame(os.path.join(C.OUT, "pv"))
    df = pd.concat([df.reset_index(drop=True), pv.reset_index(drop=True)], axis=1)
    cn = df[df["CNT"] == "QCI"].copy()
    cn["__ones"] = 1.0

    rng = np.random.default_rng(7)
    half = rng.random(len(cn)) < 0.5

    scen = [
        # (名称, 数据, X, 第一中介(娱乐), 第二中介, 权重列, 控制变量)
        ("extended_controls", cn, "dev_int_z", "h_leisure", "SELFREG", "W_FSTUWT", S.COVS + EXT),
        ("unweighted", cn, "dev_int_z", "h_leisure", "SELFREG", "__ones", S.COVS),
        ("extra_sci_class", cn, "dev_int_z", "h_leisure", "SELFREG", "W_FSTUWT", S.COVS + ["IC173Q03JA"]),
        ("split_half_a", cn[half], "dev_int_z", "h_leisure", "SELFREG", "W_FSTUWT", S.COVS),
        ("split_half_b", cn[~half], "dev_int_z", "h_leisure", "SELFREG", "W_FSTUWT", S.COVS),
        ("alt_selfreg", cn, "dev_int_z", "h_leisure", "sr_attn", "W_FSTUWT", S.COVS),
        ("alt_x_weekday", cn, "ICTWKDY", "h_leisure", "SELFREG", "W_FSTUWT", S.COVS),
        ("alt_x_weekend", cn, "ICTWKEND", "h_leisure", "SELFREG", "W_FSTUWT", S.COVS),
        ("alt_mediator_share", cn, "dev_int_z", "leisure_share", "SELFREG", "W_FSTUWT", S.COVS),
    ]

    out = {}
    for tag, d, x, m1, m2, w, covs in scen:
        n = int(S._blocks(d, x, [m1, "h_learn", m2], S.YM, covs, w)["n"])
        if w == "__ones":
            r = boot_iid(d, x, m1, "h_learn", m2, covs, rng)
        else:
            r = pool_brr(d, x, m1, "h_learn", m2, w, covs)
        ser = S.est_serial(d, S.YM, w, x=x, m1=m1, m2=m2, covs=covs)
        r.update(n=n, single_ent=float(dict(zip(S.SERIAL_Q, ser))["ind3"]))
        out[tag] = r
        print("%-20s n=%5d | 娱乐链 %+0.3f (se %.3f p=%.3f) 学习链 %+0.3f (se %.3f p=%.3f)"
              " | 合计 %+0.3f (se %.2f p=%.3f) | 单通道 %+0.3f"
              % (tag, n, r["est"][0], r["se"][0], r["p"][0], r["est"][1], r["se"][1], r["p"][1],
                 r["est"][2], r["se"][2], r["p"][2], r["single_ent"]), flush=True)

    # 基准（PV 分别估计 + Rubin 合并）与「似真值均值法」：沿用 s7b 的产出，与表3 同源
    pvm = json.load(open(os.path.join(C.OUT, "pv_mediation.json"), encoding="utf-8"))
    par, mp = pvm["parallel"]["pooled_pv"], pvm["parallel"]["mean_pv_practice"]
    q3 = ["ind_m1a_m2", "ind_m1b_m2", "ind_total"]
    out["baseline_pv_pooled"] = dict(
        n=pvm["parallel"]["n"], method="fay_brr_rubin",
        est=[par[q]["est"] for q in q3], se=[par[q]["se"] for q in q3],
        df=[par[q]["df"] for q in q3], t=[par[q]["t"] for q in q3],
        p=[par[q]["p"] for q in q3], ci=[par[q]["ci"] for q in q3],
        per_pv_min=[par[q]["per_pv_min"] for q in q3],
        per_pv_max=[par[q]["per_pv_max"] for q in q3])
    est = [mp[q]["est"] for q in q3]
    se = [mp[q]["se"] for q in q3]
    out["mean_pv_practice"] = dict(
        n=pvm["parallel"]["n"], method="fay_brr_normal_p",
        est=est, se=se, df=[1e6] * 3, t=[a / b for a, b in zip(est, se)],
        p=[float(2 * stats.norm.sf(abs(a / b))) for a, b in zip(est, se)],
        ci=[[a - 1.96 * b, a + 1.96 * b] for a, b in zip(est, se)])
    print("%-20s n=%5d | 娱乐链 %+0.3f (se %.3f p=%.4f) 学习链 %+0.3f (se %.3f p=%.4f)"
          " | 合计 %+0.3f" % ("baseline_pv_pooled", out["baseline_pv_pooled"]["n"],
                              out["baseline_pv_pooled"]["est"][0], out["baseline_pv_pooled"]["se"][0],
                              out["baseline_pv_pooled"]["p"][0], out["baseline_pv_pooled"]["est"][1],
                              out["baseline_pv_pooled"]["se"][1], out["baseline_pv_pooled"]["p"][1],
                              out["baseline_pv_pooled"]["est"][2]), flush=True)

    with open(os.path.join(C.OUT, "robustness_dual.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("已写出 output/robustness_dual.json（est/se/p 顺序 = 娱乐链, 学习链, 合计）", flush=True)


if __name__ == "__main__":
    run()
