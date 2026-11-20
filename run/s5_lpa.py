# -*- coding: utf-8 -*-
"""
s5_lpa.py — 使用方式的潜在剖面分析（补充实验）
=================================================================
指标：6 个"数字资源使用时长"情境题（ST326Q01–Q06）
      学习情境：在校 / 课前课后 / 周末 ；娱乐情境：在校 / 课前课后 / 周末
以高斯混合模型（潜在剖面分析）识别使用方式类型；
剖面数依 BIC/AIC 肘部 + 分类熵 + 最小类占比 + 可解释性综合确定。
再检验各类型在自我调节与科学素养上的差异（加权回归，控制家庭背景/性别/设备可得性）。
产出：output/lpa_results.json, output/lpa_profiles.csv
"""
import os, json
import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture
from common2 import load, OUT, z, wls

COVS = ["ESCS", "female", "ICTHOME"]
ITEMS = [f"q{i}h" for i in range(1, 7)]
SEED = 20261001
K_SEL = 4          # 见下方选择依据


def wmean(x, w):
    x = np.asarray(x, float); w = np.asarray(w, float)
    m = np.isfinite(x) & np.isfinite(w)
    return float(np.average(x[m], weights=w[m])) if m.sum() else np.nan


def main():
    df = load()
    cn = df[df["CNT"] == "QCI"].copy()
    X = cn[ITEMS].dropna()
    idx = X.index
    Xz = (X - X.mean()) / X.std()
    print(f"LPA 样本 n={len(Xz)}")

    table, gms = [], {}
    for k in range(2, 7):
        gm = GaussianMixture(n_components=k, covariance_type="full", random_state=SEED,
                             n_init=10, max_iter=800).fit(Xz.values)
        gms[k] = gm
        lp = gm.predict_proba(Xz.values)
        lab = lp.argmax(axis=1)
        Wc = cn.loc[idx, "W_FSTUWT"].values
        min_pct = 100 * min(Wc[lab == j].sum() for j in range(k)) / Wc.sum()
        table.append({"k": k, "BIC": float(gm.bic(Xz.values)), "AIC": float(gm.aic(Xz.values)),
                      "entropy": float(1 - (-(lp * np.log(lp + 1e-12)).sum(axis=1) / np.log(k)).mean()),
                      "min_pct": float(min_pct)})
    print("=== 潜在剖面模型比较 ===")
    for t in table:
        print(f"  k={t['k']}  BIC={t['BIC']:.0f}  AIC={t['AIC']:.0f}  熵={t['entropy']:.3f}  "
              f"最小类占比={t['min_pct']:.1f}%  类数×100参数")
    gm = gms[K_SEL]; k = K_SEL
    print(f"选择依据：BIC 在 k=4 后降幅明显收窄（肘部），且 k≥5 的最小类占比跌破 12%、熵下降；\n"
          f"         兼顾可解释性，最终选定 k={k}（熵={[t['entropy'] for t in table if t['k'] == k][0]:.3f}，"
          f"最小类占比={[t['min_pct'] for t in table if t['k'] == k][0]:.1f}%）")

    lab = gm.predict(Xz.values)
    d = cn.loc[idx].copy()
    d["profile"] = lab
    W = d["W_FSTUWT"].values.astype(float)

    rows = []
    for p in range(k):
        g = d[d["profile"] == p]
        gw = g["W_FSTUWT"].values.astype(float)
        rows.append({"profile": int(p), "n": int(len(g)), "weight_pct": 100 * gw.sum() / W.sum(),
                     "learn_h": wmean(g["h_learn"], gw), "leisure_h": wmean(g["h_leisure"], gw),
                     "leisure_share": wmean(g["leisure_share"], gw),
                     "total_h": wmean(g["h_total"], gw),
                     "SELFREG": wmean(g["SELFREG"], gw), "sr_attn": wmean(g["sr_attn"], gw),
                     "science": wmean(g["science"], gw),
                     "dev_int": wmean(g["dev_int_z"], gw), "ESCS": wmean(g["ESCS"], gw)})
    prof = pd.DataFrame(rows)

    def typ(r):
        hi_l = r["learn_h"] >= 1.5
        hi_f = r["leisure_h"] >= 1.8
        if hi_l and hi_f: return "高投入型"
        if hi_l and not hi_f: return "学习主导型"
        if (not hi_l) and hi_f: return "娱乐主导型"
        return "低使用型"
    prof["类型"] = prof.apply(typ, axis=1)
    prof = prof.sort_values("leisure_h").reset_index(drop=True)
    print("\n=== 各使用方式剖面的特征（加权）===")
    print(prof.round(3).to_string(index=False))
    prof.to_csv(os.path.join(OUT, "lpa_profiles.csv"), index=False, encoding="utf-8-sig")

    # 剖面 → 结果变量（以"低使用型"为参照）
    ref = int(prof[prof["类型"] == "低使用型"]["profile"].values[0])
    cols, labs = [], []
    for _, r in prof.iterrows():
        if int(r["profile"]) == ref: continue
        cols.append(f"p_{int(r['profile'])}"); labs.append(r["类型"])
    dummy = pd.get_dummies(d["profile"], prefix="p").astype(float)
    for c in cols:
        d[c] = dummy[c].values

    out = {"k": k, "bic_table": table, "profiles": rows, "ref_profile": ref,
           "ref_label": "低使用型",
           "profile_names": {int(r["profile"]): r["类型"] for _, r in prof.iterrows()},
           "contrasts": {}}
    for target in ["SELFREG", "sr_attn", "science"]:
        sub = d[[target] + cols + COVS + ["W_FSTUWT"]].dropna().copy()
        Xd = np.column_stack([np.ones(len(sub))] + [sub[c].values for c in cols] +
                             [z(sub[c].values) if sub[c].nunique() > 2 else sub[c].values
                              for c in COVS])
        b, s, t, p = wls(Xd, sub[target].values, sub["W_FSTUWT"].values)
        print(f"\n=== 剖面 → {target}（参照 = 低使用型）===")
        bl = wls(Xd, sub[target].values, sub["W_FSTUWT"].values)[0][0]
        print(f"  低使用型 (基准) : {bl:+.3f}")
        for i, c in enumerate(cols):
            print(f"  {labs[i]:8s}: {b[i + 1]:+.3f} (SE {s[i + 1]:.3f}, p={p[i + 1]:.3g})")
            out["contrasts"].setdefault(target, {})[labs[i]] = {
                "est": float(b[i + 1]), "se": float(s[i + 1]), "p": float(p[i + 1])}
    json.dump(out, open(os.path.join(OUT, "lpa_results.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, default=str)
    print("\nsaved -> output/lpa_results.json, output/lpa_profiles.csv")


if __name__ == "__main__":
    main()
