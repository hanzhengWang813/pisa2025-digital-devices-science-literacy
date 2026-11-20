# -*- coding: utf-8 -*-
"""
check_numbers.py — 交稿前的数字自检（把「正文数字」与「结果文件」对齐）
=====================================================================
为什么需要：这类稿子最容易被审稿人抓住的不是观点，而是正文/表格/附录三处
数字不一致（改一处忘一处）。本脚本从 output/*.json 重算关键量，再在
02_Revised_Manuscript_JSET.docx 的全文里逐个断言其存在，输出不一致清单。

运行：python check_numbers.py
退出码 0 = 全部通过；1 = 有不一致（需人工处理）
"""
import json, os, re, sys
from docx import Document

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "run", "output")
DOCX = os.path.join(HERE, "02_Revised_Manuscript_JSET.docx")


def load(name):
    with open(os.path.join(OUT, name), encoding="utf-8") as f:
        return json.load(f)


def doc_text(path=DOCX):
    d = Document(path)
    parts = [p.text for p in d.paragraphs]
    for t in d.tables:
        for r in t.rows:
            for c in r.cells:
                parts.append(c.text)
    return "\n".join(parts)


def fmt(v, d=2):
    """负数用 U+2212，与正文一致。"""
    s = ("%." + str(d) + "f") % v
    if s.startswith("-"):
        s = "\u2212" + s[1:]
    return s


def main():
    ms = load("pv_mediation.json")
    multi = load("multisystem_pv.json")
    pooled = load("pooled_pv.json")
    joint = load("joint_tests.json")
    comp = load("composition.json")
    alt = load("altmediator.json")
    txt = doc_text()
    txt_nospace = re.sub(r"\s+", " ", txt.replace("\u2212", "-"))

    checks = []

    def need(label, s):
        checks.append((label, s, s in txt or s in txt_nospace or
                       s.replace("\u2212", "-") in txt_nospace))

    # --- 主模型
    q = multi["QCI"]
    need("c (total)", fmt(q["ctotal"]["est"]))
    need("c' (direct)", fmt(q["cp"]["est"]))
    need("b3", fmt(q["b3"]["est"]))
    need("ind total", fmt(q["ind_total"]["est"]))
    need("serial ent", fmt(q["ind_m1a_m2"]["est"], 3))
    need("serial learn", "+" + fmt(q["ind_m1b_m2"]["est"], 2).lstrip("\u2212"))
    need("share of c", "%.1f%%" % (100 * q["share_ind_total"]))

    # --- 三个调节测量
    for k in ("SELFREG", "GOALSET", "COGABIL"):
        if k in alt:
            need("%s b3" % k, fmt(alt[k]["b3"]["est"]))
            need("%s d1" % k, fmt(alt[k]["d1"]["est"], 3))

    # --- 联合检验
    for key, lab in (("ctotal", "F c"), ("cp", "F c'"), ("b1", "F b1"),
                     ("b2", "F b2"), ("b3", "F b3"), ("d1", "F d1"),
                     ("d2", "F d2"), ("ind_total", "F ind")):
        if key in joint:
            need(lab, "%.2f" % joint[key]["F"])

    # --- 23 经济体
    need("pooled c", fmt(pooled["ctotal"]["est"]))
    need("pooled c'", fmt(pooled["cp"]["est"]))
    need("pooled ind", "+" + fmt(pooled["ind_total"]["est"]))

    # --- 构成模型（每 10 个百分点）
    need("share per 10pp", fmt(comp["b_share"]["est"] / 10))
    need("leisure hours", fmt(comp["b_leisure"]["est"]))
    need("learn hours", fmt(comp["b_learn"]["est"]))
    need("total hours", fmt(comp["b_total"]["est"]))

    # --- 结构性检查
    n_fail = sum(1 for _, _, ok in checks if not ok)
    for label, s, ok in checks:
        if not ok:
            print("  MISSING  %-16s %s" % (label, s))
    print("\n%d checks, %d missing" % (len(checks), n_fail))

    # --- 词数/摘要合规
    ps = [p.text for p in Document(DOCX).paragraphs]
    i = [k for k, t in enumerate(ps) if t.strip() == "Abstract"][0]
    ab = len(ps[i + 1].split())
    i0 = [k for k, t in enumerate(ps) if t.strip().startswith("1. Introduction")][0]
    i1 = [k for k, t in enumerate(ps) if t.strip() == "References"][0]
    prose = sum(len(ps[k].split()) for k in range(i0, i1)
                if ps[k].strip() and not ps[k].strip().startswith(("Table ", "Note.", "Figure ")))
    print("abstract %d words (limit 250) -> %s" % (ab, "OK" if ab <= 250 else "OVER"))
    print("main text %d words excluding refs/tables/legends -> %s"
          % (prose, "OK" if prose <= 6000 else "OVER"))
    return 0 if (n_fail == 0 and ab <= 250 and prose <= 6000) else 1


if __name__ == "__main__":
    sys.exit(main())
