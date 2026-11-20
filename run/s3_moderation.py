# -*- coding: utf-8 -*-
"""
s3_moderation.py — 调节效应与有调节的中介（快速实现）
=================================================================
调节变量：家庭社会经济文化地位(ESCS)、性别(女生=1)

    M1 = a1·X + a1z·(X×Z) + ...
    M2 = a2·X + a2z·(X×Z) + d21·M1 + ...
    Y  = c'·X + cpz·(X×Z) + b1·M1 + b2·M2 + ...

报告条件间接效应（Z = -1SD / +1SD）与"有调节的中介"指数及 Bootstrap 区间。
产出：output/moderation_results.json
"""
import os, json
import numpy as np
import pandas as pd
from common2 import load, OUT, z, _col, _solve_w

COVS = ["ESCS", "female", "ICTHOME"]
SEED = 20261001
NB = 3000
X_V, M1_V, M2_V, Y_V = "dev_int_z", "h_leisure", "SELFREG", "science"


def main():
    df = load()
    cn = df[df["CNT"] == "QCI"].copy()
    rng = np.random.default_rng(SEED)
    res = {}

    for mod in ["ESCS", "female"]:
        sel = list(dict.fromkeys([X_V, M1_V, M2_V, Y_V, mod] + COVS + ["W_FSTUWT"]))
        d = cn[sel].dropna().copy()
        n = len(d)
        W = d["W_FSTUWT"].values.astype(float); sw = np.sqrt(W)
        Xs = z(d[X_V].values); Zs = z(d[mod].values); XZ = Xs * Zs
        M1z = z(d[M1_V].values); M2z = z(d[M2_V].values)
        M1r = d[M1_V].values.astype(float); M2r = d[M2_V].values.astype(float)
        Yr = d[Y_V].values.astype(float)
        covc = [_col(d[c].values) for c in COVS]

        one = np.ones(n)
        D1 = np.column_stack([one, Xs, Zs, XZ] + covc)
        D2 = np.column_stack([one, Xs, M1z, Zs, XZ] + covc)
        D3 = np.column_stack([one, Xs, M1z, M2z, Zs, XZ] + covc)
        W1, W2, W3 = D1 * sw[:, None], D2 * sw[:, None], D3 * sw[:, None]
        y1, y2, y3 = M1r * sw, M2r * sw, Yr * sw

        iX, iXZ = 1, 3          # D1
        iX2, iM1, iXZ2 = 1, 2, 4  # D2
        iX3, iM1y, iM2y, iXZ3 = 1, 2, 3, 5  # D3

        bA, sA, _, pA = _solve_w(W1, y1)
        bB, sB, _, pB = _solve_w(W2, y2)
        bC, sC, _, pC = _solve_w(W3, y3)
        bT, sT, _, pT = _solve_w(W1, y3)

        a1, a1z = bA[iX], bA[iXZ]
        a2, a2z = bB[iX2], bB[iXZ2]
        d21 = bB[iM1]
        b1, b2 = bC[iM1y], bC[iM2y]
        cp, cpz = bC[iX3], bC[iXZ3]
        ctot, ctotz = bT[iX], bT[iXZ]

        def cond(a1v, a2v, cpv):
            return np.array([a1v * b1, a2v * b2, a1v * d21 * b2, cpv])
        imm = np.array([a1z * b1, a2z * b2, a1z * d21 * b2])

        print("\n" + "=" * 82)
        print(f"调节变量 = {mod}   (n={n})")
        print(f"  a1 (X→娱乐性使用)={a1:+.3f}  X×Z={a1z:+.3f} (SE {sA[iXZ]:.3f}, p={pA[iXZ]:.3g})")
        print(f"  a2 (X→自我调节)  ={a2:+.3f}  X×Z={a2z:+.3f} (SE {sB[iXZ2]:.3f}, p={pB[iXZ2]:.3g})")
        print(f"  d21(娱乐→自我调节)={d21:+.3f} (SE {sB[iM1]:.3f}, p={pB[iM1]:.3g})")
        print(f"  b1 (娱乐→科学)   ={b1:+.2f} (p={pC[iM1y]:.3g})   b2 (自我调节→科学)={b2:+.2f} (p={pC[iM2y]:.3g})")
        print(f"  c' (直接效应)    ={cp:+.2f}  X×Z={cpz:+.3f} (SE {sC[iXZ3]:.3f}, p={pC[iXZ3]:.3g})")
        print(f"  总效应 c         ={ctot:+.2f}  X×Z={ctotz:+.3f} (SE {sT[iXZ]:.3f}, p={pT[iXZ]:.3g})")
        for zv, lab in [(-1, "低(-1SD)"), (0, "均值"), (1, "高(+1SD)")]:
            c1, c2, c3, cpv = cond(a1 + a1z * zv, a2 + a2z * zv, cp + cpz * zv)
            print(f"  条件间接效应 @{lab:8s}: 经娱乐={c1:+.3f}  经自我调节={c2:+.3f}  链式={c3:+.4f} | c'={cpv:+.2f}")

        # ---- Bootstrap ----
        pr = W / W.sum()
        acc_imm = np.full((NB, 3), np.nan)
        acc_cl = np.full((NB, 3), np.nan)
        acc_ch = np.full((NB, 3), np.nan)
        acc_cp = np.full((NB, 2), np.nan)
        for b in range(NB):
            ix = rng.choice(n, size=n, replace=True, p=pr)
            try:
                _A = _solve_w(W1[ix], y1[ix])[0]
                _B = _solve_w(W2[ix], y2[ix])[0]
                _C = _solve_w(W3[ix], y3[ix])[0]
            except np.linalg.LinAlgError:
                continue
            _a1, _a1z = _A[iX], _A[iXZ]
            _a2, _a2z = _B[iX2], _B[iXZ2]
            _d21 = _B[iM1]
            _b1, _b2 = _C[iM1y], _C[iM2y]
            _cp, _cpz = _C[iX3], _C[iXZ3]
            acc_imm[b] = [_a1z * _b1, _a2z * _b2, _a1z * _d21 * _b2]
            acc_cl[b] = cond(_a1 - _a1z, _a2 - _a2z, _cp - _cpz)[:3]
            acc_ch[b] = cond(_a1 + _a1z, _a2 + _a2z, _cp + _cpz)[:3]
            acc_cp[b] = [_cp - _cpz, _cp + _cpz]

        def ci(v):
            v = v[np.isfinite(v)]
            return float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))

        names = ["经娱乐性使用", "经自我调节", "链式路径"]
        rec = {"moderator": mod, "n": int(n), "a1": float(a1), "a1z": float(a1z),
               "a1z_p": float(pA[iXZ]), "a2": float(a2), "a2z": float(a2z),
               "a2z_p": float(pB[iXZ2]), "d21": float(d21), "b1": float(b1), "b2": float(b2),
               "cp": float(cp), "cpz": float(cpz), "cpz_p": float(pC[iXZ3]),
               "ctot": float(ctot), "ctotz": float(ctotz), "ctotz_p": float(pT[iXZ]),
               "imm": {}, "cond_low": {}, "cond_high": {}, "cond_cp": {}}
        print("  【有调节的中介指数】")
        for i, nm in enumerate(names):
            lo, hi = ci(acc_imm[:, i])
            print(f"    {nm:10s}: {imm[i]:+.4f}  95%CI[{lo:+.4f},{hi:+.4f}] {'显著' if lo * hi > 0 else '不显著'}")
            rec["imm"][nm] = {"est": float(imm[i]), "ci": [lo, hi]}
        cl, ch = cond(a1 - a1z, a2 - a2z, cp - cpz), cond(a1 + a1z, a2 + a2z, cp + cpz)
        for i, nm in enumerate(names):
            lo, hi = ci(acc_cl[:, i]); rec["cond_low"][nm] = {"est": float(cl[i]), "ci": [lo, hi]}
            lo2, hi2 = ci(acc_ch[:, i]); rec["cond_high"][nm] = {"est": float(ch[i]), "ci": [lo2, hi2]}
        lo, hi = ci(acc_cp[:, 0]); rec["cond_cp"]["low"] = {"est": float(cl[3]), "ci": [lo, hi]}
        lo, hi = ci(acc_cp[:, 1]); rec["cond_cp"]["high"] = {"est": float(ch[3]), "ci": [lo, hi]}
        print(f"  条件直接效应 c': 低={cl[3]:+.2f} CI[{rec['cond_cp']['low']['ci'][0]:+.2f},"
              f"{rec['cond_cp']['low']['ci'][1]:+.2f}] ; 高={ch[3]:+.2f} "
              f"CI[{rec['cond_cp']['high']['ci'][0]:+.2f},{rec['cond_cp']['high']['ci'][1]:+.2f}]")
        res[mod] = rec

    json.dump(res, open(os.path.join(OUT, "moderation_results.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("\nsaved -> output/moderation_results.json")


if __name__ == "__main__":
    main()
