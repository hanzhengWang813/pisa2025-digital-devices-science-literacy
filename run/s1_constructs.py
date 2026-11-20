# -*- coding: utf-8 -*-
"""
s1_constructs.py — 构念检验与描述统计
=================================================================
1) 各经济体关键变量可用性筛查（确定跨国比较样本）
2) 数字自我调节 4 条目信度（Cronbach α、平均条目间相关）
3) 中国四省加权描述统计与加权相关矩阵
产出：output/availability.csv, output/desc_cn.csv, output/corr_cn.csv,
      output/constructs.json
"""
import os, json
import numpy as np
import pandas as pd
from common2 import load, OUT, z

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 50)


def cronbach(items):
    d = items.dropna()
    k = d.shape[1]
    if k < 2 or len(d) < 10:
        return np.nan, np.nan, len(d)
    item_var = d.var(axis=0, ddof=1).sum()
    tot_var = d.sum(axis=1).var(ddof=1)
    alpha = (k / (k - 1)) * (1 - item_var / tot_var)
    # 平均条目间相关
    c = d.corr().values
    iu = np.triu_indices(k, 1)
    mean_r = np.nanmean(c[iu])
    return float(alpha), float(mean_r), len(d)


def wmean(x, w):
    x = np.asarray(x, float); w = np.asarray(w, float)
    m = np.isfinite(x) & np.isfinite(w)
    return float(np.average(x[m], weights=w[m]))


def wstd(x, w):
    x = np.asarray(x, float); w = np.asarray(w, float)
    m = np.isfinite(x) & np.isfinite(w)
    mu = np.average(x[m], weights=w[m])
    return float(np.sqrt(np.average((x[m] - mu) ** 2, weights=w[m])))


def wcorr(x, y, w):
    x = np.asarray(x, float); y = np.asarray(y, float); w = np.asarray(w, float)
    m = np.isfinite(x) & np.isfinite(y) & np.isfinite(w)
    x, y, w = x[m], y[m], w[m]
    if len(x) < 10: return np.nan
    mx, my = np.average(x, weights=w), np.average(y, weights=w)
    dx, dy = x - mx, y - my
    return float(np.sum(w * dx * dy) / np.sqrt(np.sum(w * dx * dx) * np.sum(w * dy * dy)))


def main():
    df = load()
    key = ["science", "ICTWKDY", "ICTWKEND", "h_learn", "h_leisure", "SELFREG",
           "digit_sr", "ESCS", "female", "ST326Q01JA" if "ST326Q01JA" in df else "h_total"]

    # ---- 1) 可用性 ----
    rows = []
    for e, g in df.groupby("CNT"):
        rows.append({"CNT": e, "n": len(g),
                     "science": g["science"].notna().mean(),
                     "ICTWKDY": g["ICTWKDY"].notna().mean(),
                     "h_leisure": g["h_leisure"].notna().mean(),
                     "SELFREG": g["SELFREG"].notna().mean(),
                     "digit_sr": g["digit_sr"].notna().mean(),
                     "ESCS": g["ESCS"].notna().mean()})
    av = pd.DataFrame(rows).sort_values("n", ascending=False)
    av.to_csv(os.path.join(OUT, "availability.csv"), index=False)
    print("=== 可用性（比例），按样本量降序前 15 ===")
    print(av.head(15).round(3).to_string(index=False))

    usable = av[(av["ICTWKDY"] > 0.8) & (av["h_leisure"] > 0.8) &
                (av["SELFREG"] > 0.8) & (av["ESCS"] > 0.8)]
    print("\n可支撑完整链式模型（覆盖率>80%）的经济体数:", len(usable))
    print(", ".join(usable["CNT"].tolist()[:60]))

    # ---- 2) 信度（中国）----
    cn = df[df["CNT"] == "QCI"].copy()
    it = cn[["sr_item1", "sr_item2", "sr_item3", "sr_item4"]]
    alpha, mean_r, n_it = cronbach(it)
    # 分维度
    alpha_attn, r_attn, _ = cronbach(cn[["sr_item1", "sr_item2"]])       # 注意调节
    alpha_dep, r_dep, _ = cronbach(cn[["sr_item3", "sr_item4"]])         # 依赖失调
    res = {"cronbach_alpha_4item": alpha, "mean_interitem_r": mean_r, "n_reliability": n_it,
           "alpha_attention": alpha_attn, "alpha_dependence": alpha_dep,
           "corr_digit_sr_SELFREG": wcorr(cn["digit_sr"], cn["SELFREG"], cn["W_FSTUWT"])}
    print("\n=== 数字自我调节信度（中国）===")
    print(f"4 条目 Cronbach α = {alpha:.3f}，平均条目间相关 r = {mean_r:.3f}，n = {n_it}")
    print(f"注意调节(2条目) α = {alpha_attn:.3f}；依赖失调(2条目) α = {alpha_dep:.3f}")
    print(f"数字自我调节(合成) 与 SELFREG 加权相关 r = {res['corr_digit_sr_SELFREG']:.3f}")

    # ---- 3) 中国描述统计 ----
    vars_cn = {
        "science": "科学素养(PV均值)", "ICTWKDY": "上学日数字设备使用频率",
        "ICTWKEND": "周末数字设备使用频率",
        "h_learn": "学习性使用(小时/天)", "h_leisure": "娱乐性使用(小时/天)",
        "leisure_share": "娱乐使用占比", "SELFREG": "自我调节",
        "digit_sr": "数字自我调节(合成)", "ESCS": "家庭经济社会文化地位",
    }
    desc = []
    for v, lab in vars_cn.items():
        desc.append({"变量": v, "标签": lab, "加权均值": wmean(cn[v], cn["W_FSTUWT"]),
                     "加权标准差": wstd(cn[v], cn["W_FSTUWT"]),
                     "最小值": float(np.nanmin(cn[v])), "最大值": float(np.nanmax(cn[v])),
                     "缺失率%": float(100 * cn[v].isna().mean())})
    desc.append({"变量": "female", "标签": "女生比例(%)", "加权均值": 100 * wmean(cn["female"], cn["W_FSTUWT"]),
                 "加权标准差": np.nan, "最小值": 0, "最大值": 100,
                 "缺失率%": float(100 * cn["female"].isna().mean())})
    dsc = pd.DataFrame(desc)
    dsc.to_csv(os.path.join(OUT, "desc_cn.csv"), index=False)
    print("\n=== 中国四省加权描述统计 (n=%d) ===" % len(cn))
    print(dsc.round(3).to_string(index=False))

    # ---- 4) 加权相关矩阵 ----
    cv = ["science", "ICTWKDY", "ICTWKEND", "h_learn", "h_leisure", "leisure_share",
          "SELFREG", "digit_sr", "ESCS"]
    M = pd.DataFrame(index=cv, columns=cv, dtype=float)
    for i in cv:
        for j in cv:
            M.loc[i, j] = wcorr(cn[i], cn[j], cn["W_FSTUWT"])
    M.to_csv(os.path.join(OUT, "corr_cn.csv"))
    print("\n=== 中国四省加权相关矩阵 ===")
    print(M.astype(float).round(3).to_string())

    # 汇总
    res["cn_n"] = int(len(cn))
    res["corr_ICTWKDY_h_leisure"] = wcorr(cn["ICTWKDY"], cn["h_leisure"], cn["W_FSTUWT"])
    res["corr_h_leisure_SELFREG"] = wcorr(cn["h_leisure"], cn["SELFREG"], cn["W_FSTUWT"])
    res["corr_h_leisure_science"] = wcorr(cn["h_leisure"], cn["science"], cn["W_FSTUWT"])
    res["corr_SELFREG_science"] = wcorr(cn["SELFREG"], cn["science"], cn["W_FSTUWT"])
    json.dump(res, open(os.path.join(OUT, "constructs.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("\n关键加权相关: ICTWKDY~h_leisure=%.3f, h_leisure~SELFREG=%.3f, "
          "h_leisure~science=%.3f, SELFREG~science=%.3f"
          % (res["corr_ICTWKDY_h_leisure"], res["corr_h_leisure_SELFREG"],
             res["corr_h_leisure_science"], res["corr_SELFREG_science"]))


if __name__ == "__main__":
    main()
