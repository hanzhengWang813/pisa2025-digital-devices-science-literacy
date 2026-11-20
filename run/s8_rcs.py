# -*- coding: utf-8 -*-
"""
s8_rcs.py — 剂量—反应关系：限制性三次样条 (RCS) + 调整后预测曲线
=============================================================
替代原先「十分位分箱 + 二次多项式趋势线」的做法。
  * 以 3 节点 RCS（10/50/90 百分位）拟合加权回归
  * 非线性检验：RCS 第二项 (X2) 的 Fay-BRR Wald 检验
  * 控制协变量取加权均值，绘制 adjusted marginal prediction ± 95%CI
输出 output/rcs_results.json, output/fig/fig1_dose.png
"""
import os, json
import numpy as np, pandas as pd
import common2 as C
from scipy import stats

OUT = C.OUT
FIG = os.path.join(OUT, "fig")
COVS = ["ESCS", "female", "ICTHOME"]


def rcs_basis(x, knots):
    """Harrell 限制性三次样条基（返回 k-1 列）。"""
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
    d = d[["dev_int_z", "science"] + COVS + ["W_FSTUWT"] + [f"W_FSTURWT{i}" for i in range(1, 81)]].dropna()
    x = d["dev_int_z"].values.astype(float)
    y = d["science"].values.astype(float)
    print("n =", len(d), flush=True)

    knots = [np.percentile(x, p) for p in (10, 50, 90)]
    print("RCS 节点:", [round(v, 4) for v in knots], flush=True)

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

    # 点估计
    b_mean = [np.average(d[cc].values.astype(float), weights=d["W_FSTUWT"].values.astype(float))
              for cc in COVS]
    B = rcs_basis(x, knots)
    Cb = np.column_stack([C._col(d[c].values) for c in COVS])
    Xd = np.column_stack([np.ones(len(d)), B, Cb])
    beta = C._solve_w(Xd * np.sqrt(d["W_FSTUWT"].values.astype(float))[:, None],
                      y * np.sqrt(d["W_FSTUWT"].values.astype(float)))[0]
    Bg = rcs_basis(xg, knots)
    Cg = np.column_stack([[covm[c]] * len(xg) for c in COVS])
    Xg = np.column_stack([np.ones(len(xg)), Bg, Cg])
    curve = Xg @ beta

    # Fay-BRR
    reps, breps = [], []
    for i in range(1, 81):
        wc = f"W_FSTURWT{i}"
        try:
            b_r, c_r = fit_and_predict(wc)
        except Exception:
            continue
        reps.append(c_r); breps.append(b_r)
    reps = np.array(reps); breps = np.array(breps)
    var_curve = C.BRR_FACTOR * np.nansum((reps - curve) ** 2, axis=0)
    se_curve = np.sqrt(np.maximum(var_curve, 0))

    # 非线性检验（RCS 非线性项 = 第 3 个系数，索引 2）
    var_b = C.BRR_FACTOR * np.nansum((breps - beta) ** 2, axis=0)
    se_b = np.sqrt(np.maximum(var_b, 0))
    t_nl = beta[2] / se_b[2] if se_b[2] > 0 else np.nan
    p_nl = 2 * stats.t.sf(abs(t_nl), 80)

    out = {
        "n": int(len(d)), "knots": [float(v) for v in knots],
        "beta": [float(v) for v in beta], "se": [float(v) for v in se_b],
        "nonlinear_coef": float(beta[2]), "nonlinear_se": float(se_b[2]),
        "nonlinear_t": float(t_nl), "nonlinear_p": float(p_nl),
        "df": 80, "brr_factor": C.BRR_FACTOR,
        "curve": {"x": [float(v) for v in xg], "y": [float(v) for v in curve],
                  "se": [float(v) for v in se_curve]},
        "range": [float(np.percentile(x, 1)), float(np.percentile(x, 99))],
    }
    with open(os.path.join(OUT, "rcs_results.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("非线性检验: b=%.4f se=%.4f t=%.3f p=%.4f" % (beta[2], se_b[2], t_nl, p_nl), flush=True)

    # ---------------- 绘图 ----------------
    plt = C.setup_font()
    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    w = d["W_FSTUWT"].values.astype(float)
    qs = np.quantile(x, np.linspace(0.05, 0.95, 10))
    bx, by = [], []
    for i in range(len(qs) - 1):
        m = (x >= qs[i]) & (x < qs[i + 1])
        if m.sum() > 30:
            bx.append(float(np.average(x[m], weights=w[m])))
            by.append(float(np.average(y[m], weights=w[m])))
    ax.scatter(bx, by, s=26, color="#95a5a6", zorder=3, label="十分位加权均值")
    lo = curve - 1.96 * se_curve
    hi = curve + 1.96 * se_curve
    ax.fill_between(xg, lo, hi, color="#c0392b", alpha=0.16, lw=0)
    ax.plot(xg, curve, color="#c0392b", lw=2.1, label="限制性三次样条调整预测")
    ax.set_xlabel("数字设备使用强度（标准化）")
    ax.set_ylabel("科学素养（调整后预测得分）")
    ax.legend(frameon=False, fontsize=9, loc="lower left")
    ax.grid(alpha=0.25, lw=0.6)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig1_dose.png"), dpi=200)
    plt.close(fig)
    print("已更新 fig1_dose.png", flush=True)


if __name__ == "__main__":
    main()
