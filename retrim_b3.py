# -*- coding: utf-8 -*-
"""retrim_b3.py — 第三批：讨论、局限、结论压缩（目标正文 ≤ 5,950 词）"""
import json, sys
sys.path.insert(0, ".")
from retrim import load, save, find_block

B3 = [
 # ---------------- 4.1
 ("The negative association between device-use",
  "The negative association between device-use frequency and scientific literacy was large, "
  "nonlinear and present in every system we examined, and it was almost entirely direct. Roughly 95% "
  "of it remained after the two modes of use and self-regulation were taken into account, and the "
  "serial pathways that motivated the study accounted for 0.3%. This is not a matter of statistical "
  "power: the pathways were estimated with confidence intervals that exclude zero. They are simply "
  "small relative to what they are meant to explain."),
 ("The shape of the association deserves",
  "The shape deserves as much attention as the size. The curve was flat at the bottom of the "
  "distribution and fell steeply across the range where most students sit, by 52 points between the "
  "10th and 90th percentiles of use, so the average linear slope understates the difference that a "
  "typical move within the distribution is associated with. Reporting one coefficient for a heavily "
  "skewed exposure misrepresents the relation for the majority of the sample."),
 # ---------------- 4.2
 ("Self-regulation was one of the sturdier",
  "Self-regulation was one of the sturdier correlates in the data. It correlated .20 with literacy, "
  "each SD was worth 5 to 11 points across the four systems and 11 in the focal one, and it was "
  "associated with how students used their devices: negatively with entertainment-oriented use and "
  "positively with learning-oriented use. What it did not do was carry the association, and the "
  "magnitude was bounded in advance by the product of its links. With a\u2081 = 0.26 and "
  "b\u2083 = 11.3, a one-SD shift in use moves regulation by 0.26 SD, which is worth about 2.9 "
  "points \u2014 an order of magnitude below the 22-point association, before any cancellation "
  "between the two modes is allowed for. Three further observations explain why the mediation claim "
  "fails even though each component path is significant."),
 ("First, the two composition paths",
  "First, the two composition paths have opposite signs and similar magnitudes, so they cancel "
  "(\u22120.19 and +0.12 points). This is a structural property of the model rather than an accident "
  "of this sample: any population in which entertainment use is negatively and learning use "
  "positively related to regulation will produce a near-zero net serial pathway whenever the two "
  "modes rise together with overall frequency, which is what a\u2081 = 0.26 and a\u2082 = 0.10 "
  "describe. Reporting the pathways separately, as mediation studies usually do, hides the "
  "cancellation; reporting their share of the total exposes it."),
 ("Second, the person-centred results",
  "Second, the person-centred results contradict the mediation model. If regulation were the "
  "mechanism, the groups whose literacy differed most should differ most in regulation. They did not: "
  "entertainment-dominant and dual-high students scored 12.61 and 21.67 points below the low-use "
  "group with regulation indistinguishable from it, and only the learning-dominant group, which also "
  "had the highest literacy, had higher regulation. That pattern is equally consistent with "
  "regulation and learning-oriented use both reflecting a third factor, such as academic engagement "
  "or prior attainment."),
 ("Third, the measure is a general disposition",
  "Third, the measure is a general disposition, not regulation during device use. The four items ask "
  "whether students seek help when they are stuck; they say nothing about what happens when a "
  "notification arrives during a science task, and the goal-setting items ask how often students plan "
  "their studying, not how they manage a device. The mismatch is not fatal for a correlational claim "
  "but is fatal for a mechanism claim, because the mechanism is specifically about the moment of use."),
 ("The measurement choice does not, however",
  "The measurement choice does not, however, explain the size of the result. If the small mediated "
  "portion were an artefact of a narrow help-seeking scale, a broader scale should have produced a "
  "larger one. It did not: with goal setting the first link more than doubled while the second fell "
  "(7.98 against 11.26 points) and the mediated share moved from 4.9% to 2.2%. The components of the "
  "mechanism are measurable and behave as the theory expects; what fails is their product relative to "
  "the association they are meant to carry."),
 # ---------------- 4.3
 ("The configurations of use ordered achievement",
  "The configurations ordered achievement more sharply than total use did. Students who used devices "
  "mainly for learning scored highest; those who used them heavily for both purposes scored lowest, "
  "21.67 points below the low-use group. Total frequency does not separate these groups and orders "
  "them the wrong way: the learning-dominant profile, which scored highest, had a mean frequency "
  "indistinguishable from the low-use profile (\u22121.07 against \u22121.09), while the dual-high "
  "profile, which scored lowest, had the highest frequency (\u22120.53). A single intensity measure "
  "would put learning-dominant students at the bottom. This is the strongest support in our data for "
  "treating composition as a substantive variable rather than a nuisance."),
 ("The person-centred and variable-centred results",
  "The two descriptions agree only partly, and the disagreement is instructive. Continuously, the "
  "association is carried entirely by entertainment-oriented time (\u22124.62 points per SD) while "
  "learning-oriented time is flat (0.55, p = .61), and the ratio between purposes has an interval "
  "that includes zero. The profiles separate two groups with similar totals: learning-dominant "
  "students reported 1.27 hours per setting and scored 620.07, entertainment-dominant students 1.46 "
  "hours and 589.10. A ratio treats a student who does a little of both as equivalent to one who "
  "does a little of one; the profiles show that they are not equivalent in achievement."),
 ("The support therefore has two limits",
  "The support has two limits. The composition effects that are estimated precisely are effects of "
  "one mode rather than of the balance between modes, and the composition-specific coefficients are "
  "unstable across systems. Composition appears to mark differences between students rather than to "
  "cause them: a student who uses a device mainly for study is also doing something else that raises "
  "science scores, and the device use is as much a symptom of that as a cause."),
 # ---------------- 4.4
 ("The reversal between systems",
  "The reversal between systems is the result we did not anticipate and the one with the clearest "
  "methodological implication. Two readings are possible and the data do not decide between them. "
  "The first is compositional confounding: where entertainment use is socially embedded and "
  "near-universal, the students who report most of it may be the more socially connected and engaged, "
  "so the same item indexes a different population of behaviours. The second is that the item set "
  "asks about time in three settings including school, so where devices are integrated into lessons, "
  "entertainment-oriented use at school may capture a different activity from what it captures where "
  "devices are banned in class. Both point the same way: invariance of composition effects should not "
  "be assumed, and single-system estimates of these paths are not general mechanisms."),
 ("The first is compositional confounding",
  ""),
 ("The stable elements are worth stating",
  "The stable elements are worth stating separately, because they are what a general account would "
  "have to explain. The total association was negative everywhere and of similar size, regulation was "
  "positively associated with literacy everywhere, and the entertainment\u2013regulation association "
  "was negative in three systems and near zero in the fourth. What varied was the link from "
  "composition to achievement."),
 # ---------------- 4.5
 ("For theory, the practical consequence",
  "For theory, the consequence is that self-regulation should stop being the default mediator in this "
  "literature. It is a robust correlate and a plausible outcome of device use; it is not a plausible "
  "conduit for the association with achievement, at least not when measured as a general disposition. "
  "Candidate alternatives that the design did not measure include displaced study time, shortened "
  "sleep (Hale & Guan, 2015), attentional residue in class (Uncapher & Wagner, 2018) and motivational "
  "crowding-out; any of them could carry the 95% that remained direct."),
 ("For reporting practice",
  "For reporting practice, mediation studies of digital media should report the indirect share "
  "alongside the significance of each path, as is routine in epidemiology (VanderWeele, 2016). Our "
  "own results would have looked successful under the usual convention: both serial pathways were "
  "significant at p < .001. The share makes the difference between a mechanism and a rounding error "
  "visible in one number."),
 ("For practice, the implications",
  "For practice, the implications are narrower than the mediation framing suggested. Because "
  "regulation carried almost none of the association, interventions that train planning and "
  "monitoring should not be expected to offset the academic correlates of heavy device use, however "
  "valuable they are otherwise. Because the achievement gradient across configurations had no "
  "matching gradient in regulation, and because the composition coefficients reversed across "
  "systems, we would not recommend that schools reallocate device time between purposes on the basis "
  "of these data. What the data support is descriptive: how students use devices distinguishes groups "
  "more sharply than how much they use them, and that distinction is worth measuring well."),
 # ---------------- 5 limitations
 ("The design is cross-sectional. Every estimate",
  "The design is cross-sectional. Every estimate is an association, temporal order is assumed rather "
  "than observed, and reverse causation is entirely plausible: students with weaker regulation may "
  "choose more entertainment, and students with stronger science skills may choose more "
  "learning-oriented use. The serial model is a convenient partition of covariance, not a causal "
  "chain, and the small size of the indirect terms is one reason to prefer the weaker reading."),
 ("All measures are self-reported",
  "All measures are self-reported. Use hours are coarse category midpoints, the frequency indices are "
  "self-assessed, and the same respondents supplied the mediator and the covariates, so common-method "
  "variance may inflate some associations. The two mode scores are hours per setting and cannot be "
  "summed into a day."),
 ("The cross-system comparison has two weaknesses",
  "The cross-system comparison has three weaknesses. The four samples are independent by design, so "
  "treating them as such is correct, but the joint tests inherit whatever the replicate weights miss "
  "about each system's sampling and do not estimate the small between-system covariance that a "
  "multilevel model would. The pooled 23-economy model assumes a common slope, which the "
  "heterogeneity tests reject for the composition paths, so we read it only as a statement about the "
  "net indirect association. And comparability of the regulation indices across systems rests on the "
  "scaling of the PISA questionnaire, which we did not re-test for measurement invariance; a "
  "system-level difference in how the help-seeking items function would affect the b\u2083 contrasts "
  "rather than the within-system shares on which our conclusions rest."),
 ("Two features of the measures",
  "Two features of the measures limit what can be concluded about composition. The share of time "
  "spent on entertainment is a ratio of two quantities that both enter the model, so its standard "
  "error is large by construction and a null result for the share is weaker evidence than the same "
  "null on a linear term would be. And both hour scores average three settings, so a student who uses "
  "a device for two hours at school and not at home is scored like a student who does the reverse."),
 ("The profile analysis is descriptive",
  "The profile analysis is descriptive. BIC did not reach a minimum, membership was assigned by most "
  "likely class without a three-step correction for classification error (Asparouhov & Muth\u00e9n, "
  "2014), the indicators are skewed and bounded, and the model was estimated without sampling "
  "weights. Profile contrasts describe groups; they are not effects of belonging to them."),
 ("Finally, the model omits school-level",
  "Finally, the models omit school- and classroom-level factors that plausibly shape both device use "
  "and science achievement, being confined to student-level covariates. The four systems are "
  "high-performing and cannot represent Chinese education as a whole, let alone other contexts; the "
  "23-economy model widens coverage but does not make the estimates representative of any particular "
  "system."),
 # ---------------- 6 conclusion
 ("In PISA 2025, students who used digital",
  "In PISA 2025, students who used digital devices more often scored lower in scientific literacy, by "
  "about 22 points per standard deviation, with the decline steepening across the range where most "
  "students sit. The association was stable across four education systems and across a pooled sample "
  "of 23. Regulation was consistently associated with higher literacy, but it carried almost none of "
  "the association: the two serial pathways through it accounted for 0.3% of the total, all indirect "
  "pathways for 4.9%, and the mediated share fell rather than rose when regulation was measured as "
  "planning and monitoring. Configurations of use ordered achievement more sharply than total use, "
  "yet the composition paths reversed sign between systems and the ratio between purposes was not "
  "reliably related to literacy at a fixed total. Regulation is a correlate of scientific literacy, "
  "not the channel through which device use relates to it, and the search for that channel should "
  "move to mechanisms measured at the moment of use."),
]

if __name__ == "__main__":
    lines = load()
    for anchor, new_text in B3:
        i, j = find_block(lines, anchor)
        if new_text == "":
            del lines[i:j + 1]
        else:
            lines[i:j + 1] = ["para(doc, %s)" % json.dumps(new_text, ensure_ascii=True)]
    save(lines)
    print("replaced", len(B3), "blocks")
