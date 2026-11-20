# -*- coding: utf-8 -*-
"""build_html.py — 由修订后的 Markdown 母稿重建 stage2 HTML（沿用既有排版样式）。"""
import io, os, re

BASE = r"F:/workbudddy_task/2026-10-01-00-50-41"
MD = os.path.join(BASE, "paper", "论文_数字设备使用与科学素养.md")
STAGE2 = os.path.join(BASE, "output", "pisa2025-paper", "stage2")
HEAD = os.path.join(STAGE2, "_template_head.html")
OUT = os.path.join(STAGE2, "formatted-数字设备使用与科学素养.html")
NAMES = ['formatted-数字设备使用与科学素养.html']

FD = "\u3000"   # 全角空格
SEC_MAP = {
    "1 问题提出": "sec-1", "2 文献综述与研究假设": "sec-2", "3 研究设计": "sec-3",
    "4 研究结果": "sec-4", "5 讨论": "sec-5", "6 结论与教育启示": "sec-6",
    "参考文献": "sec-ref",
}
TOC = [("sec-1", "1 问题提出"), ("sec-2", "2 文献综述与研究假设"), ("sec-3", "3 研究设计"),
       ("sec-4", "4 研究结果"), ("sec-5", "5 讨论"), ("sec-6", "6 结论与教育启示"),
       ("sec-appendix", "附录 A　变量编码与来源"), ("sec-ref", "参考文献")]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inl(s):
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", esc(s))


def toc_html():
    li = "\n".join('    <li><a href="#%s">%s</a></li>' % (a, esc(t)) for a, t in TOC)
    return ('<nav class="doc-toc" aria-label="目录">\n  <p class="toc-title">目录</p>\n'
            '  <ol class="toc-list">\n%s\n  </ol>\n</nav>' % li)


def parse_table(block):
    rows = []
    for ln in block:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        rows.append(cells)
    align = rows[1]
    numeric = []
    for j, a in enumerate(align):
        a = a.strip()
        numeric.append(a.endswith(":") and not a.startswith(":"))
    head, data = rows[0], rows[2:]
    out = ["<thead>", "<tr>" + "".join(
        '<th%s>%s</th>' % (' class="num"' if numeric[j] else "", inl(c))
        for j, c in enumerate(head)) + "</tr>", "</thead>", "<tbody>"]
    for r in data:
        tds = []
        for j, c in enumerate(r):
            cls = ' class="num"' if (j < len(numeric) and numeric[j]) else ""
            tds.append("<td%s>%s</td>" % (cls, inl(c)))
        out.append("<tr>" + "".join(tds) + "</tr>")
    out.append("</tbody>")
    return "\n".join(out)


def main():
    head = io.open(HEAD, encoding="utf-8").read()
    lines = [l.rstrip("\n") for l in io.open(MD, encoding="utf-8").read().split("\n")]
    n = len(lines)
    body = []
    pending_tbl = None
    in_refs = False
    i = 0
    while i < n:
        ln = lines[i]
        st = ln.strip()
        if st == "":
            i += 1; continue
        # 分隔线
        if st == "---":
            body.append('<div data-component="divider" data-style="simple"></div>')
            i += 1; continue
        # 主标题
        if ln.startswith("# "):
            body.append('<h1 class="paper-title">%s</h1>' % esc(ln[2:].strip()))
            i += 1; continue
        if ln.startswith("## ——"):
            body.append('<p class="paper-subtitle">%s</p>' % esc(ln[3:].strip()))
            i += 1; continue
        # 摘要 + 关键词
        if st.startswith("**摘要**"):
            abstract = st.split("：", 1)[1] if "：" in st else ""
            kw = ""
            j = i + 1
            while j < n and lines[j].strip() == "":
                j += 1
            if j < n and lines[j].strip().startswith("**关键词**"):
                kw = lines[j].strip()[len("**关键词**"):].lstrip("：: ").rstrip()
            kw = kw.replace("**", "")
            body.append('<div class="abstract" aria-label="摘要">\n'
                        '  <p class="abstract-text">&nbsp;&nbsp;<strong>摘要</strong>：%s</p>\n'
                        '  <p class="keywords">&nbsp;&nbsp;<strong>关键词</strong>：%s</p>\n</div>'
                        % (inl(abstract), esc(kw)))
            body.append(toc_html())
            i = j + 1; continue
        # 三级标题
        if ln.startswith("### "):
            body.append('<p class="sub-heading">%s</p>' % esc(ln[4:].strip()))
            i += 1; continue
        # 二级标题
        if ln.startswith("## "):
            t = ln[3:].strip()
            in_refs = t.startswith("参考文献")
            aid = SEC_MAP.get(t) or ("sec-appendix" if t.startswith("附录") else
                                     re.sub(r"[^a-z0-9]+", "-", t.lower()))
            body.append('<h2 id="%s">%s</h2>' % (aid, esc(t)))
            i += 1; continue
        # 图片
        m = re.match(r"^!\[(.*?)\]\((.*?)\)\s*$", st)
        if m:
            body.append('<p class="doc-figure"><img src="%s" alt="%s" width="570"></p>'
                        % (m.group(2), esc(m.group(1))))
            i += 1; continue
        # 表/图标题
        m = re.match(r"^\*\*(表\s[A-Za-z0-9]+[%s\s].*?)\*\*$" % FD, st)
        if m:
            pending_tbl = m.group(1); i += 1; continue
        m = re.match(r"^\*\*(图\s\d+[%s\s].*?)\*\*$" % FD, st)
        if m:
            body.append('<p class="figure-caption">%s</p>' % esc(m.group(1)))
            i += 1; continue
        # 表格
        if st.startswith("|"):
            blk = []
            while i < n and lines[i].strip().startswith("|"):
                blk.append(lines[i]); i += 1
            if pending_tbl:
                # 转换器不识别 <caption>，故表标题单独成段
                body.append('<p class="table-caption">%s</p>' % inl(pending_tbl))
            body.append('<table class="three-line-table">\n%s\n</table>' % parse_table(blk))
            pending_tbl = None
            continue
        # 表注
        if st.startswith("注："):
            body.append('<p class="table-note">%s</p>' % inl(st))
            i += 1; continue
        # 参考文献条目
        if in_refs and re.match(r"^\[\d+\]", st):
            body.append('<p class="reference-item">%s</p>' % inl(st))
            i += 1; continue
        # 普通段落
        body.append("<p>%s</p>" % inl(st))
        i += 1

    html = head.rstrip("\n") + "\n<body>\n<section role=\"body\" data-page-restart=\"1\">\n" + \
           "\n".join(body) + "\n</section>\n</body>\n</html>\n"
    io.open(OUT, "w", encoding="utf-8").write(html)
    print("写出:", OUT, len(html), "字符")
    print("表格数:", html.count("<table"), "| 图片数:", html.count("<img"), "| 段落数:", html.count("<p"))


if __name__ == "__main__":
    main()
