# -*- coding: utf-8 -*-
"""
repro_paper.py — 《数字设备使用与青少年科学素养的关系》全部论文数据可复现脚本
====================================================================================
复现目标文档：
  F:/jjliu/program/数字设备使用与青少年科学素养的关系——基于PISA 2025数据的使用方式与自我调节的链式中介分析 (1).docx

重要口径说明
------------
论文表3(双通道)/表3补充(单通道)/表5(稳健性) 的中介系数（a1=0.259、链式 −0.188/+0.122、
−0.089 等）来自「中介方程左侧 z 标准化」口径。磁盘上 common2.py 的 serial_mediation /
parallel_serial_mediation 已统一为 z 标准化（p["zmed"]），因此主流程脚本（s2_mediation 等）
与本脚本现在给出完全一致的结果；本脚本仍**自带 std-LHS 中介实现**作为独立校验。注意：
旧版原始 LHS（p["raw"]）会得到 a1=0.339 等不同数值，该口径已弃用，仅出现在早期 markdown
母稿中，论文正式文档（含本 (1).docx）均使用 std-LHS 口径。

运行：
  python code/repro_paper.py
依赖：numpy, pandas, scipy, scikit-learn, pyreadstat（仅数据已落盘 analysis.parquet 时不需要）
数据：output/analysis.parquet, output/pv.parquet
"""
import os, sys, json
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
os.environ.setdefault("PISA_OUT2", os.path.join(ROOT, "output"))

import common2 as C
from common2 import load, z, _col, _solve_w, _prep, _mkui, design, wls
from sklearn.mixture import GaussianMixture

COVS = ["ESCS", "female", "ICTHOME"]
SEED = C.SEED


# ---------------------------------------------------------------------------
# 自带 std-LHS 中介实现（复现论文/JSON 数字）
# ---------------------------------------------------------------------------
def _boot_ci(arr):
    arr = arr[np.isfinite(arr).all(axis=1)] if arr.ndim == 2 else arr[np.isfinite(arr)]
    return np.percentile(arr, [2.5, 97.5], axis=0)


def serial_stdmed(df, x, m1, m2, y, covs, wcol="W_FSTUWT", nboot=5000, seed=SEED):
    """单通道串行 (PROCESS Model 6)，中介方程 LHS 用 z 标准化（论文口径）。"""
    p = _prep(df, x, [m1, m2], y, covs, wcol)
    n, sw = p["n"], p["sw"]
    Za, Zb = p["zmed"][0], p["zmed"][1]
    U1 = _mkui(p, []); U2 = _mkui(p, [Za]); U3 = _mkui(p, [Za, Zb])
    W1, W2, W3 = U1 * sw[:, None], U2 * sw[:, None], U3 * sw[:, None]
    yw1, yw2, yw3 = Za * sw, Zb * sw, p["Y"] * sw          # LHS 标准化
    b1_, s1_, _, p1_ = _solve_w(W1, yw1)
    b2_, s2_, _, p2_ = _solve_w(W2, yw2)
    b3_, s3_, _, p3_ = _solve_w(W3, yw3)
    bT, sT_, _, pT_ = _solve_w(W1, yw3)
    iX, iM1, iM2 = 1, 2, 3
    a1, a2, d21 = b1_[iX], b2_[iX], b2_[iM1]
    cp, bY1, bY2 = b3_[iX], b3_[iM1], b3_[iM2]
    ctot = bT[iX]
    ind1, ind2, ind3 = a1 * bY1, a2 * bY2, a1 * d21 * bY2
    rng = np.random.default_rng(seed)
    pr = p["W"] / p["W"].sum()
    acc = np.full((nboot, 8), np.nan)
    for b in range(nboot):
        ix = rng.choice(n, size=n, replace=True, p=pr)
        try:
            A = _solve_w(W1[ix], yw1[ix])[0]; B = _solve_w(W2[ix], yw2[ix])[0]
            C = _solve_w(W3[ix], yw3[ix])[0]; T = _solve_w(W1[ix], yw3[ix])[0]
        except np.linalg.LinAlgError:
            continue
        _a1, _a2, _d21 = A[iX], B[iX], B[iM1]
        _cp, _by1, _by2 = C[iX], C[iM1], C[iM2]
        acc[b] = [_a1 * _by1, _a2 * _by2, _a1 * _d21 * _by2,
                  _a1 * _by1 + _a2 * _by2 + _a1 * _d21 * _by2, _cp, T[iX], _by2, _d21]
    lo, hi = _boot_ci(acc)
    return dict(n=int(n), a1=float(a1), a2=float(a2), d21=float(d21), b1=float(bY1),
                b2=float(bY2), cp=float(cp), ctotal=float(ctot),
                ind1=float(ind1), ind2=float(ind2), ind3=float(ind3),
                ind_total=float(ind1 + ind2 + ind3),
                ind3_ci=[float(lo[2]), float(hi[2])],
                ind_total_ci=[float(lo[3]), float(hi[3])],
                a1_p=float(p1_[iX]), d21_p=float(p2_[iM1]), b2_p=float(p3_[iM2]),
                cp_p=float(p3_[iX]), ctotal_p=float(pT_[iX]))


def parallel_stdmed(df, x, m1a, m1b, m2, y, covs, wcol="W_FSTUWT", nboot=5000, seed=SEED):
    """双通道平行—序列，中介方程 LHS 用 z 标准化（论文口径）。"""
    p = _prep(df, x, [m1a, m1b, m2], y, covs, wcol)
    n, sw = p["n"], p["sw"]
    Za, Zb, Zm = p["zmed"][0], p["zmed"][1], p["zmed"][2]
    Ua = _mkui(p, []); Ub = _mkui(p, []); Um = _mkui(p, [Za, Zb]); Uy = _mkui(p, [Za, Zb, Zm])
    Wa, Wb = Ua * sw[:, None], Ub * sw[:, None]
    Wm, Wy = Um * sw[:, None], Uy * sw[:, None]
    ywa, ywb = Za * sw, Zb * sw
    ywm, ywy = Zm * sw, p["Y"] * sw
    A = _solve_w(Wa, ywa); B = _solve_w(Wb, ywb)
    C = _solve_w(Wm, ywm); D = _solve_w(Wy, ywy); T = _solve_w(Wa, ywy)
    iX = 1
    a1, a2 = A[0][iX], B[0][iX]
    a3, d1, d2 = C[0][iX], C[0][2], C[0][3]
    cp, b1, b2, b3 = D[0][iX], D[0][2], D[0][3], D[0][4]
    ctot = T[0][iX]

    def eff(a1, a2, a3, d1, d2, b1, b2, b3, cp, ctot):
        e = [a1 * b1, a2 * b2, a3 * b3, a1 * d1 * b3, a2 * d2 * b3]
        return e + [sum(e)] + [cp, ctot]
    full = eff(a1, a2, a3, d1, d2, b1, b2, b3, cp, ctot)
    rng = np.random.default_rng(seed)
    pr = p["W"] / p["W"].sum()
    acc = np.full((nboot, 8), np.nan)
    for b in range(nboot):
        ix = rng.choice(n, size=n, replace=True, p=pr)
        try:
            _A = _solve_w(Wa[ix], ywa[ix])[0]; _B = _solve_w(Wb[ix], ywb[ix])[0]
            _C = _solve_w(Wm[ix], ywm[ix])[0]; _D = _solve_w(Wy[ix], ywy[ix])[0]
            _T = _solve_w(Wa[ix], ywy[ix])[0]
        except np.linalg.LinAlgError:
            continue
        acc[b] = eff(_A[iX], _B[iX], _C[iX], _C[2], _C[3], _D[2], _D[3], _D[4], _D[iX], _T[iX])
    lo, hi = _boot_ci(acc)
    names = ["ind_m1a", "ind_m1b", "ind_m2", "ind_m1a_m2", "ind_m1b_m2", "ind_total", "cp", "ctotal"]
    out = dict(n=int(n), a1=float(a1), a2=float(a2), a3=float(a3), d1=float(d1), d2=float(d2),
               b1=float(b1), b2=float(b2), b3=float(b3), cp=float(cp), ctotal=float(ctot))
    for i, nm in enumerate(names):
        out[nm] = float(full[i]); out[nm + "_ci"] = [float(lo[i]), float(hi[i])]
    return out


# ---------------------------------------------------------------------------
# 复现主流程
# ---------------------------------------------------------------------------
def wcorr(x, y, w):
    m = np.isfinite(x) & np.isfinite(y) & np.isfinite(w)
    x, y, w = x[m], y[m], w[m]
    mx, my = np.average(x, weights=w), np.average(y, weights=w)
    dx, dy = x - mx, y - my
    return float(np.sum(w * dx * dy) / np.sqrt(np.sum(w * dx * dx) * np.sum(w * dy * dy)))


def main():
    OUT = C.OUT
    df = load()
    cn = df[df["CNT"] == "QCI"].copy()
    res = {}

    # ---- 表1 描述统计 / 表2 相关（s1_constructs.py）----
    desc = pd.read_csv(os.path.join(OUT, "desc_cn.csv"))
    corr = pd.read_csv(os.path.join(OUT, "corr_cn.csv"), index_col=0)
    res["表1_描述统计"] = desc.to_dict("records")
    res["表2_相关矩阵"] = corr.to_dict()

    # ---- 表3 双通道（parallel_SELFREG，s2_mediation.py）----
    P = parallel_stdmed(cn, "dev_int_z", "h_leisure", "h_learn", "SELFREG", "science", COVS, nboot=5000)
    res["表3_双通道"] = {k: round(P[k], 4) for k in
                         ["a1", "a2", "d1", "d2", "b1", "b2", "b3",
                          "ind_m1a_m2", "ind_m1b_m2", "ind_total", "ctotal"]}
    res["表3_双通道"]["链式净_点估计"] = round(P["ind_m1a_m2"] + P["ind_m1b_m2"], 4)

    # ---- 表3 补充 单通道串行（main，s2_mediation.py）----
    S = serial_stdmed(cn, "dev_int_z", "h_leisure", "SELFREG", "science", COVS, nboot=5000)
    res["表3补充_单通道"] = {k: round(S[k], 4) for k in
                            ["a1", "d21", "b2", "cp", "ctotal", "ind3", "ind_total"]}

    # ---- 表4 潜在剖面（s5_lpa.py）----
    lp = pd.read_csv(os.path.join(OUT, "lpa_profiles.csv"))
    res["表4_LPA"] = lp.to_dict("records")
    lpa = json.load(open(os.path.join(OUT, "lpa_results.json"), encoding="utf-8"))
    res["表4_LPA_k"] = lpa["k"]
    res["表4_LPA_BIC_k4"] = [t for t in lpa["bic_table"] if t["k"] == 4][0]
    res["表4_LPA_contrasts"] = {
        "science": lpa["contrasts"]["science"],
        "SELFREG_学习主导型": lpa["contrasts"]["SELFREG"]["学习主导型"],
        "sr_attn_学习主导型": lpa["contrasts"]["sr_attn"]["学习主导型"],
    }

    # ---- 表5 稳健性（单通道 std-LHS，s2 变体 + s4 稳健性）----
    ext = ["ST001D01T", "REPEAT", "ST022Q01TA", "ICTRES"]
    cn2 = cn.copy(); cn2["__ones"] = 1.0
    rng = np.random.default_rng(7); half = rng.random(len(cn)) < 0.5
    pv = json.load(open(os.path.join(OUT, "pv_mediation.json"), encoding="utf-8"))
    variants = {
        "基准模型(似真值分别估计+Rubin合并)": S,                              # s2 main = serial_stdmed
        "似真值均值法(对照)": pv["serial"]["mean_pv_practice"],                # s7b
        "扩展控制": serial_stdmed(cn, "dev_int_z", "h_leisure", "SELFREG", "science", COVS + ext, nboot=3000),
        "不使用权重": serial_stdmed(cn2, "dev_int_z", "h_leisure", "SELFREG", "science", COVS, wcol="__ones", nboot=3000),
        "追加控制科学课数字资源": serial_stdmed(cn, "dev_int_z", "h_leisure", "SELFREG", "science", COVS + ["IC173Q03JA"], nboot=3000),
        "随机分半(前半)": serial_stdmed(cn[half], "dev_int_z", "h_leisure", "SELFREG", "science", COVS, nboot=3000),
        "随机分半(后半)": serial_stdmed(cn[~half], "dev_int_z", "h_leisure", "SELFREG", "science", COVS, nboot=3000),
        "替代自我调节测量(数字注意调节)": serial_stdmed(cn, "dev_int_z", "h_leisure", "sr_attn", "science", COVS, nboot=3000),
        "替代自变量(上学日使用频率)": serial_stdmed(cn, "ICTWKDY", "h_leisure", "SELFREG", "science", COVS, nboot=3000),
        "替代自变量(周末使用频率)": serial_stdmed(cn, "ICTWKEND", "h_leisure", "SELFREG", "science", COVS, nboot=3000),
        "替代中介(娱乐使用占比)": serial_stdmed(cn, "dev_int_z", "leisure_share", "SELFREG", "science", COVS, nboot=3000),
    }
    rob_rows = []
    for nm, v in variants.items():
        it = v["ind_total"]; ch = v.get("ind3", {})
        it = it["est"] if isinstance(it, dict) else it
        ch = ch["est"] if isinstance(ch, dict) else ch
        ct = v["ctotal"]; ct = ct["est"] if isinstance(ct, dict) else ct
        rob_rows.append(dict(检验方案=nm, 间接关联合计=round(it, 2),
                             链式路径=round(ch, 3),
                             占比=round(100 * it / ct, 1)))
    res["表5_稳健性"] = rob_rows

    # ---- (五)/(四) 缓冲交互（s4_multigroup.py）----
    rob = json.load(open(os.path.join(OUT, "robustness.json"), encoding="utf-8"))
    res["(五)_缓冲交互"] = {k: round(rob["buffering"][k], 3)
                          for k in ["interaction", "sr_slope_low_leisure", "sr_slope_high_leisure"]}

    # ---- (二) 总效应 + RCS（s7b PV pooled / s8_rcs.py）----
    rcs = json.load(open(os.path.join(OUT, "rcs_results.json"), encoding="utf-8"))
    sp = pv["serial"]["pooled_pv"]
    res["(二)_总效应与RCS"] = dict(
        总效应_est=round(sp["ctotal"]["est"], 2), 总效应_ci=[round(x, 2) for x in sp["ctotal"]["ci"]],
        间接合计_PV=round(sp["ind_total"]["est"], 2),
        RCS_nonlinear_coef=round(rcs["nonlinear_coef"], 2), RCS_p=round(rcs["nonlinear_p"], 4))

    # ---- 摘要关键数 ----
    cs = json.load(open(os.path.join(OUT, "constructs.json"), encoding="utf-8"))
    res["摘要"] = dict(
        n=cs["cn_n"],
        c_total=round(sp["ctotal"]["est"], 2),
        d1=round(P["d1"], 3), d2=round(P["d2"], 3),
        chain_ent=round(P["ind_m1a_m2"], 3), chain_learn=round(P["ind_m1b_m2"], 3),
        slope_low=round(rob["buffering"]["sr_slope_low_leisure"], 2),
        slope_high=round(rob["buffering"]["sr_slope_high_leisure"], 2),
    )
    print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
    return res


if __name__ == "__main__":
    main()
