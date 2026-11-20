# -*- coding: utf-8 -*-
"""build_manuscript.py — 生成修订版英文稿（目标期刊 Journal of Science Education and Technology）"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx_helpers import *
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING

doc = new_doc("en")
add_page_numbers(doc)
add_line_numbers(doc)

# ------------------------------------------------------------------ 标题页
p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(60)
r = p.add_run("Self-regulation is a correlate, not a conduit: digital device use and "
              "scientific literacy in 23 education systems")
r.bold = True; r.font.size = Pt(16)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(24)
r = p.add_run("Running head: Self-regulation as a correlate")
r.italic = True; r.font.size = Pt(11)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

# 双盲送审：正文不出现作者信息，作者与致谢放在单独的 Title Page 文件
for line in ["Manuscript prepared for double-blind peer review.",
             "Author names, affiliations, funding and acknowledgements are given on the "
             "separate title page."]:
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(18 if "double-blind" in line else 4)
    r = p.add_run(line); r.font.size = Pt(10.5)
    r.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

pagebreak(doc)

# ------------------------------------------------------------------ 摘要
h(doc, "Abstract", 1)
para(doc, "Digital device use is consistently associated with lower academic achievement, but why is unresolved, and self-regulation is the most frequently proposed mediator. We asked whether self-regulation mediates this association and how much of it the indirect pathways carry. Using PISA 2025 we analysed 12,237 15-year-olds in Beijing, Shanghai, Jiangsu and Zhejiang (China), re-estimated the model in Finland, Korea and Hong Kong (China), and pooled 23 education systems (n = 167,180), separating learning-oriented from entertainment-oriented use. A one-standard-deviation higher use frequency was associated with 22.11 fewer points (95% CI \u221224.21 to \u221220.00), 95% of which was direct. The two serial pathways through regulation (\u22120.19 and +0.12 points) carried 0.3% of it and all indirect pathways 4.9%; with a planning-and-monitoring scale the first link doubled but the second fell, and the mediated share dropped to 2.2%. Regulation was associated with literacy in every system (5 to 11 points per SD) but did not carry the association. The total association was stable across systems (F(3, 80) = 2.27, p = .087) while the composition paths were not: entertainment-oriented use was negative in the focal system (\u22122.24 points) and positive in the other three (+5.2 to +11.0; F(3, 80) = 22.91, p < .001). In the 23-system model the net indirect effect was +0.29 points (95% CI \u22120.04 to +0.62), about 1.5% of the total and opposite in sign. Regulation is a correlate of scientific literacy, not a conduit for device-use effects; mediation studies should report the indirect share, not only its significance.")

para(doc, "**Keywords:** digital device use; scientific literacy; self-regulation; mediation; "
     "PISA 2025; cross-system comparison")

# ------------------------------------------------------------------ 1 引言
h(doc, "1. Introduction", 1)

para(doc, "Most adolescents now study, search and socialise through the same device, and PISA 2025 treats scientific literacy as a major domain while adding Learning in the Digital World as an innovative domain, which makes the question of how device use relates to science learning hard to avoid (OECD, 2026a). The empirical answer has been unstable. Meta-analytic work links heavier screen use to lower achievement (Adelantado-Renau et al., 2019), analyses of PISA data report negative associations that are stronger among rural and lower-SES students (Zhi & Chen, 2019) and that flatten or reverse at low levels of use (Yang et al., 2025), and other work finds associations small enough to be indistinguishable from noise (Orben & Przybylski, 2019).")

para(doc, "One influential reading is that total time is the wrong predictor: the same number of hours can stand for very different activities. Learning-oriented use involves searching, evaluating sources, planning and monitoring, and has been linked positively to science outcomes through motivational beliefs (Guo et al., 2022; Li, 2026; Xiong et al., 2025). Entertainment-oriented use is thought to operate through displaced study time and shortened sleep (Hale & Guan, 2015), the cognitive load imposed by switching (Sweller et al., 2011), and the attentional residue that switching leaves behind (Ophir et al., 2009; Uncapher & Wagner, 2018; van der Schuur et al., 2015). On this view composition matters more than amount.")

para(doc, "Self-regulation is the mechanism most often placed between the two. Activities differ in the opportunities they give students to set goals, monitor progress and adjust strategies, which are the processes that define self-regulated learning (Pintrich, 2000; Zimmerman, 2002; Zimmerman & Schunk, 2001); self-regulation predicts achievement, and somewhat more strongly in science than in other domains (Dent & Koenka, 2016; Li et al., 2018). If both steps hold, use patterns should shift self-regulation and self-regulation should carry part of the association. Social-cognitive theory supplies a reason to expect the shift to be bidirectional, because behaviour and environment shape self-regulation together (Bandura, 1991).")

para(doc, "What this literature rarely reports is the size of the mediation relative to the association it is meant to explain. Studies report whether an indirect path differs from zero, and increasingly its standardised size, but seldom what fraction of the total association it accounts for (MacKinnon et al., 2007; Preacher & Kelley, 2011; VanderWeele, 2016). The omission matters: when the total is large, an indirect path can be statistically robust and substantively trivial at the same time, and a mechanism claim resting on it would be unsupported even at p < .001.")

para(doc, "Two further gaps in this literature are geographic and methodological. Most tests of the composition hypothesis use a single education system, yet composition-specific paths depend on how a system organises device use: whether devices are used in lessons, how much of the curriculum is delivered digitally, and how much discretionary time school structures. And composition is almost always modelled as two correlated continuous variables, although students do not allocate time that way; a person-centred description complements the model and can be checked against it, because if self-regulation is the mechanism, groups that differ in composition should also differ in self-regulation.")


para(doc, "We address these points with PISA 2025 and ask five questions. How large is the association between device-use frequency and scientific literacy, and is it linear? How much of it runs through self-regulation and through each mode of use, expressed as a share of the total? Do students' configurations of use order their literacy differently from total use, and does self-regulation track that ordering? Are the composition paths invariant across education systems? And how much do the answers depend on how regulation is measured and on whether composition is modelled as a balance between purposes or as two quantities of time?")

para(doc, "The study makes four contributions: a full decomposition reported as shares of the total rather than as the significance of individual paths; tests of the composition paths in four systems and in 23, with design-based standard errors throughout, which bound what single-system mediation estimates can be taken to mean; a person-centred description set against the mediation model, which exposes a discrepancy the mediation results alone would hide; and a replication with three regulation measures, so that the conclusion cannot be attributed to one operationalisation of a contested construct.")

# ------------------------------------------------------------------ 2 方法
h(doc, "2. Method", 1)

h(doc, "2.1. Data and samples", 2)
para(doc, "PISA 2025 assessed 15-year-olds in 91 economies (OECD, 2026a). The focal sample was Beijing, Shanghai, Jiangsu and Zhejiang, which PISA reports as a single region (CNT = QCI; n = 12,385). After listwise deletion on the model variables, 12,237 students remained; missingness was below 0.5% for every variable, and complete cases differ from the full sample by 0.012 SD in mean scientific literacy, so deletion is not selective in any way that matters here. Three comparison systems were chosen because they have comparable coverage of the ICT and self-regulation items and differ in how devices are integrated into schooling: Finland (n = 5,652), Korea (6,416) and Hong Kong, China (5,767). The pooled analysis retained every economy with at least 2,000 students and at least 80% complete data on the five key variables; 23 met these criteria (n = 167,180; Appendix A). All variables were standardised within economy for that analysis, which approximates economy fixed effects for the intercepts.")

h(doc, "2.2. Measures", 2)
para(doc, "**Scientific literacy.** PISA provides ten plausible values (PV1SCIE\u2013PV10SCIE), each a random draw from a student's estimated proficiency distribution. They are not repeated measurements and were not averaged: every model was estimated once per plausible value and the results were pooled with Rubin's rules (Rubin, 1987). The sample mean was 597.04 points (SD = 83.52).")
para(doc, "**Frequency of device use.** Two PISA indices record how often students performed ICT activities on school days (ICTWKDY) and at weekends (ICTWKEND). Each was standardised on the pooled PISA 2025 sample and the two scores were averaged, so the index has a mean of zero for the international sample and \u22120.86 in the Chinese sample (Table 1). It measures how often students use devices, not how long they use them.")
para(doc, "**Modes of use.** Six items (ST326Q01\u2013Q06) ask how much time students spend using digital resources for learning and for entertainment in three settings: during school, before and after lessons, and at weekends. Responses have nine options from \u201cnone\u201d to \u201cmore than 7 hours\u201d and were coded at the category midpoint (0, 0.5, 1.5, \u2026, 7.5) and averaged across settings, so the scores are hours per setting, not daily hours. The entertainment share was entertainment hours divided by the sum of both modes.")
para(doc, "**Self-regulation.** SELFREG is a weighted likelihood estimate built from four items (ST433Q01, Q02, Q04, Q06; OECD, 2026b), all of which ask about help seeking: asking classmates when something is not fully understood, asking teachers for help when it is needed, asking for help when learning is difficult, and trying hard to solve a problem alone first. Responses run from strongly agree to strongly disagree and were reverse-keyed before scaling; the items formed a reliable scale in the focal sample (\u03b1 = .80, n = 12,301). Adaptive help seeking is an established self-regulated learning strategy (Pintrich, 2000; Zimmerman, 2002), but it is a strategy rather than the whole of planning and monitoring, so we describe the index as help seeking and use \u201cregulation\u201d only as shorthand.")
para(doc, "**Two further regulation indices.** GOALSET is built from four items closer to the processes the hypothesis is about \u2014 planning an approach to studying, summarising material to find gaps, self-testing, and changing an approach that is not working (\u03b1 = .88, n = 12,286). COGABIL is a narrower measure of willingness to engage with demanding problems (\u03b1 = .85, n = 12,301). Because a claim about device use should not depend on which of three related measures is chosen, we refitted the model with each in turn.")
para(doc, "**Covariates.** All models controlled for the PISA index of economic, social and cultural status (ESCS), gender (female = 1) and ICT availability at home (ICTHOME). Robustness models added grade, grade repetition, home language, school ICT resources and the reported frequency of using digital resources in science lessons (IC173Q03JA).")

h(doc, "2.3. Analytic strategy", 2)
para(doc, "**Step 1: shape of the association.** Weighted regressions with restricted cubic splines (three knots at the 10th, 50th and 90th percentiles of use frequency) described the association, with covariates at their weighted means (Harrell, 2001); nonlinearity was tested with a design-based Wald test on the spline terms.")
para(doc, "**Step 2: decomposition.** A dual-path serial model entered both modes of use simultaneously. Use frequency predicted entertainment-oriented and learning-oriented use; both predicted self-regulation; self-regulation, both modes and use frequency predicted scientific literacy. Mediators were standardised within the equations, so paths among standardised variables are fully standardised and paths predicting literacy are in score points. We also estimated a single-path model with entertainment-oriented use as the only first mediator, to show how that estimate changes when learning-oriented use is held constant.")
para(doc, "The model partitions the total association c into a direct part c\u2032 and five indirect "
     "parts, two of which are the serial pathways of interest:")
para(doc, "c = c\u2032 + a\u2081b\u2081 + a\u2082b\u2082 + a\u2083b\u2083 + "
     "(a\u2081d\u2081b\u2083) + (a\u2082d\u2082b\u2083)", indent=False, align="center")
para(doc, "We report each term in score points with its share of c, defined as the term divided by c. The share is the quantity that decides whether a mechanism claim is warranted, and the quantity this literature usually omits.")
para(doc, "**Step 3: configurations of use.** Latent profile analysis was fitted to the six hour items with two to six profiles, full covariance structure and 10 random starts (Vermunt & Magidson, 2002), compared on BIC, AIC, entropy and smallest profile. Students were assigned to their most likely profile, and literacy and regulation were compared across profiles by weighted regression against the low-use profile.")
para(doc, "**Step 4: composition as a continuous predictor.** Two weighted regressions asked what \u201cwhat students do matters more than how long\u201d implies. The first regressed literacy on use frequency, total hours and the entertainment share, so the share coefficient describes a shift between purposes at a fixed total; the second regressed literacy on use frequency, learning hours and entertainment hours entered together, which is the same model without the ratio. The two parameterisations are algebraically related but not statistically equivalent, because share and total are strongly collinear by construction.")
para(doc, "**Step 5: alternative regulation measures.** The dual-path model was re-estimated with GOALSET and with COGABIL in place of SELFREG, which tests whether the mediated pathway depends on the particular regulation measure.")
para(doc, "**Step 6: cross-system comparison.** The model was estimated separately in the focal and three comparison systems, each with the full plausible-value and replicate-weight pipeline rather than analytic standard errors. To test whether a path differs across systems, the four samples were treated as independent and contrasts formed between each comparison system and the focal one; contrasts that share the focal system covary with its variance, giving a Wald statistic with three numerator and 80 denominator degrees of freedom.")
para(doc, "**Step 7: pooled multi-system model.** The model was then estimated in the pooled 23 economies with within-economy standardisation and the same pipeline. Because economies are independent samples, pooling replicate weights gives design-based standard errors. Because the heterogeneity tests reject a common-slope model for the composition paths, this estimate describes the average association rather than a common effect.")
para(doc, "**Step 8: conditional return to self-regulation.** A product term between standardised self-regulation and standardised entertainment-oriented use tested whether the regulation\u2013literacy association varies with composition; simple slopes were evaluated at \u00b11 SD.")

h(doc, "2.4. Inference", 2)
para(doc, "All models used the final student weight (W_FSTUWT). Sampling variance was estimated with Fay's balanced repeated replication, 80 replicate weights and a Fay coefficient of 0.5, which yields 80 degrees of freedom (Fay, 1989). For indirect terms the full product of coefficients was re-estimated within each replicate rather than approximated by the delta method, and the resulting variances were pooled across plausible values with Rubin's rules. The pooled model pooled replicate weights across independent samples. All models were estimated by weighted least squares; the estimation code is provided as supplementary material.")
para(doc, "The design is cross-sectional and observational. Every estimate is an association adjusted for covariates, and the serial ordering is a modelling assumption that the data cannot verify. No alpha adjustment was applied across the many tests reported here; exact p values and intervals are given for every estimate, and the argument rests on shares of the total association rather than on the number of tests that reach significance.")

# ------------------------------------------------------------------ 3 结果
h(doc, "3. Results", 1)

h(doc, "3.1. Descriptive results", 2)
para(doc, "Table 1 gives the weighted descriptives. Students reported more entertainment-oriented use (M = 1.58 hours per setting) than learning-oriented use (M = 1.11), so entertainment accounted for 58% of the combined time. Scientific literacy correlated negatively with use frequency (r = \u2212.28) and with entertainment-oriented use (r = \u2212.10), positively with self-regulation (r = .20) and ESCS (r = .33), and not at all with learning-oriented use (r = .01). The two modes correlated at .31, which is high enough that their separate coefficients depend on simultaneous entry.")

table(doc,
      ["Variable", "M", "SD", "1", "2", "3", "4", "5", "6"],
      [["1. Scientific literacy", "597.04", "83.52", "\u2014", "", "", "", "", ""],
       ["2. Device-use frequency", "\u22120.86", "0.96", "\u2212.28", "\u2014", "", "", "", ""],
       ["3. Learning-oriented use (h)", "1.11", "1.09", ".01", ".10", "\u2014", "", "", ""],
       ["4. Entertainment-oriented use (h)", "1.58", "1.30", "\u2212.10", ".26", ".31", "\u2014", "", ""],
       ["5. Entertainment share", "0.58", "0.24", "\u2212.07", ".11", "\u2212.48", ".47", "\u2014", ""],
       ["6. Self-regulation", "0.31", "0.95", ".20", "\u2212.06", ".10", "\u2212.04", "\u2212.14", "\u2014"],
       ["7. ESCS", "\u22120.52", "1.00", ".33", "\u2212.01", ".09", "\u2212.01", "\u2212.08", ".15"]],
      widths=[5.0, 1.2, 1.1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
      caption="Table 1. Weighted descriptive statistics and correlations (n = 12,385).",
      note="Note. Weighted with the final student weight. Device-use frequency is the mean of two PISA "
           "indices standardised on the pooled international sample, so its mean is negative in this "
           "sample by construction. Correlations with scientific literacy use the mean of the ten "
           "plausible values for description only. Standard errors for the correlations come from 80 "
           "Fay-BRR replicate weights and are about .013, so |r| \u2265 .026 corresponds to p < .05.")

h(doc, "3.2. The total association is large and nonlinear", 2)
para(doc, "After adjustment, a one-SD higher use frequency was associated with 22.11 fewer points (95% CI \u221224.21 to \u221220.00), about 0.26 of the sample SD, and the association was nonlinear (nonlinear spline term b = \u221221.77, SE = 1.95, t(80) = \u221211.16, p < .001; Figure 1). The spline was fitted on the original frequency index, whose knots are empirical percentiles, so zero on the axis is the pooled international average rather than the sample average. Predicted scores were flat at the bottom of the distribution (617 at \u22123.2, 610 at the 10th percentile) and fell steeply above it: 593 at the median, 558 at the 90th percentile, 526 at +1 and 500 at +1.6. Across the interdecile range the predicted score fell by 52 points, so the linear coefficient of \u221222 points understates the slope over the range in which most students sit.")

FIG1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "run", "output", "fig", "fig1_pub.png")
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(8)
p.paragraph_format.keep_with_next = True
if os.path.exists(FIG1):
    p.add_run().add_picture(FIG1, width=Cm(15.6))
else:
    r = p.add_run("[Figure 1 placeholder]"); r.italic = True
smallnote(doc, "Figure 1. Adjusted association between device-use frequency and scientific literacy. "
          "The x-axis is the device-use frequency index, on which zero is the pooled international "
          "average; the y-axis is the predicted score with covariates at their weighted means. Dots "
          "are unadjusted decile means; the line is the spline prediction with its 95% confidence "
          "band. The curve is drawn over the range containing 98% of students "
          "(\u22123.2 to +1.6).")

h(doc, "3.3. Almost all of the association is direct", 2)
para(doc, "Table 2 reports the decomposition. Use frequency was associated with more of both modes, more strongly with entertainment-oriented use (a\u2081 = 0.26) than with learning-oriented use (a\u2082 = 0.10). With both entered, entertainment-oriented use was associated with lower self-regulation (d\u2081 = \u22120.06) and learning-oriented use with higher (d\u2082 = 0.11), and self-regulation was worth 11.26 points per SD (b\u2083). The two serial pathways therefore ran in opposite directions: \u22120.19 points through entertainment-oriented use and +0.12 through learning-oriented use.")

para(doc, "Both were significant and both were negligible. The direct part was \u221221.02 points (95% CI \u221223.18 to \u221218.85), or 95.1% of the total; all indirect parts together came to \u22121.09 points, or 4.9%: \u22120.58 through entertainment-oriented use alone, \u22120.48 through self-regulation alone, +0.04 through learning-oriented use alone, and \u22120.07 through the two serial pathways together, which is 0.3% of the total association. The mechanism the study set out to test accounts for roughly one three-hundredth of the association it was meant to explain.")

table(doc,
      ["Path or effect", "Estimate", "95% CI", "Share of c"],
      [["Use frequency \u2192 entertainment use (a\u2081)", "0.26***", "[0.23, 0.28]", "\u2014"],
       ["Use frequency \u2192 learning use (a\u2082)", "0.10***", "[0.07, 0.13]", "\u2014"],
       ["Use frequency \u2192 self-regulation (a\u2083)", "\u22120.04***", "[\u22120.07, \u22120.02]", "\u2014"],
       ["Entertainment use \u2192 self-regulation (d\u2081)", "\u22120.06***", "[\u22120.09, \u22120.04]", "\u2014"],
       ["Learning use \u2192 self-regulation (d\u2082)", "0.11***", "[0.08, 0.14]", "\u2014"],
       ["Entertainment use \u2192 literacy (b\u2081)", "\u22122.24*", "[\u22124.35, \u22120.13]", "\u2014"],
       ["Learning use \u2192 literacy (b\u2082)", "0.37", "[\u22121.73, 2.47]", "\u2014"],
       ["Self-regulation \u2192 literacy (b\u2083)", "11.26***", "[8.84, 13.69]", "\u2014"],
       ["Total association (c)", "\u221222.11***", "[\u221224.21, \u221220.00]", "100%"],
       ["Direct association (c\u2032)", "\u221221.02***", "[\u221223.18, \u221218.85]", "95.1%"],
       ["\u2014 Indirect via entertainment only (a\u2081b\u2081)", "\u22120.58*", "[\u22121.14, \u22120.02]", "2.6%"],
       ["\u2014 Indirect via learning only (a\u2082b\u2082)", "0.04", "[\u22120.17, 0.24]", "\u22120.2%"],
       ["\u2014 Indirect via self-regulation only (a\u2083b\u2083)", "\u22120.48**", "[\u22120.79, \u22120.17]", "2.2%"],
       ["\u2014 Serial via entertainment (a\u2081d\u2081b\u2083)", "\u22120.19***", "[\u22120.28, \u22120.10]", "0.8%"],
       ["\u2014 Serial via learning (a\u2082d\u2082b\u2083)", "0.12***", "[0.06, 0.18]", "\u22120.5%"],
       ["All indirect (sum of the five)", "\u22121.09**", "[\u22121.76, \u22120.42]", "4.9%"]],
      widths=[7.6, 2.4, 3.3, 2.5],
      caption="Table 2. Decomposition of the association between device-use frequency and scientific "
              "literacy (n = 12,237).",
      note="Note. Estimates from the dual-path serial model with ESCS, gender and home ICT availability "
           "controlled. Paths among standardised variables are standardised coefficients; paths "
           "predicting literacy are in PISA score points. Share of c is the estimate divided by c; the "
           "two serial shares sum to 0.3% (0.8% \u2212 0.5%). Standard errors from 80 Fay-BRR replicate "
           "weights with ten plausible values pooled by Rubin's rules. *p < .05, **p < .01, "
           "***p < .001.")

para(doc, "Two details qualify these coefficients. Learning-oriented use had no direct association with literacy once the other variables were entered (b\u2082 = 0.37, p = .73), so the positive serial pathway is carried entirely by self-regulation. And the coefficient for entertainment-oriented use depends on holding learning-oriented use constant: it was \u22120.03 (p = .013) in the single-path model against \u22120.06 here, while its zero-order correlation with self-regulation was only \u2212.04. The larger dual-path estimate therefore describes entertainment-oriented use at a given level of learning-oriented use, a narrower condition.")

h(doc, "3.4. Configurations of use order achievement, but self-regulation does not track the ordering", 2)
para(doc, "BIC fell from 160,565 at two profiles to 134,268 at six without a clear minimum, and entropy was highest at three (.880). We report the four-profile solution because its entropy (.877) is close to the maximum, its smallest profile is still 14% of the weighted sample, and it separates the two high-use configurations that the composition argument is about (Table 3).")

table(doc,
      ["Profiles", "BIC", "AIC", "Entropy", "Smallest profile (%)"],
      [["2", "160,565", "160,157", ".853", "30.0"],
       ["3", "147,165", "146,549", ".880", "19.7"],
       ["4", "140,915", "140,091", ".877", "14.0"],
       ["5", "135,949", "134,918", ".850", "11.7"],
       ["6", "134,268", "133,028", ".841", "7.4"]],
      widths=[2.4, 3.0, 3.0, 2.6, 4.4],
      caption="Table 3. Fit of latent profile models with two to six profiles (n = 12,342).",
      note="Note. Six hour indicators, full covariance structure, unweighted estimation. BIC and AIC "
           "are relative fit indices; they favour more profiles throughout, so the decision also used "
           "entropy, profile size and interpretability.")

para(doc, "The four profiles (Table 4) were low-use (32.1%), learning-dominant (16.2%), entertainment-dominant (37.8%) and dual-high (14.0%). Mean scientific literacy ordered cleanly: 620.07, 601.95, 589.10 and 582.55. Adjusted for covariates, learning-dominant students scored 13.73 points above the low-use group, entertainment-dominant students 12.61 points below it and dual-high students 21.67 points below it.")

para(doc, "Self-regulation did not follow that ordering. Only the learning-dominant group differed from the low-use group (+0.18 SD); the entertainment-dominant and dual-high groups, whose literacy was 12.61 and 21.67 points lower, did not differ (both p > .29). The composition gradient in achievement therefore has no matching gradient in self-regulation, which is the clearest single indication that self-regulation is not doing the work the mediation model assigns to it.")

table(doc,
      ["Profile", "Share", "Learning (h)", "Entertainment (h)", "Ent. share", "Literacy", "Self-reg."],
      [["Low use", "32.1%", "0.41", "0.62", "57.8%", "601.95", "0.27"],
       ["Learning-dominant", "16.2%", "1.67", "0.87", "32.3%", "620.07***", "0.48***"],
       ["Entertainment-dominant", "37.8%", "0.91", "2.01", "69.6%", "589.10***", "0.26"],
       ["Dual-high", "14.0%", "2.62", "3.45", "56.8%", "582.55***", "0.31"]],
      widths=[4.0, 1.6, 2.2, 2.6, 1.8, 2.0, 1.6],
      caption="Table 4. Configurations of device use and their correlates.",
      note="Note. Shares and hours are weighted descriptives. Literacy and self-regulation were "
           "compared with the low-use profile by weighted regression controlling for ESCS, gender and "
           "home ICT availability; stars mark differences from that profile. ***p < .001; unmarked "
           "differences, p > .29. Membership was assigned by most likely class, so classification error "
           "is not reflected in these standard errors.")

h(doc, "3.5. The mechanism does not depend on which regulation measure is used", 2)
para(doc, "Because the regulation index is a four-item help-seeking scale, the central result could in principle be an artefact of that operationalisation. It is not (Table 5): the direction of every path was the same under all three measures. With the goal-setting index, which measures the planning and monitoring processes the hypothesis is actually about, the entertainment\u2013regulation association was more than twice as large as with help seeking (d\u2081 = \u22120.15 against \u22120.06), as was the learning\u2013regulation association (0.20 against 0.11). A measure-specific artefact would look the opposite way: the theoretically better-matched scale produces the stronger first link.")
para(doc, "The second link moved the other way. Regulation was worth 11.26 points per SD when indexed by help seeking, 7.98 by goal setting and 6.50 by cognitive adaptability, so the serial pathway through entertainment-oriented use was \u22120.30 against \u22120.19 points and its share 1.4% against 0.8%. All indirect pathways came to 2.2% with goal setting and 2.5% with cognitive adaptability. The differences between these figures are not the point; their order of magnitude is: across three measures of one construct the mediated portion stays between 2% and 5%.")

table(doc,
      ["Parameter", "Help seeking (SELFREG)", "Goal setting (GOALSET)", "Cognitive adaptability (COGABIL)"],
      [["Items (\u03b1)", "4 (.80)", "4 (.88)", "4 (.85)"],
       ["Entertainment \u2192 regulation (d\u2081)", "\u22120.064 [\u22120.090, \u22120.039]",
        "\u22120.147 [\u22120.172, \u22120.122]", "\u22120.066 [\u22120.092, \u22120.041]"],
       ["Learning \u2192 regulation (d\u2082)", "0.111 [0.084, 0.138]",
        "0.200 [0.169, 0.230]", "0.108 [0.085, 0.132]"],
       ["Regulation \u2192 literacy (b\u2083)", "11.26 [8.84, 13.69]",
        "7.98 [5.21, 10.75]", "6.50 [4.58, 8.42]"],
       ["Serial via entertainment", "\u22120.188 [\u22120.276, \u22120.100]",
        "\u22120.303 [\u22120.411, \u22120.196]", "\u22120.112 [\u22120.166, \u22120.058]"],
       ["Serial via learning", "0.122 [0.060, 0.184]", "0.155 [0.074, 0.236]", "0.068 [0.033, 0.103]"],
       ["All indirect", "\u22121.089 [\u22121.763, \u22120.415]", "\u22120.480 [\u22121.077, 0.117]",
        "\u22120.543 [\u22121.183, 0.098]"],
       ["All indirect as share of c", "4.9%", "2.2%", "2.5%"]],
      widths=[4.4, 3.9, 3.8, 3.9],
      caption="Table 5. The dual-path model with three regulation measures (B-S-J-Z, China; n = 12,237).",
      note="Note. Paths among standardised variables are standardised coefficients; paths predicting "
           "literacy and indirect terms are in PISA score points. 95% confidence intervals in brackets, "
           "from 80 Fay-BRR replicate weights with ten plausible values pooled by Rubin's rules. "
           "The cognitive-adaptability index reflects willingness to engage with demanding problems rather "
           "than the strategies students use; it is included so that the result does not rest on one "
           "scale family.")

h(doc, "3.6. The association is specific to entertainment time, but the ratio between purposes is not well identified", 2)
para(doc, "Table 6 reports the two continuous formulations. With use frequency held constant, learning and entertainment hours entered together produced a clear asymmetry: each SD of entertainment hours was associated with 4.62 fewer points (95% CI \u22126.67 to \u22122.56) at a given level of learning hours, whereas learning hours were not associated with literacy (0.55, 95% CI \u22121.54 to 2.64, p = .607). As total hours plus the entertainment share, the model gave \u22123.31 points per SD of total hours (95% CI \u22125.46 to \u22121.17) and \u22120.62 points per 10 percentage points toward entertainment (95% CI \u22121.47 to 0.23, p = .155).")
para(doc, "The two formulations disagree in appearance only. The share is a ratio of two collinear quantities, so its coefficient is estimated over a narrow band of variation and its interval is wide; the same model written as two hour scores separates the modes cleanly. Read together they say that composition matters through entertainment rather than through learning, while additional learning-oriented time is not associated with higher literacy in these data (b\u2082 = 0.37, p = .73; r = .01).")
para(doc, "This narrows the composition claim as the introduction stated it. The data are consistent with a five-point gain from reallocating an SD of entertainment time to study, but do not establish it, because the learning coefficient is indistinguishable from zero and the share coefficient alone has an interval that includes no effect. What they establish is that the two modes are not interchangeable: one carries the whole negative association and the other carries no positive one.")

table(doc,
      ["Predictor", "Estimate", "95% CI", "p"],
      [["Model A: total hours and share", "", "", ""],
       ["Use frequency (per SD)", "\u221221.37", "\u221223.49 to \u221219.25", "< .001"],
       ["Total hours (per SD)", "\u22123.31", "\u22125.46 to \u22121.17", ".003"],
       ["Entertainment share (per 10 pp)", "\u22120.62", "\u22121.47 to 0.23", ".155"],
       ["Model B: learning and entertainment hours", "", "", ""],
       ["Use frequency (per SD)", "\u221221.37", "\u221223.49 to \u221219.25", "< .001"],
       ["Learning hours (per SD)", "0.55", "\u22121.54 to 2.64", ".607"],
       ["Entertainment hours (per SD)", "\u22124.62", "\u22126.67 to \u22122.56", "< .001"]],
      widths=[7.4, 2.6, 4.4, 1.8],
      caption="Table 6. Composition as a continuous predictor of scientific literacy (B-S-J-Z, China; n = 12,135).",
      note="Note. Weighted least squares with ESCS, gender and home ICT availability controlled. "
           "Estimates in PISA score points; both models also include use frequency, so the coefficients "
           "describe hours at a given frequency of use. Standard errors from 80 Fay-BRR replicate "
           "weights with ten plausible values pooled by Rubin's rules.")

h(doc, "3.7. The total association replicates across systems; the composition paths do not", 2)
para(doc, "The total association was negative in all four systems, between \u221217.20 and \u221222.11 points per SD, and the design-based joint test did not reject equality (F(3, 80) = 2.27, p = .087). The direct part was equally stable (F(3, 80) = 0.75, p = .528). The regulation\u2013literacy association was positive everywhere but differed in size (11.26, 5.21, 11.37 and 11.12 points per SD; F(3, 80) = 3.89, p = .012), being weakest in Finland. Total and direct associations behave as a general account of device use and achievement would predict.")
para(doc, "The composition paths did not (Table 7). Entertainment-oriented use was negatively associated with literacy in the focal system (\u22122.24 points) but positively in Finland (+10.95), Korea (+5.18) and Hong Kong, China (+10.47); the joint test rejected equality (F(3, 80) = 22.91, p < .001). Learning-oriented use also varied, F(3, 80) = 10.46, p < .001, from \u22126.42 in Finland to +7.20 in Korea.")
para(doc, "The indirect terms followed the same pattern. The net indirect association was \u22121.09 points in the focal system and positive in the other three (+0.74, +1.96 and +1.34; F(3, 80) = 10.72, p < .001), so in three systems the mediated part ran opposite in sign to the total. The serial pathway through entertainment-oriented use was negative in three systems (\u22120.19, \u22120.05 and \u22120.22) and indistinguishable from zero in Hong Kong, China (+0.01), which is what the near-zero entertainment\u2013regulation association there implies.")

table(doc,
      ["", "B-S-J-Z, China", "Finland", "Korea", "Hong Kong, China", "Joint test"],
      [["n", "12,237", "5,652", "6,416", "5,767", ""],
       ["Total (c)", "\u221222.11***", "\u221218.63***", "\u221219.67***", "\u221217.20***", "F = 2.27, p = .087"],
       ["Direct (c\u2032)", "\u221221.02***", "\u221219.37***", "\u221221.63***", "\u221218.54***", "F = 0.75, p = .528"],
       ["Entertainment \u2192 regulation (d\u2081)", "\u22120.064***", "\u22120.047**", "\u22120.071***", "0.003", "F = 5.20, p = .002"],
       ["Learning \u2192 regulation (d\u2082)", "0.111***", "0.033*", "0.119***", "0.075***", "F = 6.26, p < .001"],
       ["Regulation \u2192 literacy (b\u2083)", "11.26***", "5.21***", "11.37***", "11.12***", "F = 3.89, p = .012"],
       ["Entertainment \u2192 literacy (b\u2081)", "\u22122.24*", "10.95***", "5.18**", "10.47***", "F = 22.91, p < .001"],
       ["Learning \u2192 literacy (b\u2082)", "0.37", "\u22126.42***", "7.20***", "\u22120.63", "F = 10.46, p < .001"],
       ["Serial via entertainment", "\u22120.188***", "\u22120.046*", "\u22120.221***", "0.008", "F = 6.75, p < .001"],
       ["Serial via learning", "0.122***", "0.024", "0.123***", "0.121***", "F = 5.95, p = .001"],
       ["All indirect", "\u22121.09**", "0.74*", "1.96***", "1.34**", "F = 10.72, p < .001"],
       ["All indirect as share of c", "4.9%", "\u22124.0%", "\u221210.0%", "\u22127.8%", ""]],
      widths=[4.3, 2.2, 1.8, 1.8, 2.3, 3.2],
      caption="Table 7. The dual-path model in four education systems.",
      note="Note. Variables standardised within system; literacy and indirect terms in score points. "
           "Every cell is estimated with ten plausible values and 80 Fay-BRR replicate weights pooled "
           "by Rubin's rules, so the standard errors are design-based throughout; 95% confidence "
           "intervals for all cells are given in Appendix B. Joint tests are Wald F tests with "
           "3 numerator and 80 denominator degrees of freedom, treating the four samples as "
           "independent. *p < .05, **p < .01, ***p < .001.")

h(doc, "3.8. The pooled multi-system model", 2)
para(doc, "Across the 23 economies (n = 167,180) the total association was \u221220.07 points per SD (95% CI \u221221.36 to \u221218.78), about 0.19 of the pooled within-economy SD; the direct part was \u221220.36 points (95% CI \u221221.65 to \u221219.07) and the net indirect part +0.29 points (95% CI \u22120.04 to +0.62, p = .084), about 1.5% of the total and opposite in sign to it. The two serial pathways were \u22120.09 and +0.08 points. At this scale the mediated portion is not distinguishable from zero and points the wrong way.")
para(doc, "The pooled model assumes common slopes, which Table 7 rejects for the composition paths. It is reported because it answers a different question: the four-system comparison shows that the composition slopes are local, and the pooled model shows that, averaged over 23 systems with different slopes, the mediated portion stays near 1.5% and does not reach significance. Together they rule out a larger mediation effect hiding in the systems we did not examine separately.")

table(doc,
      ["Parameter", "Estimate", "95% CI", "p"],
      [["Total (c)", "\u221220.07", "\u221221.36 to \u221218.78", "< .001"],
       ["Direct (c\u2032)", "\u221220.36", "\u221221.65 to \u221219.07", "< .001"],
       ["Entertainment \u2192 regulation (d\u2081)", "\u22120.048", "\u22120.057 to \u22120.038", "< .001"],
       ["Learning \u2192 regulation (d\u2082)", "0.089", "0.079 to 0.099", "< .001"],
       ["Regulation \u2192 literacy (b\u2083)", "7.20", "6.12 to 8.27", "< .001"],
       ["Serial via entertainment", "\u22120.089", "\u22120.113 to \u22120.064", "< .001"],
       ["Serial via learning", "0.077", "0.058 to 0.096", "< .001"],
       ["All indirect", "0.29", "\u22120.04 to 0.62", ".084"],
       ["All indirect as share of c", "\u22121.5%", "", ""]],
      widths=[7.4, 2.6, 4.4, 1.8],
      caption="Table 8. Pooled model across 23 education systems (n = 167,180).",
      note="Note. All variables standardised within economy, so the coefficients are in score points per "
           "within-economy SD. Estimator as in Table 7, with replicate weights pooled across economies. "
           "The 23 economies are those with at least 2,000 students and at least 80% complete data on "
           "the five key variables; they are listed in Appendix A.")

h(doc, "3.9. The return to regulation is conditional on composition", 2)
para(doc, "The interaction between regulation and entertainment-oriented use was negative (b = \u22122.39, SE = 1.13, 95% CI \u22124.61 to \u22120.17, p = .035). At low entertainment use, one SD more regulation was associated with 13.64 more points (95% CI 10.42 to 16.86); at high entertainment use, 8.86 points (95% CI 5.53 to 12.19). The interval for the difference (4.78, 95% CI 0.34 to 9.21) nearly includes zero, and the model omitted learning-oriented use, so we treat the interaction as a lead rather than an established moderator.")

h(doc, "3.10. Robustness", 2)
para(doc, "Table 9 re-estimates the model under eight alternative specifications. The two serial terms kept their signs throughout but moved in size: the entertainment pathway ranged from \u22120.32 to \u22120.12, and the two random halves of the sample produced \u22120.26 and \u22120.12; the learning pathway ranged from +0.03 to +0.14 and lost significance when entertainment hours were replaced by the entertainment share. The net indirect association ranged from \u22120.90 to \u22122.15 points. No specification produced an indirect share above about 10%, which is the property the argument rests on.")

table(doc,
      ["Specification", "Serial via entertainment", "Serial via learning", "All indirect"],
      [["Baseline", "\u22120.19***", "0.12***", "\u22121.09**"],
       ["Extended controls", "\u22120.18***", "0.10***", "\u22121.69***"],
       ["Unweighted", "\u22120.19***", "0.11***", "\u22121.23***"],
       ["Control for digital resources in science lessons", "\u22120.16***", "0.09***", "\u22121.13***"],
       ["Random half, first", "\u22120.26***", "0.14**", "\u22121.05*"],
       ["Random half, second", "\u22120.12*", "0.10**", "\u22121.11*"],
       ["Alternative mediator: entertainment share", "\u22120.13***", "0.03", "\u22120.90**"],
       ["Alternative predictor: school days only", "\u22120.12***", "0.09**", "\u22121.03***"],
       ["Alternative predictor: weekends only", "\u22120.24***", "0.12***", "\u22122.15***"]],
      widths=[7.4, 3.6, 2.6, 2.2],
      caption="Table 9. Robustness of the decomposition.",
      note="Note. Values in score points. Standard errors from 80 Fay-BRR replicate weights with ten "
           "plausible values pooled by Rubin's rules, except the unweighted model (500 bootstrap "
           "resamples). Extended controls add grade, grade repetition, home language and school ICT "
           "resources. *p < .05, **p < .01, ***p < .001.")

# ------------------------------------------------------------------ 4 讨论
h(doc, "4. Discussion", 1)

h(doc, "4.1. A robust association that is almost entirely direct", 2)
para(doc, "The negative association between device-use frequency and scientific literacy was large, nonlinear and present in every system we examined, and it was almost entirely direct. Roughly 95% of it remained after the two modes of use and self-regulation were taken into account, and the serial pathways that motivated the study accounted for 0.3%. This is not a matter of statistical power: the pathways were estimated with confidence intervals that exclude zero. They are simply small relative to what they are meant to explain.")

para(doc, "The shape deserves as much attention as the size. The curve was flat at the bottom of the distribution and fell steeply across the range where most students sit, by 52 points between the 10th and 90th percentiles of use, so the average linear slope understates the difference that a typical move within the distribution is associated with. Reporting one coefficient for a heavily skewed exposure misrepresents the relation for the majority of the sample.")

h(doc, "4.2. Self-regulation: a correlate, not a conduit", 2)
para(doc, "Self-regulation was one of the sturdier correlates in the data: it correlated .20 with literacy, each SD was worth 5 to 11 points across the four systems and 11 in the focal one, and it was associated with how students used their devices, negatively with entertainment-oriented use and positively with learning-oriented use. What it did not do was carry the association, and the magnitude was bounded in advance by the product of its links: with a\u2081 = 0.26 and b\u2083 = 11.3, a one-SD shift in use moves regulation by 0.26 SD, worth about 2.9 points, an order of magnitude below the 22-point association before any cancellation is allowed for. Three observations explain why the mediation claim fails even though each component path is significant.")

para(doc, "First, the two composition paths have opposite signs and similar magnitudes, so they cancel (\u22120.19 and +0.12 points). This is structural rather than accidental: any population in which entertainment use is negatively and learning use positively related to regulation produces a near-zero net serial pathway whenever the two modes rise together with overall frequency, which a\u2081 = 0.26 and a\u2082 = 0.10 describe. Reporting the pathways separately hides the cancellation; reporting their share of the total exposes it.")

para(doc, "Second, the person-centred results contradict the mediation model. If regulation were the mechanism, the groups whose literacy differed most should differ most in regulation. They did not: entertainment-dominant and dual-high students scored 12.61 and 21.67 points below the low-use group with regulation indistinguishable from it, and only the learning-dominant group, which also had the highest literacy, had higher regulation. That pattern is equally consistent with regulation and learning-oriented use both reflecting a third factor, such as academic engagement or prior attainment.")

para(doc, "Third, the measure is a general disposition, not regulation during device use. The four items ask whether students seek help when they are stuck; they say nothing about what happens when a notification arrives during a science task, and the goal-setting items ask how often students plan their studying, not how they manage a device. The mismatch is not fatal for a correlational claim but is fatal for a mechanism claim, because the mechanism is specifically about the moment of use.")
para(doc, "The measurement choice does not, however, explain the size of the result. If the small mediated portion were an artefact of a narrow help-seeking scale, a broader scale should have produced a larger one. It did not: with goal setting the first link more than doubled while the second fell (7.98 against 11.26 points) and the mediated share moved from 4.9% to 2.2%. The components of the mechanism are measurable and behave as the theory expects; what fails is their product relative to the association they are meant to carry.")

h(doc, "4.3. Composition orders achievement without carrying the association", 2)
para(doc, "The configurations ordered achievement more sharply than total use did. Students who used devices mainly for learning scored highest; those who used them heavily for both purposes scored lowest, 21.67 points below the low-use group. Total frequency does not separate these groups and orders them the wrong way: the learning-dominant profile, which scored highest, had a mean frequency indistinguishable from the low-use profile (\u22121.07 against \u22121.09), while the dual-high profile, which scored lowest, had the highest frequency (\u22120.53). A single intensity measure would put learning-dominant students at the bottom. This is the strongest support in our data for treating composition as a substantive variable rather than a nuisance.")

para(doc, "The two descriptions agree only partly, and the disagreement is instructive. Continuously, the association is carried entirely by entertainment-oriented time (\u22124.62 points per SD) while learning-oriented time is flat (0.55, p = .61), and the ratio between purposes has an interval that includes zero. The profiles separate two groups with similar totals: learning-dominant students reported 1.27 hours per setting and scored 620.07, entertainment-dominant students 1.46 hours and 589.10. A ratio treats a student who does a little of both as equivalent to one who does a little of one; the profiles show that they are not equivalent in achievement.")
para(doc, "The support has two limits. The composition effects that are estimated precisely are effects of one mode rather than of the balance between modes, and the composition-specific coefficients are unstable across systems. Composition appears to mark differences between students rather than to cause them: a student who uses a device mainly for study is also doing something else that raises science scores, and the device use is as much a symptom of that as a cause.")

h(doc, "4.4. Why the composition paths do not generalise", 2)
para(doc, "The reversal between systems is the result we did not anticipate and the one with the clearest methodological implication. Two readings are possible and the data do not decide between them. The first is compositional confounding: where entertainment use is socially embedded and near-universal, the students who report most of it may be the more socially connected and engaged, so the same item indexes a different population of behaviours. The second is that the item set asks about time in three settings including school, so where devices are integrated into lessons, entertainment-oriented use at school may capture a different activity from what it captures where devices are banned in class. Both point the same way: invariance of composition effects should not be assumed, and single-system estimates of these paths are not general mechanisms.")


para(doc, "The stable elements are worth stating separately, because they are what a general account would have to explain. The total association was negative everywhere and of similar size, regulation was positively associated with literacy everywhere, and the entertainment\u2013regulation association was negative in three systems and near zero in the fourth. What varied was the link from composition to achievement.")

h(doc, "4.5. Implications", 2)
para(doc, "For theory, the consequence is that self-regulation should stop being the default mediator in this literature. It is a robust correlate and a plausible outcome of device use; it is not a plausible conduit for the association with achievement, at least not when measured as a general disposition. Candidate alternatives that the design did not measure include displaced study time, shortened sleep (Hale & Guan, 2015), attentional residue in class (Uncapher & Wagner, 2018) and motivational crowding-out; any of them could carry the 95% that remained direct.")

para(doc, "For reporting practice, mediation studies of digital media should report the indirect share alongside the significance of each path, as is routine in epidemiology (VanderWeele, 2016). Our own results would have looked successful under the usual convention: both serial pathways were significant at p < .001. The share makes the difference between a mechanism and a rounding error visible in one number.")

para(doc, "For practice, the implications are narrower than the mediation framing suggested. Because regulation carried almost none of the association, interventions that train planning and monitoring should not be expected to offset the academic correlates of heavy device use, however valuable they are otherwise. Because the achievement gradient across configurations had no matching gradient in regulation, and because the composition coefficients reversed across systems, we would not recommend that schools reallocate device time between purposes on the basis of these data. What the data support is descriptive: how students use devices distinguishes groups more sharply than how much they use them, and that distinction is worth measuring well.")

# ------------------------------------------------------------------ 5 局限
h(doc, "5. Limitations", 1)
para(doc, "The design is cross-sectional. Every estimate is an association, temporal order is assumed rather than observed, and reverse causation is entirely plausible: students with weaker regulation may choose more entertainment, and students with stronger science skills may choose more learning-oriented use. The serial model is a convenient partition of covariance, not a causal chain, and the small size of the indirect terms is one reason to prefer the weaker reading.")

para(doc, "All measures are self-reported. Use hours are coarse category midpoints, the frequency indices are self-assessed, and the same respondents supplied the mediator and the covariates, so common-method variance may inflate some associations. The two mode scores are hours per setting and cannot be summed into a day.")

para(doc, "The cross-system comparison has three weaknesses. The four samples are independent by design, so treating them as such is correct, but the joint tests inherit whatever the replicate weights miss about each system's sampling and do not estimate the small between-system covariance that a multilevel model would. The pooled 23-economy model assumes a common slope, which the heterogeneity tests reject for the composition paths, so we read it only as a statement about the net indirect association. And comparability of the regulation indices across systems rests on the scaling of the PISA questionnaire, which we did not re-test for measurement invariance; a system-level difference in how the help-seeking items function would affect the b\u2083 contrasts rather than the within-system shares on which our conclusions rest.")
para(doc, "Two features of the measures limit what can be concluded about composition. The entertainment share is a ratio of two quantities that both enter the model, so its standard error is large by construction and a null result for the share is weaker evidence than the same null on a linear term; and both hour scores average three settings, so a student who uses a device for two hours at school and not at home is scored like one who does the reverse.")

para(doc, "The profile analysis is descriptive. BIC did not reach a minimum, membership was assigned by most likely class without a three-step correction for classification error (Asparouhov & Muth\u00e9n, 2014), the indicators are skewed and bounded, and the model was estimated without sampling weights. Profile contrasts describe groups; they are not effects of belonging to them.")

para(doc, "Finally, the models omit school- and classroom-level factors that plausibly shape both device use and science achievement, being confined to student-level covariates. The four systems are high-performing and cannot represent Chinese education as a whole, let alone other contexts; the 23-economy model widens coverage but does not make the estimates representative of any particular system.")

# ------------------------------------------------------------------ 6 结论
h(doc, "6. Conclusion", 1)
para(doc, "In PISA 2025, students who used digital devices more often scored lower in scientific literacy, by about 22 points per standard deviation, with the decline steepening across the range where most students sit. The association was stable across four education systems and across a pooled sample of 23. Regulation was consistently associated with higher literacy, but it carried almost none of the association: the two serial pathways through it accounted for 0.3% of the total, all indirect pathways for 4.9%, and the mediated share fell rather than rose when regulation was measured as planning and monitoring. Configurations of use ordered achievement more sharply than total use, yet the composition paths reversed sign between systems and the ratio between purposes was not reliably related to literacy at a fixed total. Regulation is a correlate of scientific literacy, not the channel through which device use relates to it, and the search for that channel should move to mechanisms measured at the moment of use.")

# ------------------------------------------------------------------ 参考文献
# ------------------------------------------------------------------ 附录 B
h(doc, "Statements and Declarations", 1)
para(doc, "**Funding.** [To be completed by the authors.]", indent=False)
para(doc, "**Competing interests.** The authors have no competing interests to declare.", indent=False)
para(doc, "**Ethics approval.** This study is a secondary analysis of anonymised, publicly available "
     "PISA 2025 data. The data are collected by the OECD under its own consent and confidentiality "
     "procedures; no additional ethics approval or informed consent was required for the present "
     "analysis.", indent=False)
para(doc, "**Consent to participate.** Not applicable (secondary analysis of anonymised data).",
     indent=False)
para(doc, "**Data availability.** The PISA 2025 public-use student questionnaire and cognitive data "
     "are available from the OECD. All analysis code, the derived analysis file and the result files "
     "used in this manuscript are provided as supplementary material and will be deposited in a "
     "public repository on acceptance.", indent=False)
para(doc, "**Reporting standard.** We report all estimates that were computed, including those that "
     "were not significant, and we give exact p values and 95% confidence intervals rather than "
     "significance stars alone.", indent=False)

h(doc, "Appendix B. Design-based confidence intervals for Table 7", 1)
para(doc, "Note. Every cell is estimated with ten plausible values and 80 Fay-BRR replicate weights "
     "pooled by Rubin's rules. Values are point estimates with 95% confidence intervals in "
     "brackets.")
import json as _json, os as _os
_p = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "run", "output", "multisystem_pv.json")
if _os.path.exists(_p):
    _r = _json.load(open(_p, encoding="utf-8"))
    _rows = []
    for _k, _lab in [("ctotal", "Total (c)"), ("cp", "Direct (c\u2032)"),
                     ("d1", "Entertainment \u2192 regulation (d\u2081)"),
                     ("d2", "Learning \u2192 regulation (d\u2082)"),
                     ("b3", "Regulation \u2192 literacy (b\u2083)"),
                     ("b1", "Entertainment \u2192 literacy (b\u2081)"),
                     ("b2", "Learning \u2192 literacy (b\u2082)"),
                     ("ind_m1a_m2", "Serial via entertainment"),
                     ("ind_m1b_m2", "Serial via learning"),
                     ("ind_total", "All indirect")]:
        _row = [_lab]
        for _sys in ["QCI", "FIN", "KOR", "HKG"]:
            _e = _r[_sys][_k]
            _f = "%.3f" if abs(_e["est"]) < 5 else "%.2f"
            _row.append((_f + " [" + _f + ", " + _f + "]") % (_e["est"], _e["ci"][0], _e["ci"][1]))
        _rows.append(_row)
    table(doc, ["Parameter", "B-S-J-Z, China", "Finland", "Korea", "Hong Kong, China"], _rows,
          widths=[3.6, 3.2, 3.1, 3.1, 3.2], font_size=8,
          caption="Table B1. Estimates with 95% confidence intervals, by system.")

h(doc, "References", 1)
refs = [
 "Adelantado-Renau, M., Moliner-Urdiales, D., Cavero-Redondo, I., Beltran-Valls, M. R., Martínez-Vizcaíno, V., & Álvarez-Bueno, C. (2019). Association between screen media use and academic performance among children and adolescents: A systematic review and meta-analysis. JAMA Pediatrics, 173(11), 1058–1067.",
 "Asparouhov, T., & Muthén, B. (2014). Auxiliary variables in mixture modeling: Three-step approaches using Mplus. Structural Equation Modeling, 21(3), 329–341.",
 "Bandura, A. (1991). Social cognitive theory of self-regulation. Organizational Behavior and Human Decision Processes, 50(2), 248–287.",
 "Dent, A. L., & Koenka, A. C. (2016). The relation between self-regulated learning and academic achievement across childhood and adolescence: A meta-analysis. Educational Psychology Review, 28(3), 425–474.",
 "Fay, R. E. (1989). Theory and application of replicate weighting for variance calculations. In Proceedings of the Section on Survey Research Methods (pp. 212–217). American Statistical Association.",
 "Guo, Q., Qiao, C., & Ibrahim, B. (2022). The mechanism of influence between ICT and students' science literacy: A hierarchical and structural equation modelling study. Journal of Science Education and Technology, 31(2), 272–288.",
 "Hale, L., & Guan, S. (2015). Screen time and sleep among school-aged children and adolescents: A systematic literature review. Sleep Medicine Reviews, 21, 50–58.",
 "Harrell, F. E. (2001). Regression modeling strategies. Springer.",
 "Li, J., Ye, H., Tang, Y., Zhou, Z., & Hu, X. (2018). What are the effects of self-regulation phases and strategies for Chinese students? A meta-analysis of two decades research of the association between self-regulation and academic performance. Frontiers in Psychology, 9, 2434.",
 "Li, Z. (2026). Investigating the roles of digital use quality in developing students' scientific literacy. Journal of Science Education and Technology, 35, 1354–1375.",
 "MacKinnon, D. P., Fairchild, A. J., & Fritz, M. S. (2007). Mediation analysis. Annual Review of Psychology, 58, 593–614.",
 "OECD. (2026a). PISA 2025 assessment and analytical framework. OECD Publishing. https://doi.org/10.1787/86c36975-en",
 "OECD. (2026b). PISA 2025 technical report. OECD Publishing.",
 "Ophir, E., Nass, C., & Wagner, A. D. (2009). Cognitive control in media multitaskers. Proceedings of the National Academy of Sciences, 106(37), 15583–15587.",
 "Orben, A., & Przybylski, A. K. (2019). The association between adolescent well-being and digital technology use. Nature Human Behaviour, 3(2), 173–182.",
 "Pintrich, P. R. (2000). The role of goal orientation in self-regulated learning. In M. Boekaerts, P. R. Pintrich, & M. Zeidner (Eds.), Handbook of self-regulation (pp. 451–502). Academic Press.",
 "Preacher, K. J., & Kelley, K. (2011). Effect size measures for mediation models: Quantitative strategies for communicating indirect effects. Psychological Methods, 16(2), 93–115.",
 "Rubin, D. B. (1987). Multiple imputation for nonresponse in surveys. Wiley.",
 "Sweller, J., Ayres, P., & Kalyuga, S. (2011). Cognitive load theory. Springer.",
 "Uncapher, M. R., & Wagner, A. D. (2018). Minds and brains of media multitaskers: Current findings and future directions. Proceedings of the National Academy of Sciences, 115(40), 9889–9896.",
 "van der Schuur, W. A., Baumgartner, S. E., Sumter, S. R., & Valkenburg, P. M. (2015). The consequences of media multitasking for youth: A review. Computers in Human Behavior, 53, 204–215.",
 "VanderWeele, T. J. (2016). Mediation analysis: A practitioner's guide. Annual Review of Public Health, 37, 17–32.",
 "Vermunt, J. K., & Magidson, J. (2002). Latent class cluster analysis. In J. A. Hagenaars & A. L. McCutcheon (Eds.), Applied latent class analysis (pp. 89–106). Cambridge University Press.",
 "Xiong, F., Nie, Y., Bai, B., & Lee, A. N. (2025). Outside school ICT use for learning and science performance: The mediating role of motivation and epistemological beliefs. European Journal of Education, 60(1), e12838. https://doi.org/10.1111/ejed.12838",
 "Yang, R., Li, Y., & Ye, J. (2025). Can digital device use improve secondary school students' subject literacy? An empirical analysis based on PISA 2022 data. Basic Education, 22, 66–78, 92. [in Chinese]",
 "Zhi, T., & Chen, C. (2019). The impact of internet use time on secondary school students' subject literacy: From the perspective of internet use motivation. Journal of East China Normal University (Educational Sciences), 37, 61–74. [in Chinese]",
 "Zimmerman, B. J. (2002). Becoming a self-regulated learner: An overview. Theory Into Practice, 41(2), 64–70.",
 "Zimmerman, B. J., & Schunk, D. H. (2001). Self-regulated learning and academic achievement: Theoretical perspectives (2nd ed.). Lawrence Erlbaum.",
]
for r_ in refs:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.75)
    p.paragraph_format.first_line_indent = Cm(-0.75)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(r_); run.font.size = Pt(10)

pagebreak(doc)
h(doc, "Appendix A. Economies in the pooled model", 1)
para(doc, "The 23 economies that met the inclusion criteria (at least 2,000 students and at least 80% "
     "complete data on all key variables) are identified by their PISA codes: ARE, AUS, AUT, BRN, EST, "
     "FIN, GRC, HKG, HUN, IRL, ITA, JPN, KOR, MAC, MNG, MYS, POL, QCI, QUA, ROU, SGP, TAP, TUR. "
     "QCI denotes Beijing, Shanghai, Jiangsu and Zhejiang (China); HKG Hong Kong (China); MAC Macao "
     "(China). Variables were standardised within economy before pooling.")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "02_Revised_Manuscript_JSET.docx")
doc.save(out)
print("saved:", out)
