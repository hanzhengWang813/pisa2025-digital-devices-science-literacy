# -*- coding: utf-8 -*-
"""
s12_corr_inference.py — 表2 加权相关矩阵的标准化数值与设计基础推断
=====================================================================
s1_constructs.py 只给出加权相关系数（wcorr），没有标准误，表2 的星号因此没有
可追溯的代码依据；同时表2「使用强度」一行用的是样本内标准化的复合指数，
而 s7b 的中介模型用的是 common2.add_derived 的 dev_int_z（全样本标准化）。
本脚本按模型口径重算表2，并给出与正文一致的标准误：

  1) 复合强度指数 dev_int_z（与 s7b/est_parallel 的 X 完全相同）
  2) 相关系数用最终学生权重加权
  3) 标准误：80 套 Fay-BRR 复制权重，BRR_FACTOR = 1/(80*(1-0.5)^2) = 0.05
  4) p：t 分布，df = 80

产出：output/corr_design_inference.csv（r, se, t, p, star），供表2 与表注核对。
"""
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

import common2 as C

REPW = C.REPW
BRR = C.BRR_FACTOR
DF = 80.0

# 表2 的行顺序（与正文明细一致）
VARS = [
    ("science", "science"),
    ("intensity", "dev_int_z"),
    ("learning", "h_learn"),
    ("entertainment", "h_leisure"),
    ("share", "leisure_share"),
    ("selfreg", "SELFREG"),
    ("family", "ESCS"),
]


def wcorr(x, y, w):
    m = np.isfinite(x) & np.isfinite(y) & np.isfinite(w)
    x, y, w = x[m], y[m], w[m]
    mx, my = np.average(x, weights=w), np.average(y, weights=w)
    dx, dy = x - mx, y - my
    return float(np.sum(w * dx * dy) / np.sqrt(np.sum(w * dx * dx) * np.sum(w * dy * dy)))


def star(p):
    return "***" if p < .001 else ("**" if p < .01 else ("*" if p < .05 else ""))


def main():
    df = C.load()                       # add_derived 内含 dev_int_z
    cn = df[df["CNT"] == "QCI"].reset_index(drop=True)
    print("QCI n =", len(cn))

    cols = {k: cn[c].values.astype(float) for k, c in VARS}
    W0 = cn["W_FSTUWT"].values.astype(float)
    wrep = {rc: cn[rc].values.astype(float) for rc in REPW}

    rows = []
    names = [k for k, _ in VARS]
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            r = wcorr(cols[a], cols[b], W0)
            reps = np.array([wcorr(cols[a], cols[b], w) for w in wrep.values()])
            var = BRR * np.nansum((reps - r) ** 2)
            se = float(np.sqrt(var))
            t = r / se if se > 0 else np.nan
            p = float(2 * stats.t.sf(abs(t), DF))
            rows.append(dict(row=a, col=b, r=round(r, 3), se=round(se, 4),
                             t=round(t, 3), p=p, star=star(p)))
    out = pd.DataFrame(rows)
    path = os.path.join(C.OUT, "corr_design_inference.csv")
    out.to_csv(path, index=False)
    print(out.to_string(index=False))
    print("\nsaved ->", path)


if __name__ == "__main__":
    main()
