# -*- coding: utf-8 -*-
"""
s15_joint_tests.py — 用 s14 的设计基础结果做「跨系统等值」联合 Wald 检验
=====================================================================
背景：原稿的 F(3,80) 来自 s9_interaction.py（加权 bootstrap）。该 bootstrap 的
      间接效应区间存在技术问题（区间不含点估计，见报告第九节④），不适合再作为
      正文的检验依据。
做法：四个经济体是独立样本，故 contrast h_i = θ_i − θ_QCI 的协方差为
          var(h_i) = v_i + v_QCI,
          cov(h_i, h_j) = v_QCI  (i ≠ j)
      W = h' V^{-1} h ~ chi2(3)，F = W/3，df2 = 80（BRR 复制数）。
输出：output/joint_tests.json，并打印可粘进论文的句子。
"""
import os, json
import numpy as np
from scipy import stats

OUT = os.path.join(os.path.dirname(__file__), "output")
SYSTEMS = ["QCI", "FIN", "KOR", "HKG"]
KEYS = [("ctotal", "Total (c)"), ("cp", "Direct (c')"),
        ("d1", "Entertainment -> self-regulation"),
        ("d2", "Learning -> self-regulation"),
        ("b1", "Entertainment -> literacy"),
        ("b2", "Learning -> literacy"),
        ("b3", "Self-regulation -> literacy"),
        ("ind_m1a_m2", "Serial via entertainment"),
        ("ind_m1b_m2", "Serial via learning"),
        ("ind_total", "All indirect")]


def main():
    res = json.load(open(os.path.join(OUT, "multisystem_pv.json"), encoding="utf-8"))
    out = {}
    print("%-36s %8s %8s %8s %8s   F(3,80)   p" % ("parameter", "QCI", "FIN", "KOR", "HKG"))
    print("-" * 96)
    for key, label in KEYS:
        theta = np.array([res[s][key]["est"] for s in SYSTEMS])
        var = np.array([res[s][key]["se"] ** 2 for s in SYSTEMS])
        h = theta[1:] - theta[0]
        k = len(h)
        V = np.diag(var[1:] + var[0]) + np.full((k, k), var[0]) - np.diag(np.full(k, var[0]))
        W = float(h @ np.linalg.solve(V, h))
        F = W / k
        p = float(stats.f.sf(F, k, 80))
        out[key] = dict(theta=[float(v) for v in theta], se=[float(np.sqrt(v)) for v in var],
                        contrasts=[float(v) for v in h], W=W, df1=k, df2=80, F=F, p=p)
        print("%-36s %8.3f %8.3f %8.3f %8.3f   %6.2f  %s"
              % (label, *theta, F, "< .001" if p < .001 else "%.3f" % p))

    with open(os.path.join(OUT, "joint_tests.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print("\n可粘用句：")
    for key, label in KEYS:
        r = out[key]
        if r["p"] < .10:
            print("  %-36s F(3, 80) = %.2f, p %s" %
                  (label, r["F"], "< .001" if r["p"] < .001 else "= %.3f" % r["p"]))
    print("\nsaved ->", os.path.join(OUT, "joint_tests.json"))


if __name__ == "__main__":
    main()
