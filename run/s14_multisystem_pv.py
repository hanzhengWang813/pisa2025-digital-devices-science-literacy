# -*- coding: utf-8 -*-
"""
s14_multisystem_pv.py — 用「10 个似真值 + 80 套 Fay-BRR + Rubin 合并」重估四经济体双通道模型
=====================================================================================
目的：现稿表 5（四经济体比较）的点估计来自 s4_multigroup.py，其标准误是解析标准误，
      没有反映 PISA 的分层整群抽样（QCI 的 ctotal_se 只有 0.66，而设计基础标准误是 1.07，
      低估约 40%）。跨国比较表如果就这样投出去，审稿人一定会指出。

本脚本复用 s7b_pv_models.py 里已经验证过的 est_parallel / brr_var / rubin，
对每个经济体分别做「PV 分别估计 + BRR 抽样方差 + Rubin 合并」，输出带设计基础 95%CI 的表 5。

运行：
    python s14_multisystem_pv.py
输出：
    output/multisystem_pv.json
    控制台直接打印可粘进论文的表 5
预计耗时：每个经济体约 10 个 PV x 81 次估计 x 5 个方程 ≈ 数分钟（12,000 人量级）
"""
import os, json
import numpy as np
import pandas as pd

import common2 as C
from s7b_pv_models import est_parallel, brr_var, rubin, PAR_Q

PVS = ["PV%dSCIE" % i for i in range(1, 11)]
SYSTEMS = ["QCI", "FIN", "KOR", "HKG"]
LABEL = {"QCI": "B-S-J-Z, China", "FIN": "Finland", "KOR": "Korea", "HKG": "Hong Kong, China"}


def load_all():
    """analysis.parquet + pv.parquet，按行序对齐（s7_pv_extract.py 已断言过对齐）。"""
    df = C.load()
    pv = pd.read_parquet(os.path.join(C.OUT, "pv.parquet"))
    if len(pv) != len(df):
        raise RuntimeError("pv.parquet 与 analysis.parquet 行数不一致，请重跑 s7_pv_extract.py")
    return pd.concat([df.reset_index(drop=True), pv.reset_index(drop=True)], axis=1)


def run_system(df, cnt):
    sub = df[df["CNT"] == cnt].copy()
    TH, UU = [], []
    for p in PVS:
        th, u = brr_var(sub, est_parallel, p)
        TH.append(th); UU.append(u)
    rb = rubin(np.array(TH), np.array(UU))
    out = {}
    for i, q in enumerate(PAR_Q):
        out[q] = dict(est=float(rb["Q"][i]), se=float(rb["SE"][i]), df=float(rb["df"][i]),
                      p=float(rb["p"][i]), ci=[float(rb["ci_lo"][i]), float(rb["ci_hi"][i])])
    # 间接合计占 c 的比例（可负，符号表示方向相反）
    out["share_ind_total"] = out["ind_total"]["est"] / out["ctotal"]["est"] if out["ctotal"]["est"] else np.nan
    out["n"] = int(len(sub))
    return out


def star(p):
    return "***" if p < .001 else "**" if p < .01 else "*" if p < .05 else ""


def main():
    df = load_all()
    res = {}
    for cnt in SYSTEMS:
        print("estimating", cnt, "...", flush=True)
        res[cnt] = run_system(df, cnt)
        r = res[cnt]
        print("  %-16s n=%6d  c=%+7.2f [%+7.2f,%+7.2f]  c'=%+7.2f  "
              "chain_ent=%+.3f  chain_learn=%+.3f  ind_total=%+.2f  share=%.1f%%"
              % (LABEL[cnt], r["n"], r["ctotal"]["est"], r["ctotal"]["ci"][0], r["ctotal"]["ci"][1],
                 r["cp"]["est"], r["ind_m1a_m2"]["est"], r["ind_m1b_m2"]["est"],
                 r["ind_total"]["est"], 100 * r["share_ind_total"]), flush=True)

    os.makedirs(C.OUT, exist_ok=True)
    with open(os.path.join(C.OUT, "multisystem_pv.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)

    # ---- 直接打印论文表 5（设计基础） ----
    print("\n" + "=" * 100)
    print("Table 5 (design-based). Dual-path model in four education systems")
    print("=" * 100)
    rows = [("Total (c)", "ctotal"), ("Direct (c')", "cp"),
            ("Entertainment -> self-reg. (d1)", "d1"), ("Learning -> self-reg. (d2)", "d2"),
            ("Self-regulation -> literacy (b3)", "b3"),
            ("Entertainment -> literacy (b1)", "b1"), ("Learning -> literacy (b2)", "b2"),
            ("Serial via entertainment", "ind_m1a_m2"), ("Serial via learning", "ind_m1b_m2"),
            ("All indirect", "ind_total")]
    for lab, key in rows:
        cells = []
        for cnt in SYSTEMS:
            r = res[cnt][key]
            cells.append("%.3f%s [%.3f, %.3f]" % (r["est"], star(r["p"]), r["ci"][0], r["ci"][1])
                         if abs(r["est"]) < 5 else
                         "%.2f%s [%.2f, %.2f]" % (r["est"], star(r["p"]), r["ci"][0], r["ci"][1]))
        print("%-34s | %s" % (lab, " | ".join(cells)))
    print("\nsaved ->", os.path.join(C.OUT, "multisystem_pv.json"))


if __name__ == "__main__":
    main()
