# -*- coding: utf-8 -*-
"""
s4_multigroup.py — 跨国/多群组比较与稳健性检验
=================================================================
1) 四个可比经济体（中国四省、芬兰、韩国、中国香港）分别估计链式中介
2) 全球 23 个可比经济体合并样本（组内标准化，近似国别固定效应）
3) 稳健性：扩展控制变量、不加权估计、平行—序列模型跨国
产出：output/multigroup.json, output/robustness.json
"""
import os, json
import numpy as np
import pandas as pd
from common2 import (load, OUT, z, serial_mediation, parallel_serial_mediation, wls, design)

COVS = ["ESCS", "female", "ICTHOME"]
COVS_W = ["ESCS_w", "female", "ICTHOME_w"]
ECON = {"QCI": "中国四省", "FIN": "芬兰", "KOR": "韩国", "HKG": "中国香港"}


def line(tag, r):
    lo3, hi3 = r["ind3_ci"]; lo1, hi1 = r["ind1_ci"]; lo2, hi2 = r["ind2_ci"]
    lot, hit = r["ind_total_ci"]
    print(f"  {tag:12s} n={r['n']:6d} | a1={r['a1']:+.3f} d21={r['d21']:+.3f} b1={r['b1']:+.2f} "
          f"b2={r['b2']:+.2f} c'={r['cp']:+.2f} c={r['ctotal']:+.2f}")
    print(f"  {'':12s} 间接: 经娱乐={r['ind1']:+.3f}[{lo1:+.2f},{hi1:+.2f}] "
          f"经自我调节={r['ind2']:+.3f}[{lo2:+.2f},{hi2:+.2f}] "
          f"链式={r['ind3']:+.4f}[{lo3:+.4f},{hi3:+.4f}] 合计={r['ind_total']:+.2f}[{lot:+.2f},{hit:+.2f}] "
          f"占比={100 * r['prop_ind_total']:.1f}%")


def main():
    df = load()
    res = {}

    # ===== 1) 多群组 =====
    print("=" * 96)
    print("多群组：各经济体内部标准化的链式中介（X=设备使用强度 → 娱乐性使用 → 自我调节 → 科学素养）")
    for e, lab in ECON.items():
        d = df[df["CNT"] == e]
        r = serial_mediation(d, "dev_int_z", "h_leisure", "SELFREG", "science", COVS, nboot=5000)
        line(f"{lab}", r)
        res[e] = {"label": lab, **{k: v for k, v in r.items()}}

    # ===== 2) 全球合并（组内标准化，近似国家固定效应）=====
    print("\n" + "=" * 96)
    print("全球可比样本合并（组内标准化）")
    keep = []
    for e, g in df.groupby("CNT"):
        if (g["ICTWKDY"].notna().mean() > .8 and g["h_leisure"].notna().mean() > .8 and
                g["SELFREG"].notna().mean() > .8 and g["ESCS"].notna().mean() > .8 and len(g) >= 2000):
            keep.append(e)
    gw = df[df["CNT"].isin(keep)].copy()
    print(f"纳入经济体数: {len(keep)}，总样本 {len(gw)}")
    r = serial_mediation(gw, "dev_int_w", "h_leisure_w", "SELFREG_w", "science_w",
                         COVS_W, nboot=2000, prestd=True)
    line("全球合并", r)
    res["GLOBAL"] = {"label": f"全球{len(keep)}个经济体", "economies": keep,
                     **{k: v for k, v in r.items()}}

    # 平行—序列（全球）
    p = parallel_serial_mediation(gw, "dev_int_w", "h_leisure_w", "h_learn_w", "SELFREG_w",
                                  "science_w", COVS_W, nboot=2000, prestd=True)
    print(f"  平行—序列(全球): 娱乐→自我调节={p['d1']:+.3f}(p={p['d1_p']:.2g})  "
          f"学习→自我调节={p['d2']:+.3f}(p={p['d2_p']:.2g})  "
          f"经娱乐链={p['ind_m1a_m2']:+.4f} 经学习链={p['ind_m1b_m2']:+.4f}")
    res["GLOBAL_parallel"] = {k: v for k, v in p.items()}
    json.dump(res, open(os.path.join(OUT, "multigroup.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    # ===== 3) 稳健性 =====
    print("\n" + "=" * 96)
    print("稳健性检验（中国四省）")
    cn = df[df["CNT"] == "QCI"].copy()
    rob = {}

    # (a) 扩展控制：+年级 +留级 +家庭语言 +ICT资源
    ext = ["ST001D01T", "REPEAT", "ST022Q01TA", "ICTRES"]
    r = serial_mediation(cn, "dev_int_z", "h_leisure", "SELFREG", "science", COVS + ext, nboot=3000)
    print("  (a) 扩展控制变量:"); line("  扩展控制", r); rob["extended_controls"] = r

    # (b) 不加权
    cn2 = cn.copy(); cn2["__ones"] = 1.0
    r = serial_mediation(cn2, "dev_int_z", "h_leisure", "SELFREG", "science", COVS,
                         wcol="__ones", nboot=3000)
    print("  (b) 不加权:"); line("  未加权", r); rob["unweighted"] = r

    # (c) 控制数字设备可用性之外，再加"科学课使用数字资源"
    r = serial_mediation(cn, "dev_int_z", "h_leisure", "SELFREG", "science",
                         COVS + ["IC173Q03JA"], nboot=3000)
    print("  (c) 追加控制科学课数字资源使用:"); line("  追加控制", r); rob["extra_sci_class"] = r

    # (d) 随机分半稳健性
    print("  (d) 随机分半（检验结果不依赖特定子样本）")
    rng = np.random.default_rng(7)
    half = rng.random(len(cn)) < 0.5
    r = serial_mediation(cn[half], "dev_int_z", "h_leisure", "SELFREG", "science", COVS, nboot=3000)
    print("  (d) 随机分半(前半):"); line("  分半A", r); rob["split_half_a"] = r
    r = serial_mediation(cn[~half], "dev_int_z", "h_leisure", "SELFREG", "science", COVS, nboot=3000)
    print("  (d) 随机分半(后半):"); line("  分半B", r); rob["split_half_b"] = r

    # (e) 自我调节作为调节变量（缓冲效应）: 娱乐性使用×自我调节 → 科学素养
    print("  (e) 自我调节的缓冲效应（娱乐性使用 × 自我调节 → 科学素养）")
    d = cn[["science", "h_leisure", "SELFREG", "dev_int_z", "ESCS", "female", "ICTHOME", "W_FSTUWT"]].dropna()
    Xm = design(d, ["h_leisure", "SELFREG"], ["dev_int_z", "ESCS", "female", "ICTHOME"])
    inter = (z(d["h_leisure"].values) * z(d["SELFREG"].values)).reshape(-1, 1)
    b, s, t, pv = wls(np.hstack([Xm, inter]), d["science"].values, d["W_FSTUWT"].values)
    print(f"      娱乐性使用×自我调节 交互 = {b[-1]:+.3f} (SE {s[-1]:.3f}, p={pv[-1]:.3g})")
    print(f"      娱乐性使用的条件斜率 @低自我调节(-1SD) = {b[1] - b[-1]:+.2f} ; "
          f"@高自我调节(+1SD) = {b[1] + b[-1]:+.2f}")
    print(f"      自我调节的条件斜率   @低娱乐性使用(-1SD) = {b[2] - b[-1]:+.2f} ; "
          f"@高娱乐性使用(+1SD) = {b[2] + b[-1]:+.2f}   ← 论文 4.5 与摘要报告的是这一组")
    # 注意：模型为 design(d, ["h_leisure","SELFREG"], covs)，故 b[1]=h_leisure、b[2]=SELFREG。
    # 条件斜率 = 该变量主效应 ∓ 交互项。论文报告的“自我调节斜率随娱乐性使用变化”对应 b[2]∓b[-1]。
    rob["buffering"] = {
        "interaction": float(b[-1]), "se": float(s[-1]), "p": float(pv[-1]),
        "b_leisure": float(b[1]), "b_selfreg": float(b[2]),
        # 自我调节的条件斜率（随娱乐性使用高/低变化）——论文摘要与 4.5 报告的即此项
        "sr_slope_low_leisure": float(b[2] - b[-1]),
        "sr_slope_high_leisure": float(b[2] + b[-1]),
        # 娱乐性使用的条件斜率（随自我调节高/低变化）——供对照，注意与上一组区分
        "leisure_slope_low_sr": float(b[1] - b[-1]),
        "leisure_slope_high_sr": float(b[1] + b[-1]),
        "n": int(len(d))}

    json.dump(rob, open(os.path.join(OUT, "robustness.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("\nsaved -> output/multigroup.json, output/robustness.json")


if __name__ == "__main__":
    main()
