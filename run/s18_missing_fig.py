# -*- coding: utf-8 -*-
"""
s18_missing_fig.py — 两件投稿必需的补充材料
================================================================
(A) 缺失率：模型五个关键变量与三个协变量在 QCI 的缺失比例、listwise 后 n，
    以及「用完整案例 vs 用可得案例」两个样本的描述统计差（判断 listwise 是否有偏）。
(B) Figure 1 出版版：3 结点 RCS + Fay-BRR 95% CI，300 dpi，serif 字体，
    轴标签与正文一致（0 = 国际合并样本均值）。
输出：
    output/missing.json
    output/fig/fig1_pub.png
"""
import os, json
import numpy as np, pandas as pd
import common2 as C

OUT = C.OUT
FIG = os.path.join(OUT, "fig")
COVS = ["ESCS", "female", "ICTHOME"]
KEY = ["dev_int_z", "h_leisure", "h_learn", "SELFREG", "science"]


def rcs_basis(x, knots):
    x = np.asarray(x, float); k = len(knots); t = np.asarray(knots, float)
    out = [x]
    for j in range(1, k - 1):
        a = (x - t[j - 1]) ** 3
        b = (x - t[k - 2]) ** 3 * (t[k - 1] - t[j - 1]) / (t[k - 1] - t[k - 2])
        cc = (x - t[k - 1]) ** 3 * (t[k - 2] - t[j - 1]) / (t[k - 1] - t[k - 2])
        out.append((np.maximum(a, 0) - np.maximum(b, 0) + np.maximum(cc, 0)) /
                   (t[k - 1] - t[0]) ** 2)
    return np.column_stack(out)


def missing_section(df):
    d = df[df["CNT"] == "QCI"]
    rec = {"n_raw": int(len(d))}
    for c in KEY + COVS + ["use_total", "leisure_share"]:
        if c in d.columns:
            rec[c] = round(100 * float(d[c].isna().mean()), 2)
    rec["n_key_complete"] = int(d[KEY].notna().all(axis=1).sum())
    rec["n_model"] = int(d[KEY + COVS].notna().all(axis=1).sum())

    # 完整案例 vs 全体（加权均值），看 listwise 是否挑样本
    w = d["W_FSTUWT"].values.astype(float)
    ok = d[KEY + COVS].notna().all(axis=1).values
    cmp = {}
    for c in ["science", "SELFREG", "dev_int_z", "ESCS", "female"]:
        v = d[c].values.astype(float)
        fin = np.isfinite(v) & np.isfinite(w)
        a = float(np.average(v[fin], weights=w[fin]))
        b = float(np.average(v[ok & fin], weights=w[ok & fin]))
        cmp[c] = {"all": round(a, 3), "listwise": round(b, 3),
                  "diff_in_sd": round((b - a) / float(np.nanstd(v)), 3)}
    rec["complete_case_vs_all"] = cmp
    return rec


def figure(df):
    d = df[df["CNT"] == "QCI"].copy()
    keep = ["dev_int_z", "science"] + COVS + ["W_FSTUWT"] + ["W_FSTURWT%d" % i for i in range(1, 81)]
    d = d[[c for c in keep if c in d.columns]].dropna()
    x = d["dev_int_z"].values.astype(float)
    y = d["science"].values.astype(float)
    knots = [np.percentile(x, p) for p in (10, 50, 90)]
    covm = {c: float(np.average(d[c].values.astype(float), weights=d["W_FSTUWT"].values.astype(float)))
            for c in COVS}
    xlo, xhi = np.percentile(x, 1), np.percentile(x, 99)
    xg = np.linspace(xlo, xhi, 200)

    def fit_predict(wcol):
        w = d[wcol].values.astype(float)
        B = rcs_basis(x, knots)
        Xd = np.column_stack([np.ones(len(d)), B, np.column_stack([C._col(d[c].values) for c in COVS])])
        beta = C._solve_w(Xd * np.sqrt(w)[:, None], y * np.sqrt(w))[0]
        Bg = rcs_basis(xg, knots)
        Xg = np.column_stack([np.ones(len(xg)), Bg,
                              np.column_stack([[covm[c]] * len(xg) for c in COVS])])
        return Xg @ beta

    curve = fit_predict("W_FSTUWT")
    reps = []
    for i in range(1, 81):
        try:
            reps.append(fit_predict("W_FSTURWT%d" % i))
        except Exception:
            continue
    reps = np.array(reps)
    se = np.sqrt(np.maximum(C.BRR_FACTOR * np.nansum((reps - curve) ** 2, axis=0), 0))

    # 未调整的十分位均值
    w = d["W_FSTUWT"].values.astype(float)
    qs = np.quantile(x, np.linspace(0.05, 0.95, 10))
    bx, by = [], []
    for i in range(len(qs) - 1):
        m = (x >= qs[i]) & (x < qs[i + 1])
        if m.sum() > 30:
            bx.append(float(np.average(x[m], weights=w[m])))
            by.append(float(np.average(y[m], weights=w[m])))

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif", "Songti SC"],
        "font.size": 9, "axes.labelsize": 9.5, "axes.titlesize": 9.5,
        "xtick.labelsize": 8.5, "ytick.labelsize": 8.5, "legend.fontsize": 8,
        "axes.linewidth": 0.8, "mathtext.fontset": "dejavuserif",
    })
    fig, ax = plt.subplots(figsize=(6.3, 3.9))
    ax.scatter(bx, by, s=22, color="#8d9aa5", edgecolor="none", zorder=3,
               label="Unadjusted decile means")
    ax.fill_between(xg, curve - 1.959964 * se, curve + 1.959964 * se,
                    color="#b03a2e", alpha=0.15, lw=0,
                    label="95% confidence band")
    ax.plot(xg, curve, color="#b03a2e", lw=1.9, zorder=4,
            label="Adjusted spline prediction")
    ax.axhline(0, color="none")
    ax.set_xlabel("Device-use frequency index (0 = pooled international average)")
    ax.set_ylabel("Predicted scientific literacy")
    ax.grid(alpha=0.22, lw=0.6, ls="-")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.legend(frameon=False, loc="lower left")
    ax.set_xlim(xlo - 0.1, xhi + 0.1)
    lo_all = float(min(np.min(curve - 1.959964 * se), min(by)))
    hi_all = float(max(np.max(curve + 1.959964 * se), max(by)))
    ax.set_ylim(lo_all - 18, hi_all + 14)
    fig.tight_layout()
    os.makedirs(FIG, exist_ok=True)
    p = os.path.join(FIG, "fig1_pub.png")
    fig.savefig(p, dpi=400, bbox_inches="tight")
    plt.close(fig)
    print("saved", p, "| range %.2f..%.2f | interdecile drop %.1f"
          % (xg[0], xg[-1], float(np.interp(np.percentile(x, 90), xg, curve)
                                  - np.interp(np.percentile(x, 10), xg, curve))), flush=True)
    return p


def main():
    df = C.load()
    m = missing_section(df)
    print(json.dumps(m, ensure_ascii=False, indent=1))
    with open(os.path.join(OUT, "missing.json"), "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)
    figure(df)


if __name__ == "__main__":
    main()
