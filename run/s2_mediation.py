# -*- coding: utf-8 -*-
"""
s2_mediation.py — 链式中介与平行—序列中介（主模型）
=================================================================
主模型：数字设备使用 → 使用方式 → 自我调节 → 科学素养
样本：中国四省（QCI）
估计：加权 OLS + 加权 Bootstrap（5000 次）95% 百分位区间
      核心路径另报 Fay-BRR（80 套复制权重）标准误
产出：output/mediation_results.json
"""
import os, json
import numpy as np
import pandas as pd
from common2 import (load, OUT, z, wls, design, serial_mediation,
                     parallel_serial_mediation, REPW, BRR_FACTOR)

COVS = ["ESCS", "female", "ICTHOME"]


def brr_paths(df, x, m1, m2, y, covs=COVS):
    """对链式模型核心路径做 BRR 标准误。"""
    def est(d, weight=None):
        w = d["W_FSTUWT"].values if weight is None else weight
        A = wls(design(d, [x], covs), d[m1].values.astype(float), w)[0]
        B = wls(design(d, [x, m1], covs), d[m2].values.astype(float), w)[0]
        C = wls(design(d, [x, m1, m2], covs), d[y].values.astype(float), w)[0]
        return np.array([A[1], B[1], B[2], C[2], C[3], C[1]])
    full = est(df)
    reps = []
    for rc in REPW:
        try:
            reps.append(est(df, df[rc].values))
        except Exception:
            pass
    reps = np.array(reps)
    var = BRR_FACTOR * np.nansum((reps - full) ** 2, axis=0)
    return full, np.sqrt(np.maximum(var, 0))


def show(tag, r, labels=("a1", "a2", "d21", "b1", "b2", "c'")):
    print(f"\n--- {tag} (n={r['n']}) ---")
    print(f"  a1(X→M1) = {r['a1']:+.3f} (SE {r['a1_se']:.3f}, p={r['a1_p']:.3g})")
    print(f"  a2(X→M2) = {r['a2']:+.3f} (SE {r['a2_se']:.3f}, p={r['a2_p']:.3g})")
    print(f"  d21(M1→M2)= {r['d21']:+.3f} (SE {r['d21_se']:.3f}, p={r['d21_p']:.3g})")
    print(f"  b1(M1→Y) = {r['b1']:+.2f} (SE {r['b1_se']:.2f}, p={r['b1_p']:.3g})")
    print(f"  b2(M2→Y) = {r['b2']:+.2f} (SE {r['b2_se']:.2f}, p={r['b2_p']:.3g})")
    print(f"  c'(直接)  = {r['cp']:+.2f} (SE {r['cp_se']:.2f}, p={r['cp_p']:.3g})")
    print(f"  c (总效应)= {r['ctotal']:+.2f}")
    for k, lab in [("ind1", "X→M1→Y"), ("ind2", "X→M2→Y"), ("ind3", "X→M1→M2→Y(链式)")]:
        lo, hi = r[k + "_ci"]
        print(f"  {lab:22s} = {r[k]:+.4f}  95%CI[{lo:+.4f}, {hi:+.4f}]"
              f"  {'显著' if lo * hi > 0 else '不显著'}")
    print(f"  间接合计 = {r['ind_total']:+.3f}, 占总效应 {100 * r['prop_ind_total']:.1f}%")


def main():
    df = load()
    cn = df[df["CNT"] == "QCI"].copy()
    res = {}

    # ===== 主模型 =====
    print("=" * 78)
    print("主模型：数字设备使用强度 → 娱乐性使用 → 自我调节 → 科学素养（中国四省）")
    m = serial_mediation(cn, "dev_int_z", "h_leisure", "SELFREG", "science", COVS, nboot=5000)
    show("主模型 M2=自我调节(SELFREG)", m)
    res["main"] = {k: v for k, v in m.items() if not k.startswith("_")}

    # BRR 稳健标准误
    full, se = brr_paths(cn, "dev_int_z", "h_leisure", "SELFREG", "science")
    print("  [BRR 标准误] a1=%.3f(%.4f) a2=%.3f(%.4f) d21=%.3f(%.4f) b1=%.2f(%.2f) b2=%.2f(%.2f) c'=%.2f(%.2f)"
          % (full[0], se[0], full[1], se[1], full[2], se[2], full[3], se[3], full[4], se[4], full[5], se[5]))
    res["main_brr"] = {"paths": full.tolist(), "se": se.tolist()}

    # ===== 变体 =====
    variants = {
        "m2_digit_attention": dict(m2="sr_attn"),      # 数字情境注意调节
        "x_weekday": dict(x="ICTWKDY"),                # 上学日频率
        "x_weekend": dict(x="ICTWKEND"),               # 周末频率
        "m1_share": dict(m1="leisure_share"),          # 娱乐占比
    }
    for name, v in variants.items():
        args = dict(x="dev_int_z", m1="h_leisure", m2="SELFREG")
        args.update(v)
        r = serial_mediation(cn, args["x"], args["m1"], args["m2"], "science", COVS, nboot=3000)
        show(f"变体 {name}  ({args['x']}→{args['m1']}→{args['m2']})", r)
        res[name] = {k: val for k, val in r.items() if not k.startswith("_")}

    # ===== 平行—序列模型：娱乐性与学习性使用双通道 =====
    print("\n" + "=" * 78)
    print("平行—序列模型：娱乐性/学习性使用 → 自我调节 → 科学素养（中国四省）")
    for m2 in ["SELFREG", "sr_attn"]:
        p = parallel_serial_mediation(cn, "dev_int_z", "h_leisure", "h_learn", m2, "science",
                                      COVS, nboot=3000)
        print(f"\n--- M2 = {m2} (n={p['n']}) ---")
        print(f"  a1(→娱乐性使用)={p['a1']:+.3f}(p={p['a1_p']:.2g})  a2(→学习性使用)={p['a2']:+.3f}(p={p['a2_p']:.2g})")
        print(f"  d1(娱乐→M2)={p['d1']:+.3f}(p={p['d1_p']:.3g})  d2(学习→M2)={p['d2']:+.3f}(p={p['d2_p']:.3g})")
        print(f"  b1(娱乐→Y)={p['b1']:+.2f}(p={p['b1_p']:.2g})  b2(学习→Y)={p['b2']:+.2f}(p={p['b2_p']:.2g})  "
              f"b3(M2→Y)={p['b3']:+.2f}(p={p['b3_p']:.2g})  c'={p['cp']:+.2f}")
        for k, lab in [("ind_m1a", "X→娱乐→Y"), ("ind_m1b", "X→学习→Y"), ("ind_m2", "X→M2→Y"),
                       ("ind_m1a_m2", "X→娱乐→M2→Y"), ("ind_m1b_m2", "X→学习→M2→Y")]:
            lo, hi = p[k + "_ci"]
            print(f"  {lab:18s}={p[k]:+.4f} CI[{lo:+.4f},{hi:+.4f}] {'显著' if lo * hi > 0 else '不显著'}")
        print(f"  间接合计={p['ind_total']:+.3f} 占比{100 * p['prop_ind_total']:.1f}%  总效应c={p['ctotal']:+.2f}")
        res["parallel_" + m2] = {k: v for k, v in p.items() if not k.startswith("_")}

    json.dump(res, open(os.path.join(OUT, "mediation_results.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("\nsaved -> output/mediation_results.json")


if __name__ == "__main__":
    main()
