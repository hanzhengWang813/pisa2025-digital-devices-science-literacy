# -*- coding: utf-8 -*-
"""
s9_interaction.py — 跨国系数差异的正式检验（pooled + X×Country 交互）
==================================================================
回应方法审稿意见：「一个国家显著、另一个不显著」不等于「两个系数显著不同」。
  * 合并四经济体样本（QCI/FIN/KOR/HKG），变量按经济体内部标准化
  * 分层检验：X×Country（直接效应）、M1×Country（娱乐→科学素养）、M2×Country（自我调节→科学素养）
  * Fay-BRR 方差 + 联合 Wald F 检验（df1=q, df2=80）
输出 output/interaction_results.json
"""
import os, json
import numpy as np, pandas as pd
import common2 as C
from scipy import stats

OUT = C.OUT
CTS = ["QCI", "FIN", "KOR", "HKG"]
DUMS = ["FIN", "KOR", "HKG"]
COVS = ["ESCS_w", "female", "ICTHOME_w"]
X, M1, M2, Y = "dev_int_w", "h_leisure_w", "SELFREG_w", "science_w"


def wald_joint(v, b, q):
    """联合 Wald：F = b' V^{-1} b / q, 参考 F(q, 80)。"""
    Vi = np.linalg.pinv(v)
    W = float(b @ Vi @ b)
    F = W / q
    p = float(stats.f.sf(F, q, 80))
    return W, F, p


def main():
    df = C.load()
    d = df[df["CNT"].isin(CTS)].copy()
    need = [X, M1, M2, Y] + COVS + ["CNT", "W_FSTUWT"] + [f"W_FSTURWT{i}" for i in range(1, 81)]
    d = d[need].dropna().copy()
    print("合并样本 n =", len(d), flush=True)
    for c in DUMS:
        d[c] = (d["CNT"] == c).astype(float)
    # 参照组 QCI 的交互列 = 该经济体指示变量
    base = np.column_stack([C._col(d[c].values) for c in COVS])
    Xv = d[X].values.astype(float); M1v = d[M1].values.astype(float)
    M2v = d[M2].values.astype(float); Yv = d[Y].values.astype(float)
    Dv = np.column_stack([d[c].values.astype(float) for c in DUMS])
    one = np.ones(len(d))

    def build():
        """完全交互模型：同时纳入 X×Country, M1×Country, M2×Country，
        避免因遗漏其他交互项而使参照组系数产生偏误。"""
        cols = [one, Xv, M1v, M2v] + [base[:, j] for j in range(base.shape[1])] + \
               [Dv[:, j] for j in range(Dv.shape[1])]
        names = ["const", "X", "M1", "M2"] + COVS + DUMS
        for inter in ["X", "M1", "M2"]:
            src = {"X": Xv, "M1": M1v, "M2": M2v}[inter]
            for j in range(Dv.shape[1]):
                cols.append(src * Dv[:, j]); names.append(f"{inter}x{DUMS[j]}")
        return np.column_stack(cols), names

    res = {}
    Xd, names = build()
    w = d["W_FSTUWT"].values.astype(float)
    beta = C._solve_w(Xd * np.sqrt(w)[:, None], Yv * np.sqrt(w))[0]
    reps = []
    for i in range(1, 81):
        wi = d[f"W_FSTURWT{i}"].values.astype(float)
        try:
            reps.append(C._solve_w(Xd * np.sqrt(wi)[:, None], Yv * np.sqrt(wi))[0])
        except Exception:
            continue
    reps = np.array(reps)
    V = C.BRR_FACTOR * ((reps - beta).T @ (reps - beta))
    se = np.sqrt(np.maximum(np.diag(V), 0))
    res["full"] = {"names": names,
                   "beta": {n: float(beta[i]) for i, n in enumerate(names)},
                   "se": {n: float(se[i]) for i, n in enumerate(names)},
                   "t": {n: float(beta[i] / se[i]) if se[i] > 0 else None for i, n in enumerate(names)},
                   "p": {n: float(2 * stats.t.sf(abs(beta[i] / se[i]), 80)) if se[i] > 0 else None
                         for i, n in enumerate(names)}}
    print("[完全交互模型] 参照组 QCI：X=%.4f  M1=%.4f  M2=%.4f (SD 单位)"
          % (res["full"]["beta"]["X"], res["full"]["beta"]["M1"], res["full"]["beta"]["M2"]), flush=True)

    for inter in ["X", "M1", "M2"]:
        idx = [i for i, n in enumerate(names) if n.startswith(inter + "x")]
        bI, VI = beta[idx], V[np.ix_(idx, idx)]
        W, F, p = wald_joint(VI, bI, len(idx))
        tag = f"{inter}xCountry"
        res[tag] = {"joint": {"W": W, "F": F, "df1": len(idx), "df2": 80, "p": p,
                              "terms": [names[i] for i in idx]}}
        print(f"[{tag}] 联合检验 F({len(idx)},80)={F:.3f}, p={p:.6f}", flush=True)
        for i in idx:
            print(f"    {names[i]:<12} b={beta[i]:8.4f} se={se[i]:7.4f} "
                  f"p={2*stats.t.sf(abs(beta[i]/se[i]),80):.4f}", flush=True)

    res["meta"] = {"countries": CTS, "ref": "QCI", "df": 80, "brr_factor": C.BRR_FACTOR,
                   "n": int(len(d)), "standardization": "within-country (group) standardized"}
    with open(os.path.join(OUT, "interaction_results.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("已写出 output/interaction_results.json", flush=True)


if __name__ == "__main__":
    main()
