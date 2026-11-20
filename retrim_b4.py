# -*- coding: utf-8 -*-
"""retrim_b4.py — 第四批：摘要降到 ≤250 词，正文逼近 5,950 词"""
import json, sys
sys.path.insert(0, ".")
from retrim import load, save, find_block

B4 = [
 ("Digital device use is consistently",
  "Digital device use is consistently associated with lower academic achievement, but why is "
  "unresolved, and self-regulation is the most frequently proposed mediator. We asked whether "
  "self-regulation mediates this association and how much of it the indirect pathways carry. Using "
  "PISA 2025 we analysed 12,237 15-year-olds in Beijing, Shanghai, Jiangsu and Zhejiang (China), "
  "re-estimated the model in Finland, Korea and Hong Kong (China), and pooled 23 education systems "
  "(n = 167,180), separating learning-oriented from entertainment-oriented use. A "
  "one-standard-deviation higher use frequency was associated with 22.11 fewer score points (95% CI "
  "\u221224.21 to \u221220.00), and 95% of that association was direct. The two serial pathways "
  "through regulation (\u22120.19 and +0.12 points) carried 0.3% of it and all indirect pathways "
  "4.9%; with a planning-and-monitoring scale in place of the four-item help-seeking index the first "
  "link doubled but the second fell, and the mediated share dropped to 2.2%. Regulation was "
  "associated with literacy in every system (5 to 11 points per standard deviation) but did not "
  "carry the device-use association. The total association was stable across the four systems "
  "(F(3, 80) = 2.27, p = .087) while the composition paths were not: entertainment-oriented use was "
  "negatively associated with literacy in the focal system (\u22122.24 points) and positively in the "
  "other three (+5.2 to +11.0; F(3, 80) = 22.91, p < .001). In the 23-system model the net indirect "
  "association was +0.29 points (95% CI \u22120.04 to +0.62), about 1.5% of the total and opposite in "
  "sign. Regulation is a correlate of scientific literacy, not a conduit for device-use effects; "
  "mediation studies should report the indirect share, not only its significance."),

 # 引言：把「地理」与「个体中心」两段并成一段
 ("A second limitation is geographic",
  "Two further limitations are geographic and methodological. Most tests of the composition "
  "hypothesis use a single education system, yet composition-specific paths depend on how a system "
  "organises device use: whether devices are used in lessons, how much of the curriculum is "
  "delivered digitally, and how much discretionary time school structures. And composition is almost "
  "always modelled as two correlated continuous variables, although students do not allocate time "
  "that way; a person-centred description complements the model and can be checked against it, "
  "because if self-regulation is the mechanism, groups that differ in composition should also differ "
  "in self-regulation."),
 ("A third limitation is that composition",
  ""),

 # 2.2 再压
 ("Modes of use. Six items",
  "**Modes of use.** Six items (ST326Q01\u2013Q06) ask how much time students spend using digital "
  "resources for learning and for entertainment in three settings: during school, before and after "
  "lessons, and at weekends. Responses have nine options from \u201cnone\u201d to \u201cmore than 7 "
  "hours\u201d and were coded at the category midpoint (0, 0.5, 1.5, \u2026, 7.5) and averaged across "
  "settings, so the scores are hours per setting, not daily hours. The entertainment share was "
  "entertainment hours divided by the sum of both modes."),
 ("Two further regulation indices",
  "**Two further regulation indices.** GOALSET is built from four items closer to the processes the "
  "hypothesis is about \u2014 planning an approach to studying, summarising material to find gaps, "
  "self-testing, and changing an approach that is not working (\u03b1 = .88, n = 12,286). COGABIL is "
  "a narrower measure of willingness to engage with demanding problems (\u03b1 = .85, n = 12,301). "
  "Because a claim about device use should not depend on which of three related measures is chosen, "
  "we refitted the model with each in turn."),

 # 2.3：Step 1/3/4/6 各再压
 ("Step 1: shape of the association",
  "**Step 1: shape of the association.** Weighted regressions with restricted cubic splines (three "
  "knots at the 10th, 50th and 90th percentiles of use frequency) described the association, with "
  "covariates at their weighted means (Harrell, 2001); nonlinearity was tested with a design-based "
  "Wald test on the spline terms."),
 ("Step 3: configurations of use",
  "**Step 3: configurations of use.** Latent profile analysis was fitted to the six hour items with "
  "two to six profiles, full covariance structure and 10 random starts (Vermunt & Magidson, 2002), "
  "compared on BIC, AIC, entropy and smallest profile. Students were assigned to their most likely "
  "profile, and literacy and regulation were compared across profiles by weighted regression against "
  "the low-use profile."),
 ("Step 4: composition as a continuous predictor",
  "**Step 4: composition as a continuous predictor.** Two weighted regressions asked what \u201cwhat "
  "students do matters more than how long\u201d implies. The first regressed literacy on use "
  "frequency, total hours and the entertainment share, so the share coefficient describes a shift "
  "between purposes at a fixed total; the second regressed literacy on use frequency, learning hours "
  "and entertainment hours entered together, which is the same model without the ratio. The two "
  "parameterisations are algebraically related but not statistically equivalent, because share and "
  "total are strongly collinear by construction."),
 ("Step 6: cross-system comparison",
  "**Step 6: cross-system comparison.** The model was estimated separately in the focal and three "
  "comparison systems, each with the full plausible-value and replicate-weight pipeline rather than "
  "analytic standard errors. To test whether a path differs across systems, the four samples were "
  "treated as independent and contrasts formed between each comparison system and the focal one; "
  "contrasts that share the focal system covary with its variance, giving a Wald statistic with three "
  "numerator and 80 denominator degrees of freedom."),
 ("Step 7: pooled multi-system model",
  "**Step 7: pooled multi-system model.** The model was then estimated in the pooled 23 economies "
  "with within-economy standardisation and the same pipeline. Because economies are independent "
  "samples, pooling replicate weights gives design-based standard errors. Because the heterogeneity "
  "tests reject a common-slope model for the composition paths, this estimate describes the average "
  "association rather than a common effect."),

 # 3.3 / 3.6 / 3.7 再压
 ("Table 2 reports the decomposition",
  "Table 2 reports the decomposition. Use frequency was associated with more of both modes, more "
  "strongly with entertainment-oriented use (a\u2081 = 0.26) than with learning-oriented use "
  "(a\u2082 = 0.10). With both entered, entertainment-oriented use was associated with lower "
  "self-regulation (d\u2081 = \u22120.06) and learning-oriented use with higher (d\u2082 = 0.11), and "
  "self-regulation was worth 11.26 points per SD (b\u2083). The two serial pathways therefore ran in "
  "opposite directions: \u22120.19 points through entertainment-oriented use and +0.12 through "
  "learning-oriented use."),
 ("Two details qualify these coefficients",
  "Two details qualify these coefficients. Learning-oriented use had no direct association with "
  "literacy once the other variables were entered (b\u2082 = 0.37, p = .73), so the positive serial "
  "pathway is carried entirely by self-regulation. And the coefficient for entertainment-oriented use "
  "depends on holding learning-oriented use constant: it was \u22120.03 (p = .013) in the single-path "
  "model against \u22120.06 here, while its zero-order correlation with self-regulation was only "
  "\u2212.04. The larger dual-path estimate therefore describes entertainment-oriented use at a given "
  "level of learning-oriented use, a narrower condition."),
 ("Table 6 reports the two continuous",
  "Table 6 reports the two continuous formulations. With use frequency held constant, learning and "
  "entertainment hours entered together produced a clear asymmetry: each SD of entertainment hours was "
  "associated with 4.62 fewer points (95% CI \u22126.67 to \u22122.56) at a given level of learning "
  "hours, whereas learning hours were not associated with literacy (0.55, 95% CI \u22121.54 to 2.64, "
  "p = .607). As total hours plus the entertainment share, the model gave \u22123.31 points per SD of "
  "total hours (95% CI \u22125.46 to \u22121.17) and \u22120.62 points per 10 percentage points "
  "toward entertainment (95% CI \u22121.47 to 0.23, p = .155)."),

 # 4.2：合并前两段
 ("Self-regulation was one of the sturdier",
  "Self-regulation was one of the sturdier correlates in the data: it correlated .20 with literacy, "
  "each SD was worth 5 to 11 points across the four systems and 11 in the focal one, and it was "
  "associated with how students used their devices, negatively with entertainment-oriented use and "
  "positively with learning-oriented use. What it did not do was carry the association, and the "
  "magnitude was bounded in advance by the product of its links: with a\u2081 = 0.26 and "
  "b\u2083 = 11.3, a one-SD shift in use moves regulation by 0.26 SD, worth about 2.9 points, an "
  "order of magnitude below the 22-point association before any cancellation is allowed for. Three "
  "observations explain why the mediation claim fails even though each component path is "
  "significant."),
 ("First, the two composition paths have opposite",
  "First, the two composition paths have opposite signs and similar magnitudes, so they cancel "
  "(\u22120.19 and +0.12 points). This is structural rather than accidental: any population in which "
  "entertainment use is negatively and learning use positively related to regulation produces a "
  "near-zero net serial pathway whenever the two modes rise together with overall frequency, which "
  "a\u2081 = 0.26 and a\u2082 = 0.10 describe. Reporting the pathways separately hides the "
  "cancellation; reporting their share of the total exposes it."),

 # 5：合并两条测量局限
 ("Two features of the measures limit",
  "Two features of the measures limit what can be concluded about composition. The entertainment "
  "share is a ratio of two quantities that both enter the model, so its standard error is large by "
  "construction and a null result for the share is weaker evidence than the same null on a linear "
  "term; and both hour scores average three settings, so a student who uses a device for two hours at "
  "school and not at home is scored like one who does the reverse."),
]

if __name__ == "__main__":
    lines = load()
    for anchor, new_text in B4:
        i, j = find_block(lines, anchor)
        if new_text == "":
            del lines[i:j + 1]
        else:
            lines[i:j + 1] = ["para(doc, %s)" % json.dumps(new_text, ensure_ascii=True)]
    save(lines)
    print("replaced", len(B4), "blocks")
