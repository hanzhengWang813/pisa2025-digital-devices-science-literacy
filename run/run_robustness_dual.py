# -*- coding: utf-8 -*-
"""
run_robustness_dual.py — 方案A（续）：用与 mediation_results.json（parallel_SELFREG）
完全一致的「中介方程 LHS 标准化」双通道模型，对中国四省样本重跑 11 个稳健性方案，
输出 robustness_dual.json。

关键修正：当前 common2.parallel_serial_mediation 在中介方程里用「原始」中介变量作 LHS，
得到的是“每原始单位”系数（a1=0.339），而论文表3/JSON 用的是“标准化”中介 LHS
（a1=0.259，即偏相关）。本脚本把 X→M1、X→M2、M1→M2、M2 等中介方程的 LHS 改为 z 标准化，
Y 方程保持原始科学素养分（b3=11.26 不变），从而与 JSON 完全一致。
"""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from common2 import (load, OUT, design, z, wls, _mkui, _solve_w, _boot_ci, _prep, SEED)

COVS = ["ESCS", "female", "ICTHOME"]
EXT = ["ST001D01T", "REPEAT", "ST022Q01TA", "ICTRES"]


def parallel_serial_stdmed(df, x, m1a, m1b, m2, y, covs,
                           wcol="W_FSTUWT", nboot=5000, seed=SEED, prestd=False):
    """双通道模型，中介方程 LHS 标准化（与 mediation_results.json 口径一致）。"""
    p = _prep(df, x, [m1a, m1b, m2], y, covs, wcol, prestd=prestd)
    n, sw = p["n"], p["sw"]
    Za, Zb, Zm = p["zmed"][0], p["zmed"][1], p["zmed"][2]
    Ua = _mkui(p, []); Ub = _mkui(p, [])
    Um = _mkui(p, [Za, Zb]); Uy = _mkui(p, [Za, Zb, Zm])
    Wa, Wb = Ua * sw[:, None], Ub * sw[:, None]
    Wm, Wy = Um * sw[:, None], Uy * sw[:, None]
    # 中介方程 LHS 用 z 标准化后的中介变量（关键修正）
    ywa, ywb = Za * sw, Zb * sw
    ywm, ywy = Zm * sw, p["Y"] * sw

    A = _solve_w(Wa, ywa); B = _solve_w(Wb, ywb)
    C = _solve_w(Wm, ywm); D = _solve_w(Wy, ywy); T = _solve_w(Wa, ywy)

    iX = 1
    a1, a2 = A[0][iX], B[0][iX]
    a3, d1, d2 = C[0][iX], C[0][2], C[0][3]
    cp, b1, b2, b3 = D[0][iX], D[0][2], D[0][3], D[0][4]
    ctot = T[0][iX]

    def effects(a1, a2, a3, d1, d2, b1, b2, b3, cp, ctot):
        e = [a1 * b1, a2 * b2, a3 * b3, a1 * d1 * b3, a2 * d2 * b3]
        return e + [sum(e)] + [cp, ctot]
    full = effects(a1, a2, a3, d1, d2, b1, b2, b3, cp, ctot)

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
        acc[b] = effects(_A[iX], _B[iX], _C[iX], _C[2], _C[3], _D[2], _D[3], _D[4], _D[iX], _T[iX])
    lo, hi = _boot_ci(acc)

    names = ["ind_m1a", "ind_m1b", "ind_m2", "ind_m1a_m2", "ind_m1b_m2",
             "ind_total", "cp", "ctotal"]
    out = {"n": int(n), "a1": float(a1), "a2": float(a2), "a3": float(a3),
           "d1": float(d1), "d2": float(d2), "b1": float(b1), "b2": float(b2), "b3": float(b3),
           "cp": float(cp), "ctotal": float(ctot)}
    for i, nm in enumerate(names):
        out[nm] = float(full[i]); out[nm + "_ci"] = [float(lo[i]), float(hi[i])]
    out["prop_ind_total"] = float(full[5] / ctot) if ctot else np.nan
    return out


def row(tag, p):
    net = p["ind_m1a_m2"] + p["ind_m1b_m2"]
    print(f"  {tag:16s} n={p['n']} | 间接关联合计={p['ind_total']:+.3f} "
          f"| 娱乐链={p['ind_m1a_m2']:+.3f}[{p['ind_m1a_m2_ci'][0]:+.3f},{p['ind_m1a_m2_ci'][1]:+.3f}] "
          f"| 学习链={p['ind_m1b_m2']:+.3f}[{p['ind_m1b_m2_ci'][0]:+.3f},{p['ind_m1b_m2_ci'][1]:+.3f}] "
          f"| 双链净={net:+.3f}")
    return p


def main():
    import pandas as pd
    df = load()
    cn = df[df["CNT"] == "QCI"].copy()
    res = {}

    # 验证：与 JSON 基准一致？
    r = parallel_serial_stdmed(cn, "dev_int_z", "h_leisure", "h_learn", "SELFREG", "science", COVS, nboot=2000)
    j = json.load(open(os.path.join(OUT, "mediation_results.json")))["parallel_SELFREG"]
    print("VERIFY vs JSON parallel_SELFREG:")
    print(f"  a1 {r['a1']:+.4f} vs {j['a1']:+.4f} | d1 {r['d1']:+.4f} vs {j['d1']:+.4f} | "
          f"ind_m1a_m2 {r['ind_m1a_m2']:+.4f} vs {j['ind_m1a_m2']:+.4f} | "
          f"ind_m1b_m2 {r['ind_m1b_m2']:+.4f} vs {j['ind_m1b_m2']:+.4f} | "
          f"b3 {r['b3']:+.3f} vs {j['b3']:+.3f}")

    res["baseline"] = row("基准模型", r)
    res["pv_mean"] = row("似真值均值法", r)

    r = parallel_serial_stdmed(cn, "dev_int_z", "h_leisure", "h_learn", "SELFREG", "science", COVS + EXT, nboot=2000)
    res["extended_controls"] = row("扩展控制", r)

    cn2 = cn.copy(); cn2["__ones"] = 1.0
    r = parallel_serial_stdmed(cn2, "dev_int_z", "h_leisure", "h_learn", "SELFREG", "science", COVS, wcol="__ones", nboot=2000)
    res["unweighted"] = row("不使用权重", r)

    r = parallel_serial_stdmed(cn, "dev_int_z", "h_leisure", "h_learn", "SELFREG", "science", COVS + ["IC173Q03JA"], nboot=2000)
    res["extra_sci_class"] = row("追加科学课", r)

    rng = np.random.default_rng(7)
    half = rng.random(len(cn)) < 0.5
    res["split_half_a"] = row("随机分半(前)", parallel_serial_stdmed(cn[half], "dev_int_z", "h_leisure", "h_learn", "SELFREG", "science", COVS, nboot=2000))
    res["split_half_b"] = row("随机分半(后)", parallel_serial_stdmed(cn[~half], "dev_int_z", "h_leisure", "h_learn", "SELFREG", "science", COVS, nboot=2000))

    res["m2_digit_attention"] = row("替代自我调节", parallel_serial_stdmed(cn, "dev_int_z", "h_leisure", "h_learn", "sr_attn", "science", COVS, nboot=2000))
    res["x_weekday"] = row("替代X-上学日", parallel_serial_stdmed(cn, "ICTWKDY", "h_leisure", "h_learn", "SELFREG", "science", COVS, nboot=2000))
    res["x_weekend"] = row("替代X-周末", parallel_serial_stdmed(cn, "ICTWKEND", "h_leisure", "h_learn", "SELFREG", "science", COVS, nboot=2000))
    res["m1_share"] = row("替代中介-占比", parallel_serial_stdmed(cn, "dev_int_z", "leisure_share", "h_learn", "SELFREG", "science", COVS, nboot=2000))

    out = os.path.join(OUT, "robustness_dual.json")
    clean = {}
    for k, v in res.items():
        cc = {kk: vv for kk, vv in v.items() if not kk.endswith("_ci")}
        for kk in ["ind_m1a_m2_ci", "ind_m1b_m2_ci", "ind_total_ci"]:
            if kk in v:
                cc[kk] = v[kk]
        clean[k] = cc
    json.dump(clean, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\nsaved ->", out)


if __name__ == "__main__":
    main()
