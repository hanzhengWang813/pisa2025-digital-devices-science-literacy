# -*- coding: utf-8 -*-
"""docx_helpers.py — 共用排版工具（中英文两用）"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def _set_cell_border(cell, **kwargs):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement("w:tcBorders")
        tcPr.append(tcBorders)
    for edge in ("top", "left", "bottom", "right"):
        if edge in kwargs:
            ed = kwargs[edge]
            el = tcBorders.find(qn("w:" + edge))
            if el is None:
                el = OxmlElement("w:" + edge)
                tcBorders.append(el)
            for k, v in ed.items():
                el.set(qn("w:" + k), str(v))


def _tbl_borders(table, sz=4, color="999999"):
    tbl = table._tbl
    tblPr = tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement("w:" + edge)
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), str(sz))
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), color)
        borders.append(el)
    tblPr.append(borders)


def new_doc(lang="en"):
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Cm(2.5)
    sec.bottom_margin = Cm(2.5)
    sec.left_margin = Cm(2.6)
    sec.right_margin = Cm(2.6)
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(12 if lang == "en" else 10.5)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "宋体" if lang != "en" else "SimSun")
    pf = st.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE if lang == "en" else WD_LINE_SPACING.ONE_POINT_FIVE
    pf.space_before = Pt(0)
    pf.space_after = Pt(0 if lang == "en" else 4)
    return doc


def h(doc, text, level=1, lang="en"):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14 if level == 1 else 10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = True
    r.font.name = "Times New Roman" if lang == "en" else "黑体"
    r._element.rPr.rFonts.set(qn("w:eastAsia"), "黑体")
    r.font.size = Pt(14 if level == 1 else 11.5 if level == 2 else 10.5)
    if level == 3:
        r.italic = True
    return p


def para(doc, text, lang="en", indent=True, size=None, bold=False, italic=False,
         align=None, space_after=None, spacing=None):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    if indent and lang == "en":
        pf.first_line_indent = Cm(0.75)
    if align == "center":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == "justify" or align is None:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if space_after is not None:
        pf.space_after = Pt(space_after)
    if spacing is not None:
        pf.line_spacing_rule = spacing
    # 支持 **粗体** 与 *斜体* 片段
    import re
    tokens = re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text)
    for tk in tokens:
        if not tk:
            continue
        if tk.startswith("**") and tk.endswith("**"):
            r = p.add_run(tk[2:-2]); r.bold = True
        elif tk.startswith("*") and tk.endswith("*") and len(tk) > 2:
            r = p.add_run(tk[1:-1]); r.italic = True
        else:
            r = p.add_run(tk)
        if bold:
            r.bold = True
        if italic:
            r.italic = True
        if size:
            r.font.size = Pt(size)
    return p


def bullet(doc, text, lang="en"):
    p = doc.add_paragraph(style="List Bullet" if lang == "en" else "List Bullet")
    p.paragraph_format.left_indent = Cm(0.9)
    p.paragraph_format.space_after = Pt(2)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(text)
    return p


def num(doc, text):
    p = doc.add_paragraph(style="List Number")
    p.paragraph_format.left_indent = Cm(0.9)
    p.paragraph_format.space_after = Pt(2)
    p.add_run(text)
    return p


def table(doc, header, rows, widths=None, lang="en", font_size=9, header_bold=True,
          align_right_from=1, caption=None, note=None):
    if caption:
        cp = doc.add_paragraph()
        cp.paragraph_format.space_before = Pt(10)
        cp.paragraph_format.space_after = Pt(3)
        cp.paragraph_format.keep_with_next = True
        r = cp.add_run(caption)
        r.bold = True
        r.font.size = Pt(10)
        if lang != "en":
            r.font.name = "黑体"
            r._element.rPr.rFonts.set(qn("w:eastAsia"), "黑体")
    t = doc.add_table(rows=1, cols=len(header))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = True
    _tbl_borders(t)
    hdr = t.rows[0].cells
    for i, txt in enumerate(header):
        hdr[i].text = ""
        p = hdr[i].paragraphs[0]
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT if i == 0 else WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(txt)
        r.bold = header_bold
        r.font.size = Pt(font_size)
        if lang != "en":
            r.font.name = "黑体"
            r._element.rPr.rFonts.set(qn("w:eastAsia"), "黑体")
    for row in rows:
        cells = t.add_row().cells
        for i, txt in enumerate(row):
            cells[i].text = ""
            p = cells[i].paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
            if i == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(str(txt))
            r.font.size = Pt(font_size)
            if str(txt).startswith("—") and i == 0:
                r.italic = True
    if widths:
        t.autofit = False
        for i, w in enumerate(widths):
            for row in t.rows:
                row.cells[i].width = Cm(w)
    if note:
        np_ = doc.add_paragraph()
        np_.paragraph_format.space_before = Pt(2)
        np_.paragraph_format.space_after = Pt(8)
        np_.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        np_.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = np_.add_run(note)
        r.font.size = Pt(8)
        r.italic = False
    return t


def smallnote(doc, text, lang="en"):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(text)
    r.font.size = Pt(8.5)
    return p


def pagebreak(doc):
    doc.add_page_break()


def add_page_numbers(doc, text_prefix=""):
    for section in doc.sections:
        footer = section.footer
        p = footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        fldChar1 = OxmlElement("w:fldChar"); fldChar1.set(qn("w:fldCharType"), "begin")
        instrText = OxmlElement("w:instrText"); instrText.set(qn("xml:space"), "preserve")
        instrText.text = " PAGE "
        fldChar2 = OxmlElement("w:fldChar"); fldChar2.set(qn("w:fldCharType"), "end")
        run._r.append(fldChar1); run._r.append(instrText); run._r.append(fldChar2)
        run.font.size = Pt(9)


def add_line_numbers(doc, restart="continuous", count_by=1):
    """给所有节加连续行号（Springer/JSET 初投要求）。"""
    for section in doc.sections:
        sectPr = section._sectPr
        for old in sectPr.findall(qn("w:lnNumType")):
            sectPr.remove(old)
        ln = OxmlElement("w:lnNumType")
        ln.set(qn("w:countBy"), str(count_by))
        ln.set(qn("w:restart"), restart)
        sectPr.append(ln)
