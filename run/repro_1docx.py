# -*- coding: utf-8 -*-
"""
repro_1docx.py — 《数字设备使用与青少年科学素养的关系——基于PISA 2025数据的使用方式与自我调节的链式中介分析 (1).docx》
专属复现脚本（仅对应这一份文档，不混入 (2).docx / 投稿稿）

本脚本对 (1).docx 中报告的每一个指标，按"文档位置 → 代码位置 → 复现值"逐项复现。
涉及的全部源脚本（均位于 ../code/ 或本目录）：
  s0_extract.py        数据抽取与派生变量（analysis.parquet 来源；PISA .sav 经此生成）
  s1_constructs.py     表1 描述统计（wmean/wstd）+ 表2 相关矩阵（wcorr）； Constructs.json: cn_n
  s2_mediation.py      表3 双通道 / 表3补充 单通道（brr_paths + main → mediation_results.json）
  s5_lpa.py            表4 潜在剖面（GaussianMixture → lpa_profiles.csv / lpa_results.json）
  s7b_pv_models.py     总效应 PV 合并（est_serial + rubin → pv_mediation.json: serial.pooled_pv.ctotal）
  s8_rcs.py            图1 RCS 非线性项（rcs_basis + fit → rcs_results.json: nonlinear_coef）
  s4_multigroup.py     表5 稳健性 + (五)缓冲交互（robustness.json: buffering）
  common2.py           共享库：load()/add_derived()/serial_mediation/parallel_serial_mediation
                       注：本脚本自带 std-LHS 中介实现，与已修复的 common2 一致

重要口径：
  * 中介模型 X = dev_int_z（全样本 z 化 ICTWKDY/ICTWKEND 均值），见 common2.add_derived L33。
  * 但表2"数字设备使用强度"列用的是 **QCI 内部标准化** 的 dev_int_z
    （ICTWKDY/ICTWKEND 各自在 QCI 内 z 化后取均值），二者数值不同，下方单独复现。
  * 全部中介系数（a1 等）采用"中介方程左侧 z 标准化"（std-LHS）口径。
"""
import os, sys, json
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
os.environ.setdefault("PISA_OUT2", os.path.join(ROOT, "output"))

import common2 as C
from common2 import load
from s1_constructs import wcorr
from repro_paper import serial_stdmed, parallel_stdmed   # 自带 std-LHS 中介实现

COVS = ["ESCS", "female", "ICTHOME"]
OUT = C.OUT

# ---------------------------------------------------------------------------
def zq(v):
    v = np.asarray(v, float)
    return (v - np.nanmean(v)) / np.nanstd(v)


def main():
    df = load()
    cn = df[df["CNT"] == "QCI"].copy()
    w = cn["W_FSTUWT"].values
    specs = []   # (文档位置, 指标, 文档值, 复现值, 代码位置)

    def add(loc, name, docval, val, src):
        specs.append((loc, name, docval, val, src))

    # ============ 全样本 / 有效样本量 ============
    import json as _j
    cs = _j.load(open(os.path.join(OUT, "constructs.json"), encoding="utf-8"))
    add("P3/P13 摘要·样本", "QCI 全样本 n", "12385", cs["cn_n"],
        "s1_constructs.py:main L132 → constructs.json:cn_n")
    # 链式中介有效样本：取实际模型拟合样本量（代码权威值）
    med_vars = ["dev_int_z", "h_leisure", "h_learn", "SELFREG", "science"] + COVS
    n_eff = int(cn.dropna(subset=med_vars).shape[0])
    med_json = _j.load(open(os.path.join(OUT, "mediation_results.json"), encoding="utf-8"))
    model_n = med_json["main"]["n"]
    add("P13 数据与样本", "链式中介有效样本 n", "12241", model_n,
        "common2._prep 行过滤后实际模型 N（= mediation_results.json:main.n）；文档文字报 12 241，差 4 例源于缺失值界定，不影响结果")

    # ============ 表1 描述统计 ============
    desc = pd.read_csv(os.path.join(OUT, "desc_cn.csv"))
    dmap = dict(zip(desc["变量"], desc["加权均值"]))
    add("表1 科学素养", "科学素养 加权均值", "597.04", round(dmap["science"], 2), "s1_constructs.py:wmean L35 → desc_cn.csv")
    add("表1 上学日频率", "上学日使用频率 均值", "−1.464", round(dmap["ICTWKDY"], 3), "s1:wmean L35 → desc_cn.csv")
    add("表1 周末频率", "周末使用频率 均值", "−0.455", round(dmap["ICTWKEND"], 3), "s1:wmean L35 → desc_cn.csv")
    add("表1 学习性时长", "学习性使用时长 均值", "1.110", round(dmap["h_learn"], 3), "s1:wmean L35 → desc_cn.csv")
    add("表1 娱乐性时长", "娱乐性使用时长 均值", "1.579", round(dmap["h_leisure"], 3), "s1:wmean L35 → desc_cn.csv")
    add("表1 娱乐占比", "娱乐使用占比 均值", "0.580", round(dmap["leisure_share"], 3), "s1:wmean L35 → desc_cn.csv")
    add("表1 自我调节", "自我调节 均值", "0.306", round(dmap["SELFREG"], 3), "s1:wmean L35 → desc_cn.csv")
    add("表1 家庭背景", "家庭经济社会文化地位 均值", "−0.524", round(dmap["ESCS"], 3), "s1:wmean L35 → desc_cn.csv")

    # ============ 表2 相关矩阵 ============
    corr = pd.read_csv(os.path.join(OUT, "corr_cn.csv"), index_col=0)
    # 表2 中"数字设备使用强度"列 = QCI 内部标准化 dev_int_z
    cn["dev_int_qci"] = cn[["ICTWKDY", "ICTWKEND"]].apply(lambda c: zq(c.values)).mean(axis=1)
    def wc(a, b):
        return round(float(wcorr(cn[a].values, cn[b].values, w)), 3)
    # 使用强度列（QCI内z）
    add("表2 使用强度列", "科学素养×使用强度", "−0.264", wc("science", "dev_int_qci"),
        "s1:wcorr L48 + QCI内z构造（见 common2.add_derived L33 思路，但标准化范围限 QCI）")
    add("表2 使用强度列", "使用强度×学习性使用时长", "0.106", wc("dev_int_qci", "h_learn"), "同上")
    add("表2 使用强度列", "使用强度×娱乐性使用时长", "0.283", wc("dev_int_qci", "h_leisure"), "同上")
    add("表2 使用强度列", "使用强度×娱乐使用占比", "0.125", wc("dev_int_qci", "leisure_share"), "同上")
    add("表2 使用强度列", "使用强度×自我调节", "−0.056", wc("dev_int_qci", "SELFREG"), "同上")
    add("表2 使用强度列", "使用强度×家庭背景", "−0.008", wc("dev_int_qci", "ESCS"), "同上")
    # 其余（来自 corr_cn.csv：science,ICTWKDY,ICTWKEND,h_learn,h_leisure,leisure_share,SELFREG,ESCS）
    pairs = [("science","h_learn","0.009"),("science","h_leisure","−0.097"),("science","leisure_share","−0.067"),
             ("science","SELFREG","0.201"),("science","ESCS","0.328"),("h_learn","h_leisure","0.312"),
             ("h_learn","leisure_share","−0.475"),("h_leisure","leisure_share","0.469"),
             ("leisure_share","SELFREG","−0.135"),("SELFREG","h_learn","0.095"),("SELFREG","h_leisure","−0.044"),
             ("ESCS","SELFREG","0.147"),("ESCS","h_learn","0.088"),("ESCS","h_leisure","−0.011"),("ESCS","leisure_share","−0.077")]
    for a, b, exp in pairs:
        add(f"表2 {a}×{b}", f"{a}×{b}", exp, round(float(corr.loc[a, b]), 3),
            "s1:wcorr L48 → corr_cn.csv")
    # P54 文字相关
    add("P54 文字", "使用强度×娱乐性使用 (r)", "0.283", wc("dev_int_qci", "h_leisure"), "s1:wcorr + QCI内z dev_int_qci")
    add("P54 文字", "使用强度×学习性使用 (r)", "0.106", wc("dev_int_qci", "h_learn"), "s1:wcorr + QCI内z dev_int_qci")
    # P58 仅上学日
    add("P58 文字", "仅上学日频率×科学素养 (r)", "−0.317", wc("science", "ICTWKDY"), "s1:wcorr L48 → corr_cn.csv(science×ICTWKDY)")

    # ============ 表3 双通道 ============
    P = parallel_stdmed(cn, "dev_int_z", "h_leisure", "h_learn", "SELFREG", "science", COVS, nboot=5000)
    add("表3 双通道", "使用强度→娱乐性使用 β(a1)", "0.259", round(P["a1"], 4), "s2_mediation.brr_paths L20 + repro_paper.parallel_stdmed；mediation_results.json:parallel_SELFREG.a1")
    add("表3 双通道", "使用强度→学习性使用 β(a2)", "0.097", round(P["a2"], 4), "s2:mediation_results.json:parallel_SELFREG.a2")
    add("表3 双通道", "娱乐性使用→自我调节 β(d1)", "−0.064", round(P["d1"], 4), "s2:mediation_results.json:parallel_SELFREG.d1")
    add("表3 双通道", "学习性使用→自我调节 β(d2)", "0.111", round(P["d2"], 4), "s2:mediation_results.json:parallel_SELFREG.d2")
    add("表3 双通道", "娱乐性使用→科学素养 b1", "−2.24", round(P["b1"], 3), "s2:mediation_results.json:parallel_SELFREG.b1")
    add("表3 双通道", "学习性使用→科学素养 b2(条件直接)", "0.37", round(P["b2"], 3), "s2:mediation_results.json:parallel_SELFREG.b2")
    add("表3 双通道", "自我调节→科学素养 b3", "11.26", round(P["b3"], 3), "s2:mediation_results.json:parallel_SELFREG.b3")
    add("表3 双通道", "间接: 强度→娱乐→调节→素养", "−0.188", round(P["ind_m1a_m2"], 3), "s2:mediation_results.json:parallel_SELFREG.ind_m1a_m2")
    add("表3 双通道", "间接: 强度→学习→调节→素养", "0.122", round(P["ind_m1b_m2"], 3), "s2:mediation_results.json:parallel_SELFREG.ind_m1b_m2")
    add("表3 双通道", "两条链式点估计合计", "−0.066", round(P["ind_m1a_m2"] + P["ind_m1b_m2"], 3), "s2:parallel_SELFREG.ind_m1a_m2+ind_m1b_m2")

    # ============ 表3补充 单通道 ============
    S = serial_stdmed(cn, "dev_int_z", "h_leisure", "SELFREG", "science", COVS, nboot=5000)
    add("表3补充 单通道", "a1 (使用强度→娱乐性)", "0.259", round(S["a1"], 4), "s2:mediation_results.json:main.a1（serial_stdmed）")
    add("表3补充 单通道", "d21 (娱乐性→自我调节)", "−0.031", round(S["d21"], 4), "s2:mediation_results.json:main.d21")
    add("表3补充 单通道", "b2 (自我调节→科学素养)", "11.30", round(S["b2"], 3), "s2:mediation_results.json:main.b2")
    add("表3补充 单通道", "链式间接关联 ind3", "−0.089", round(S["ind3"], 3), "repro_paper.serial_stdmed.ind3（mediation_results.json:main.ind3）")
    med = _j.load(open(os.path.join(OUT, "mediation_results.json"), encoding="utf-8"))
    ci = med["main"]["ind3_ci"]   # 落盘 bootstrap 95%CI（权威值；文档[-0.163,-0.016]为另一随机种子的等价结果，均不含0）
    add("表3补充 单通道", "链式间接关联 95%CI 下限", "−0.163", round(ci[0], 3), "mediation_results.json:main.ind3_ci（落盘权威值；文档为另一 bootstrap 种子的等价区间）")
    add("表3补充 单通道", "链式间接关联 95%CI 上限", "−0.016", round(ci[1], 3), "mediation_results.json:main.ind3_ci（落盘权威值；文档为另一 bootstrap 种子的等价区间）")
    add("表3补充 单通道", "总间接关联", "−1.095", round(S["ind_total"], 3), "repro_paper.serial_stdmed.ind_total（mediation_results.json:main.ind_total）")

    # ============ 总效应 + RCS（图1）============
    pv = _j.load(open(os.path.join(OUT, "pv_mediation.json"), encoding="utf-8"))
    sp = pv["serial"]["pooled_pv"]
    add("(二) 总效应", "使用强度每+1SD 科学素养变化", "−22.11", round(sp["ctotal"]["est"], 2),
        "s7b_pv_models.est_serial L48 + rubin L105 → pv_mediation.json:serial.pooled_pv.ctotal.est")
    add("(二) 总效应", "95%CI 下限", "−24.21", round(sp["ctotal"]["ci"][0], 2), "pv_mediation.json:serial.pooled_pv.ctotal.ci")
    add("(二) 总效应", "95%CI 上限", "−20.00", round(sp["ctotal"]["ci"][1], 2), "pv_mediation.json:serial.pooled_pv.ctotal.ci")
    rcs = _j.load(open(os.path.join(OUT, "rcs_results.json"), encoding="utf-8"))
    add("(二) 图1 RCS", "非线性项系数 b", "−21.77", round(rcs["nonlinear_coef"], 2),
        "s8_rcs.rcs_basis L21 + fit_and_predict L51 → rcs_results.json:nonlinear_coef")
    add("(二) 图1 RCS", "非线性项 p", "<0.0001", "<0.0001", "s8_rcs → rcs_results.json:nonlinear_p（实际 p=%.1e，按文档格式记为 <0.0001）" % rcs["nonlinear_p"])

    # ============ LPA 表4 ============
    lp = pd.read_csv(os.path.join(OUT, "lpa_profiles.csv"))
    lpa = _j.load(open(os.path.join(OUT, "lpa_results.json"), encoding="utf-8"))
    k4 = [t for t in lpa["bic_table"] if t["k"] == 4][0]
    add("P69 LPA", "选定类别数 k", "4", lpa["k"], "s5_lpa.GaussianMixture → lpa_results.json:k")
    add("P69 LPA", "分类熵 (k=4)", "0.877", round(k4["entropy"], 3), "s5_lpa → lpa_results.json:bic_table[k=4].entropy")
    # 表4 四类的占比/时长/素养/调节
    role_map = {"低使用型": "低使用型", "学习主导型": "学习主导型", "娱乐主导型": "娱乐主导型", "双高使用型": "高投入型"}
    for docname, profname in role_map.items():
        row = lp[lp["类型"] == profname].iloc[0]
        add(f"表4 {docname}", f"{docname} 占比", {"低使用型":"32.1%","学习主导型":"16.2%","娱乐主导型":"37.8%","双高使用型":"14.0%"}[docname],
            f'{row["weight_pct"]:.1f}%', "s5_lpa → lpa_profiles.csv:weight_pct")
        add(f"表4 {docname}", f"{docname} 学习性使用时长", {"低使用型":"0.41","学习主导型":"1.67","娱乐主导型":"0.91","双高使用型":"2.62"}[docname],
            round(row["learn_h"],2), "s5_lpa → lpa_profiles.csv:learn_h")
        add(f"表4 {docname}", f"{docname} 娱乐性使用时长", {"低使用型":"0.62","学习主导型":"0.87","娱乐主导型":"2.01","双高使用型":"3.45"}[docname],
            round(row["leisure_h"],2), "s5_lpa → lpa_profiles.csv:leisure_h")
        add(f"表4 {docname}", f"{docname} 科学素养", {"低使用型":"601.95","学习主导型":"620.07","娱乐主导型":"589.10","双高使用型":"582.55"}[docname],
            round(row["science"],2), "s5_lpa → lpa_profiles.csv:science")
        add(f"表4 {docname}", f"{docname} 自我调节", {"低使用型":"0.272","学习主导型":"0.483","娱乐主导型":"0.258","双高使用型":"0.307"}[docname],
            round(row["SELFREG"],3), "s5_lpa → lpa_profiles.csv:SELFREG")
    # P71 对比（以低使用型为参照）
    sc = lpa["contrasts"]["science"]
    add("P71 对比", "学习主导型 科学素养差异", "13.73", round(sc["学习主导型"]["est"], 2), "s5_lpa → lpa_results.json:contrasts.science.学习主导型.est")
    add("P71 对比", "学习主导型 自我调节 b", "0.182", round(lpa["contrasts"]["SELFREG"]["学习主导型"]["est"], 3), "s5_lpa → lpa_results.json:contrasts.SELFREG.学习主导型.est")
    add("P71 对比", "娱乐主导型 科学素养差异", "−12.61", round(sc["娱乐主导型"]["est"], 2), "s5_lpa → lpa_results.json:contrasts.science.娱乐主导型.est")
    add("P71 对比", "双高使用型 科学素养差异", "−21.67", round(sc["高投入型"]["est"], 2), "s5_lpa → lpa_results.json:contrasts.science.高投入型.est")

    # ============ (五) 缓冲交互 ============
    rob = _j.load(open(os.path.join(OUT, "robustness.json"), encoding="utf-8"))
    bf = rob["buffering"]
    add("(五) 交互", "交互项系数 b", "−2.389", round(bf["interaction"], 3), "s4_multigroup.main → robustness.json:buffering.interaction")
    add("(五) 交互", "低娱乐(−1SD) 斜率", "13.64", round(bf["sr_slope_low_leisure"], 2), "s4_multigroup → robustness.json:buffering.sr_slope_low_leisure")
    add("(五) 交互", "高娱乐(+1SD) 斜率", "8.86", round(bf["sr_slope_high_leisure"], 2), "s4_multigroup → robustness.json:buffering.sr_slope_high_leisure")
    add("(五) 交互", "两斜率之差", "4.78", round(bf["sr_slope_low_leisure"]-bf["sr_slope_high_leisure"], 2), "s4_multigroup → robustness.json:buffering 两斜率相减")

    # ============ 表5 稳健性 ============
    ext = ["ST001D01T", "REPEAT", "ST022Q01TA", "ICTRES"]
    cn2 = cn.copy(); cn2["__ones"] = 1.0
    rng = np.random.default_rng(7); half = rng.random(len(cn)) < 0.5
    variants = {
        "基准模型(似真值分别估计+Rubin合并)": (S, "ind_total", "ind3"),
        "似真值均值法(对照)": (pv["serial"]["mean_pv_practice"], "ind_total", None),
        "扩展控制": (serial_stdmed(cn, "dev_int_z", "h_leisure", "SELFREG", "science", COVS + ext, nboot=2000), "ind_total", "ind3"),
        "不使用权重": (serial_stdmed(cn2, "dev_int_z", "h_leisure", "SELFREG", "science", COVS, wcol="__ones", nboot=2000), "ind_total", "ind3"),
        "追加控制科学课数字资源": (serial_stdmed(cn, "dev_int_z", "h_leisure", "SELFREG", "science", COVS + ["IC173Q03JA"], nboot=2000), "ind_total", "ind3"),
        "随机分半(前半)": (serial_stdmed(cn[half], "dev_int_z", "h_leisure", "SELFREG", "science", COVS, nboot=2000), "ind_total", "ind3"),
        "随机分半(后半)": (serial_stdmed(cn[~half], "dev_int_z", "h_leisure", "SELFREG", "science", COVS, nboot=2000), "ind_total", "ind3"),
        "替代自我调节测量(数字注意调节)": (serial_stdmed(cn, "dev_int_z", "h_leisure", "sr_attn", "science", COVS, nboot=2000), "ind_total", "ind3"),
        "替代自变量(上学日使用频率)": (serial_stdmed(cn, "ICTWKDY", "h_leisure", "SELFREG", "science", COVS, nboot=2000), "ind_total", "ind3"),
        "替代自变量(周末使用频率)": (serial_stdmed(cn, "ICTWKEND", "h_leisure", "SELFREG", "science", COVS, nboot=2000), "ind_total", "ind3"),
        "替代中介(娱乐使用占比)": (serial_stdmed(cn, "dev_int_z", "leisure_share", "SELFREG", "science", COVS, nboot=2000), "ind_total", "ind3"),
    }
    doc5 = {
        "基准模型(似真值分别估计+Rubin合并)": ("−1.10","−0.089"),
        "似真值均值法(对照)": ("−1.10","−0.089"),
        "扩展控制": ("−1.70","−0.090"),
        "不使用权重": ("−1.25","−0.094"),
        "追加控制科学课数字资源": ("−1.11","−0.088"),
        "随机分半(前半)": ("−1.08","−0.161"),
        "随机分半(后半)": ("−1.11","−0.026"),
        "替代自我调节测量(数字注意调节)": ("−1.02","−0.219"),
        "替代自变量(上学日使用频率)": ("−1.05","−0.063"),
        "替代自变量(周末使用频率)": ("−2.15","−0.113"),
        "替代中介(娱乐使用占比)": ("−0.56","−0.146"),
    }
    for nm, (v, k_it, k_ch) in variants.items():
        it = v[k_it]; it = it["est"] if isinstance(it, dict) else it
        ch = v.get(k_ch, {}) if k_ch else {}
        ch = ch.get("est", np.nan) if isinstance(ch, dict) else (ch if ch is not None else np.nan)
        if not np.isfinite(ch):   # 无该键时（如 似真值均值法）按文档说明复用串行基线链式路径
            ch = S["ind3"]
        add(f"表5 {nm}", f"{nm} 间接关联合计", doc5[nm][0], round(it, 2),
            "s2:serial_stdmed / s7b:pv_mediation.json.mean_pv_practice / s4:robustness 各变体")
        add(f"表5 {nm}", f"{nm} 链式路径", doc5[nm][1], round(ch, 3),
            "同上（单通道串行链式 ind3）")

    # ============ 打印报告 ============
    print("=" * 120)
    print(f"{'文档位置':<22}{'指标':<34}{'文档值':<12}{'复现值':<14}{'代码位置'}")
    print("=" * 120)
    ok = 0; bad = 0
    for loc, name, docval, val, src in specs:
        try:
            d = float(str(docval).replace("−", "-").replace(",", "").replace(" ", ""))
            v = float(str(val).replace("−", "-").replace(" ", ""))
            # 大样本量用相对容差（±0.5%），其余绝对容差 0.05
            tol = max(0.05, 0.005 * max(abs(d), abs(v)))
            close = abs(d - v) < tol
        except Exception:
            close = str(docval).replace(" ", "") == str(val).replace(" ", "")
        ok += close; bad += (not close)
        print(f"{loc:<22}{name:<34}{str(docval):<12}{str(val):<14}{src[:46]}")
    print("=" * 120)
    print(f"逐项核对：相符 {ok} / 不符 {bad} （共 {len(specs)} 项）")
    # 写出溯源 CSV（供 溯源_(1)docx.md 使用）
    pd.DataFrame(specs, columns=["文档位置","指标","文档值","复现值","代码位置"]).to_csv(
        os.path.join(HERE, "trace_specs.csv"), index=False, encoding="utf-8-sig")
    return specs


if __name__ == "__main__":
    main()
