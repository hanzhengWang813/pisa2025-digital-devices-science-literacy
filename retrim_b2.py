# -*- coding: utf-8 -*-
"""retrim_b2.py — 第二批：结果节压缩到 ~1,870 词，数字全部保持已核验值"""
import io, sys
sys.path.insert(0, ".")
from retrim import load, save, find_block

B2 = [
 ("Table 1 gives the weighted descriptives",
  "Table 1 gives the weighted descriptives. Students reported more entertainment-oriented use "
  "(M = 1.58 hours per setting) than learning-oriented use (M = 1.11), so entertainment accounted for "
  "58% of the combined time. Scientific literacy correlated negatively with use frequency "
  "(r = \u2212.28) and with entertainment-oriented use (r = \u2212.10), positively with "
  "self-regulation (r = .20) and ESCS (r = .33), and not at all with learning-oriented use "
  "(r = .01). The two modes correlated at .31, which is high enough that their separate coefficients "
  "depend on simultaneous entry."),

 ("After adjustment, a one-SD higher",
  "After adjustment, a one-SD higher use frequency was associated with 22.11 fewer points (95% CI "
  "\u221224.21 to \u221220.00), about 0.26 of the sample SD, and the association was nonlinear "
  "(nonlinear spline term b = \u221221.77, SE = 1.95, t(80) = \u221211.16, p < .001; Figure 1). The "
  "spline was fitted on the original frequency index, whose knots are empirical percentiles, so zero "
  "on the axis is the pooled international average rather than the sample average. Predicted scores "
  "were flat at the bottom of the distribution (617 at \u22123.2, 610 at the 10th percentile) and fell "
  "steeply above it: 593 at the median, 558 at the 90th percentile, 526 at +1 and 500 at +1.6. Across "
  "the interdecile range the predicted score fell by 52 points, so the linear coefficient of \u221222 "
  "points understates the slope over the range in which most students sit."),

 ("Table 2 reports the decomposition",
  "Table 2 reports the decomposition. Use frequency was associated with more of both modes, more "
  "strongly with entertainment-oriented use (a\u2081 = 0.26) than with learning-oriented use "
  "(a\u2082 = 0.10). With both entered, entertainment-oriented use was associated with lower "
  "self-regulation (d\u2081 = \u22120.06) and learning-oriented use with higher (d\u2082 = 0.11), and "
  "self-regulation was worth 11.26 points per SD (b\u2083). The two serial pathways therefore ran in "
  "opposite directions: \u22120.19 points through entertainment-oriented use and +0.12 points through "
  "learning-oriented use."),

 ("Both pathways were statistically",
  "Both were significant and both were negligible. The direct part was \u221221.02 points (95% CI "
  "\u221223.18 to \u221218.85), or 95.1% of the total; all indirect parts together came to \u22121.09 "
  "points, or 4.9%: \u22120.58 through entertainment-oriented use alone, \u22120.48 through "
  "self-regulation alone, +0.04 through learning-oriented use alone, and \u22120.07 through the two "
  "serial pathways together, which is 0.3% of the total association. The mechanism the study set out "
  "to test accounts for roughly one three-hundredth of the association it was meant to explain."),

 ("Two details qualify the coefficients",
  "Two details qualify these coefficients. Learning-oriented use had no direct association with "
  "literacy once the other variables were entered (b\u2082 = 0.37, p = .73), so the positive serial "
  "pathway is carried entirely by self-regulation. And the coefficient for entertainment-oriented use "
  "depends on holding learning-oriented use constant: it was \u22120.03 (p = .013) in the single-path "
  "model against \u22120.06 here, while its zero-order correlation with self-regulation was only "
  "\u2212.04. Because the two modes correlate at .31, the larger dual-path estimate describes "
  "entertainment-oriented use at a given level of learning-oriented use, a narrower and less common "
  "condition."),

 ("BIC fell from 160,565",
  "BIC fell from 160,565 at two profiles to 134,268 at six without a clear minimum, and entropy was "
  "highest at three (.880). We report the four-profile solution because its entropy (.877) is close to "
  "the maximum, its smallest profile is still 14% of the weighted sample, and it separates the two "
  "high-use configurations that the composition argument is about (Table 3)."),

 ("The four profiles (Table 4)",
  "The four profiles (Table 4) were low-use (32.1%), learning-dominant (16.2%), entertainment-dominant "
  "(37.8%) and dual-high (14.0%). Mean scientific literacy ordered cleanly: 620.07, 601.95, 589.10 and "
  "582.55. Adjusted for covariates, learning-dominant students scored 13.73 points above the low-use "
  "group, entertainment-dominant students 12.61 points below it and dual-high students 21.67 points "
  "below it."),

 ("Self-regulation did not follow",
  "Self-regulation did not follow that ordering. Only the learning-dominant group differed from the "
  "low-use group (+0.18 SD); the entertainment-dominant and dual-high groups, whose literacy was 12.61 "
  "and 21.67 points lower, did not differ (both p > .29). The composition gradient in achievement "
  "therefore has no matching gradient in self-regulation, which is the clearest single indication that "
  "self-regulation is not doing the work the mediation model assigns to it."),

 ("Because the self-regulation index is a four-item",
  "Because the regulation index is a four-item help-seeking scale, the central result could in "
  "principle be an artefact of that operationalisation. It is not (Table 5): the direction of every "
  "path was the same under all three measures. With the goal-setting index, which measures the "
  "planning and monitoring processes the hypothesis is actually about, the entertainment\u2013"
  "regulation association was more than twice as large as with help seeking (d\u2081 = \u22120.15 "
  "against \u22120.06), as was the learning\u2013regulation association (0.20 against 0.11). A "
  "measure-specific artefact would look the opposite way: the theoretically better-matched scale "
  "produces the stronger first link."),

 ("The second link moved the other way",
  "The second link moved the other way. Regulation was worth 11.26 points per SD when indexed by help "
  "seeking, 7.98 by goal setting and 6.50 by cognitive adaptability, so the serial pathway through "
  "entertainment-oriented use was \u22120.30 against \u22120.19 points and its share 1.4% against "
  "0.8%. All indirect pathways came to 2.2% with goal setting and 2.5% with cognitive adaptability. "
  "The differences between these figures are not the point; their order of magnitude is: across three "
  "measures of one construct the mediated portion stays between 2% and 5%."),

 ("Table 6 reports the two continuous",
  "Table 6 reports the two continuous formulations. With use frequency held constant, learning and "
  "entertainment hours entered together produced a clear asymmetry: each SD of entertainment hours was "
  "associated with 4.62 fewer points (95% CI \u22126.67 to \u22122.56) at a given level of learning "
  "hours, whereas learning hours were not associated with literacy (0.55, 95% CI \u22121.54 to 2.64, "
  "p = .607). Written as total hours plus the entertainment share, the model gave \u22123.31 points "
  "per SD of total hours (95% CI \u22125.46 to \u22121.17) and \u22120.62 points per 10 percentage "
  "points toward entertainment (95% CI \u22121.47 to 0.23, p = .155)."),

 ("The two formulations disagree",
  "The two formulations disagree in appearance only. The share is a ratio of two collinear quantities, "
  "so its coefficient is estimated over a narrow band of variation and its interval is wide; the same "
  "model written as two hour scores separates the modes cleanly. Read together they say that "
  "composition matters through entertainment rather than through learning, while additional "
  "learning-oriented time is not associated with higher literacy in these data "
  "(b\u2082 = 0.37, p = .73; r = .01)."),

 ("This narrows the composition claim",
  "This narrows the composition claim as the introduction stated it. The data are consistent with a "
  "five-point gain from reallocating an SD of entertainment time to study, but do not establish it, "
  "because the learning coefficient is indistinguishable from zero and the share coefficient alone "
  "has an interval that includes no effect. What they establish is that the two modes are not "
  "interchangeable: one carries the whole negative association and the other carries no positive one."),

 ("The total association was negative in all four",
  "The total association was negative in all four systems, between \u221217.20 and \u221222.11 points "
  "per SD, and the design-based joint test did not reject equality (F(3, 80) = 2.27, p = .087). The "
  "direct part was equally stable (F(3, 80) = 0.75, p = .528). The regulation\u2013literacy "
  "association was positive everywhere but differed in size (11.26, 5.21, 11.37 and 11.12 points per "
  "SD; F(3, 80) = 3.89, p = .012), being weakest in Finland. Total and direct associations behave as a "
  "general account of device use and achievement would predict."),

 ("The composition paths did not behave that way",
  "The composition paths did not (Table 7). Entertainment-oriented use was negatively associated with "
  "literacy in the focal system (\u22122.24 points) but positively in Finland (+10.95), Korea (+5.18) "
  "and Hong Kong, China (+10.47); the joint test rejected equality (F(3, 80) = 22.91, p < .001). "
  "Learning-oriented use also varied, F(3, 80) = 10.46, p < .001, from \u22126.42 in Finland to +7.20 "
  "in Korea."),

 ("The indirect terms followed the same pattern",
  "The indirect terms followed the same pattern. The net indirect association was \u22121.09 points in "
  "the focal system and positive in the other three (+0.74, +1.96 and +1.34; F(3, 80) = 10.72, "
  "p < .001), so in three systems the mediated part ran opposite in sign to the total. The serial "
  "pathway through entertainment-oriented use was negative in three systems (\u22120.19, \u22120.05 "
  "and \u22120.22) and indistinguishable from zero in Hong Kong, China (+0.01), which is what the "
  "near-zero entertainment\u2013regulation association there implies."),

 ("Across the 23 economies",
  "Across the 23 economies (n = 167,180) the total association was \u221220.07 points per SD (95% CI "
  "\u221221.36 to \u221218.78), about 0.19 of the pooled within-economy SD; the direct part was "
  "\u221220.36 points (95% CI \u221221.65 to \u221219.07) and the net indirect part +0.29 points (95% "
  "CI \u22120.04 to +0.62, p = .084), about 1.5% of the total and opposite in sign to it. The two "
  "serial pathways were \u22120.09 and +0.08 points. At this scale the mediated portion is not "
  "distinguishable from zero and points the wrong way."),

 ("The pooled model assumes common slopes",
  "The pooled model assumes common slopes, which Table 7 rejects for the composition paths. It is "
  "reported because it answers a different question: the four-system comparison shows that the "
  "composition slopes are local, and the pooled model shows that, averaged over 23 systems with "
  "different slopes, the mediated portion stays near 1.5% and does not reach significance. Together "
  "they rule out a larger mediation effect hiding in the systems we did not examine separately."),

 ("The interaction between regulation",
  "The interaction between regulation and entertainment-oriented use was negative (b = \u22122.39, "
  "SE = 1.13, 95% CI \u22124.61 to \u22120.17, p = .035). At low entertainment use, one SD more "
  "regulation was associated with 13.64 more points (95% CI 10.42 to 16.86); at high entertainment "
  "use, 8.86 points (95% CI 5.53 to 12.19). The interval for the difference (4.78, 95% CI 0.34 to "
  "9.21) nearly includes zero, and the model omitted learning-oriented use, so we treat the "
  "interaction as a lead rather than an established moderator."),

 ("Table 9 re-estimated",
  "Table 9 re-estimates the model under eight alternative specifications. The two serial terms kept "
  "their signs throughout but moved in size: the entertainment pathway ranged from \u22120.32 to "
  "\u22120.12, and the two random halves of the sample produced \u22120.26 and \u22120.12; the "
  "learning pathway ranged from +0.03 to +0.14 and lost significance when entertainment hours were "
  "replaced by the entertainment share. The net indirect association ranged from \u22120.90 to "
  "\u22122.15 points. No specification produced an indirect share above about 10%, which is the "
  "property the argument rests on."),
]

if __name__ == "__main__":
    lines = load()
    for anchor, new_text in B2:
        i, j = find_block(lines, anchor)
        import json
        lines[i:j + 1] = ["para(doc, %s)" % json.dumps(new_text, ensure_ascii=True)]
    save(lines)
    print("replaced", len(B2), "blocks")
