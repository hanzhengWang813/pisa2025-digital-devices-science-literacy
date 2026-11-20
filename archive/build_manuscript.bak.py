# -*- coding: utf-8 -*-
"""build_manuscript.py — 生成修订版英文稿（目标期刊 Journal of Science Education and Technology）"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx_helpers import *
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING

doc = new_doc("en")
add_page_numbers(doc)

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

for line in ["[Author 1]\u00b9, [Author 2]\u00b9",
             "\u00b9 [Department], [University], [City], China",
             "Corresponding author: [Name]; [email]"]:
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(18 if line.startswith("[Author") else 4)
    r = p.add_run(line); r.font.size = Pt(12)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(36)
r = p.add_run("Declarations of interest: none.  Funding: [to be completed].  "
              "Data: PISA 2025 public-use student file (OECD).  "
              "Analysis code and result files are available from the corresponding author.")
r.font.size = Pt(10)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

pagebreak(doc)

# ------------------------------------------------------------------ 摘要
h(doc, "Abstract", 1)
para(doc, "Digital device use is consistently associated with lower academic achievement, but the "
     "reason is unresolved, and self-regulation is the most frequently proposed mediator. We asked not "
     "only whether self-regulation mediates this association but also how much of it the indirect "
     "pathways carry. Using PISA 2025, we analysed 12,237 15-year-olds in Beijing, Shanghai, Jiangsu and "
     "Zhejiang (China), re-estimated the model in Finland, Korea and Hong Kong (China), and pooled 23 "
     "education systems (n = 167,180). The models separated learning-oriented from entertainment-oriented "
     "use and decomposed the total association into direct and indirect parts. A one-standard-deviation "
     "higher device-use frequency was associated with 22.11 fewer score points (95% CI \u221224.21 to "
     "\u221220.00). Ninety-five per cent of this association was direct. The two serial pathways through "
     "regulation (\u22120.19 and +0.12 points) together accounted for 0.3% of the association; all "
     "indirect pathways together accounted for 4.9%. The regulation index is a four-item help-seeking "
     "scale, so we repeated the model with two further regulation measures; with the planning and "
     "monitoring scale the first link was twice as large but the second was smaller, and the mediated "
     "share fell to 2.2%. Regulation was associated with scientific literacy in every system (5 to 11 "
     "points per standard deviation), but it did not carry the device-use association. The total "
     "association was stable across the four systems (F(3, 80) = 2.27, p = .087), whereas the "
     "composition paths were not: entertainment-oriented use was negatively associated with literacy in "
     "the focal system (\u22122.24 points) and positively associated with it in the other three (+5.2 to "
     "+11.0; F(3, 80) = 22.91, p < .001). In the 23-system model the net indirect association was +0.29 "
     "points (95% CI \u22120.04 to +0.62), about 1.5% of the total and opposite in sign to it. "
     "Regulation is a correlate of scientific literacy, not a conduit for device-use effects. Studies "
     "that test mediation in this literature should report the indirect share of the total association, "
     "not only its significance.")

para(doc, "**Keywords:** digital device use; scientific literacy; self-regulation; mediation; "
     "PISA 2025; cross-system comparison")

# ------------------------------------------------------------------ 1 引言
h(doc, "1. Introduction", 1)

para(doc, "Most adolescents now study, search and socialise through the same device. PISA 2025 "
     "treats scientific literacy as a major domain and adds Learning in the Digital World as an "
     "innovative domain, which makes the question of how device use relates to science learning "
     "difficult to avoid (OECD, 2026a). The empirical answer has been surprisingly unstable. "
     "Meta-analytic work links heavier screen media use to lower academic performance "
     "(Adelantado-Renau et al., 2019). Analyses of PISA data report negative associations that are "
     "stronger among rural and lower-SES students (Zhi & Chen, 2019) and that flatten or reverse at "
     "low levels of use, with tentative thresholds near two hours of learning-oriented and one hour of "
     "entertainment-oriented use (Yang et al., 2025). Other work finds associations so small that they "
     "are difficult to distinguish from noise (Orben & Przybylski, 2019).")

para(doc, "One influential reading of this disagreement is that total time is the wrong predictor. "
     "The same number of hours can stand for very different activities, and those activities differ in "
     "what they demand from the student. Learning-oriented use involves searching, evaluating sources, "
     "planning and monitoring, and it has been linked positively and indirectly to science outcomes "
     "through motivational beliefs (Guo et al., 2022; Li, 2026; Xiong et al., 2025). "
     "Entertainment-oriented use is thought to operate through displaced study time and shortened sleep "
     "(Hale & Guan, 2015), through the cognitive load imposed by switching between tasks "
     "(Sweller et al., 2011), and through the attentional residue that switching leaves behind "
     "(Ophir et al., 2009; van der Schuur et al., 2015; Uncapher & Wagner, 2018). On this view, "
     "composition matters more than amount.")

para(doc, "Self-regulation is the mechanism most often placed between the two. The argument has two "
     "steps. First, activities differ in the opportunities they give students to set goals, monitor "
     "progress and adjust strategies, which are the processes that define self-regulated learning "
     "(Zimmerman, 2002; Pintrich, 2000; Zimmerman & Schunk, 2001). Second, self-regulation predicts "
     "achievement, and it predicts it somewhat more strongly in science than in other domains "
     "(Dent & Koenka, 2016; Li et al., 2018). If both steps hold, then use patterns should shift "
     "self-regulation, and self-regulation should carry part of the association between device use and "
     "scientific literacy. Social-cognitive theory supplies the reason to expect the shift to be "
     "bidirectional, because behaviour and the environment shape self-regulation together "
     "(Bandura, 1991).")

para(doc, "What this literature rarely reports is the size of the mediation relative to the "
     "association it is meant to explain. Mediation studies typically report whether an indirect path "
     "differs from zero, and they increasingly report standardised indirect effects; they seldom report "
     "what fraction of the total association the indirect path accounts for (MacKinnon et al., 2007; "
     "Preacher & Kelley, 2011; VanderWeele, 2016). The omission matters here. When the total "
     "association is large, an indirect path can be statistically robust and substantively trivial at "
     "the same time, and a mechanism claim resting on it would be unsupported even at p < .001.")

para(doc, "A second limitation is geographic. Most tests of the composition hypothesis use a single "
     "education system, or a single system per study. Composition-specific paths, however, depend on "
     "how a system organises device use: on whether devices are used in lessons, on how much of the "
     "curriculum is delivered digitally, and on how much of students' discretionary time is structured "
     "by school. A single-system estimate therefore cannot separate a general mechanism from a local "
     "pattern, and the same coefficients may carry different meanings in different systems.")

para(doc, "A third limitation is that composition is almost always modelled as two correlated "
     "continuous variables. Students do not allocate time that way. Some use devices heavily for both "
     "purposes, some for neither, and a model that estimates average slopes across the whole sample "
     "averages over these configurations. A person-centred description is a useful complement, "
     "particularly because it can be checked against the mediation model: if self-regulation is the "
     "mechanism, then groups that differ in composition should also differ in self-regulation.")

para(doc, "We address these points with PISA 2025 data. The study has five questions. First, how large "
     "is the association between the frequency of device use and scientific literacy, and is it linear? "
     "Second, how much of that association runs through self-regulation and through each mode of use, "
     "expressed as a share of the total? Third, do students' configurations of use order their "
     "scientific literacy differently from total use, and does self-regulation track that ordering? "
     "Fourth, are the composition-specific paths invariant across education systems? Fifth, how much do "
     "the answers depend on how regulation is measured, and on whether composition is modelled as a "
     "balance between purposes or as two separate quantities of time?")

para(doc, "The study makes four contributions. It reports a full decomposition of the association "
     "rather than the significance of individual paths, and shows that the association is almost "
     "entirely direct. It tests the composition paths in four education systems and in a pooled sample "
     "of 23, with design-based standard errors throughout, and shows that the total association is "
     "stable while the composition paths are not, which bounds what single-system mediation estimates "
     "can be taken to mean. It sets a person-centred description against the mediation model, which "
     "exposes a discrepancy that the mediation results alone would hide. And it repeats the mediation "
     "with three regulation measures, so that the conclusion cannot be attributed to one "
     "operationalisation of a contested construct.")

# ------------------------------------------------------------------ 2 方法
h(doc, "2. Method", 1)

h(doc, "2.1. Data and samples", 2)
para(doc, "PISA 2025 assessed 15-year-olds in 91 economies (OECD, 2026a). The focal sample comprised "
     "students in Beijing, Shanghai, Jiangsu and Zhejiang, which PISA reports as a single "
     "region (CNT = QCI; n = 12,385). After listwise deletion on the variables in the dual-path model, "
     "12,237 students remained. Three further systems were selected for comparison because they have "
     "comparable coverage of the ICT and self-regulation items and because they differ in how digital "
     "devices are integrated into schooling: Finland (n = 5,652), Korea (n = 6,416) and Hong Kong "
     "(China) (n = 5,767; 30,072 students in total). For the pooled analysis we retained every economy "
     "with at least 2,000 students and at least 80% complete data on the five key variables; 23 "
     "economies met these criteria (n = 167,180; economy codes are listed in Appendix A). All variables "
     "were standardised within economy for that analysis, which approximates economy fixed effects for "
     "the intercepts.")

h(doc, "2.2. Measures", 2)
para(doc, "**Scientific literacy.** PISA provides ten plausible values (PV1SCIE\u2013PV10SCIE), each a "
     "random draw from a student's estimated proficiency distribution. They are not repeated "
     "measurements and were not averaged for estimation. Every model was estimated ten times, once per "
     "plausible value, and the results were pooled with Rubin's rules (Rubin, 1987). The sample mean "
     "was 597.04 points (SD = 83.52).")
para(doc, "**Frequency of device use.** Two PISA indices record how often students performed ICT "
     "activities on school days (ICTWKDY) and at weekends (ICTWKEND). Each was standardised on the "
     "pooled PISA 2025 sample and the two scores were averaged. The resulting index therefore has a "
     "mean of zero for the pooled international sample, not for the Chinese sample, in which its mean "
     "is \u22120.86 (Table 1). This index measures how often students use devices, not how long they "
     "use them.")
para(doc, "**Modes of use.** Six items (ST326Q01\u2013Q06) ask how much time students spend using "
     "digital resources for learning and for entertainment in three settings: during school, before and "
     "after lessons, and at weekends. Each item has nine response options from \u201cnone\u201d to "
     "\u201cmore than 7 hours\u201d; responses were coded at the category midpoint (0, 0.5, 1.5, "
     "\u2026, 7.5 hours, with 7.5 assigned to the open category) and averaged across the three "
     "settings. The resulting scores are hours per setting, not total daily hours, and we describe them "
     "accordingly throughout. The entertainment share was computed as entertainment hours divided by "
     "the sum of both modes.")
para(doc, "**Self-regulation.** We used the PISA 2025 self-regulation index (SELFREG), a weighted "
     "likelihood estimate built from four questionnaire items (ST433Q01, Q02, Q04, Q06; OECD, 2026b). "
     "All four ask "
     "about help seeking: whether students ask their classmates when they do not fully understand "
     "something, whether they ask their teachers for help when they need it, whether they ask for help "
     "when they have trouble learning, and whether they try hard to solve a problem on their own first. "
     "The response scale runs from strongly agree to strongly disagree, so the items were reverse-keyed "
     "before scaling. In the focal sample the four items formed a reliable scale (\u03b1 = .80, "
     "n = 12,301). Adaptive help seeking is an established self-regulated learning strategy "
     "(Zimmerman, 2002; Pintrich, 2000), but it is a strategy, not the whole of planning and monitoring, "
     "We therefore describe the index as a measure of help seeking, and use the shorter label "
     "\u201cregulation\u201d only as shorthand.")
para(doc, "Two further regulation indices from the same questionnaire were used as construct checks. "
     "The goal-setting index (GOALSET) is built from four items that come closer to the processes the "
     "mediation hypothesis is about: planning an approach to studying, summarising material to find "
     "gaps in understanding, self-testing to check comprehension, and changing an approach that is not "
     "working (\u03b1 = .88, n = 12,286). The cognitive-adaptability index (COGABIL) is a third, "
     "narrower measure drawn from the same block (\u03b1 = .85, n = 12,301). Because a mediation claim "
     "about device use should not "
     "depend on which of three related regulation measures is chosen, we refitted the dual-path model "
     "with each in turn.")
para(doc, "**Covariates.** All models controlled for the PISA index of economic, social and cultural "
     "status (ESCS), gender (female = 1) and ICT availability at home (ICTHOME). Robustness models "
     "added grade, grade repetition, home language, the school ICT resources index and the reported "
     "frequency of using digital resources in science lessons (IC173Q03JA).")

h(doc, "2.3. Analytic strategy", 2)
para(doc, "**Step 1: shape of the association.** Weighted regressions with restricted cubic splines "
     "(three knots at the 10th, 50th and 90th percentiles of use frequency) described the association "
     "between use frequency and scientific literacy, with covariates held at their weighted means "
     "(Harrell, 2001). Nonlinearity was tested with a design-based Wald test on the nonlinear spline "
     "terms.")
para(doc, "**Step 2: decomposition.** A dual-path serial model entered both modes of use "
     "simultaneously. Use frequency predicted entertainment-oriented use and learning-oriented use; "
     "both predicted self-regulation; self-regulation, both modes and use frequency predicted "
     "scientific literacy. All mediators were standardised within the equations, so paths among "
     "standardised variables are fully standardised and paths predicting literacy are in score points. "
     "We also estimated a single-path model with entertainment-oriented use as the only first mediator, "
     "to show how the estimate of that path changes when learning-oriented use is held constant.")
para(doc, "The model partitions the total association c into a direct part c\u2032 and five indirect "
     "parts, two of which are the serial pathways of interest:")
para(doc, "c = c\u2032 + a\u2081b\u2081 + a\u2082b\u2082 + a\u2083b\u2083 + "
     "(a\u2081d\u2081b\u2083) + (a\u2082d\u2082b\u2083)", indent=False, align="center")
para(doc, "We report each term in score points together with its share of c, defined as the term "
     "divided by c. The share is the quantity that decides whether a mechanism claim is warranted, and "
     "it is the quantity this literature usually omits.")
para(doc, "**Step 3: configurations of use.** Latent profile analysis was fitted to the six hour items, "
     "with two to six profiles, full covariance structure and 10 random starts (Vermunt & Magidson, "
     "2002). Models were compared on BIC, AIC, entropy and the smallest profile; the choice is discussed "
     "with the results. Students were assigned to their most likely profile, and scientific literacy and "
     "self-regulation were compared across profiles by weighted regression with the low-use profile as "
     "reference, adjusting for the same covariates.")
para(doc, "**Step 4: composition as a continuous predictor.** Two weighted regressions asked the "
     "question that the phrase \u201cwhat students do matters more than how long\u201d actually implies. "
     "In the first, literacy was regressed on use frequency, total hours of device use and the "
     "entertainment share, so that the share coefficient describes a shift between purposes at a fixed "
     "total. In the second, literacy was regressed on use frequency, learning hours and entertainment "
     "hours entered together, which is the same model written without the ratio. The two "
     "parameterisations are algebraically related but not statistically equivalent: the share and the "
     "total are strongly collinear by construction, so the first estimates a ratio effect with wide "
     "intervals, and the second separates the two modes.")
para(doc, "**Step 5: alternative regulation measures.** The dual-path model was re-estimated with "
     "GOALSET and with COGABIL in place of SELFREG. This tests whether the size of the mediated pathway "
     "depends on the particular regulation measure, which it should not if the mechanism is a general "
     "one.")
para(doc, "**Step 6: cross-system comparison.** The dual-path model was estimated separately in the "
     "focal system and in the three comparison systems, each with the full plausible-value and "
     "replicate-weight pipeline rather than with analytic standard errors. To test whether a path "
     "differs across systems, we treated the four samples as independent and formed contrasts between "
     "each comparison system and the focal system. The variance of a contrast is the sum of the two "
     "design-based variances, and two contrasts that share the focal system covary with the variance of "
     "the focal estimate; the resulting quadratic form gives a Wald statistic with three numerator and "
     "80 denominator degrees of freedom.")
para(doc, "**Step 7: pooled multi-system model.** The dual-path model was then estimated in the pooled "
     "sample of 23 economies with within-economy standardisation, using the same plausible-value and "
     "replicate-weight pipeline. Economies are independent samples, so pooling the replicate weights "
     "gives design-based standard errors for the pooled estimate rather than the bootstrap "
     "approximations used in some secondary analyses of PISA. Because the heterogeneity tests reject a "
     "common-slope model for the composition paths, this estimate is read as a description of the "
     "average association, not as a common effect.")
para(doc, "**Step 8: conditional return to self-regulation.** A product term between standardised "
     "self-regulation and standardised entertainment-oriented use tested whether the association between "
     "self-regulation and literacy varies with composition; simple slopes were evaluated at \u00b11 SD.")

h(doc, "2.4. Inference", 2)
para(doc, "All models used the final student weight (W_FSTUWT). Sampling variance was estimated with "
     "Fay's balanced repeated replication, using 80 replicate weights and a Fay coefficient of 0.5, "
     "which yields 80 degrees of freedom (Fay, 1989). For indirect terms the full product of "
     "coefficients was re-estimated within each replicate rather than approximated by the delta method, "
     "and the resulting variances were pooled across the ten plausible values with Rubin's rules. The "
     "pooled 23-economy model used the same pipeline, pooling replicate weights across economies that "
     "are independent samples. All models were estimated with weighted least squares; the code is "
     "available from the authors.")
para(doc, "The design is cross-sectional and observational. Every estimate is an association adjusted "
     "for covariates, and the serial ordering is a modelling assumption that the data cannot verify.")

# ------------------------------------------------------------------ 3 结果
h(doc, "3. Results", 1)

h(doc, "3.1. Descriptive results", 2)
para(doc, "Table 1 gives the weighted descriptives. Students reported more entertainment-oriented use "
     "(M = 1.58 hours per setting) than learning-oriented use (M = 1.11); entertainment accounted for "
     "58% of the combined time. Scientific literacy correlated negatively with use frequency "
     "(r = \u2212.28) and with entertainment-oriented use (r = \u2212.10), positively with "
     "self-regulation (r = .20) and with ESCS (r = .33), and not at all with learning-oriented use "
     "(r = .01). The two modes of use correlated at .31, which is high enough that their separate "
     "coefficients depend on simultaneous entry.")

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
para(doc, "After adjustment, a one-SD higher use frequency was associated with 22.11 fewer points "
     "(95% CI \u221224.21 to \u221220.00), about 0.26 of the sample SD. The association was nonlinear "
     "(nonlinear spline term b = \u221221.77, SE = 1.95, t(80) = \u221211.16, p < .001; Figure 1). "
     "The spline was fitted on the original frequency index rather than on the within-sample "
     "standardised score used in the models, because its knots are empirical percentiles of that "
     "index; zero on the axis is therefore the pooled international average, not the sample average. "
     "Predicted scores were flat at the bottom of the distribution, at 617 points at \u22123.2 and "
     "610 at the 10th percentile (\u22121.93), and fell steeply above it: 593 at the median "
     "(\u22120.63), 558 at the 90th percentile (+0.27), 526 at +1 and 500 at +1.6, the upper end of "
     "the observed range. Across the interdecile range the predicted score fell by 52 points, so the "
     "linear coefficient of \u221222 points understates the slope over the range in which most "
     "students sit.")

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(6)
r = p.add_run("[Figure 1 here]")
r.italic = True; r.font.size = Pt(11)
smallnote(doc, "Figure 1. Adjusted association between device-use frequency and scientific literacy. "
          "The x-axis is the device-use frequency index, on which zero is the pooled international "
          "average; the y-axis is the predicted scientific literacy score with covariates at their "
          "weighted means. Grey dots are unadjusted decile means; the red line is the spline prediction "
          "with its 95% confidence band. The curve is drawn over the observed range only "
          "(\u22123.2 to +1.6).")

h(doc, "3.3. Almost all of the association is direct", 2)
para(doc, "Table 2 reports the decomposition. Use frequency was associated with more of both modes of "
     "use, and more strongly with entertainment-oriented use (a\u2081 = 0.26) than with "
     "learning-oriented use (a\u2082 = 0.10). With both modes entered, entertainment-oriented use was "
     "associated with lower self-regulation (d\u2081 = \u22120.06) and learning-oriented use with "
     "higher self-regulation (d\u2082 = 0.11). Self-regulation was associated with 11.26 more points "
     "per SD (b\u2083). The two serial pathways therefore ran in opposite directions: \u22120.19 points "
     "through entertainment-oriented use and +0.12 points through learning-oriented use.")

para(doc, "Both pathways were statistically significant and both were negligible. The direct part of "
     "the association was \u221221.02 points (95% CI \u221223.18 to \u221218.85), or 95.1% of the "
     "total. All indirect parts together came to \u22121.09 points, or 4.9%: \u22120.58 through "
     "entertainment-oriented use alone, \u22120.48 through self-regulation alone, +0.04 through "
     "learning-oriented use alone, and \u22120.07 through the two serial pathways together, which is "
     "0.3% of the total association. The mechanism the study set out to test accounts for roughly one "
     "three-hundredth of the association it was meant to explain.")

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

para(doc, "Two details qualify the coefficients in Table 2. First, learning-oriented use had no direct "
     "association with literacy once the other variables were entered (b\u2082 = 0.37, p = .73), so the "
     "positive serial pathway is carried entirely by self-regulation. Second, the coefficient for "
     "entertainment-oriented use depends on holding learning-oriented use constant: in the single-path "
     "model it was \u22120.03 (p = .013), compared with \u22120.06 in the dual-path model, while its "
     "zero-order correlation with self-regulation was only \u2212.04. Because the two modes correlate "
     "at .31, the larger dual-path estimate describes entertainment-oriented use at a given level of "
     "learning-oriented use, which is a narrower and less common condition than the single-path "
     "estimate describes.")

h(doc, "3.4. Configurations of use order achievement, but self-regulation does not track the ordering", 2)
para(doc, "BIC fell from 160,565 at two profiles to 134,268 at six, without a clear minimum, and "
     "entropy was highest at three profiles (.880). We report the four-profile solution because its "
     "entropy (.877) is close to the maximum, its smallest profile is still 14% of the weighted sample, "
     "and it separates the two high-use configurations that the composition argument is about. The fit "
     "indices for two to six profiles are given in Table 3.")

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

para(doc, "The four profiles (Table 4) were a low-use group (32.1%), a learning-dominant group (16.2%), "
     "an entertainment-dominant group (37.8%) and a dual-high group (14.0%). Mean scientific literacy "
     "ordered cleanly: 620.07 for learning-dominant, 601.95 for low-use, 589.10 for entertainment-"
     "dominant and 582.55 for dual-high. Adjusted for covariates, learning-dominant students scored "
     "13.73 points above the low-use group, entertainment-dominant students 12.61 points below it and "
     "dual-high students 21.67 points below it.")

para(doc, "Self-regulation did not follow this ordering. Only the learning-dominant group differed from "
     "the low-use group (+0.18 SD); the entertainment-dominant and dual-high groups, whose literacy was "
     "12.61 and 21.67 points lower, did not differ in self-regulation (both p > .29). The composition "
     "gradient in achievement therefore has no matching gradient in self-regulation. This is the "
     "clearest single indication that self-regulation is not doing the work the mediation model "
     "assigns to it, and we return to it in the discussion.")

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
para(doc, "Because the self-regulation index is a four-item help-seeking scale, the central result of "
     "this paper could in principle be an artefact of that operationalisation. It is not. Table 5 "
     "refits the dual-path model with three regulation measures taken from the same questionnaire. The "
     "direction of every path was the same under all three. With the goal-setting index, which measures "
     "the planning and monitoring processes that the mediation hypothesis is actually about, the "
     "association between entertainment-oriented use and regulation was more than twice as large as "
     "with help seeking (d\u2081 = \u22120.15 against \u22120.06), and its association with "
     "learning-oriented use was also larger (0.20 against 0.11). This is the opposite of what a "
     "measure-specific artefact would look like: the theoretically better-matched scale produces the "
     "stronger first link.")
para(doc, "The second link moved the other way. Regulation was worth 11.26 points per SD when indexed "
     "by help seeking, 7.98 when indexed by goal setting and 6.50 when indexed by cognitive "
     "adaptability. The serial pathway through entertainment-oriented use was therefore \u22120.30 "
     "points with goal setting against \u22120.19 with help seeking, and because the total association "
     "is unchanged, its share was 1.4% against 0.8%. All indirect pathways together came to 2.2% with "
     "goal setting and 2.5% with cognitive adaptability. The differences between these figures are not "
     "the point; their order of magnitude is. Across three measures of the same broad construct, the "
     "mediated portion stays between 2% and 5% of the total.")

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
para(doc, "Table 6 reports the two continuous formulations of the composition claim. With use frequency "
     "held constant, learning hours and entertainment hours entered together produced a clear asymmetry. "
     "Each SD of entertainment hours was associated with 4.62 fewer points (95% CI \u22126.67 to "
     "\u22122.56) at a given level of learning hours, whereas learning hours were not associated with "
     "literacy (0.55, 95% CI \u22121.54 to 2.64, p = .607). Written instead as total hours plus the "
     "entertainment share, the model gave \u22123.31 points per SD of total hours (95% CI \u22125.46 "
     "to \u22121.17) and \u22120.62 points per 10 percentage points toward entertainment (95% CI "
     "\u22121.47 to 0.23, p = .155).")
para(doc, "The two formulations disagree in appearance only. The share is a ratio of two collinear "
     "quantities, so its coefficient is estimated over a narrow band of variation and its interval is "
     "wide; the same model written as two hour scores separates the modes cleanly. Read together they "
     "say that the mode of use matters through entertainment rather than through learning. It is "
     "entertainment-heavy use that carries the negative association, while additional learning-oriented "
     "time is not associated with higher literacy in these data (b\u2082 = 0.37, p = .73; r = .01).")
para(doc, "This narrows the composition claim as it was stated in the introduction. The data are "
     "consistent with a five-point gain from reallocating an SD of entertainment time to study, but "
     "they do not establish it, because the learning coefficient underlying that figure is "
     "indistinguishable from zero and the share coefficient alone has an interval that includes no "
     "effect. What they do establish is that the two modes are not interchangeable: one carries the "
     "whole negative association and the other carries no positive one.")

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
para(doc, "The total association was negative in all four systems, between \u221217.20 and \u221222.11 "
     "points per SD, and the design-based joint test did not reject equality across systems "
     "(F(3, 80) = 2.27, p = .087). The direct part was equally stable (F(3, 80) = 0.75, p = .528). The "
     "association between regulation and literacy was "
     "positive in every system but differed in size (11.26, 5.21, 11.37 and 11.12 points per SD; "
     "F(3, 80) = 3.89, p = .012), being weaker in Finland. The total association and its direct part are "
     "what a general account of device use and achievement would need to explain, and they behave as a "
     "general account would predict.")
para(doc, "The composition paths did not behave that way (Table 7). Entertainment-oriented use was "
     "negatively associated with literacy in the focal system (\u22122.24 points) but positively "
     "associated with it in Finland (+10.95), Korea (+5.18) and Hong Kong, China (+10.47); the joint "
     "test rejected equality (F(3, 80) = 22.91, p < .001). Learning-oriented use also varied by system, "
     "F(3, 80) = 10.46, p < .001, from \u22126.42 in Finland to +7.20 in Korea.")
para(doc, "The indirect terms followed the same pattern. The net indirect association was \u22121.09 "
     "points in the focal system and positive in the other three (+0.74, +1.96 and +1.34; "
     "F(3, 80) = 10.72, p < .001), so in three of the four systems the mediated part ran opposite in "
     "sign to the total association. The serial pathway through entertainment-oriented use was negative "
     "in three systems (\u22120.19, \u22120.05 and \u22120.22) and indistinguishable from zero in "
     "Hong Kong, China (+0.01), which is what the near-zero association between entertainment-oriented "
     "use and regulation in that system implies.")

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
para(doc, "Across the 23 economies that met the inclusion rule (n = 167,180), the total association was "
     "\u221220.07 points per SD of use (95% CI \u221221.36 to \u221218.78 points), which is about 0.19 "
     "of the pooled within-economy SD. The direct part was \u221220.36 points (95% CI \u221221.65 to "
     "\u221219.07) and "
     "the net indirect part +0.29 points (95% CI \u22120.04 to +0.62, p = .084), which is about 1.5% of "
     "the total and opposite in sign to it. The two serial pathways were \u22120.09 and +0.08 points. "
     "At this scale the mediated portion is not distinguishable from zero, and the point estimate points "
     "the wrong way.")
para(doc, "The pooled model assumes common slopes, which the heterogeneity tests of Table 7 reject for "
     "the composition paths. It is reported because it answers a different question. The four-system "
     "comparison shows that the composition slopes are local; the pooled model shows that, averaged over "
     "23 systems with different composition slopes, the mediated portion of the association remains at "
     "about 1.5% and does not reach significance. The two results together rule out the possibility that "
     "a larger mediation effect is hiding in the systems we did not examine separately.")

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
para(doc, "The interaction between regulation and entertainment-oriented use was negative "
     "(b = \u22122.39, SE = 1.13, 95% CI \u22124.61 to \u22120.17, p = .035). At low "
     "entertainment-oriented use, one SD more regulation was associated with 13.64 more points "
     "(95% CI 10.42 to 16.86); at high entertainment-oriented use the figure was 8.86 points "
     "(95% CI 5.53 to 12.19). The slopes differed by 4.78 points (95% CI 0.34 to 9.21). The lower "
     "bound of that interval is close to zero, the model did not include learning-oriented use, and we "
     "therefore treat the interaction as a lead rather than as an established moderator.")

h(doc, "3.10. Robustness", 2)
para(doc, "Table 9 re-estimated the dual-path model under eight alternative specifications. The two "
     "serial terms kept their signs throughout, but their sizes moved: the entertainment pathway ranged "
     "from \u22120.32 to \u22120.12, and the two random halves of the sample produced \u22120.26 and "
     "\u22120.12. The learning pathway ranged from +0.03 to +0.14 and lost significance when "
     "entertainment hours were replaced by the entertainment share. The net indirect association ranged "
     "from \u22120.90 to \u22122.15 points. In every specification it remained small relative to the "
     "total association, which is the property that matters for the argument of this paper: the "
     "conclusion does not depend on which of these specifications is preferred, because none of them "
     "produces an indirect share above about 10%.")

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
para(doc, "The negative association between device-use frequency and scientific literacy was large, "
     "nonlinear and present in every system we examined. It was also almost entirely direct. Roughly "
     "95% of it remained after the two modes of use and self-regulation were taken into account, and "
     "the serial pathways that motivated the study accounted for 0.3%. This is not a matter of "
     "statistical power: the pathways were estimated with confidence intervals that exclude zero. They "
     "are simply small relative to what they are meant to explain.")

para(doc, "The shape of the association deserves as much attention as its size. The curve was flat "
     "at the bottom of the distribution and fell steeply across the range where most students sit, by "
     "52 points between the 10th and 90th percentiles of use. The average linear slope of 22 points "
     "therefore understates the difference that a typical move within the distribution is associated "
     "with. Reporting one coefficient for a heavily skewed exposure misrepresents the relation for the "
     "majority of the sample.")

h(doc, "4.2. Self-regulation: a correlate, not a conduit", 2)
para(doc, "Self-regulation was one of the sturdier correlates in the data. It correlated .20 with "
     "literacy, and each SD was worth 5 to 11 points across the four systems, and 11 points in the "
     "focal one. "
     "It was also, in the focal system, associated with how students used their devices: negatively "
     "with entertainment-oriented use and positively with learning-oriented use. What it did not do was "
     "carry the association. Three observations explain why the mediation claim fails even though each "
     "of its component paths is significant.")

para(doc, "First, the two composition paths have opposite signs and similar magnitudes, so they cancel "
     "almost exactly (\u22120.19 and +0.12 points). This is a structural property of the model, not an "
     "accident of this sample: any population in which entertainment use is negatively and learning use "
     "positively related to self-regulation will produce a near-zero net serial pathway whenever the "
     "two modes rise together with overall frequency, which is what a\u2081 = 0.26 and a\u2082 = 0.10 "
     "describe. Reporting the two pathways separately, as mediation studies usually do, hides the "
     "cancellation; reporting their share of the total exposes it.")

para(doc, "Second, the person-centred results contradict the mediation model. If self-regulation were "
     "the mechanism, the groups whose literacy differed most should differ most in self-regulation. "
     "They did not: entertainment-dominant and dual-high students scored 12.61 and 21.67 points below "
     "the low-use group with self-regulation indistinguishable from it. Only the learning-dominant "
     "group, which also had the highest literacy, had higher self-regulation. That pattern is equally "
     "consistent with self-regulation and learning-oriented use both reflecting a third factor, such as "
     "academic engagement or prior attainment, rather than one causing the other.")

para(doc, "Third, the measure is a general disposition, not a measure of regulation during device use. "
     "The four items of SELFREG ask whether students seek help when they are stuck; they say nothing "
     "about what happens when a notification arrives during a science task. The same applies to the "
     "goal-setting items, which ask how often students plan and monitor their studying, not how they "
     "manage a device. The mismatch is not fatal for a correlational claim, but it is fatal for a "
     "mechanism claim, because the mechanism is specifically about the moment of use. A measure of "
     "regulation-in-context, or of the attentional costs of switching, would be needed to test it.")
para(doc, "The measurement choice does not, however, explain the size of the result, and it is worth "
     "separating the two questions. If the small mediated portion were an artefact of a narrow "
     "help-seeking scale, then a broader regulation scale should have produced a larger one. It did "
     "not: with the goal-setting index, which is the better match to the theory, the first link more "
     "than doubled (\u22120.15 against \u22120.06) while the second link fell (7.98 against 11.26 points), and "
     "the mediated share moved from 4.9% to 2.2%. The components of the mechanism are measurable and "
     "behave as the theory expects; what fails is their product relative to the association they are "
     "meant to carry.")

h(doc, "4.3. Composition orders achievement without carrying the association", 2)
para(doc, "The configurations of use ordered achievement more sharply than total use did. Students who "
     "used devices mainly for learning scored highest, and students who used them heavily for both "
     "purposes scored lowest, 21.67 points below the low-use group. Total frequency does not separate "
     "these groups, and it orders them the wrong way: the learning-dominant profile, which scored "
     "highest, had a mean frequency indistinguishable from the low-use profile (\u22121.07 vs "
     "\u22121.09), while the dual-high profile, which scored lowest, had the highest frequency of the "
     "four (\u22120.53). A single intensity measure would put learning-dominant students at the bottom. This is the strongest support in our data for treating composition as a "
     "substantive variable rather than a nuisance.")

para(doc, "The person-centred and variable-centred results agree, but only partly, and the "
     "disagreement is instructive. When use is measured continuously, the association is carried "
     "entirely by entertainment-oriented time (\u22124.62 points per SD) while learning-oriented time is "
     "flat (0.55, p = .61), and the ratio between the two purposes, entered with total hours held "
     "constant, has an interval that includes zero. The profile comparison, by contrast, separates two "
     "groups whose totals are similar: learning-dominant students reported 1.27 hours per setting and "
     "scored 620.07, entertainment-dominant students reported 1.46 hours and scored 589.10. The "
     "difference between these two results is what the categorical measure adds. A ratio treats a "
     "student who does a little of both as equivalent to a student who does a little of one, and the "
     "profiles show that these are not equivalent in achievement.")
para(doc, "The support therefore has two limits, and the second is the same limit that undermines the "
     "mediation model. First, the composition effects that are estimated precisely are effects of one "
     "mode rather than of the balance between modes. Second, the composition-specific coefficients are "
     "unstable across systems and the indirect terms built from them are small and sign-inconsistent. "
     "Composition appears to mark differences between students rather than to cause them. A student who "
     "uses a device mainly for study is, in these data, a student who is also doing something else that "
     "raises science scores; the device use is a symptom of that something else as much as a cause of "
     "it.")

h(doc, "4.4. Why the composition paths do not generalise", 2)
para(doc, "The reversal between systems is the result we did not anticipate and the one with the "
     "clearest methodological implication. Entertainment-oriented use was negatively associated with "
     "literacy in the Chinese sample and positively associated with it in Finland, Korea and Hong Kong "
     "(China). Two readings are possible, and the data do not decide between them.")

para(doc, "The first is compositional confounding. In systems where most entertainment use is socially "
     "embedded and near-universal, the students who report the most of it may be the more socially "
     "connected and the more engaged, not the more disengaged; the same item then indexes a different "
     "population of behaviours in different systems. The second is that the item set asks about time "
     "with digital resources in three settings including school, so in systems where devices are "
     "integrated into lessons, \u201centertainment-oriented use at school\u201d may capture a different "
     "activity from what it captures where devices are banned in class. Both readings point the same "
     "way: cross-system invariance of composition effects should not be assumed, and single-system "
     "estimates of these paths should not be read as general mechanisms.")

para(doc, "The stable elements are worth stating separately, because they are what a general account "
     "would have to explain. The total association was negative everywhere and of similar size. "
     "Self-regulation was positively associated with literacy everywhere. The association between "
     "entertainment-oriented use and self-regulation was negative in three of four systems and near "
     "zero in the fourth. What varied was the link from composition to achievement.")

h(doc, "4.5. Implications", 2)
para(doc, "For theory, the practical consequence is that self-regulation should stop being the default "
     "mediator in this literature. It is a robust correlate and a plausible outcome of device use; it "
     "is not a plausible conduit for the association with achievement, at least not when measured as a "
     "general disposition, whether as help seeking or as planning and monitoring. Candidate alternatives that the present design did not measure include "
     "displaced study time, shortened sleep (Hale & Guan, 2015), attentional residue in class "
     "(Uncapher & Wagner, 2018) and motivational crowding-out. Any of these could carry the 95% that "
     "remained direct.")

para(doc, "For reporting practice, we suggest that mediation studies of digital media report the "
     "indirect share of the total association alongside the significance of each path, as is routine in "
     "epidemiology (VanderWeele, 2016). Our own results would have looked successful under the usual "
     "convention: both serial pathways were significant at p < .001. The share makes the difference "
     "between a mechanism and a rounding error visible in one number.")

para(doc, "For practice, the implications are narrower than the mediation framing suggested. Because "
     "self-regulation carried almost none of the association, interventions that train planning and "
     "monitoring should not be expected to offset the academic correlates of heavy device use, however "
     "valuable they are for other reasons. Because the composition gradient in achievement was not "
     "accompanied by a gradient in self-regulation, and because the composition coefficients reversed "
     "across systems, we would not recommend that schools reallocate device time between purposes on "
     "the basis of these data. What the data do support is descriptive: how students use devices "
     "distinguishes groups more sharply than how much they use them, and the distinction is worth "
     "measuring well.")

# ------------------------------------------------------------------ 5 局限
h(doc, "5. Limitations", 1)
para(doc, "The design is cross-sectional. Every estimate is an association, the temporal order is "
     "assumed rather than observed, and reverse causation is entirely plausible: students with weaker "
     "self-regulation may choose more entertainment, and students with stronger science skills may "
     "choose more learning-oriented use. The serial model is a convenient partition of covariance, not "
     "a causal chain, and the small size of the indirect terms is one reason to prefer the weaker "
     "reading.")

para(doc, "All measures are self-reported. Use hours are coarse category midpoints, the frequency "
     "indices are self-assessed, and the same respondents supplied the mediator and the covariates, so "
     "common-method variance may inflate some associations. The two mode-of-use scores are hours per "
     "setting rather than total daily hours and cannot be summed into a day.")

para(doc, "The cross-system comparison has two weaknesses. The four samples are independent by design, so "
     "treating them as such is correct, but the joint tests inherit whatever the replicate weights miss "
     "about each system's sampling and they do not estimate the small between-system covariance that a "
     "multilevel model would. The pooled 23-economy model assumes a common slope across "
     "economies, which the heterogeneity tests reject for the composition paths; we therefore read that "
     "model only as a statement about the net indirect association.")
para(doc, "Two features of the measures limit what can be concluded about composition. The share of time "
     "spent on entertainment is a ratio of two quantities that both enter the model, so its standard "
     "error is large by construction and a null result for the share is weaker evidence than the same "
     "null on a linear term would be. And both hour scores are averages over three settings rather than "
     "daily totals, so a student who uses a device for two hours at school and not at all at home is "
     "scored like a student who does the reverse.")

para(doc, "The profile analysis is descriptive. BIC did not reach a minimum, membership was assigned by "
     "most likely class without a three-step correction for classification error (Asparouhov & "
     "Muthén, 2014), the indicators are skewed and bounded, and the model was estimated without "
     "sampling weights. Profile contrasts should be read as descriptions of groups, not as effects of "
     "belonging to them.")

para(doc, "Finally, the model omits school-level and classroom-level factors that plausibly shape both "
     "device use and science achievement, being confined to student-level covariates. The four systems "
     "are high-performing and cannot represent Chinese education as a whole, let alone other contexts; "
     "the 23-economy model widens coverage but does not make the estimates representative of any "
     "particular system.")

# ------------------------------------------------------------------ 6 结论
h(doc, "6. Conclusion", 1)
para(doc, "In PISA 2025, students who used digital devices more often scored lower in scientific "
     "literacy, by about 22 points per standard deviation, and the decline steepened across the range "
     "where most students sit. This association was stable across four education systems and across a "
     "pooled sample of 23. Regulation was consistently associated with higher literacy, but it carried "
     "almost none of the association: the two serial pathways through it accounted for 0.3% of the "
     "total, all indirect pathways together for 4.9%, and the mediated share fell rather than rose when "
     "regulation was measured as planning and monitoring instead of help seeking. Patterns of use "
     "ordered achievement more sharply than total use did, yet the composition-specific paths reversed "
     "sign between education systems and the ratio between purposes was not reliably related to "
     "literacy at a fixed total. Regulation is a correlate of scientific literacy, not the channel "
     "through which device use relates to it, and the search for that channel should move to mechanisms "
     "that are measured at the moment of use.")

# ------------------------------------------------------------------ 参考文献
# ------------------------------------------------------------------ 附录 B
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
 "Li, J., et al. (2018). What are the effects of self-regulation phases and strategies for Chinese students? A meta-analysis of two decades research of the association between self-regulation and academic performance. Frontiers in Psychology, 9, 2434.",
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
 "Xiong, F., et al. (2025). Outside school ICT use for learning and science performance: The mediating role of motivation and epistemological beliefs. European Journal of Education, 60, e12838.",
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
