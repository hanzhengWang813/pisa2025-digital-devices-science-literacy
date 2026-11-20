# -*- coding: utf-8 -*-
"""
s8_rcs_fig_en.py — English-labeled RCS figure (Fig. 1 for the English manuscript)
=================================================================================
Recomputes the restricted cubic spline (3 knots at 10/50/90 pct) with weighted
regression + Fay-BRR 95% CI, and renders Fig. 1 with English axis labels, legend
and (grey dots = unadjusted decile means; red band = 95% CI; red line = adjusted
prediction). Outputs output/fig/fig1_dose_en.png without touching the Chinese
figure (fig1_dose.png) produced by s8_rcs.py.
"""
import os, json
import numpy as np, pandas as pd
import common2 as C
from scipy import stats

OUT = C.OUT
FIG = os.path.join(OUT, "fig")
COVS = ["ESCS", "female", "ICTHOME"]


def rcs_basis(x, knots):
    x = np.asarray(x, float)
    k = len(knots)
    t = np.asarray(knots, float)
    out = [x]
    for j in range(1, k - 1):
        a = (x - t[j - 1]) ** 3
        b = (x - t[k - 2]) ** 3 * (t[k - 1] - t[j - 1]) / (t[k - 1] - t[k - 2])
        cc = (x - t[k - 1]) ** 3 * (t[k - 2] - t[j - 1]) / (t[k - 1] - t[k - 2])
        out.append((np.maximum(a, 0) - np.maximum(b, 0) + np.maximum(cc, 0)) /
                   (t[k - 1] - t[0]) ** 2)
    return np.column_stack(out)


def main():
    df = C.load()
    d = df[df["CNT"] == "QCI"].copy()
    d = d[["dev_int_z", "science"] + COVS + ["W_FSTUWT"] +
          [f"W_FSTURWT{i}" for i in range(1, 81)]].dropna()
    x = d["dev_int_z"].values.astype(float)
    y = d["science"].values.astype(float)
    print("n =", len(d), flush=True)

    knots = [np.percentile(x, p) for p in (10, 50, 90)]
    print("RCS knots:", [round(v, 4) for v in knots], flush=True)

    covm = {c: float(np.average(d[c].values.astype(float),
                                weights=d["W_FSTUWT"].values.astype(float))) for c in COVS}
    xg = np.linspace(np.percentile(x, 1), np.percentile(x, 99), 200)

    def fit_and_predict(wcol):
        w = d[wcol].values.astype(float)
        B = rcs_basis(x, knots)
        Cb = np.column_stack([C._col(d[c].values) for c in COVS])
        Xd = np.column_stack([np.ones(len(d)), B, Cb])
        beta = C._solve_w(Xd * np.sqrt(w)[:, None], y * np.sqrt(w))[0]
        Bg = rcs_basis(xg, knots)
        Cg = np.column_stack([[covm[c]] * len(xg) for c in COVS])
        Xg = np.column_stack([np.ones(len(xg)), Bg, Cg])
        return beta, Xg @ beta

    B = rcs_basis(x, knots)
    Cb = np.column_stack([C._col(d[c].values) for c in COVS])
    Xd = np.column_stack([np.ones(len(d)), B, Cb])
    beta = C._solve_w(Xd * np.sqrt(d["W_FSTUWT"].values.astype(float))[:, None],
                      y * np.sqrt(d["W_FSTUWT"].values.astype(float)))[0]
    Bg = rcs_basis(xg, knots)
    Cg = np.column_stack([[covm[c]] * len(xg) for c in COVS])
    Xg = np.column_stack([np.ones(len(xg)), Bg, Cg])
    curve = Xg @ beta

    reps = []
    for i in range(1, 81):
        try:
            reps.append(fit_and_predict(f"W_FSTURWT{i}")[1])
        except Exception:
            continue
    reps = np.array(reps)
    var_curve = C.BRR_FACTOR * np.nansum((reps - curve) ** 2, axis=0)
    se_curve = np.sqrt(np.maximum(var_curve, 0))

    # unadjusted decile means (not covariate-adjusted)
    w = d["W_FSTUWT"].values.astype(float)
    qs = np.quantile(x, np.linspace(0.05, 0.95, 10))
    bx, by = [], []
    for i in range(len(qs) - 1):
        m = (x >= qs[i]) & (x < qs[i + 1])
        if m.sum() > 30:
            bx.append(float(np.average(x[m], weights=w[m])))
            by.append(float(np.average(y[m], weights=w[m])))

    # ---------------- plotting (English) ----------------
    plt = C.setup_font()
    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    ax.scatter(bx, by, s=26, color="#95a5a6", zorder=3, label="Unadjusted decile means")
    lo = curve - 1.959964 * se_curve
    hi = curve + 1.959964 * se_curve
    ax.fill_between(xg, lo, hi, color="#c0392b", alpha=0.16, lw=0,
                    label="95% confidence interval")
    ax.plot(xg, curve, color="#c0392b", lw=2.1, label="Adjusted RCS prediction")
    ax.set_xlabel("Intensity of digital device use (standardized)")
    ax.set_ylabel("Scientific literacy (adjusted predicted score)")
    ax.legend(frameon=False, fontsize=9, loc="lower left")
    ax.grid(alpha=0.25, lw=0.6)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    os.makedirs(FIG, exist_ok=True)
    out_path = os.path.join(FIG, "fig1_dose_en.png")
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    print("saved", out_path, flush=True)


if __name__ == "__main__":
    main()
