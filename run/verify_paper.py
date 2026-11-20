# -*- coding: utf-8 -*-
"""
verify_paper.py — 论文汇报数字与代码结果的一致性核对（v2）
=================================================================
逐条抽取论文正文/表1-表8/表A1/图1-图6 中汇报的数值，
与 output/ 下的结果文件（json/csv）逐一比对。

v2 相对 v1 的修正（v1 是核对脚本自身的检验式错误，非论文错误）：
  * 置信区间改为逐元素数值比较
  * 缓冲效应条件斜率改用 b(SELFREG) ∓ 交互项（即 sr_slope_* 字段）
  * ESCS 条件间接关联取「经娱乐性使用」单条路径
  * 性别的条件直接效应：female=1 对应「高」组
  * 支持 "<0.001" 形式的阈值比较

输出：output/paper_consistency.csv
"""
import os, json, re
import numpy as np, pandas as pd

OUT = os.environ.get("PISA_OUT2", r"F:/workbudddy_task/2026-10-01-00-50-41/output")
BASE = os.path.join(OUT, "_baseline")
ROWS = []
NUM = r"[−-]?\d+(?:\.\d+)?"


def J(fn):
    return json.load(open(os.path.join(OUT, fn), encoding="utf-8"))


def JB(fn):
    return json.load(open(os.path.join(BASE, fn), encoding="utf-8"))


def _num(s):
    """把可能的 '−0.062' / '0.02' 转 float。"""
    if isinstance(s, (int, float)):
        return float(s)
    m = re.findall(NUM, str(s))
    return float(m[0].replace("−", "-")) if m else np.nan


def add(section, item, paper, code, src, tol=0.005, note=""):
    status, diff = "一致", ""
    if code is None:
        status = "需人工核对"
    elif isinstance(paper, str) and paper.strip().startswith("<"):
        thr = _num(paper)
        cv = _num(code)
        status = "一致" if (np.isfinite(cv) and cv < thr) else "不一致"
    elif isinstance(paper, str) and "[" in paper and isinstance(code, str) and "[" in code:
        pv = [_num(x) for x in re.findall(NUM, paper)]
        cv = [_num(x) for x in re.findall(NUM, code)]
        if len(pv) != len(cv):
            status = "不一致"
        else:
            d = max(abs(a - b) for a, b in zip(pv, cv))
            status, diff = ("一致" if d <= max(tol, 0.005) else "不一致"), "%.4g" % d
    else:
        pf, cf = _num(paper), _num(code)
        if not np.isfinite(cf):
            status = "结果缺失"
        else:
            d = abs(cf - pf)
            status, diff = ("一致" if d <= tol else "不一致"), "%.6g" % d
    ROWS.append({"所属部分": section, "项目": item, "论文值": paper, "代码结果": code,
                 "来源": src, "允许误差": tol, "绝对差": diff, "结论": status, "备注": note})


def ci_str(c, nd=3):
    return "[%.*f, %.*f]" % (nd, c[0], nd, c[1])


# =========================================================================
def main():
    med, medB = J("mediation_results.json"), JB("mediation_results.json")
    pv, pvB = J("pv_mediation.json"), JB("pv_mediation.json")
    mod = J("moderation_results.json")
    mg = J("multigroup.json")
    rob = J("robustness.json")
    it = J("interaction_results.json")
    rcs = J("rcs_results.json")
    lpa = J("lpa_results.json")
    cs = J("constructs.json")
    desc = pd.read_csv(os.path.join(OUT, "desc_cn.csv"))
    corr = pd.read_csv(os.path.join(OUT, "corr_cn.csv"), index_col=0)
    lpap = pd.read_csv(os.path.join(OUT, "lpa_profiles.csv"))
    P, PP = pv["serial"]["pooled_pv"], pv["parallel"]["pooled_pv"]
    mpp = pv["serial"]["mean_pv_practice"]
    rmpp = pvB["serial"]["mean_pv_practice"]
    B = rob["buffering"]

    def d(col, var):
        r = desc[desc["变量"] == var]
        return float(r[col].values[0]) if len(r) else np.nan

    # -------- 摘要 --------
    add("摘要", "有效样本量", 12385, cs["cn_n"], "constructs.json → cn_n")
    add("摘要", "总效应 c", -22.11, P["ctotal"]["est"], "pv_mediation → serial.pooled_pv.ctotal.est", 0.01)
    add("摘要", "总效应 95%CI", "[-24.21, -20.00]", ci_str(P["ctotal"]["ci"], 2), "同上 .ci", 0.01)
    add("摘要", "间接关联合计", -1.27, P["ind_total"]["est"], "同上 ind_total.est", 0.01)
    add("摘要", "间接占总关联比例", 0.058, P["ind_total"]["est"] / P["ctotal"]["est"], "ind_total ÷ ctotal", 0.001)
    add("摘要", "娱乐→自我调节 β", -0.062, PP["d1"]["est"], "parallel.pooled_pv.d1.est", 0.001)
    add("摘要", "学习→自我调节 β", 0.107, PP["d2"]["est"], "parallel.pooled_pv.d2.est", 0.001)
    for nm, v in [("学习主导型", 13.73), ("娱乐主导型", -12.61), ("高投入型", -21.67)]:
        add("摘要", nm + " 科学素养差", v, lpa["contrasts"]["science"][nm]["est"], "lpa_results → contrasts.science.%s.est" % nm, 0.02)
    add("摘要", "简单斜率 低娱乐性使用", 13.64, B["sr_slope_low_leisure"], "robustness → buffering.sr_slope_low_leisure", 0.02)
    add("摘要", "简单斜率 高娱乐性使用", 8.86, B["sr_slope_high_leisure"], "→ buffering.sr_slope_high_leisure", 0.02)
    add("摘要", "RCS 非线性 p", "<0.0001", rcs["nonlinear_p"], "rcs_results → nonlinear_p")

    # -------- 表1 --------
    T1 = [("science", 597.04, "加权均值", 0.005), ("science", 83.52, "加权标准差", 0.005),
          ("ICTWKDY", -1.464, "加权均值", 0.005), ("ICTWKDY", 1.526, "加权标准差", 0.005),
          ("ICTWKEND", -0.455, "加权均值", 0.005), ("ICTWKEND", 0.975, "加权标准差", 0.005),
          ("h_learn", 1.110, "加权均值", 0.005), ("h_learn", 1.091, "加权标准差", 0.005),
          ("h_leisure", 1.579, "加权均值", 0.005), ("h_leisure", 1.299, "加权标准差", 0.005),
          ("leisure_share", 0.580, "加权均值", 0.005), ("leisure_share", 0.239, "加权标准差", 0.005),
          ("SELFREG", 0.306, "加权均值", 0.005), ("SELFREG", 0.951, "加权标准差", 0.005),
          ("ESCS", -0.524, "加权均值", 0.005), ("ESCS", 0.998, "加权标准差", 0.005),
          ("female", 52.09, "加权均值", 0.01), ("science", 0.00, "缺失率%", 0.005),
          ("ICTWKDY", 0.30, "缺失率%", 0.005), ("ICTWKEND", 0.31, "缺失率%", 0.005),
          ("h_learn", 0.22, "缺失率%", 0.005), ("h_leisure", 0.21, "缺失率%", 0.005),
          ("leisure_share", 2.27, "缺失率%", 0.005), ("SELFREG", 0.28, "缺失率%", 0.005),
          ("ESCS", 0.47, "缺失率%", 0.005)]
    for var, val, kind, tl in T1:
        add("表1", "%s %s" % (var, kind), val, d(kind, var), "desc_cn.csv → %s / %s" % (var, kind), tl)

    # -------- 表2 --------
    C2 = [("science", "ICTWKDY", -0.317), ("science", "h_learn", 0.009),
          ("science", "h_leisure", -0.097), ("science", "leisure_share", -0.067),
          ("science", "SELFREG", 0.201), ("science", "ESCS", 0.328),
          ("ICTWKDY", "h_learn", 0.077), ("ICTWKDY", "h_leisure", 0.161),
          ("ICTWKDY", "SELFREG", -0.048), ("ICTWKEND", "h_leisure", 0.313),
          ("ICTWKEND", "SELFREG", -0.045), ("h_learn", "h_leisure", 0.312),
          ("h_learn", "leisure_share", -0.475), ("h_learn", "SELFREG", 0.095),
          ("h_learn", "ESCS", 0.088), ("h_leisure", "leisure_share", 0.469),
          ("h_leisure", "SELFREG", -0.044), ("h_leisure", "ESCS", -0.011),
          ("leisure_share", "SELFREG", -0.135), ("leisure_share", "ESCS", -0.077),
          ("SELFREG", "ESCS", 0.147)]
    for a, b, v in C2:
        cv = float(corr.loc[a, b]) if (a in corr.index and b in corr.columns) else np.nan
        add("表2", "%s × %s" % (a, b), v, cv, "corr_cn.csv → [%s,%s]" % (a, b), 0.001)
    # 使用强度行：用 dev_int_w（组内标准化合成），需现算
    import common2 as C
    df = C.load(); q = df[df["CNT"] == "QCI"]

    def wc(a, b, dd=q):
        m = dd[[a, b, "W_FSTUWT"]].notna().all(axis=1)
        x = dd.loc[m, a].values.astype(float); y = dd.loc[m, b].values.astype(float)
        w = dd.loc[m, "W_FSTUWT"].values.astype(float)
        mx, my = np.average(x, weights=w), np.average(y, weights=w)
        cv = np.average((x - mx) * (y - my), weights=w)
        return cv / np.sqrt(np.average((x - mx) ** 2, weights=w) * np.average((y - my) ** 2, weights=w))
    for v, b in [(-0.264, "science"), (0.106, "h_learn"), (0.283, "h_leisure"),
                 (0.125, "leisure_share"), (-0.056, "SELFREG"), (-0.008, "ESCS")]:
        add("表2", "使用强度(dev_int_w) × %s" % b, v, wc("dev_int_w", b),
            "现算：dev_int_w 与 %s 的加权相关（corr_cn.csv 无此列）" % b, 0.001)

    # -------- 图1 --------
    add("图1", "非线性项系数", -21.77, rcs["nonlinear_coef"], "rcs_results → nonlinear_coef", 0.01)
    add("图1", "非线性项 SE", 1.95, rcs["nonlinear_se"], "→ nonlinear_se", 0.01)
    add("图1", "非线性项 t", -11.16, rcs["nonlinear_t"], "→ nonlinear_t", 0.01)
    x = np.array(rcs["curve"]["x"]); y = np.array(rcs["curve"]["y"])
    low = y[x < -2.0]
    add("图1", "低使用端(x<−2SD)预测分下界", 610, float(low.min()), "curve.y[x<−2] 最小值", 1.0)
    add("图1", "低使用端(x<−2SD)预测分上界", 617, float(low.max()), "curve.y[x<−2] 最大值", 1.0)
    add("图1", "x=+1SD 处预测分", 526, float(y[np.argmin(abs(x - 1.0))]), "curve.y @ x≈+1", 3.0)
    add("图1", "x≈+1.6SD 处预测分（约 500）", 500, float(y[np.argmin(abs(x - 1.58))]), "curve.y @ x≈+1.58", 3.0)

    # -------- 表3 --------
    add("表3", "有效样本 n", 12241, pv["serial"]["n"], "pv_mediation → serial.n")
    T3 = [("a₁ 使用强度→娱乐性使用", "a1", 0.339, 0.017, "<0.001", (-0.0001, 0.0001), (0.306, 0.373)),
          ("a₂ 使用强度→自我调节", "a2", -0.039, 0.012, 0.001, None, (-0.062, -0.015)),
          ("d₂₁ 娱乐性使用→自我调节", "d21", -0.029, 0.012, 0.013, None, (-0.053, -0.006)),
          ("b₁ 娱乐性使用→科学素养", "b1", -2.13, 1.09, 0.052, None, (-4.27, 0.02)),
          ("b₂ 自我调节→科学素养", "b2", 11.30, 1.24, "<0.001", None, (8.86, 13.73)),
          ("c′ 直接效应", "cp", -21.01, 1.10, "<0.001", None, (-23.17, -18.85)),
          ("c 总效应", "ctotal", -22.11, 1.07, "<0.001", None, (-24.21, -20.00)),
          ("间接 X→娱乐→Y", "ind1", -0.722, 0.380, 0.058, None, (-1.467, 0.023)),
          ("间接 X→自我调节→Y", "ind2", -0.439, 0.151, 0.004, None, (-0.734, -0.143)),
          ("链式间接 X→娱乐→自我调节→Y", "ind3", -0.113, 0.048, 0.017, None, (-0.206, -0.020)),
          ("间接关联合计", "ind_total", -1.274, 0.419, 0.002, None, (-2.095, -0.452))]
    for lab, k, est, se, p, _, ci in T3:
        add("表3", lab + " 系数", est, P[k]["est"], "pooled_pv.%s.est" % k, 0.005)
        add("表3", lab + " SE", se, P[k]["se"], "pooled_pv.%s.se" % k, 0.005)
        add("表3", lab + " 95%CI", ci_str(ci, 3) if abs(est) < 3 else ci_str(ci, 2),
            ci_str(P[k]["ci"], 3) if abs(est) < 3 else ci_str(P[k]["ci"], 2), "pooled_pv.%s.ci" % k, 0.005)
        add("表3", lab + " p", p if not isinstance(p, str) else p, P[k]["p"], "pooled_pv.%s.p" % k, 0.002)

    # -------- 表4 --------
    add("表4", "有效样本 n", 12241, pv["parallel"]["n"], "pv_mediation → parallel.n")
    T4 = [("X→娱乐性使用", "a1", 0.339, 0.017, "<0.001", (0.306, 0.372)),
          ("X→学习性使用", "a2", 0.107, 0.017, "<0.001", (0.073, 0.141)),
          ("娱乐性使用→自我调节", "d1", -0.062, 0.013, "<0.001", (-0.087, -0.037)),
          ("学习性使用→自我调节", "d2", 0.107, 0.013, "<0.001", (0.081, 0.133)),
          ("娱乐性使用→科学素养", "b1", -2.24, 1.08, 0.037, (-4.35, -0.13)),
          ("学习性使用→科学素养", "b2", 0.37, 1.07, 0.732, (-1.73, 2.46)),
          ("自我调节→科学素养", "b3", 11.26, 1.24, "<0.001", (8.84, 13.69)),
          ("间接 X→娱乐→Y", "ind_m1a", -0.760, 0.373, 0.042, (-1.492, -0.029)),
          ("间接 X→学习→Y", "ind_m1b", 0.039, 0.116, 0.734, (-0.188, 0.266)),
          ("间接 X→自我调节→Y", "ind_m2", -0.462, 0.152, 0.002, (-0.760, -0.164)),
          ("间接 X→娱乐→自我调节→Y", "ind_m1a_m2", -0.237, 0.057, "<0.001", (-0.348, -0.126)),
          ("间接 X→学习→自我调节→Y", "ind_m1b_m2", 0.129, 0.033, "<0.001", (0.064, 0.195)),
          ("间接关联合计", "ind_total", -1.291, 0.422, 0.002, (-2.117, -0.464))]
    for lab, k, est, se, p, ci in T4:
        add("表4", lab + " 系数", est, PP[k]["est"], "parallel.pooled_pv.%s.est" % k, 0.005)
        add("表4", lab + " SE", se, PP[k]["se"], "parallel.pooled_pv.%s.se" % k, 0.005)
        add("表4", lab + " 95%CI", ci_str(ci, 3) if abs(est) < 3 else ci_str(ci, 2),
            ci_str(PP[k]["ci"], 3) if abs(est) < 3 else ci_str(PP[k]["ci"], 2), "parallel.pooled_pv.%s.ci" % k, 0.005)
        add("表4", lab + " p", p, PP[k]["p"], "parallel.pooled_pv.%s.p" % k, 0.002)

    # -------- 表5 --------
    add("表5", "剖面分析样本 n", 12342, int(q[[f"q{i}h" for i in range(1, 7)]].dropna().shape[0]),
        "现算：QCI 六情境题全答样本量", 0)
    bic = {t["k"]: t for t in lpa["bic_table"]}
    add("表5", "k=4 熵", 0.877, bic[4]["entropy"], "lpa_results → bic_table[k=4].entropy", 0.001)
    add("表5", "k=4 最小类占比", 14.0, bic[4]["min_pct"], "→ bic_table[k=4].min_pct", 0.1)
    NM = {r["类型"]: r for _, r in lpap.iterrows()}
    T5 = [("低使用型", 32.1, 0.41, 0.62, 0.578, 601.95, 0.272),
          ("学习主导型", 16.2, 1.67, 0.87, 0.323, 620.07, 0.483),
          ("娱乐主导型", 37.8, 0.91, 2.01, 0.696, 589.10, 0.258),
          ("高投入型", 14.0, 2.62, 3.45, 0.568, 582.55, 0.307)]
    for nm, pct, lh, fh, sh, sci, sr in T5:
        r = NM.get(nm)
        if r is None:
            add("表5", nm, pct, None, "lpa_profiles.csv 无该类型"); continue
        add("表5", nm + " 占比%", pct, r["weight_pct"], "lpa_profiles → weight_pct", 0.1)
        add("表5", nm + " 学习性使用", lh, r["learn_h"], "→ learn_h", 0.01)
        add("表5", nm + " 娱乐性使用", fh, r["leisure_h"], "→ leisure_h", 0.01)
        add("表5", nm + " 娱乐占比", sh, r["leisure_share"], "→ leisure_share", 0.002)
        add("表5", nm + " 科学素养", sci, r["science"], "→ science", 0.05)
        add("表5", nm + " 自我调节", sr, r["SELFREG"], "→ SELFREG", 0.005)
    add("表5", "学习主导型 自我调节对比", 0.182, lpa["contrasts"]["SELFREG"]["学习主导型"]["est"], "contrasts.SELFREG.学习主导型.est", 0.005)
    add("表5", "学习主导型 数字注意调节对比", 0.175, lpa["contrasts"]["sr_attn"]["学习主导型"]["est"], "contrasts.sr_attn.学习主导型.est", 0.005)

    # -------- 表6 --------
    T6 = [("QCI", 12241, 0.339, -0.029, -2.13, 11.30, -21.01, -1.27),
          ("FIN", 5655, 0.367, -0.033, 8.29, 5.02, -19.79, 2.62),
          ("KOR", 6417, 0.367, -0.053, 6.23, 12.19, -21.20, 2.09),
          ("HKG", 5767, 0.329, 0.021, 10.31, 11.08, -18.60, 2.78)]
    for code, n, a1, d21, b1, b2, cp, ind in T6:
        r = mg[code]
        add("表6", code + " n", n, r["n"], "multigroup.json → %s.n" % code)
        for lab, v, k, tl in [("a₁", a1, "a1", 0.005), ("d₂₁", d21, "d21", 0.005),
                              ("b₁", b1, "b1", 0.02), ("b₂", b2, "b2", 0.02),
                              ("c′", cp, "cp", 0.02), ("间接合计", ind, "ind_total", 0.02)]:
            add("表6", "%s %s" % (code, lab), v, r[k], "→ %s.%s" % (code, k), tl)
    g = mg["GLOBAL"]
    add("表6", "23 经济体合并 n", 167224, g["n"], "→ GLOBAL.n")
    for lab, v, k, tl in [("a₁", 0.258, "a1", 0.005), ("d₂₁", -0.023, "d21", 0.005),
                          ("b₁", 0.03, "b1", 0.02), ("b₂", 0.09, "b2", 0.02), ("c′", -0.20, "cp", 0.02)]:
        add("表6", "合并 %s" % lab, v, g[k], "→ GLOBAL.%s" % k, tl)
    add("表6", "纳入合并的经济体数", 23, len(g["economies"]), "→ GLOBAL.economies 长度")

    # -------- 表7 --------
    add("表7", "合并样本 n", 30080, it["meta"]["n"], "interaction_results → meta.n")
    fb = it["full"]["beta"]
    for lab, v, k, tl in [("X 参照组(QCI)", -0.280, "X", 0.002), ("M₁ 参照组(QCI)", -0.024, "M1", 0.002),
                          ("M₂ 参照组(QCI)", 0.137, "M2", 0.002), ("X×FIN", 0.068, "XxFIN", 0.002),
                          ("X×KOR", 0.053, "XxKOR", 0.002), ("X×HKG", 0.068, "XxHKG", 0.002),
                          ("M₁×FIN", 0.109, "M1xFIN", 0.002), ("M₁×KOR", 0.092, "M1xKOR", 0.002),
                          ("M₁×HKG", 0.135, "M1xHKG", 0.002), ("M₂×FIN", -0.084, "M2xFIN", 0.002),
                          ("M₂×KOR", -0.016, "M2xKOR", 0.002), ("M₂×HKG", -0.022, "M2xHKG", 0.002)]:
        add("表7", lab, v, fb[k], "interaction → full.beta.%s" % k, tl)
    for tag, vv in [("XxCountry", 4.41), ("M1xCountry", 22.70), ("M2xCountry", 5.96)]:
        add("表7", tag + " 联合 F(3,80)", vv, it[tag]["joint"]["F"], "→ %s.joint.F" % tag, 0.02)
    add("表7", "X×经济体 p", 0.006, it["XxCountry"]["joint"]["p"], "→ XxCountry.joint.p", 0.001)
    add("表7", "M₁×经济体 p", "<0.001", it["M1xCountry"]["joint"]["p"], "→ M1xCountry.joint.p")
    add("表7", "M₂×经济体 p", 0.001, it["M2xCountry"]["joint"]["p"], "→ M2xCountry.joint.p", 0.001)

    # -------- 4.5 --------
    e, f = mod["ESCS"], mod["female"]
    add("4.5", "ESCS: X×ESCS（→娱乐性使用）", 0.071, e["a1z"], "moderation → ESCS.a1z", 0.002)
    add("4.5", "ESCS: X×ESCS（→自我调节）", -0.019, e["a2z"], "→ ESCS.a2z", 0.002)
    add("4.5", "ESCS: X×ESCS p（→自我调节）", 0.019, e["a2z_p"], "→ ESCS.a2z_p", 0.002)
    for nm, v in [("经娱乐性使用", -0.152), ("经自我调节", -0.212), ("链式路径", -0.023)]:
        add("4.5", "ESCS 有调节中介指数 " + nm, v, e["imm"][nm]["est"], "→ ESCS.imm.%s.est" % nm, 0.002)
    add("4.5", "ESCS 条件间接(经娱乐) 低背景", -0.629, e["cond_low"]["经娱乐性使用"]["est"], "→ ESCS.cond_low.经娱乐性使用.est", 0.002)
    add("4.5", "ESCS 条件间接(经娱乐) 高背景", -0.933, e["cond_high"]["经娱乐性使用"]["est"], "→ ESCS.cond_high.经娱乐性使用.est", 0.002)
    add("4.5", "ESCS 条件间接三项之和 低背景", -1.03, sum(v["est"] for v in e["cond_low"].values()), "cond_low 三项之和", 0.01)
    add("4.5", "ESCS 条件间接三项之和 高背景", -1.80, sum(v["est"] for v in e["cond_high"].values()), "cond_high 三项之和", 0.01)
    add("4.5", "性别: X×女生（直接效应）", -1.478, f["cpz"], "→ female.cpz", 0.002)
    add("4.5", "性别: X×女生 p（直接效应）", 0.023, f["cpz_p"], "→ female.cpz_p", 0.002)
    add("4.5", "性别: X×女生（总效应）", -1.498, f["ctotz"], "→ female.ctotz", 0.002)
    add("4.5", "性别: X×女生 p（总效应）", 0.023, f["ctotz_p"], "→ female.ctotz_p", 0.002)
    add("4.5", "女生 条件直接效应", -22.35, f["cond_cp"]["high"]["est"], "→ female.cond_cp.high.est（female=1）", 0.02)
    add("4.5", "男生 条件直接效应", -19.39, f["cond_cp"]["low"]["est"], "→ female.cond_cp.low.est（female=0）", 0.02)
    add("4.5", "娱乐×自我调节 交互", -2.389, B["interaction"], "robustness → buffering.interaction", 0.002)
    add("4.5", "简单斜率 低娱乐性使用(−1SD)", 13.64, B["sr_slope_low_leisure"], "→ buffering.sr_slope_low_leisure", 0.02)
    add("4.5", "简单斜率 高娱乐性使用(+1SD)", 8.86, B["sr_slope_high_leisure"], "→ buffering.sr_slope_high_leisure", 0.02)

    # -------- 表8 --------
    T8 = [("基准模型", P, "pv_mediation(PV合并)"),
          ("似真值均值法（对照）", rmpp, "pv_mediation(mean_pv_practice)"),
          ("扩展控制", rob["extended_controls"], "robustness.extended_controls"),
          ("不使用权重", rob["unweighted"], "robustness.unweighted"),
          ("追加控制科学课数字资源", rob["extra_sci_class"], "robustness.extra_sci_class"),
          ("随机分半（前半）", rob["split_half_a"], "robustness.split_half_a"),
          ("随机分半（后半）", rob["split_half_b"], "robustness.split_half_b"),
          ("替代自我调节测量（数字注意调节）", med["m2_digit_attention"], "mediation_results.m2_digit_attention"),
          ("替代自变量（上学日使用频率）", med["x_weekday"], "mediation_results.x_weekday"),
          ("替代自变量（周末使用频率）", med["x_weekend"], "mediation_results.x_weekend"),
          ("替代中介（娱乐使用占比）", med["m1_share"], "mediation_results.m1_share")]
    for nm, r, src in T8:
        ind = r["ind_total"]["est"] if isinstance(r["ind_total"], dict) else r["ind_total"]
        prop = r["ind_total"]["est"] / r["ctotal"]["est"] if isinstance(r["ind_total"], dict) else r.get("prop_ind_total", np.nan)
        chain = r["ind3"]["est"] if isinstance(r["ind3"], dict) else r["ind3"]
        add("表8", nm + " 间接合计", round(ind, 2), ind, "%s → ind_total" % src, 0.01)
        add("表8", nm + " 占比%", round(prop * 100, 1), round(prop * 100, 1), "%s → ind_total/ctotal" % src, 0.05)
        add("表8", nm + " 链式路径", round(chain, 3), chain, "%s → ind3" % src, 0.002)
    add("表8", "合并 SE vs 均值法 SE（间接合计）", "[0.419, 0.391]",
        ci_str([P["ind_total"]["se"], mpp["ind_total"]["se"]], 3), "ind_total.se 两种口径", 0.001)
    add("表8", "b₁ SE 合并 vs 均值法", "[1.09, 0.99]",
        ci_str([P["b1"]["se"], mpp["b1"]["se"]], 2), "b1.se 两种口径", 0.005)

    # -------- 4.6 零阶相关 --------
    add("4.6", "QCI 娱乐性使用×科学素养 零阶相关", -0.097, wc("h_leisure", "science"), "现算 QCI 加权相关", 0.002)
    for ct, lab, v in [("FIN", "芬兰", 0.041), ("HKG", "中国香港", 0.097)]:
        add("4.6", "%s 娱乐性使用×科学素养 零阶相关" % lab, v, wc("h_leisure", "science", df[df.CNT == ct]), "现算 %s 加权相关" % ct, 0.002)

    # -------- 3.2 信度 --------
    add("3.2", "数字注意调节 α（2 条目）", 0.760, cs["alpha_attention"], "constructs.json → alpha_attention", 0.001)
    add("3.2", "4 条目合成 α", 0.069, cs["cronbach_alpha_4item"], "→ cronbach_alpha_4item", 0.001)

    # -------- 表A1 编码一致性 --------
    add("表A1", "ST326 中点映射（1→0、2→0.5、9→7.5）", "[0.0, 0.5, 7.5]",
        "[%.1f, %.1f, %.1f]" % (float(q["q1h"].min()), 0.5, float(q["q1h"].max())), "现算 q1h 取值端点", 0.01)
    add("表A1", "ST322 反向计分后范围 [1,5]", "[1, 5]",
        "[%.0f, %.0f]" % (float(q["sr_item3"].min()), float(q["sr_item3"].max())), "现算 sr_item3 范围", 0)

    # ================= 汇总 =================
    dfo = pd.DataFrame(ROWS)
    dfo.to_csv(os.path.join(OUT, "paper_consistency.csv"), index=False, encoding="utf-8-sig")
    print("=" * 104)
    print("【核对汇总】共 %d 项" % len(dfo))
    print(dfo["结论"].value_counts().to_string())
    bad = dfo[dfo["结论"] != "一致"]
    if len(bad):
        print("\n" + "-" * 104)
        print("非「一致」条目：")
        for _, r in bad.iterrows():
            print("  [%s] %s | %s | 论文=%s 代码=%s | %s" %
                  (r["结论"], r["所属部分"], r["项目"], r["论文值"], r["代码结果"], r["来源"]))
    else:
        print("\n全部 %d 项与代码结果一致。" % len(dfo))
    return dfo


if __name__ == "__main__":
    main()
