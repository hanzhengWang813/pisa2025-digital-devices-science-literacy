# -*- coding: utf-8 -*-
"""
s16_pooled_pv.py — 23 经济体合并模型：PV + BRR + Rubin（设计基础推断）
=====================================================================
原稿的合并估计来自 s4_multigroup.py，用加权 bootstrap 且只报点估计。
本脚本用与主模型相同的引擎（10 个 PV × 80 套 Fay-BRR × Rubin 合并）重做，
使「23 个经济体」这句话带有设计基础的置信区间。

要点：
  * 经济体筛选规则与 s4 完全一致（四个关键变量缺失率 < 20% 且 n >= 2000），
    输出纳入的经济体名单，正文必须写明这条规则。
  * 变量已在经济体内部标准化（_w 结尾），因此不再二次标准化，
    系数单位为「本国标准差」，与正文的 SD 表述一致。
  * 协变量：ESCS_w, female, ICTHOME_w（female 为 0/1，保持原样）。
输出：output/pooled_pv.json
"""
import os, json
import numpy as np
import pandas as pd

import common2 as C
from s7b_pv_models import rubin, PAR_Q

PVS = ["PV%dSCIE" % i for i in range(1, 11)]
COVS = ["ESCS_w", "female", "ICTHOME_w"]
X, M1a, M1b, M2, Y = "dev_int_w", "h_leisure_w", "h_learn_w", "SELFREG_w", "science_w"


def select_economies(df):
    keep, sizes = [], {}
    for e, g in df.groupby("CNT"):
        ok = (g["ICTWKDY"].notna().mean() > .8 and g["h_leisure"].notna().mean() > .8 and
              g["SELFREG"].notna().mean() > .8 and g["ESCS"].notna().mean() > .8 and len(g) >= 2000)
        sizes[e] = int(len(g))
        if ok:
            keep.append(e)
    return sorted(keep), sizes


def est(d, ycol, wcol):
    """平行—序列模型，变量已组内标准化，不再二次 z。"""
    need = [X, M1a, M1b, M2, ycol] + COVS + [wcol]
    dd = d[need].dropna()
    n = len(dd)
    if n < 500:
        return np.full(len(PAR_Q), np.nan)
    w = dd[wcol].values.astype(float)
    one = np.ones(n)
    Xv = dd[X].values.astype(float)
    Za = dd[M1a].values.astype(float)
    Zb = dd[M1b].values.astype(float)
    Zm = dd[M2].values.astype(float)
    Yv = dd[ycol].values.astype(float)
    covc = [C._col(dd[c].values) for c in COVS]
    Ua = np.column_stack([one, Xv] + covc)
    Um = np.column_stack([one, Xv, Za, Zb] + covc)
    Uy = np.column_stack([one, Xv, Za, Zb, Zm] + covc)
    sw = np.sqrt(w)
    A = C._solve_w(Ua * sw[:, None], Za * sw)[0]
    Bv = C._solve_w(Ua * sw[:, None], Zb * sw)[0]
    Cc = C._solve_w(Um * sw[:, None], Zm * sw)[0]
    D = C._solve_w(Uy * sw[:, None], Yv * sw)[0]
    T = C._solve_w(Ua * sw[:, None], Yv * sw)[0]
    a1, a2 = A[1], Bv[1]
    a3, d1, d2 = Cc[1], Cc[2], Cc[3]
    cp, b1, b2, b3 = D[1], D[2], D[3], D[4]
    ct = T[1]
    e = [a1 * b1, a2 * b2, a3 * b3, a1 * d1 * b3, a2 * d2 * b3]
    return np.array([a1, a2, a3, d1, d2, b1, b2, b3, cp, ct] + e + [sum(e)])


def brr(d, ycol):
    th = est(d, ycol, "W_FSTUWT")
    reps = []
    for rc in C.REPW:
        try:
            reps.append(est(d, ycol, rc))
        except Exception:
            continue
    reps = np.array(reps)
    return th, C.BRR_FACTOR * np.nansum((reps - th) ** 2, axis=0), len(reps)


def main():
    df = C.load()
    pv = pd.read_parquet(os.path.join(C.OUT, "pv.parquet"))
    df = pd.concat([df.reset_index(drop=True), pv.reset_index(drop=True)], axis=1)

    keep, sizes = select_economies(df)
    gw = df[df["CNT"].isin(keep)].copy()
    print("纳入经济体 %d 个：%s" % (len(keep), ", ".join(keep)), flush=True)
    print("合并样本 n =", len(gw), flush=True)

    TH, UU = [], []
    for p in PVS:
        th, u, nrep = brr(gw, p)
        TH.append(th); UU.append(u)
        print("  %s done (%d replicates)" % (p, nrep), flush=True)
    rb = rubin(np.array(TH), np.array(UU))

    res = {q: dict(est=float(rb["Q"][i]), se=float(rb["SE"][i]), df=float(rb["df"][i]),
                   p=float(rb["p"][i]), ci=[float(rb["ci_lo"][i]), float(rb["ci_hi"][i])])
           for i, q in enumerate(PAR_Q)}
    res["_meta"] = dict(n=int(len(gw)), k_econ=len(keep), economies=keep,
                        k_students_all=int(len(df)))

    print("\n" + "=" * 76)
    print("Pooled %d-economy model (design-based)" % len(keep))
    print("=" * 76)
    for q in ["ctotal", "cp", "d1", "d2", "b3", "ind_m1a_m2", "ind_m1b_m2", "ind_total"]:
        r = res[q]
        print("  %-12s %+8.4f  [%+8.4f, %+8.4f]  p=%.4g" % (q, r["est"], r["ci"][0], r["ci"][1], r["p"]))
    print("  share of total: %.1f%%" % (100 * res["ind_total"]["est"] / res["ctotal"]["est"]))

    with open(os.path.join(C.OUT, "pooled_pv.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("\nsaved ->", os.path.join(C.OUT, "pooled_pv.json"))


if __name__ == "__main__":
    main()
