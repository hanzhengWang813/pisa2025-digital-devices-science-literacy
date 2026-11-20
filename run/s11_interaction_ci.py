# -*- coding: utf-8 -*-
"""
s11_interaction_ci.py — 3.5 节交互效应与简单斜率的标准误、置信区间
=====================================================================
3.5 节原只报 b 与 p，缺标准误与区间。本脚本按与正文其他模型一致的口径补算：
  1) 10 个似真值分别估计同一交互模型（娱乐性使用 × 自我调节 → 科学素养）
  2) 每个 PV 用 80 套 Fay-BRR 复制权重得抽样方差 U_k
  3) Rubin 规则合并，得到 b、简单斜率（±1 SD）及其 95% CI
同时输出现行正文所用「似真值合并量表」上的解析标准误（WLS），供对照。

产出：results/interaction_ci.json
"""
import os, json
import numpy as np
import pandas as pd
from scipy import stats
import common2 as C
from common2 import design, z

PVS = ["PV%dSCIE" % i for i in range(1, 11)]
M = len(PVS)
COVS = ["dev_int_z", "ESCS", "female", "ICTHOME"]


def _fit(y, df, w):
    """返回 (b_inter, slope@-1SD, slope@+1SD, vcov)。"""
    X = design(df, ["h_leisure", "SELFREG"], COVS)
    inter = (z(df["h_leisure"].values) * z(df["SELFREG"].values)).reshape(-1, 1)
    X = np.hstack([X, inter])
    sw = np.sqrt(w)
    Xw, yw = X * sw[:, None], np.asarray(y, float) * sw
    XtX = Xw.T @ Xw
    k = X.shape[1]
    XtX = XtX + 1e-10 * (np.trace(XtX) / k) * np.eye(k)
    beta = np.linalg.solve(XtX, Xw.T @ yw)
    resid = yw - Xw @ beta
    s2 = float(resid @ resid) / max(len(yw) - k, 1)
    V = np.linalg.inv(XtX) * s2
    b_int, b_sr = beta[-1], beta[2]
    return np.array([b_int, b_sr - b_int, b_sr + b_int]), V


def main():
    df = C.load()
    pv = C.read_frame(os.path.join(C.OUT, "pv"))
    df = pd.concat([df.reset_index(drop=True), pv.reset_index(drop=True)], axis=1)
    d = df[df["CNT"] == "QCI"][["h_leisure", "SELFREG", "dev_int_z", "ESCS", "female",
                                "ICTHOME", "W_FSTUWT"] + C.REPW + PVS].dropna()
    n = len(d)

    TH, UU, ANA = [], [], []
    for p in PVS:
        th, V = _fit(d[p].values, d, d["W_FSTUWT"].values)
        reps = []
        for rc in C.REPW:
            try:
                reps.append(_fit(d[p].values, d, d[rc].values)[0])
            except Exception:
                continue
        reps = np.array(reps)
        TH.append(th)
        UU.append(C.BRR_FACTOR * np.nansum((reps - th) ** 2, axis=0))
        # 解析 SE（单 PV、全样本）
        ANA.append(np.sqrt(np.array([V[-1, -1],
                                     V[2, 2] + V[-1, -1] - 2 * V[2, -1],
                                     V[2, 2] + V[-1, -1] + 2 * V[2, -1]])))

    TH, UU, ANA = np.array(TH), np.array(UU), np.array(ANA)
    Q = TH.mean(axis=0)
    Ubar = UU.mean(axis=0)
    B = TH.var(axis=0, ddof=1)
    T = Ubar + (1 + 1 / M) * B
    SE = np.sqrt(T)
    df_r = (M - 1) * (1 + Ubar / ((1 + 1 / M) * B)) ** 2
    t = Q / SE
    p = 2 * stats.t.sf(np.abs(t), df_r)
    crit = stats.t.ppf(0.975, df_r)
    out = {
        "n": int(n),
        "method": "10 plausible values x 80 Fay-BRR replicate weights, Rubin's rules",
        "labels": ["interaction", "slope_low_leisure(-1SD)", "slope_high_leisure(+1SD)"],
        "est": [float(v) for v in Q],
        "se": [float(v) for v in SE],
        "df": [float(v) for v in df_r],
        "t": [float(v) for v in t],
        "p": [float(v) for v in p],
        "ci": [[float(a), float(b)] for a, b in zip(Q - crit * SE, Q + crit * SE)],
        "se_analytic_single_pv": [float(v) for v in ANA.mean(axis=0)],
        "slope_diff": {"est": float(-2 * Q[0]), "se": float(2 * SE[0]),
                       "ci": [float(-2 * Q[0] - 2 * crit[0] * SE[0]),
                              float(-2 * Q[0] + 2 * crit[0] * SE[0])],
                       "p": float(2 * stats.t.sf(abs(2 * Q[0] / (2 * SE[0])), df_r[0]))},
    }
    os.makedirs(os.path.join(C.OUT, "..", "results"), exist_ok=True)
    with open(os.path.join(C.OUT, "interaction_ci.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    for lab, e, s, c in zip(out["labels"], out["est"], out["se"], out["ci"]):
        print("%-26s %+9.4f  se=%.4f  ci=[%+.3f, %+.3f]" % (lab, e, s, c[0], c[1]))
    print("difference %+.4f se=%.4f ci=[%+.3f, %+.3f]" %
          (out["slope_diff"]["est"], out["slope_diff"]["se"],
           out["slope_diff"]["ci"][0], out["slope_diff"]["ci"][1]))
    print("analytic SE (mean over PVs):", ["%.4f" % v for v in out["se_analytic_single_pv"]])
    print("saved -> output/interaction_ci.json")


if __name__ == "__main__":
    main()
