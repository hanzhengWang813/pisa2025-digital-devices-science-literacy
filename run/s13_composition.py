# -*- coding: utf-8 -*-
"""
s13_composition.py — 「总量 + 构成」模型（10 个似真值 + 80 套 Fay-BRR + Rubin 合并）
=================================================================================
目的：直接检验「用法比用量更重要」这句话。
      模型 A（构成式）：literacy ~ 使用强度 + 总时长 + 娱乐占比 + 控制变量
              —— 总时长固定时，娱乐占比每高 10 个百分点，科学素养差多少分。
      模型 B（并列式）：literacy ~ 使用强度 + 学习时长 + 娱乐时长 + 控制变量
              —— 与现稿双通道模型的 b1/b2 对照（同一参数化的另一种写法）。

注意：h_total = (h_learn + h_leisure) / 2 仅在所有 6 题都作答时严格成立；
      个别缺失时 h_total 是可用题目的均值，与 (L+E)/2 略有不一致，
      因此模型 B 与现稿 b1/b2 会有小数级差异，属预期，可在表注说明。

运行：
    python s13_composition.py
输出：
    output/composition.json
    控制台打印两个模型的主要系数（含设计基础 95%CI）与可直接粘用的句子
"""
import os, json
import numpy as np

import common2 as C
from s7b_pv_models import rubin

PVS = ["PV%dSCIE" % i for i in range(1, 11)]
COVS = ["ESCS", "female", "ICTHOME"]
QNAMES = ["b_x", "b_total", "b_share", "b_learn", "b_leisure"]


def est_composition(d, ycol="science", wcol="W_FSTUWT"):
    """返回 [b_x, b_total, b_share, b_learn, b_leisure]（模型 A 与 B 拼在一起估计）。"""
    need = ["dev_int_z", "h_total", "leisure_share", "h_learn", "h_leisure", ycol] + COVS + [wcol]
    dd = d[need].dropna()
    if len(dd) < 500:
        return np.full(len(QNAMES), np.nan)
    w = dd[wcol].values.astype(float)
    y = dd[ycol].values.astype(float)

    X = C.z(dd["dev_int_z"].values)
    T = C.z(dd["h_total"].values)          # 总时长（每 SD）
    S = dd["leisure_share"].values.astype(float)   # 占比按 0-1 原尺度，便于解释「10 个百分点」
    L = C.z(dd["h_learn"].values)
    E = C.z(dd["h_leisure"].values)
    cov = [C._col(dd[c].values) for c in COVS]
    one = np.ones(len(dd))

    XA = np.column_stack([one, X, T, S] + cov)                    # 模型 A
    XB = np.column_stack([one, X, L, E] + cov)                    # 模型 B
    bA = C._solve_w(XA * np.sqrt(w)[:, None], y * np.sqrt(w))[0]
    bB = C._solve_w(XB * np.sqrt(w)[:, None], y * np.sqrt(w))[0]
    return np.array([bA[1], bA[2], bA[3], bB[2], bB[3]])


def brr_var(d, ycol):
    th = est_composition(d, ycol, "W_FSTUWT")
    reps = []
    for rc in C.REPW:
        try:
            reps.append(est_composition(d, ycol, rc))
        except Exception:
            continue
    reps = np.array(reps)
    return th, C.BRR_FACTOR * np.nansum((reps - th) ** 2, axis=0), len(reps)


def star(p):
    return "***" if p < .001 else "**" if p < .01 else "*" if p < .05 else ""


def load_all():
    """analysis + pv，按行序对齐（同 s14）。"""
    import pandas as pd
    df = C.load()
    pv = pd.read_parquet(os.path.join(C.OUT, "pv.parquet"))
    if len(pv) != len(df):
        raise RuntimeError("pv.parquet 与 analysis 行数不一致")
    return pd.concat([df.reset_index(drop=True), pv.reset_index(drop=True)], axis=1)


def main():
    df = load_all()
    cn = df[df["CNT"] == "QCI"].copy()
    TH, UU = [], []
    for p in PVS:
        th, u, nrep = brr_var(cn, p)
        TH.append(th); UU.append(u)
        print("  PV %s done (%d replicates)" % (p, nrep), flush=True)
    rb = rubin(np.array(TH), np.array(UU))

    res = {q: dict(est=float(rb["Q"][i]), se=float(rb["SE"][i]), df=float(rb["df"][i]),
                   p=float(rb["p"][i]), ci=[float(rb["ci_lo"][i]), float(rb["ci_hi"][i])])
           for i, q in enumerate(QNAMES)}

    print("\n" + "=" * 92)
    print("Model A  literacy ~ use frequency + total hours (per SD) + entertainment share")
    print("=" * 92)
    lbl = {"b_x": "use frequency (per SD)", "b_total": "total hours (per SD)",
           "b_share": "entertainment share (per 10 pp)"}
    for q in ["b_x", "b_total", "b_share"]:
        r = res[q]; e = r["est"] * (0.10 if q == "b_share" else 1.0)
        print("  %-30s %+8.2f%s  [%+8.2f, %+8.2f]  p=%.4f"
              % (lbl[q], e, star(r["p"]), r["ci"][0] * (0.10 if q == "b_share" else 1),
                 r["ci"][1] * (0.10 if q == "b_share" else 1), r["p"]))
    print("\nModel B  literacy ~ use frequency + learning hours + entertainment hours")
    for q, lab in [("b_learn", "learning hours (per SD)"), ("b_leisure", "entertainment hours (per SD)")]:
        r = res[q]
        print("  %-30s %+8.2f%s  [%+8.2f, %+8.2f]  p=%.4f"
              % (lab, r["est"], star(r["p"]), r["ci"][0], r["ci"][1], r["p"]))

    # ---- 可直接粘进论文的句子（数字已填） ----
    sh = res["b_share"]; sh10 = sh["est"] * 0.10
    sig = "was" if sh["p"] < .05 else "was not"
    print("\n可粘用句：")
    print("  At a fixed total amount of use, a 10-percentage-point shift toward entertainment was "
          "associated with %.2f points (95%% CI %.2f to %.2f, p = %.3f), which %s statistically "
          "significant." % (sh10, sh["ci"][0] * .1, sh["ci"][1] * .1, sh["p"], sig))

    with open(os.path.join(C.OUT, "composition.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("\nsaved ->", os.path.join(C.OUT, "composition.json"))


if __name__ == "__main__":
    main()
