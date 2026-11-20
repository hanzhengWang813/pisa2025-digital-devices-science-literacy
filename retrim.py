# -*- coding: utf-8 -*-
"""
retrim.py — 在 build_manuscript.py 里按「段首锚点」整段替换正文
=================================================================
用法：python retrim.py batch1
      （batch1/batch2/batch3 定义在下方 BATCHES 里）

为什么不在 docx 上改：build_manuscript.py 是唯一真源，改 docx 会在下次
重新生成时丢失。这里只替换 para(...) 整块，表格(table)块一律不动。
锚点取段首 20–40 个 ASCII 字符，必须落在源码第一行内。
"""
import io, json, sys

SRC = "build_manuscript.py"


def load():
    with io.open(SRC, encoding="utf-8") as f:
        return f.read().split("\n")


def save(lines):
    with io.open(SRC, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def find_block(lines, anchor):
    """返回 (i, j)：分块起止行号（含）。anchor 是段首文本。"""
    prefix = 'para(doc, "'
    for i, l in enumerate(lines):
        if l.startswith(prefix):
            head = l[len(prefix):].replace("**", "")
            if head.startswith(anchor.replace("**", "")):
                j = i
                while not lines[j].rstrip().endswith('")'):
                    j += 1
                    if j - i > 40:
                        raise RuntimeError("block too long: " + anchor)
                return i, j
    raise KeyError("anchor not found: " + anchor)


def apply(batch):
    lines = load()
    n_ok = 0
    for anchor, new_text in batch:
        i, j = find_block(lines, anchor)
        if new_text == "":
            del lines[i:j + 1]
        else:
            lit = json.dumps(new_text, ensure_ascii=True)
            lines[i:j + 1] = ["para(doc, %s)" % lit]
        n_ok += 1
    save(lines)
    print("replaced %d blocks" % n_ok)


def insert_after(anchor, new_text):
    """在某个 paragraph 之后插入新段（用于补声明、补句子）。"""
    lines = load()
    i, j = find_block(lines, anchor)
    lit = json.dumps(new_text, ensure_ascii=True)
    lines[j + 1:j + 1] = ["", "para(doc, %s)" % lit]
    save(lines)
    print("inserted after", anchor[:30])


# ---------------------------------------------------------------- batch 1
B1 = [
 ("Digital device use is consistently",
  "Digital device use is consistently associated with lower academic achievement, but why is "
  "unresolved, and self-regulation is the most frequently proposed mediator. We asked not only "
  "whether self-regulation mediates this association but also how much of it the indirect pathways "
  "carry. Using PISA 2025 we analysed 12,237 15-year-olds in Beijing, Shanghai, Jiangsu and Zhejiang "
  "(China), re-estimated the model in Finland, Korea and Hong Kong (China), and pooled 23 education "
  "systems (n = 167,180), separating learning-oriented from entertainment-oriented use and "
  "decomposing the total association into direct and indirect parts. A one-standard-deviation higher "
  "use frequency was associated with 22.11 fewer score points (95% CI \u221224.21 to \u221220.00), and "
  "95% of that association was direct. The two serial pathways through regulation (\u22120.19 and "
  "+0.12 points) carried 0.3% of it; all indirect pathways together carried 4.9%. Refitting the "
  "model with a planning-and-monitoring scale instead of the four-item help-seeking index doubled the "
  "first link but reduced the second, and the mediated share fell to 2.2%. Regulation was associated "
  "with literacy in every system (5 to 11 points per standard deviation) but did not carry the "
  "device-use association. The total association was stable across the four systems (F(3, 80) = 2.27, "
  "p = .087) whereas the composition paths were not: entertainment-oriented use was negatively "
  "associated with literacy in the focal system (\u22122.24 points) and positively associated with it "
  "in the other three (+5.2 to +11.0; F(3, 80) = 22.91, p < .001). In the 23-system model the net "
  "indirect association was +0.29 points (95% CI \u22120.04 to +0.62), about 1.5% of the total and "
  "opposite in sign. Regulation is a correlate of scientific literacy, not a conduit for device-use "
  "effects; mediation studies in this literature should report the indirect share of the total, not "
  "only its significance."),

 ("Most adolescents now study",
  "Most adolescents now study, search and socialise through the same device, and PISA 2025 treats "
  "scientific literacy as a major domain while adding Learning in the Digital World as an innovative "
  "domain, which makes the question of how device use relates to science learning hard to avoid "
  "(OECD, 2026a). The empirical answer has been unstable. Meta-analytic work links heavier screen use "
  "to lower achievement (Adelantado-Renau et al., 2019), analyses of PISA data report negative "
  "associations that are stronger among rural and lower-SES students (Zhi & Chen, 2019) and that "
  "flatten or reverse at low levels of use (Yang et al., 2025), and other work finds associations "
  "small enough to be indistinguishable from noise (Orben & Przybylski, 2019)."),

 ("One influential reading",
  "One influential reading is that total time is the wrong predictor: the same number of hours can "
  "stand for very different activities. Learning-oriented use involves searching, evaluating sources, "
  "planning and monitoring, and has been linked positively to science outcomes through motivational "
  "beliefs (Guo et al., 2022; Li, 2026; Xiong et al., 2025). Entertainment-oriented use is thought to "
  "operate through displaced study time and shortened sleep (Hale & Guan, 2015), the cognitive load "
  "imposed by switching (Sweller et al., 2011), and the attentional residue that switching leaves "
  "behind (Ophir et al., 2009; Uncapher & Wagner, 2018; van der Schuur et al., 2015). On this view "
  "composition matters more than amount."),

 ("Self-regulation is the mechanism most often",
  "Self-regulation is the mechanism most often placed between the two. Activities differ in the "
  "opportunities they give students to set goals, monitor progress and adjust strategies, which are "
  "the processes that define self-regulated learning (Pintrich, 2000; Zimmerman, 2002; Zimmerman & "
  "Schunk, 2001); self-regulation predicts achievement, and somewhat more strongly in science than in "
  "other domains (Dent & Koenka, 2016; Li et al., 2018). If both steps hold, use patterns should "
  "shift self-regulation and self-regulation should carry part of the association. Social-cognitive "
  "theory supplies a reason to expect the shift to be bidirectional, because behaviour and environment "
  "shape self-regulation together (Bandura, 1991)."),

 ("What this literature rarely reports",
  "What this literature rarely reports is the size of the mediation relative to the association it is "
  "meant to explain. Studies report whether an indirect path differs from zero, and increasingly its "
  "standardised size, but seldom what fraction of the total association it accounts for (MacKinnon et "
  "al., 2007; Preacher & Kelley, 2011; VanderWeele, 2016). The omission matters: when the total is "
  "large, an indirect path can be statistically robust and substantively trivial at the same time, "
  "and a mechanism claim resting on it would be unsupported even at p < .001."),

 ("A second limitation is geographic",
  "A second limitation is geographic. Most tests of the composition hypothesis use a single education "
  "system, yet composition-specific paths depend on how a system organises device use: whether "
  "devices are used in lessons, how much of the curriculum is delivered digitally, and how much of "
  "students' discretionary time is structured by school. A single-system estimate therefore cannot "
  "separate a general mechanism from a local pattern."),

 ("A third limitation is that composition",
  "A third limitation is that composition is almost always modelled as two correlated continuous "
  "variables, although students do not allocate time that way. Some use devices heavily for both "
  "purposes, some for neither, and average slopes average over these configurations. A person-centred "
  "description complements the model and can be checked against it: if self-regulation is the "
  "mechanism, groups that differ in composition should also differ in self-regulation."),

 ("We address these points with PISA",
  "We address these points with PISA 2025 and ask five questions. How large is the association "
  "between device-use frequency and scientific literacy, and is it linear? How much of it runs through "
  "self-regulation and through each mode of use, expressed as a share of the total? Do students' "
  "configurations of use order their literacy differently from total use, and does self-regulation "
  "track that ordering? Are the composition paths invariant across education systems? And how much do "
  "the answers depend on how regulation is measured and on whether composition is modelled as a "
  "balance between purposes or as two quantities of time?"),

 ("The study makes four contributions",
  "The study makes four contributions: a full decomposition reported as shares of the total rather "
  "than as the significance of individual paths; tests of the composition paths in four systems and "
  "in 23, with design-based standard errors throughout, which bound what single-system mediation "
  "estimates can be taken to mean; a person-centred description set against the mediation model, "
  "which exposes a discrepancy the mediation results alone would hide; and a replication with three "
  "regulation measures, so that the conclusion cannot be attributed to one operationalisation of a "
  "contested construct."),

 ("PISA 2025 assessed 15-year-olds",
  "PISA 2025 assessed 15-year-olds in 91 economies (OECD, 2026a). The focal sample was Beijing, "
  "Shanghai, Jiangsu and Zhejiang, which PISA reports as a single region (CNT = QCI; n = 12,385). "
  "After listwise deletion on the model variables, 12,237 students remained; missingness was below "
  "0.5% for every variable, and complete cases differ from the full sample by 0.012 SD in mean "
  "scientific literacy, so deletion is not selective in any way that matters here. Three comparison "
  "systems were chosen because they have comparable coverage of the ICT and self-regulation items and "
  "differ in how devices are integrated into schooling: Finland (n = 5,652), Korea (6,416) and Hong "
  "Kong, China (5,767). The pooled analysis retained every economy with at least 2,000 students and "
  "at least 80% complete data on the five key variables; 23 met these criteria (n = 167,180; "
  "Appendix A). All variables were standardised within economy for that analysis, which approximates "
  "economy fixed effects for the intercepts."),

 ("**Scientific literacy.** PISA provides",
  "**Scientific literacy.** PISA provides ten plausible values (PV1SCIE\u2013PV10SCIE), each a random draw "
  "from a student's estimated proficiency distribution. They are not repeated measurements and were "
  "not averaged: every model was estimated once per plausible value and the results were pooled with "
  "Rubin's rules (Rubin, 1987). The sample mean was 597.04 points (SD = 83.52)."),

 ("Frequency of device use.",
  "**Frequency of device use.** Two PISA indices record how often students performed ICT activities on "
  "school days (ICTWKDY) and at weekends (ICTWKEND). Each was standardised on the pooled PISA 2025 "
  "sample and the two scores were averaged, so the index has a mean of zero for the international "
  "sample and \u22120.86 in the Chinese sample (Table 1). It measures how often students use devices, "
  "not how long they use them."),

 ("**Modes of use.** Six items",
  "**Modes of use.** Six items (ST326Q01\u2013Q06) ask how much time students spend using digital "
  "resources for learning and for entertainment in three settings: during school, before and after "
  "lessons, and at weekends. Responses have nine options from \u201cnone\u201d to \u201cmore than 7 "
  "hours\u201d and were coded at the category midpoint (0, 0.5, 1.5, \u2026, 7.5, with 7.5 assigned to "
  "the open category) and averaged across settings, so the scores are hours per setting, not total "
  "daily hours. The entertainment share was entertainment hours divided by the sum of both modes."),

 ("Self-regulation. We used the PISA 2025",
  "**Self-regulation.** SELFREG is a weighted likelihood estimate built from four items (ST433Q01, Q02, "
  "Q04, Q06; OECD, 2026b), all of which ask about help seeking: asking classmates when something is "
  "not fully understood, asking teachers for help when it is needed, asking for help when learning is "
  "difficult, and trying hard to solve a problem alone first. Responses run from strongly agree to "
  "strongly disagree and were reverse-keyed before scaling; the items formed a reliable scale in the "
  "focal sample (\u03b1 = .80, n = 12,301). Adaptive help seeking is an established self-regulated "
  "learning strategy (Pintrich, 2000; Zimmerman, 2002), but it is a strategy rather than the whole of "
  "planning and monitoring, so we describe the index as help seeking and use \u201cregulation\u201d "
  "only as shorthand."),

 ("Two further regulation indices",
  "**Two further regulation indices.** They come from the same block served as construct checks. GOALSET is built from four "
  "items closer to the processes the mediation hypothesis is about \u2014 planning an approach to "
  "studying, summarising material to find gaps in understanding, self-testing, and changing an "
  "approach that is not working (\u03b1 = .88, n = 12,286). COGABIL is a narrower measure of "
  "willingness to engage with demanding problems (\u03b1 = .85, n = 12,301). Because a claim about "
  "device use should not depend on which of three related regulation measures is chosen, we refitted "
  "the model with each in turn."),

 ("**Covariates.** All models controlled",
  "**Covariates.** All models controlled for the PISA index of economic, social and cultural status "
  "(ESCS), gender (female = 1) and ICT availability at home (ICTHOME). Robustness models added grade, "
  "grade repetition, home language, school ICT resources and the reported frequency of using digital "
  "resources in science lessons (IC173Q03JA)."),

 ("Step 1: shape",
  "**Step 1: shape of the association.**  Weighted regressions with restricted cubic splines (three knots "
  "at the 10th, 50th and 90th percentiles of use frequency) described the association, with covariates "
  "held at their weighted means (Harrell, 2001). Nonlinearity was tested with a design-based Wald "
  "test on the spline terms."),

 ("Step 2: decomposition",
  "**Step 2: decomposition.** A dual-path serial model entered both modes of use simultaneously. Use "
  "frequency predicted entertainment-oriented and learning-oriented use; both predicted "
  "self-regulation; self-regulation, both modes and use frequency predicted scientific literacy. "
  "Mediators were standardised within the equations, so paths among standardised variables are fully "
  "standardised and paths predicting literacy are in score points. We also estimated a single-path "
  "model with entertainment-oriented use as the only first mediator, to show how that estimate "
  "changes when learning-oriented use is held constant."),

 ("We report each term in score points",
  "We report each term in score points with its share of c, defined as the term divided by c. The "
  "share is the quantity that decides whether a mechanism claim is warranted, and the quantity this "
  "literature usually omits."),

 ("Step 3: configurations",
  "**Step 3: configurations of use.** Latent profile analysis was fitted to the six hour items with two "
  "to six profiles, full covariance structure and 10 random starts (Vermunt & Magidson, 2002); models "
  "were compared on BIC, AIC, entropy and the smallest profile. Students were assigned to their most "
  "likely profile, and literacy and self-regulation were compared across profiles by weighted "
  "regression against the low-use profile with the same covariates."),

 ("Step 4: composition as a continuous",
  "**Step 4: composition as a continuous predictor.**  Two weighted regressions asked what the phrase "
  "\u201cwhat students do matters more than how long\u201d actually implies. In the first, literacy "
  "was regressed on use frequency, total hours and the entertainment share, so the share coefficient "
  "describes a shift between purposes at a fixed total. In the second, literacy was regressed on use "
  "frequency, learning hours and entertainment hours entered together, which is the same model "
  "written without the ratio. The two parameterisations are algebraically related but not "
  "statistically equivalent: share and total are strongly collinear by construction, so the first "
  "estimates a ratio effect with wide intervals and the second separates the modes."),

 ("Step 5: alternative regulation",
  "**Step 5: alternative regulation measures.** The dual-path model was re-estimated with GOALSET and "
  "with COGABIL in place of SELFREG, which tests whether the mediated pathway depends on the "
  "particular regulation measure."),

 ("Step 6: cross-system comparison",
  "**Step 6: cross-system comparison.** The dual-path model was estimated separately in the focal and "
  "three comparison systems, each with the full plausible-value and replicate-weight pipeline rather "
  "than analytic standard errors. To test whether a path differs across systems, the four samples "
  "were treated as independent and contrasts formed between each comparison system and the focal one; "
  "the variance of a contrast is the sum of the two design-based variances, and contrasts that share "
  "the focal system covary with its variance, giving a Wald statistic with three numerator and 80 "
  "denominator degrees of freedom."),

 ("Step 7: pooled",
  "**Step 7: pooled multi-system model.** The model was then estimated in the pooled 23 economies with "
  "within-economy standardisation and the same pipeline. Economies are independent samples, so "
  "pooling replicate weights gives design-based standard errors. Because the heterogeneity tests "
  "reject a common-slope model for the composition paths, this estimate describes the average "
  "association rather than a common effect."),

 ("Step 8: conditional return",
  "**Step 8: conditional return to self-regulation.** A product term between standardised "
  "self-regulation and standardised entertainment-oriented use tested whether the regulation\u2013"
  "literacy association varies with composition; simple slopes were evaluated at \u00b11 SD."),

 ("All models used the final student weight",
  "All models used the final student weight (W_FSTUWT). Sampling variance was estimated with Fay's "
  "balanced repeated replication, 80 replicate weights and a Fay coefficient of 0.5, which yields 80 "
  "degrees of freedom (Fay, 1989). For indirect terms the full product of coefficients was "
  "re-estimated within each replicate rather than approximated by the delta method, and the resulting "
  "variances were pooled across plausible values with Rubin's rules. The pooled model pooled "
  "replicate weights across independent samples. All models were estimated by weighted least squares; "
  "the estimation code is provided as supplementary material."),

 ("The design is cross-sectional and observational",
  "The design is cross-sectional and observational. Every estimate is an association adjusted for "
  "covariates, and the serial ordering is a modelling assumption that the data cannot verify. No "
  "alpha adjustment was applied across the many tests reported here; exact p values and intervals are "
  "given for every estimate, and the argument rests on shares of the total association rather than on "
  "the number of tests that reach significance."),
]

BATCHES = {"batch1": B1}

if __name__ == "__main__":
    apply(BATCHES[sys.argv[1] if len(sys.argv) > 1 else "batch1"])
