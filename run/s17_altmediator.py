# -*- coding: utf-8 -*-
"""
s17_altmediator.py — 换用 GOALSET（计划/监控）作中介的补充检验
=============================================================
动机：核对应试者最可能追问的一点 —— 论文的中介变量 SELFREG 实际由 4 个「求助」
      条目构成（ST433Q01/02/04/06，α≈.80），并不测量计划与监控。
      而同一份问卷里有 GOALSET（ST432 四题：制定学习计划、自制摘要检验理解、
      自查是否读懂、方法无效时更换方法），才是与论文理论表述一致的量表。
本脚本用同一引擎（10 PV × 80 Fay-BRR × Rubin）把中介换成 GOALSET，
看「娱乐性使用 → 自我调节 → 科学素养」这条链是否仍然成立。

输出：output/altmediator.json
"""
import os, json
import numpy as np
import pandas as pd

import common2 as C
from s7b_pv_models import est_parallel, brr_var, rubin, PAR_Q

PVS = ["PV%dSCIE" % i for i in range(1, 11)]
MEDS = {"SELFREG": "SELFREG", "GOALSET": "GOALSET", "COGABIL": "COGABIL"}


def load_all():
    df = C.load()
    pv = pd.read_parquet(os.path.join(C.OUT, "pv.parquet"))
    return pd.concat([df.reset_index(drop=True), pv.reset_index(drop=True)], axis=1)


def run_med(df, med):
    cn = df[df["CNT"] == "QCI"]
    TH, UU = [], []
    for p in PVS:
        th, u = brr_var(cn, lambda d, y, w: est_parallel(d, y, w, m2=med), p)
        TH.append(th); UU.append(u)
    rb = rubin(np.array(TH), np.array(UU))
    return {q: dict(est=float(rb["Q"][i]), se=float(rb["SE"][i]), p=float(rb["p"][i]),
                    ci=[float(rb["ci_lo"][i]), float(rb["ci_hi"][i])])
            for i, q in enumerate(PAR_Q)}


def main():
    df = load_all()
    out = {}
    print("%-10s %8s %8s %8s %8s %10s %9s" %
          ("mediator", "d1", "d2", "b3", "ind_m1a_m2", "ind_m1b_m2", "alpha"))
    for name, col in MEDS.items():
        if col not in df.columns:
            print("  跳过", col, "（不在数据中）"); continue
        r = run_med(df, col)
        out[name] = r
        print("%-10s %+8.3f %+8.3f %+8.3f %+8.3f %+10.3f  %s" %
              (name, r["d1"]["est"], r["d2"]["est"], r["b3"]["est"],
               r["ind_m1a_m2"]["est"], r["ind_m1b_m2"]["est"],
               "%.3f" % r["d1"]["p"]))
    with open(os.path.join(C.OUT, "altmediator.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("\nsaved ->", os.path.join(C.OUT, "altmediator.json"))


if __name__ == "__main__":
    main()
