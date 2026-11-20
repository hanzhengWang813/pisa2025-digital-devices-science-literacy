# -*- coding: utf-8 -*-
"""build_frontmatter.py — 生成 JSET 投稿所需的「标题页」与「投稿信」"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx_helpers import *
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

TITLE = ("Self-regulation is a correlate, not a conduit: digital device use and "
         "scientific literacy in 23 education systems")

# ============================================================ 1. 标题页
doc = new_doc("en")
add_page_numbers(doc)

p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(10)
r = p.add_run("Title Page"); r.bold = True; r.font.size = Pt(13)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(18)
r = p.add_run(TITLE); r.bold = True; r.font.size = Pt(15)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

para(doc, "Running head: Self-regulation as a correlate", indent=False, italic=True, size=10.5,
     align="center")

h(doc, "Authors", 2)
para(doc, "[Author One]\u00b9  (ORCID: 0000-0000-0000-0000)", indent=False)
para(doc, "[Author Two]\u00b9  (ORCID: 0000-0000-0000-0000)", indent=False)
para(doc, "\u00b9 [Department], [University], [City], [Postcode], China", indent=False)

h(doc, "Corresponding author", 2)
para(doc, "[Author One]", indent=False)
para(doc, "[Department], [University], [Street address], [City], China", indent=False)
para(doc, "Email: [name]@[university].edu.cn    Telephone: [+86 \u2026]", indent=False)

h(doc, "Manuscript information", 2)
para(doc, "Article type: Original research", indent=False)
para(doc, "Main text: 5,598 words (excluding title page, abstract, references, tables and "
          "figure legends); abstract 249 words; 9 tables; 1 figure; online supplement with the "
          "estimation code and result files.", indent=False)
para(doc, "Keywords: digital device use; scientific literacy; self-regulation; mediation; "
          "PISA 2025; cross-system comparison", indent=False)

h(doc, "Declarations", 2)
para(doc, "**Funding.** [To be completed.]", indent=False)
para(doc, "**Competing interests.** The authors declare no competing interests.", indent=False)
para(doc, "**Ethics approval.** Secondary analysis of anonymised, publicly available PISA 2025 "
          "data collected by the OECD; no additional approval or consent was required.",
     indent=False)
para(doc, "**Data availability.** Public-use PISA 2025 data from the OECD; all analysis code and "
          "result files accompany the submission as supplementary material.", indent=False)
para(doc, "**Acknowledgements.** [To be completed.]", indent=False)
para(doc, "**Author contributions.** [To be completed, e.g. conceptualisation, formal analysis, "
          "writing \u2013 original draft.]", indent=False)

out1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "03_Title_Page_JSET.docx")
doc.save(out1)
print("saved", out1)

# ============================================================ 2. 投稿信
doc = new_doc("en")

para(doc, "[Date]", indent=False)
para(doc, "The Editor-in-Chief", indent=False)
para(doc, "Journal of Science Education and Technology", indent=False)
para(doc, "", indent=False)
para(doc, "Dear Editor,", indent=False)
para(doc, "Please consider the enclosed manuscript, \u201c" + TITLE + "\u201d, for publication as "
     "an original research article in the Journal of Science Education and Technology.")

para(doc, "The paper asks a question that the digital-technology literature keeps answering in "
     "opposite directions: why is heavier device use associated with lower science achievement? "
     "Self-regulation is the mediator most often proposed, and the usual test asks only whether "
     "the indirect path differs from zero. We ask how much of the association that path actually "
     "carries. Using PISA 2025 data for Beijing, Shanghai, Jiangsu and Zhejiang (n = 12,237), "
     "re-estimated in Finland, Korea and Hong Kong (China), and pooled across 23 education "
     "systems (n = 167,180), we decompose the association into its direct and indirect parts and "
     "report each as a share of the total.")

para(doc, "Three findings organise the paper. First, 95% of the association is direct; the two "
     "serial pathways through self-regulation, though statistically robust, carry 0.3% of it, and "
     "all indirect pathways together carry 4.9%. Second, this is not an artefact of the regulation "
     "measure: refitting the model with a planning-and-monitoring scale doubles the first link "
     "while shrinking the second, and the mediated share falls to 2.2%. Third, the "
     "composition-specific paths are not invariant across systems: entertainment-oriented use is "
     "negatively associated with literacy in the Chinese sample and positively associated with it "
     "in the other three (F(3, 80) = 22.91, p < .001), although the total association is stable "
     "(F(3, 80) = 2.27, p = .087). A person-centred analysis of use configurations, set against "
     "the mediation model, exposes the same discrepancy from a different angle.")

para(doc, "We think the paper suits the Journal's readership for three reasons. It speaks directly "
     "to how digital resources are used in science learning rather than to screen time in the "
     "abstract; it reports the full decomposition that science-education studies of ICT usually "
     "omit, which gives readers a number they can use to judge existing claims; and it bounds what "
     "single-system mediation estimates can mean, which is a methodological point that travels "
     "beyond this dataset.")

para(doc, "On method, every estimate uses the ten plausible values and the 80 Fay-BRR replicate "
     "weights with Rubin's rules, so standard errors are design-based throughout; indirect terms "
     "are re-estimated within each replicate rather than approximated by the delta method. Every "
     "number in the text is reproduced by the accompanying code, and the manuscript reports all "
     "estimates that were computed, including null results.")

para(doc, "The manuscript is original, is not under consideration elsewhere, and has not been "
     "published previously in any form. All authors have approved the submission and declare no "
     "competing interests. The manuscript is prepared for double-blind review, with author "
     "details on the separate title page.")

para(doc, "Thank you for your consideration.")

para(doc, "", indent=False)
para(doc, "Yours sincerely,", indent=False)
para(doc, "[Author One], on behalf of all authors", indent=False)
para(doc, "[Department], [University], [City], China", indent=False)
para(doc, "[name]@[university].edu.cn", indent=False)

out2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "04_Cover_Letter_JSET.docx")
doc.save(out2)
print("saved", out2)
