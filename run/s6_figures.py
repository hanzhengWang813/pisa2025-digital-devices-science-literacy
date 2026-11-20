# -*- coding: utf-8 -*-
"""
s6_figures.py — 论文图表生成（全部输出到 output/fig/）
"""
import os, json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from common2 import load, OUT, setup_font, z

FIG = os.path.join(OUT, "fig")
os.makedirs(FIG, exist_ok=True)
setup_font()

J = lambda f: json.load(open(os.path.join(OUT, f), encoding="utf-8"))


# ---------------------------------------------------------------- 图1 路径图
def fig_chain():
    med = J("mediation_results.json")["main"]
    fig, ax = plt.subplots(figsize=(11, 4.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 4.4); ax.axis("off")
    box = dict(boxstyle="round,pad=0.45", fc="#eaf2fb", ec="#2c6fbb", lw=1.6)
    box2 = dict(boxstyle="round,pad=0.45", fc="#fdeeee", ec="#c0392b", lw=1.6)
    box3 = dict(boxstyle="round,pad=0.45", fc="#eef8ef", ec="#1e8449", lw=1.6)

    def node(x, y, t, st, style):
        ax.text(x, y, t, ha="center", va="center", fontsize=11.5, style=style, bbox=box if style is None else style)
    ax.text(0.8, 2.2, "数字设备\n使用强度", ha="center", va="center", fontsize=12, bbox=box)
    ax.text(3.5, 3.4, "使用方式\n（娱乐性使用）", ha="center", va="center", fontsize=12, bbox=box2)
    ax.text(6.2, 3.4, "自我调节", ha="center", va="center", fontsize=12, bbox=box3)
    ax.text(9.2, 2.2, "科学素养", ha="center", va="center", fontsize=12, bbox=box)

    def arrow(x1, y1, x2, y2, txt, col="#333", dy=0.22, style="-|>"):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=16,
                                     lw=1.8, color=col, shrinkA=2, shrinkB=2,
                                     connectionstyle="arc3,rad=0.0"))
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + dy, txt, ha="center", va="center",
                fontsize=10.5, color=col)

    arrow(1.55, 2.55, 2.85, 3.25, f"a1={med['a1']:+.3f}***")
    arrow(4.15, 3.4, 5.55, 3.4, f"d21={med['d21']:+.3f}**")
    arrow(4.15, 3.1, 2.9, 3.1, "", col="#888")
    arrow(5.55, 3.1, 4.15, 3.1, "", col="#888")
    arrow(6.85, 3.25, 8.45, 2.55, f"b2={med['b2']:+.2f}***")
    arrow(3.5, 2.85, 3.5, 2.15, f"b1={med['b1']:+.2f}**", col="#c0392b")
    ax.add_patch(FancyArrowPatch((3.5, 2.15), (8.6, 2.15), arrowstyle="-|>", mutation_scale=16,
                                 lw=1.8, color="#c0392b", shrinkA=0, shrinkB=2))
    arrow(4.15, 1.9, 8.45, 1.9, "", col="#888")
    ax.text(5.9, 1.98, f"b1={med['b1']:+.2f}**（娱乐性使用→科学素养）", ha="center", fontsize=10.5, color="#c0392b")
    arrow(1.35, 1.85, 8.5, 1.85, "", col="#555")
    ax.text(4.9, 1.62, f"直接效应 c'={med['cp']:+.2f}***   总效应 c={med['ctotal']:+.2f}（每 1 个标准差）",
            ha="center", fontsize=11, color="#555")

    ax.text(0.15, 0.35,
            "注：X→娱乐性使用→自我调节→科学素养 的链式间接效应 = %.4f，95%%CI[%.4f, %.4f]；\n"
            "间接效应合计 %.2f 分，占总效应 %.1f%%。*** p<.001, ** p<.01, * p<.05（加权 Bootstrap，n=%d）"
            % (med["ind3"], med["ind3_ci"][0], med["ind3_ci"][1], med["ind_total"],
               100 * med["prop_ind_total"], med["n"]),
            fontsize=9.5, color="#666", ha="left")
    ax.set_title("图2  数字设备使用与科学素养的链式中介模型（中国四省）", fontsize=13, pad=6)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig2_chain.png"), dpi=200); plt.close(fig)


# ---------------------------------------------------------------- 图2 剂量反应
def fig_dose():
    df = load(); cn = df[df["CNT"] == "QCI"].copy()
    d = cn[["dev_int_z", "science", "W_FSTUWT"]].dropna()
    d = d.assign(bin=pd.qcut(d["dev_int_z"], 10, labels=False, duplicates="drop"))
    g = d.groupby("bin").apply(lambda s: pd.Series({
        "x": np.average(s["dev_int_z"], weights=s["W_FSTUWT"]),
        "y": np.average(s["science"], weights=s["W_FSTUWT"]),
        "n": len(s)}), include_groups=False).reset_index()
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.plot(g["x"], g["y"], "o-", color="#c0392b", lw=2.2, ms=7, label="分箱加权均值（十分位）")
    xs = np.linspace(d["dev_int_z"].min(), d["dev_int_z"].max(), 80)
    c = np.polyfit(z(d["dev_int_z"].values), d["science"].values, 2)
    ax.plot(xs, np.polyval(c, xs), "--", color="#2c3e50", lw=1.7, label="二次趋势")
    ax.axhline(np.average(d["science"], weights=d["W_FSTUWT"]), color="#888", lw=1, ls=":")
    ax.set_xlabel("数字设备使用强度（组内标准分）"); ax.set_ylabel("科学素养（加权均值）")
    ax.set_title("图1  数字设备使用强度与科学素养的剂量—反应关系", fontsize=12)
    ax.legend(); ax.grid(alpha=.3); fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig1_dose.png"), dpi=200); plt.close(fig)


# ---------------------------------------------------------------- 图3 使用方式双通道
def fig_parallel():
    p = J("mediation_results.json")["parallel_SELFREG"]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.3))
    ax = axes[0]
    labs = ["娱乐性使用", "学习性使用"]
    vals = [p["d1"], p["d2"]]; errs = [1.96 * p["d1_se"], 1.96 * p["d2_se"]]
    bars = ax.bar(labs, vals, yerr=errs, capsize=5, color=["#c0392b", "#1e8449"], width=.55)
    ax.axhline(0, color="k", lw=.9)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + (0.006 if v >= 0 else -0.014), f"{v:+.3f}",
                ha="center", fontsize=10.5)
    ax.set_ylabel("对自我调节的影响（每 1 个标准差）")
    ax.set_title("(a) 不同使用方式对自我调节的作用", fontsize=11.5)
    ax.grid(axis="y", alpha=.3)

    ax = axes[1]
    labs = ["经娱乐性使用", "经学习性使用", "经自我调节", "链式(娱乐→自我调节)"]
    keys = ["ind_m1a", "ind_m1b", "ind_m2", "ind_m1a_m2"]
    vals = [p[k] for k in keys]
    los = [p[k + "_ci"][0] for k in keys]; his = [p[k + "_ci"][1] for k in keys]
    ypos = np.arange(len(keys))[::-1]
    ex_lo = np.maximum(np.array(vals) - np.array(los), 0); ex_hi = np.maximum(np.array(his) - np.array(vals), 0)
    ax.errorbar(vals, ypos, xerr=[ex_lo, ex_hi],
                fmt="o", color="#2c6fbb", ecolor="#888", capsize=4, ms=7)
    ax.axvline(0, color="k", lw=.9)
    ax.set_yticks(ypos); ax.set_yticklabels(labs, fontsize=10.5)
    ax.set_xlabel("间接效应（科学与素养分数）")
    ax.set_title("(b) 各间接路径的效应量与 95%CI", fontsize=11.5)
    ax.grid(axis="x", alpha=.3)
    fig.suptitle("图3  使用方式的双通道作用：娱乐性使用与学习性使用的分化", fontsize=12.5, y=1.02)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig3_parallel.png"), dpi=200, bbox_inches="tight"); plt.close(fig)


# ---------------------------------------------------------------- 图4 潜在剖面
def fig_profiles():
    prof = pd.read_csv(os.path.join(OUT, "lpa_profiles.csv"))
    prof = prof.sort_values("leisure_share")
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.3))
    ax = axes[0]
    x = np.arange(len(prof)); w = .38
    ax.bar(x - w / 2, prof["learn_h"], w, label="学习性使用", color="#1e8449")
    ax.bar(x + w / 2, prof["leisure_h"], w, label="娱乐性使用", color="#c0392b")
    ax.set_xticks(x); ax.set_xticklabels([f"{t}\n({p:.1f}%)" for t, p in
                                          zip(prof["类型"], prof["weight_pct"])], fontsize=10)
    ax.set_ylabel("日均使用时长（小时）"); ax.legend()
    ax.set_title("(a) 各使用方式剖面的时长结构", fontsize=11.5); ax.grid(axis="y", alpha=.3)

    ax = axes[1]
    ax.bar(x - w / 2, prof["SELFREG"], w, label="自我调节", color="#2c6fbb")
    ax2 = ax.twinx()
    ax2.bar(x + w / 2, prof["science"], w, label="科学素养", color="#e67e22")
    ax.set_xticks(x); ax.set_xticklabels(prof["类型"], fontsize=10)
    ax.set_ylabel("自我调节（标准化）", color="#2c6fbb")
    ax2.set_ylabel("科学素养（分）", color="#e67e22")
    ax.set_title("(b) 各剖面的自我调节与科学素养", fontsize=11.5)
    ax.grid(axis="y", alpha=.3)
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=9)
    fig.suptitle("图4  使用方式的潜在剖面（中国四省，n=%d）" % int(prof["n"].sum()), fontsize=12.5, y=1.02)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig4_profiles.png"), dpi=200, bbox_inches="tight"); plt.close(fig)


# ---------------------------------------------------------------- 图5 多群组
def fig_multigroup():
    mg = J("multigroup.json")
    order = ["QCI", "FIN", "KOR", "HKG", "GLOBAL"]
    rows = []
    for e in order:
        if e not in mg: continue
        r = mg[e]
        rows.append({"lab": mg[e].get("label", e),
                     "a1": r["a1"], "d21": r["d21"], "b1": r["b1"], "b2": r["b2"],
                     "ind": r["ind_total"], "ind_lo": r["ind_total_ci"][0], "ind_hi": r["ind_total_ci"][1],
                     "prop": 100 * r["prop_ind_total"], "c": r["ctotal"], "n": r["n"]})
    t = pd.DataFrame(rows)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
    ax = axes[0]
    coefs = ["a1", "d21", "b2"]; names = ["a1(使用→娱乐)", "d21(娱乐→自我调节)", "b2(自我调节→科学/10)"]
    x = np.arange(len(t)); w = .26
    disp = {"a1": t["a1"], "d21": t["d21"], "b2": t["b2"] / 10.0}
    for i, (c, nm) in enumerate(zip(coefs, names)):
        ax.bar(x + (i - 1) * w, disp[c], w, label=nm)
    ax.axhline(0, color="k", lw=.8)
    ax.set_xticks(x); ax.set_xticklabels(t["lab"], fontsize=10)
    ax.set_title("(a) 路径系数的跨国比较（标准化）", fontsize=11.5)
    ax.legend(fontsize=9); ax.grid(axis="y", alpha=.3)

    ax = axes[1]
    ypos = np.arange(len(t))[::-1]
    xerr_lo = np.maximum(t["ind"] - t["ind_lo"], 0); xerr_hi = np.maximum(t["ind_hi"] - t["ind"], 0)
    ax.errorbar(t["ind"], ypos, xerr=[xerr_lo, xerr_hi],
                fmt="o", color="#c0392b", ecolor="#888", capsize=5, ms=8)
    ax.axvline(0, color="k", lw=.9)
    for y, v, pr, nn in zip(ypos, t["ind"], t["prop"], t["n"]):
        ax.text(v, y + .22, f"{v:+.2f}（占总效应 {pr:.0f}%，n={nn}）", fontsize=9, ha="center")
    ax.set_yticks(ypos); ax.set_yticklabels(t["lab"], fontsize=10.5)
    ax.set_ylim(-0.7, len(t) - 0.1)
    ax.set_xlabel("间接效应合计（科学素养分数）")
    ax.set_title("(b) 间接效应合计及 95%CI", fontsize=11.5)
    ax.grid(axis="x", alpha=.3)
    fig.suptitle("图6  链式中介的跨国一致性", fontsize=12.5, y=1.02)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig6_multigroup.png"), dpi=200, bbox_inches="tight"); plt.close(fig)


# ---------------------------------------------------------------- 图6 调节
def fig_moderation():
    md = J("moderation_results.json")
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.3))
    for ax, mod, lab in zip(axes, ["ESCS", "female"], ["家庭经济社会文化地位(ESCS)", "性别"]):
        r = md[mod]
        a1z, a2z, cpz = r["a1z"], r["a2z"], r["cpz"]
        a1, a2, cp = r["a1"], r["a2"], r["cp"]
        zs = np.linspace(-2, 2, 50)
        ind1 = (a1 + a1z * zs) * r["b1"]
        ind2 = (a2 + a2z * zs) * r["b2"]
        ax.plot(zs, ind1, color="#c0392b", lw=2, label="经娱乐性使用")
        ax.plot(zs, ind2, color="#2c6fbb", lw=2, label="经自我调节")
        ax.axhline(0, color="k", lw=.8)
        ax.set_xlabel(f"{lab}（标准分）"); ax.set_ylabel("条件间接效应（分）")
        ax.set_title(f"{lab} 的调节作用", fontsize=11.5)
        ax.legend(fontsize=9); ax.grid(alpha=.3)
    fig.suptitle("图5  条件间接效应随调节变量的变化（中国四省）", fontsize=12.5, y=1.02)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig5_moderation.png"), dpi=200, bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    for f in [fig_chain, fig_parallel, fig_profiles, fig_multigroup, fig_moderation]:  # fig_dose 由 s8_rcs.py 生成
        try:
            f(); print("ok:", f.__name__)
        except Exception as e:
            print("FAIL:", f.__name__, type(e).__name__, e)
    print("fig dir ->", FIG)
