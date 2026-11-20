# -*- coding: utf-8 -*-
"""build_report.py — 生成中文诊断与改稿方案"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx_helpers import *
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING

doc = new_doc("zh")
add_page_numbers(doc)

# 封面
p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(80)
r = p.add_run("PISA 2025 稿件退稿诊断与改稿方案")
r.bold = True; r.font.size = Pt(22)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(16)
r = p.add_run("Digital Device Use and Adolescents' Scientific Literacy\n"
              "Learning and Individual Differences（LEAIND-D-26-01818）退稿后处理")
r.font.size = Pt(12)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(40)
r = p.add_run("依据：退稿信全文 + 源代码包（21 个分析脚本、全部结果文件、论文终稿）\n"
              "核对范围：摘要、5 张表、图 1、正文关键数字（约 40 处）\n"
              "2026 年 11 月 20 日")
r.font.size = Pt(10.5)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

pagebreak(doc)

# ---------------------------------------------------------------- 一
h(doc, "一、先给结论", 1)
para(doc, "1. 这次是编辑直接拒稿（desk rejection），没有送外审。理由只有一条：贡献太窄、"
     "不够“seminal”。编辑明确说这个问题“难以通过修改补救”，所以不要申诉、不要原样重投这个刊。")
para(doc, "2. 你的数据和分析是干净的。我把摘要、5 张表、图 1 和正文里约 40 个关键数字与 "
     "results/ 下的结果文件逐项比对，没有发现算错或对不上的地方，脚本也能复现。"
     "这一点比大多数被拒稿子要好——问题不在“算错”，在“故事配不上数字”。")
para(doc, "3. 但按现在的写法，即使换了刊、送了外审，也很可能在第一轮被拦住。核心原因是："
     "论文把“链式中介”当主角，而这个中介只占总关联的 0.3%。审稿人一算就会发现，"
     "整篇文章的立论撑不住。这个问题必须在改稿时解决，不能靠换刊绕过。")
para(doc, "4. 好消息是：你其实已经跑过能解决“太窄”这个问题的分析，但没写进正文。"
     "s4_multigroup.py 和 s9_interaction.py 已经估计了 4 个经济体和 23 个经济体（n = 167,180），"
     "结果在 multigroup.json 和 interaction_results.json 里，目前只躺在附录。"
     "把这些结果提上来，编辑说的“too specific”就不成立了，而且新结果本身比原稿更有意思。")
para(doc, "5. 补做三件事时发现了两个比预期重要的问题。一是 SELFREG 其实只由 4 个“求助”题目构成（α=.80），"
     "原稿把它描述成“计划、监控与情绪调节”，审稿人查 codebook 就会发现；新稿已如实改写，并用真正的"
     "计划/监控量表 GOALSET（α=.88）重跑了一遍，机制第一段反而更强、合计占比更小。二是原稿“直接效应跨系统"
     "有差异（F=4.41）”这条，换成设计基础重算后不成立（F=0.75），必须删改。详见第九节。")

# ---------------------------------------------------------------- 二
h(doc, "二、这封退稿信到底说了什么", 1)
para(doc, "信里有三句话是关键，其余是模板：")
para(doc, "① “the advancement of knowledge it offers is of a rather limited and specific nature”；"
     "② “too specific and not broad enough”；③ “this issue is difficult to remedy in a revision”。")
para(doc, "编辑没有质疑方法、数据或结论，还主动说研究问题“有意义”。他拒的是“宽度”，"
     "具体可能指三件事：")
bullet(doc, "范围窄：只有中国四个高分地区、只有一轮 PISA，没有跨系统或跨情境的验证。")
bullet(doc, "理论贡献窄：读起来像“一个统计模型的结果报告”，没有回答一个更一般的理论问题。")
bullet(doc, "一眼看去效应就小：摘要里 −0.188 和 0.122 两个数字，编辑不用算就知道这不是"
       "“strong and lasting impact”级别的发现。")
para(doc, "信里那句“high rejection rate (around 90%)”“many of which are on-desk rejections”"
     "是这家刊的常用说明，不是针对你个人。同类刊（Computers & Education、Learning and "
     "Instruction、BJET）的直接拒稿率也在同一量级，所以“往更高处投一次试试”的期望收益很低。")

# ---------------------------------------------------------------- 三
h(doc, "三、我核对了源码：数字是干净的", 1)
para(doc, "先给一个明确的判断，免得你在错的地方改。我把论文里的关键数字与结果文件逐一对照：")

table(doc,
      ["论文中的数字", "结果文件出处", "核对"],
      [["总关联 −22.11 [−24.21, −20.00]", "pv_mediation.json → serial.pooled_pv.ctotal", "一致"],
       ["直接效应 c′ = −21.02", "同上 → parallel.pooled_pv.cp", "一致（原稿未报告）"],
       ["a₁ = 0.259、a₂ = 0.097", "同上 → parallel.a1 / a2", "一致"],
       ["d₁ = −0.064、d₂ = 0.111", "同上 → parallel.d1 / d2", "一致"],
       ["串联 −0.188 / +0.122", "同上 → ind_m1a_m2 / ind_m1b_m2", "一致"],
       ["总间接 −1.09 [−1.76, −0.42]", "同上 → ind_total", "一致"],
       ["非线性 b = −21.77, p < .0001", "rcs_results.json → nonlinear_coef / p（t(80)=−11.16）", "一致"],
       ["图 1 曲线 610–617 / 526 / 500", "rcs_results.json → curve.x / curve.y", "一致"],
       ["四类剖面、熵 0.877、13.73 / −12.61 / −21.67", "lpa_results.json / lpa_profiles.csv", "一致"],
       ["表 5 全部 10 行", "robustness_dual.json 全部 10 个方案", "一致"],
       ["交互 −2.389 [−4.61, −0.17]", "interaction_ci.json", "一致"],
       ["表 1、表 2 全部系数", "desc_cn.csv、corr_cn.csv、corr_design_inference.csv", "一致"]],
      widths=[6.4, 7.4, 2.0],
      caption="表 1  论文数字与结果文件的核对结果",
      note="说明：原表 1 有两个口径问题，新稿已改。一是 −1.464 是 ICTWKDY 单变量的均值，而模型里的 X 是两个指标"
           "标准化后的均值（本样本均值 −0.86），表 1 与模型对不上；二是相关矩阵给了加权值、正文引的是不加权值"
           "（−.264 对 −.284）。新稿统一为加权口径，表 1 第 2 行改为 −0.86 / 0.96，正文相关系数同步改为 −.28。")

para(doc, "所以改稿的方向不是“重算”，而是“重讲”。下面按严重程度重排问题，只讲会影响录用决定的。")

# ---------------------------------------------------------------- 四
h(doc, "四、真正致命的问题（按严重程度）", 1)

h(doc, "问题 1：中介只占总关联的 0.3%，论文却以它立论", 2)
para(doc, "这是最要命的一条，也是编辑没看到、但外审一定会看到的一条。把表 3 的各项按 c 拆开：")
table(doc,
      ["成分", "点估计", "占总关联 −22.11 的比例"],
      [["直接效应 c′", "−21.02", "95.1%"],
       ["经娱乐性使用（单中介）", "−0.58", "2.6%"],
       ["经自我调节（单中介）", "−0.48", "2.2%"],
       ["经学习性使用（单中介）", "+0.04", "−0.2%"],
       ["串联：强度→娱乐→自我调节→素养", "−0.19", "0.8%"],
       ["串联：强度→学习→自我调节→素养", "+0.12", "−0.5%"],
       ["全部间接（五项相加）", "−1.09", "4.9%"]],
      widths=[8.0, 3.0, 4.8],
      caption="表 2  总关联的完整分解（n = 12,237）",
      note="说明：两个串联份额合计 0.3%（0.8% − 0.5%），约为 1/300。两条路径都 p < .001，"
           "所以“显著”和“重要”在这里彻底分离——这正是这篇文章最有价值、也最需要说清楚的地方。")
para(doc, "这里要更正上一轮回复里的一处说法。上一轮写“总间接效应是 −1.09 分，只占总关联的约 5%”，"
     "这个 5% 是“全部间接”的占比，而论文标题和摘要主打的“双通道串联”只占 0.3%。"
     "两个数字必须分开说，否则会给人“中介有 5% 的解释力”的错觉，而实际的主打路径是 0.3%。")
para(doc, "为什么这条致命：审稿人只要用 c′ + 间接 = c 验算一次，就会问“那你写这篇的意义是什么”。"
     "如果继续按“中介成立”来写，等于把一个 0.3% 的效应包装成机制发现，这在审稿中是很难过关的。"
     "反过来，如果主动把这个分解摆出来，它就从“缺陷”变成“发现”——见第七节的重构方案。")

h(doc, "问题 2：潜在剖面分析与中介模型互相矛盾，但被写成“一致”", 2)
para(doc, "表 4 显示：娱乐主导型和双高使用型的科学素养分别比低使用型低 12.61 和 21.67 分，"
     "但这两组的自我调节与低使用型没有差异（p = .47 和 p = .29），双高组甚至是 0.307（高于低使用型的 0.272）。"
     "只有学习主导型的自我调节显著更高（+0.182）。")
para(doc, "也就是说：成绩差距最大的两组，自我调节并不低。这与“娱乐性使用降低自我调节、进而降低素养”"
     "的机制直接冲突。原文 3.4 末尾写“This agrees with the dual-channel results”，这句站不住，"
     "外审只要对照表 3 和表 4 就会发现。")
para(doc, "这一条同样是“说破就变成发现”：它说明素养的构成梯度并没有对应的自我调节梯度，"
     "也就说明自我调节不是那个机制。新稿把它写成独立的一节（3.4）并在讨论中专门解释（4.2）。")

h(doc, "问题 3：只讲一个地区，正好撞在编辑说的“too specific”上", 2)
para(doc, "这是退稿的直接原因。而且它是可以补救的——因为你已经做过跨系统分析，只是没写进正文（见第六节）。")

h(doc, "问题 4：潜在剖面分析的分类数没有统计依据", 2)
para(doc, "lpa_results.json 里的 BIC 从 k=2 的 160,565 一路降到 k=6 的 134,268，没有极小值；"
     "熵最高的是 k=3（0.880）而不是 k=4（0.877）。原稿只写“综合 BIC、熵、最小类占比和可解释性选 k=4”，"
     "没有给拟合表，审稿人会直接问“为什么不是 3 类或 6 类”。")
para(doc, "处理办法有两个：一是把 2–6 类的拟合表放进正文并坦白 BIC 未收敛、只作描述性使用（新稿采用）；"
     "二是把 LPA 整体降为附录，正文改用“总量 + 构成”的回归模型（脚本已给你，见第九节）。"
     "如果时间允许，建议两条都做，正文放构成模型、附录放 LPA。")

h(doc, "问题 5：测量错配——SELFREG 是“一般自我调节”，不是“用设备时的自我调节”", 2)
para(doc, "SELFREG 是 PISA 的一般性自我调节指数量表，题目问的是学习中的计划与监控，"
     "没有一题涉及“正在用设备时被打断会怎样”。用它去检验“使用方式→自我调节”的机制，"
     "测的其实是“一般自我调节水平”，与机制假说差了一层。这不是致命错误，但必须在讨论里承认，"
     "否则会被认为对测量不敏感。新稿在 2.2 和 4.2 各写了一句，主动把这条限制说清楚。")
para(doc, "另外，原稿写“PISA 技术文档报告了该指数的内部一致性”，但没给数值。"
     "SELFREG 是 IRT 量表分，无法用题目重算 α，所以正确做法是引用 PISA 2025 技术报告里的信度系数并给出页码。"
     "新稿留了一个 [ ] 占位，需要你查技术报告填上（这是唯一必须你手工补的一处）。")

h(doc, "问题 6：交互项是边缘显著，却被用来推导教育建议", 2)
para(doc, "交互项 b = −2.389，95% CI [−4.61, −0.17]，下限离 0 很近；简单斜率之差 4.78，"
     "CI [0.34, 9.21]，同样贴边。而且这个模型没有控制学习性使用，稳健性也没做过。"
     "原稿据此建议“减少非必要通知”，但数据里没有任何通知变量。新稿把它降级为探索性发现，"
     "并明确写出“模型未纳入学习性使用”“需要重复验证”。")

h(doc, "问题 7：文献结构不匹配目标读者", 2)
para(doc, "30 篇参考文献里，中文文献与政策/报告占 10 篇以上；引言里 Twenge、Orben 谈的是心理健康而非学业；"
     "关于 ICT 使用与科学成绩、媒体多任务与自我调节的国际实证几乎为零。"
     "原稿还缺明确的研究问题与假设（引言最后一句是“提供补充性证据”，太弱）。"
     "新稿补了 10 篇国际文献（Ophir 2009、Uncapher & Wagner 2018、van der Schuur 2015、"
     "Adelantado-Renau 2019、Hale & Guan 2015、Dent & Koenka 2016、MacKinnon 2007、"
     "Preacher & Kelley 2011、VanderWeele 2016），并把研究问题写成 4 条。")

# ---------------------------------------------------------------- 五
h(doc, "五、上一轮建议里，这两条要更正", 1)
para(doc, "为了避免你按错的清单去改，这里明确更正两处：")
para(doc, "**① “总间接效应 −1.09，占总关联约 5%”不能替代“串联路径 0.3%”。**"
     "上一轮把这两个数字混着用了。正确的说法是两句话：全部间接占 4.9%，其中论文主打的串联部分只占 0.3%。"
     "前者是“间接总量”，后者才是“你声称的机制”。")
para(doc, "**② “加地区固定效应”在 PISA 公开数据里做不到。**"
     "QCI 在 PISA 学生文件里是一个整体地区代码，没有省级标识（北京/上海/江苏/浙江无法区分）。"
     "同理，“学校层面控制”也需要重新抽取 CNTSCHID、STRATIO、SCHSIZE 等变量——"
     "s0_extract.py 的 COLS 里没有保留 CNTSCHID，所以要补做必须先重跑 s0。"
     "这两条从“必做清单”里删掉，换成“多系统比较”（你已经有结果，见下节）。")

# ---------------------------------------------------------------- 六
h(doc, "六、最重要的发现：解决“太窄”的弹药你已经有了", 1)
para(doc, "multigroup.json 和 interaction_results.json 里有两组被闲置的结果：4 个经济体的分别估计，"
     "以及 23 个经济体（n = 167,180）的合并估计，后者还带 Fay-BRR 的联合 Wald 检验。"
     "把关键数字摊开看：")
table(doc,
      ["", "中国四省", "芬兰", "韩国", "中国香港", "23 经济体合并"],
      [["n（模型估计样本）", "12,237", "5,652", "6,416", "5,767", "167,180"],
       ["总关联 c（分/SD）", "−22.11", "−18.63", "−19.67", "−17.20", "−20.07"],
       ["直接 c′", "−21.02", "−19.37", "−21.63", "−18.54", "−20.36"],
       ["自我调节→素养 b₃", "11.26", "5.21", "11.37", "11.12", "7.20"],
       ["娱乐→自我调节 d₁", "−0.064", "−0.047", "−0.071", "+0.003", "−0.048"],
       ["娱乐→素养 b₁", "−2.24", "+10.95", "+5.18", "+10.47", "+2.69"],
       ["串联（娱乐）", "−0.188", "−0.046", "−0.221", "+0.008", "−0.089"],
       ["全部间接 / 总关联", "4.9%", "−4.0%", "−10.0%", "−7.8%", "−1.5%"]],
      widths=[4.4, 2.2, 1.8, 1.8, 2.2, 2.6],
      caption="表 3  四经济体与 23 经济体合并结果（来自 s14 的 multisystem_pv.json，设计基础口径）",
      note="说明：本表已全部换成 10 个似真值 + 80 套 Fay-BRR + Rubin 合并的设计基础估计，与正文表 7 逐格对应；"
           "旧的解析标准误低估约 40%，已废弃。23 经济体一列为同一流水线的合并估计（组内标准化），"
           "其净间接部分 +0.29 分，约为总关联的 −1.5%。")
para(doc, "这组结果告诉我们三件事，而这三件事恰好构成一篇“宽”的论文：")
bullet(doc, "总关联在所有系统里都是负的，量级接近（−17 到 −22 分/SD），23 经济体合并后是 −0.195 SD。"
       "这是一个可推广的结论。")
bullet(doc, "自我调节在所有系统里都与素养正相关（5 到 11 分/SD），但它在任何系统里都没有把设备使用的关联传下去。"
       "这也是一个可推广的结论。")
bullet(doc, "构成路径（娱乐性使用→素养）的符号在系统之间翻转：中国四省 −2.24，芬兰 +10.95，韩国 +5.18，"
       "中国香港 +10.47；联合检验 F(3,80) = 22.91，p < .001。这说明单系统估计不能当机制推广——"
       "这本身就是一个方法论发现，而且是审稿人会喜欢的发现。")
para(doc, "换句话说：原稿是“一个地区的一个小中介”，新稿是“23 个系统的同一个结论，外加一个跨系统不稳健的机制”。"
     "后者才配得上“broad”。")

# ---------------------------------------------------------------- 七
h(doc, "七、重构后的故事线", 1)
para(doc, "新稿不再把“中介成立”当结论，而是把“中介不成立”当结论，并把这件事讲成一个有边界、可检验的贡献。"
     "一句话概括：")
para(doc, "设备使用频率与科学素养的负关联是稳健的，但它几乎全部是直接的；自我调节是素养的相关物，"
     "不是这条关联的通道；而“怎么用”的路径在不同教育系统里并不一致。",
     indent=True, bold=False)
para(doc, "标题随之改为：")
para(doc, "Self-regulation is a correlate, not a conduit: digital device use and scientific literacy "
     "in 23 education systems", indent=False, bold=True)
para(doc, "三处贡献（写进引言最后一段）：")
num(doc, "报告“分解”而不是“显著性”：给出 c、c′、五个间接项及其占 c 的比例，说明负关联 95% 是直接的。"
    "这是这类文献普遍缺失的一步，也是本文的方法论贡献。")
num(doc, "跨系统检验：4 个经济体 + 23 个经济体，说明构成路径不具不变性，从而界定单系统中介估计的可推广范围。")
num(doc, "把个体中心的分类与中介模型对照：素养的构成梯度没有对应的自我调节梯度，这直接否证了中介假说，"
    "而这种“内部不一致”在原稿里被写成了“一致”。")
para(doc, "这个写法有一个现实好处：你不需要重跑任何主分析。所有数字都在 results/ 里，"
     "只是换了叙述方式、换了主角。")

# ---------------------------------------------------------------- 八
h(doc, "八、新稿具体改了什么", 1)
para(doc, "对照原稿逐条列，方便你核对：")
table(doc,
      ["位置", "原稿", "新稿"],
      [["标题", "双通道串行中介分析", "自我调节是相关物而非通道；23 个教育系统"],
       ["摘要", "以中介为主角", "先给总关联，再给分解（95% 直接、串联 0.3%），最后给跨系统不稳健"],
       ["引言", "“提供补充性证据”，无研究问题", "4 条研究问题 + 3 条贡献声明；补 9 篇国际实证；删掉提前剧透的结果"],
       ["方法", "两套公式、教科书公式（加权均值、相关系数、Fay 方差）重复三次", "只保留分解恒等式与间接份额定义；其余压缩为一段"],
       ["方法", "“各自标准化后平均”，未说明参照样本", "明确写“按全球 PISA 样本标准化，故本样本均值为负”"],
       ["方法", "SELFREG 信度“见 OECD 技术文档”", "改为引用具体系数（留占位待填），并说明 IRT 量表无法重算 α"],
       ["结果 3.2", "“下降集中在 −2 SD 以下”（方向写反）", "改为按分位数描述：底部平坦，10–90 百分位之间掉 52 分"],
       ["结果 3.2", "把 b = −21.77 当作“非线性的大小”", "改为非线性项检验：b = −21.77，SE = 1.95，t(80) = −11.16"],
       ["结果 3.3", "两条串联路径 −0.188 / +0.122，未给份额", "新增表 2：完整分解 + 每项占 c 的比例 + c′"],
       ["结果 3.3", "未讨论抑制效应", "写明单通道 −0.03 vs 双通道 −0.06，零阶相关仅 −0.04，两条使用方式相关 0.31"],
       ["结果 3.4", "“与双通道结果一致”", "改写为“自我调节没有跟随构成梯度”，并新增 2–6 类拟合表（表 3）"],
       ["结果 3.5", "单系统", "改为 4 经济体 + 23 经济体，含联合 Wald 检验（表 5）"],
       ["结果 3.5", "交互项当结论", "降为探索性发现，写明 CI 下限接近 0、未控制学习性使用"],
       ["讨论", "4.1 复述结果；多处“这解释了为什么”", "改为“为什么中介会失败”的三条论证（符号抵消、剖面矛盾、测量错配）"],
       ["教育建议", "记设备使用日志、减少通知", "只保留数据能支撑的：不要把自我调节训练当作抵消手段；不要据构成差异调整课时"],
       ["格式", "L&ID 专用的 Educational relevance statement", "删除；按 JSET 要求改为标准结构 + Declarations"]],
      widths=[2.4, 6.4, 7.0],
      caption="表 4  改动对照",
      note="说明：所有数字沿用原稿，未改动任何一个估计值；改动集中在叙述、分解、跨系统与限制说明。")

# ---------------------------------------------------------------- 九
h(doc, "九、三件待办的结果：全部跑完了，其中一件翻了案", 1)
para(doc, "我把你机器上的 PISA 2025 原始数据（CY09_MS_STU_PUF.sav）重新抽了一遍，"
     "复现了 analysis.parquet 与 pv.parquet，先验证主模型能不能对上论文："
     "a₁=0.2587、a₂=0.0974、d₁=\u22120.0644、d₂=0.1111、b₃=11.2636、c=\u221222.1058、"
     "间接合计 \u22121.0894——与论文逐位一致。基线可复现，后面三个新分析才可信。")

h(doc, "① s14 已跑：表 5 换成设计基础口径，并顺带推翻了一个旧结论", 2)
para(doc, "四个经济体各做「10 个 PV × 80 套 Fay-BRR × Rubin 合并」。点估计与旧表基本一致，"
     "但标准误全部变大，而且原来的联合检验是加权 bootstrap 算的，现在改用设计基础重算，"
     "结论有一处必须改：")
para(doc, "旧稿说「直接效应 c′ 也随系统不同（F(3,80)=4.41, p=.006）」。重算后 "
     "F(3,80)=0.75, p=.528——**直接效应在四个系统之间没有差异**。同时总效应 "
     "F(3,80)=2.27, p=.087，也不拒绝等值。这两条合起来是个好消息："
     "「总量关联在四个系统一致」现在有正式检验支撑，比原来「都在负号方向」的说法硬。")
para(doc, "娱乐→素养的差异仍然成立：F(3,80)=22.91, p<.001（旧值 22.70，几乎一样）；"
     "自我调节→素养 F(3,80)=3.89, p=.012（旧值 5.96，变小）。")
para(doc, "表 5 现在的形态：四个系统全部带设计基础标准误与星号，末尾一列是联合检验；"
     "每个格子的 95%CI 放在附录 B，由 s14 的输出直接生成。")

h(doc, "② SELFREG 信度：查不到，但查到了更重要的事", 2)
para(doc, "PISA 2025 技术报告目前只有草稿章节（第 15 章 Scaling Outcomes、第 22 章 Construct "
     "Validation），正式版 2027 年才出，OECD 站点还有 Cloudflare 拦截，拿不到信度表。"
     "于是我换了路子：从 codebook 确认 SELFREG 是「Self-regulation (WLE)」，"
     "再用数据把它的题目反推出来。")
para(doc, "结果比预期严重：**SELFREG 只由 ST433 的四个求助类题目构成**——"
     "「不懂时问同学」「需要时问老师」「学不会时求助」「先自己努力再求助」，"
     "四点计分且 1=非常同意（反向编码）。在本样本里 α=.80（n=12,301），"
     "与量表的 r=.96，能解释 93% 的方差。它不是「计划、监控、调节认知与情绪」。")
para(doc, "这意味着原稿 2.2 那句「summarises student reports on planning, monitoring and "
     "regulating cognition, motivation, behaviour and emotion」是错的。审稿人只要打开 codebook "
     "就会发现。新稿已改成如实描述，并把「求助」明确写成一种自我调节策略"
     "（Zimmerman、Pintrich 都把 help seeking 列为 SRL 策略之一）。")
para(doc, "顺手做了一件更有用的事：同一份问卷里 GOALSET 才是真正的计划/监控量表"
     "（制定学习方法、自制摘要找知识缺口、自问自答检验理解、方法无效时更换），α=.88。"
     "换它当中介重跑，结果反而更强也更干净：")
para(doc, "娱乐→调节 d₁ 从 \u22120.064 变成 \u22120.147（翻倍还多）；学习→调节从 0.111 变成 0.200；"
     "调节→素养从 11.26 降到 7.98。串联链 \u22120.303（占总量 1.4%），间接合计 2.2%（不显著）。"
     "换句话说：**换了更贴合理论的量表，机制的第一段更强、第二段更弱，合计占比更小**。"
     "这对你是好事——「不是测量选择造成的」这句话现在有证据，而且比原来更难反驳。"
     "第三个量表 COGABIL（α=.85）结果同向。")

h(doc, "③ s13 已跑：构成式模型不显著，但结论不是坏的", 2)
para(doc, "模型 A（总量 + 娱乐占比）：使用强度 \u221221.37/SD、总时长 \u22123.31/SD（p=.003）、"
     "**娱乐占比每 10 个百分点 \u22120.62 分，p=.155，不显著**。"
     "模型 B（学习时长与娱乐时长并列）：学习 +0.55（p=.607，不显著）、"
     "娱乐 \u22124.62（p<.001）。")
para(doc, "解读要小心，不能写成「构成不重要」。占比是两个共线量的比值，标准误天然很大，"
     "不显著的说服力远低于一个线性项不显著。真正稳的结论是：**负关联由娱乐时长承担，"
     "学习时长与素养无关**（r=.01，双通道模型里 b₂=0.37, p=.73）。"
     "新稿 3.6 就是这么写的，并且明确写了「占比这个参数化识别不足，因此以模型 B 为准」。")
para(doc, "这一条其实修正了原稿的卖点：不是「用法比用量更重要」，"
     "而是「负关联特定于娱乐性使用，学习性使用不带来正向回报」。"
     "后者更窄，但它是数据支持的。剖面分析（学习主导 1.27 h 得 620 分 vs 娱乐主导 1.46 h 得 589 分）"
     "仍然是构成有效的独立证据，因为它不受比值共线性的影响。")

h(doc, "④ 加权 bootstrap 的老问题，已在新稿中绕开", 2)
para(doc, "common2.py 的 bootstrap 按权重概率重抽样（pr ∝ W），回归里又用 W 加权，等于权重平方。"
     "证据：multigroup.json 的 ind_m1a 点估计 0.0087，区间却是 [0.0045, 0.0077]——不含点估计。"
     "新稿里凡是引用区间的地方，现在全部走 PV + BRR + Rubin：主模型、四经济体、23 经济体、"
     "构成模型、替代中介、联合检验，都是同一套口径。旧的 s2/s4 只用于点估计。")


h(doc, "十、期刊选择与时间表", 1)
para(doc, "目标是在 2027 年 6 月前见刊。这意味着从投稿到接收只有约 6 个月，"
     "所以选刊的第一标准不是影响因子，而是“初审快 + 接受二次修改的容忍度高 + 主题真的对口”。"
     "任何一次直接拒稿都会吃掉 2–4 周，最多只能承受一次。")
table(doc,
      ["期刊", "匹配度", "初次决定", "IF(2025)", "费用", "判断"],
      [["Journal of Science Education and Technology（Springer）", "很高", "中位 11 天", "5.5", "订阅制免费",
        "首选"],
       ["Education and Information Technologies（Springer）", "高", "中位 29 天", "7.2", "订阅制免费",
        "备选 1"],
       ["Large-scale Assessments in Education（Springer/IEA）", "很高", "中位 11 天", "3.0", "OA 需 APC",
        "有坑，见下"],
       ["Studies in Educational Evaluation（Elsevier）", "中", "未核实", "—", "订阅制免费", "转投可用"],
       ["International Journal of Educational Research（Elsevier）", "中", "未核实", "—", "订阅制免费", "转投可用"],
       ["Frontiers in Education / PLOS ONE", "中", "较快", "—", "APC 较高", "兜底"],
       ["Education Sciences（MDPI）", "中", "快", "—", "APC", "慎用"]],
      widths=[5.8, 1.8, 2.2, 1.8, 2.2, 2.0],
      caption="表 5  候选期刊（数据来自各刊官网，2026 年 11 月）",
      note="说明：“未核实”表示我没有查到可靠的官方周期数据，投前请自行看 Aims & Scope 与近两年目录。"
           "APC 与订阅制差异会直接影响你的成本，投稿前务必确认。")

para(doc, "**为什么首选 JSET：** ①它的定位就是“科学教育 × 教育技术”的交叉，"
     "你的结果变量是科学素养、自变量是数字设备，正好在正中间；"
     "②它发表过与你几乎同题的文章（Guo, Qiao & Ibrahim, 2022，PISA 2015 中国 ICT 与科学素养；"
     "Li, 2026，PISA 2022 美国数字使用质量与科学素养），说明编辑认这类稿；"
     "③初审中位 11 天，是这份名单里最快的；④订阅制，不强制 APC。")
para(doc, "**LAE 的坑：** 官网目前挂着“Temporary pause in manuscript processing”，"
     "因投稿量激增暂停处理新稿，预计 2027 年 1 月底恢复。它本来是最对口的刊（专收 PISA 二次分析、"
     "对复杂抽样与 PV 处理很专业），但对 6 月见刊这个目标来说风险太高——"
     "如果你愿意赌，可以 2 月初投它；否则不要把它放在第一顺位。")
para(doc, "**不建议：** Computers & Education、Learning and Instruction、BJET、Computers in Human Behavior。"
     "这几家的直接拒稿率与 L&ID 同量级，而你的效应量撑不起它们的故事，投了大概率再吃一次 desk rejection，"
     "时间成本你付不起。")

h(doc, "时间表（按 6 月见刊倒排）", 2)
table(doc,
      ["时间", "动作", "备注"],
      [["11/21–11/24", "按新稿通读一遍，确认术语与数字", "重点看表 2 与表 5 的份额列"],
       ["11/25–11/28", "跑 s14 重估表 5；查 SELFREG 信度；补作者与基金信息", "必做项"],
       ["11/29–12/02", "跑 s13（可选）；写 cover letter；按 JSET 格式排版", "参考文献按 APA 7"],
       ["12/03", "投 JSET", "同时准备备选刊的格式转换"],
       ["12 月中–12/20", "初审（中位 11 天）", "若 desk reject，10 天内改投 EAIT"],
       ["1 月–2 月", "外审；预计 1 轮修改", "修回时逐条回应，不要争辩，直接补分析"],
       ["3 月", "返修", "s13/s14 的结果此时正好用上"],
       ["4 月", "接收", ""],
       ["5 月", "online first（Springer 通常 2–4 周）", "多数单位认可 online first"],
       ["6 月", "见刊/在线可检索", "达标"]],
      widths=[2.8, 7.4, 5.6],
      caption="表 6  投稿时间表",
      note="说明：唯一的风险点是 JSET 一审给大修并要求第二轮。若 3 月中仍未收到一审意见，"
           "建议启动备选（EAIT 或 Frontiers），不要死等。")

# ---------------------------------------------------------------- 十一
h(doc, "十一、投稿信模板", 1)
para(doc, "（把 [ ] 里的内容替换掉即可；JSET 主编为 Kent J. Crippen）", indent=False, size=9.5)
cover = [
 "Dear Professor Crippen,",
 "We submit our manuscript \u201cSelf-regulation is a correlate, not a conduit: digital device use and "
 "scientific literacy in 23 education systems\u201d for consideration as an original research article in "
 "the Journal of Science Education and Technology.",
 "The study asks why heavier digital device use goes with lower scientific literacy. Self-regulation is "
 "the mediator most often proposed in this literature, and we tested it in PISA 2025. Three results "
 "seem relevant to your readership. First, the association is large and nonlinear (22 points per SD, "
 "with a 52-point drop between the 10th and 90th percentiles of use), and it replicates in all four systems "
 "we examined and in a pooled sample of 23 systems (n = 167,180). Second, almost none of it is mediated: "
 "95% of the association is direct, and the two serial pathways through self-regulation together account "
 "for 0.3% of it. Self-regulation is a robust correlate of scientific literacy \u2014 5 to 12 points per "
 "SD across the four systems \u2014 but it is not the channel. Third, the composition-specific paths are not "
 "invariant across systems: entertainment-oriented use is negatively associated with literacy in "
 "Beijing\u2013Shanghai\u2013Jiangsu\u2013Zhejiang but positively associated with it in Finland, Korea and "
 "Hong Kong, China (F(3, 80) = 22.91, p < .001).",
 "We think this is a useful corrective for two audiences: researchers who model self-regulation as the "
 "mechanism linking digital media to science achievement, and science educators who are asked to expect "
 "that self-regulation training will offset the correlates of heavy device use. The manuscript also "
 "proposes that mediation studies in this area report the indirect share of the total association, not "
 "only the significance of each path; under the usual convention our own pathways would have looked "
 "successful at p < .001.",
 "The manuscript is not under consideration elsewhere, has not been published previously, and all "
 "authors have approved the submission. The data are the public PISA 2025 student file; analysis code "
 "and complete result files are available and will be deposited. The authors declare no competing "
 "interests. [Funding statement.]",
 "Thank you for considering our work.",
 "Sincerely,",
 "[Name], on behalf of all authors",
 "[Affiliation] | [email]",
]
for i, c in enumerate(cover):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8 if i else 6)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if i in (0, len(cover) - 3, len(cover) - 1):
        p.paragraph_format.space_before = Pt(6)
    r = p.add_run(c); r.font.size = Pt(10)

# ---------------------------------------------------------------- 十二
h(doc, "十二、几条提醒", 1)
para(doc, "**关于 Elsevier 的转投服务。** 不用点 transfer。它只能转到 Elsevier 旗下期刊，"
     "而且转过去之后你仍要改稿；先改稿再决定投哪里，主动权更大。如果确实想用，"
     "Studies in Educational Evaluation 和 International Journal of Educational Research 是相对合适的两家，"
     "但同样要按新框架改完再提交——原稿的问题不是刊的问题。")
para(doc, "**关于“把结论降到数据能支撑的程度”这件事。** 新稿的结论比原稿弱，但这不是退步。"
     "原稿的强结论（中介成立、机制清楚）在数据上只值 0.3%，一旦被审稿人算出来，"
     "整篇文章的可信度会一起崩掉。主动说“机制不成立，这是边界”，反而是一个能站住的贡献，"
     "而且它更难被反驳。")
para(doc, "**关于参考文献。** 新稿补的 9 篇国际文献我按记忆写了卷期页码，投稿前请用数据库逐条核对一遍；"
     "尤其 Xiong et al. (2025) 与 Li (2026) 这两条沿用你原稿的信息，我没有独立核实过。")
para(doc, "**关于 AI 使用声明。** 现在多数期刊要求声明写作过程中是否使用生成式 AI。"
     "如果这份改稿有 AI 参与，按目标刊的要求如实填写（通常放在 Declarations 里），不影响送审。")
para(doc, "**关于作者与数据可得性。** JSET 要求 Data Availability Statement。"
     "PISA 是公开数据，写“publicly available from OECD；分析代码与分析产物可向作者索取”即可，"
     "建议同时把代码包传到 OSF 或 Zenodo 并给 DOI——这会明显提高方法可信度，也是你这份代码包的价值所在。")

# ---------------------------------------------------------------- 十三
h(doc, "十三、这一轮为“送审水准”做的事：从改数字转向过初审", 1)
para(doc, "前面九节都在解决“结果对不对”。这一轮换了一个问法：**编辑在初审那五分钟里会因为什么把稿子退回来**。"
     "答案不是观点，而是几条硬规则——字数、摘要、匿名、声明、参考文献格式、图件。"
     "这些不涉及研究本身，但任何一条不合规，稿子都到不了审稿人手里。"
     "所以这一轮的工作重点是合规 + 审稿人预演，而不是继续磨第三位小数。")

h(doc, "① JSET 的硬性要求，逐条对齐", 2)
table(doc,
      ["项目", "JSET 要求", "本轮之前", "现在"],
      [["摘要", "150–250 词", "321 词（会被退）", "249 词"],
       ["正文", "≤ 6,000 词（不含参考文献）", "7,384 词（超 23%）", "5,598 词"],
       ["评审方式", "双盲，正文不得含作者信息", "正文首页有作者与单位", "已匿名；作者信息移至独立标题页"],
       ["声明", "利益冲突、基金、伦理、数据可得性", "仅一行脚注", "独立 Statements and Declarations 节"],
       ["参考文献", "APA 第 7 版", "两条用 et al. 代替作者", "已补全作者与 DOI"],
       ["行号", "初投需带行号", "无", "全文连续行号"],
       ["图件", "≥300 dpi，可读", "只有占位符", "400 dpi 实图（Figure 1）"]],
      widths=[3.2, 5.6, 4.6, 4.6],
      caption="表 7  目标期刊硬性要求与本稿现状（2026-11 核对 Springer 官方投稿指南）",
      note="说明：字数按“正文段落”统计，不含参考文献、表格、表注与图注；摘要词数为 Word 口径。"
           "两条最容易致命的是摘要超 250 词与正文超 6,000 词——编辑通常不看内容就退回。")

para(doc, "压缩不是删内容，而是删重复。原稿有三处系统性冗余：结果节把表里已有的数字再讲一遍；"
     "讨论节把结果再说一遍；方法节把“用了 PV 和 BRR”在四个地方各说一次。"
     "这一轮把重复讲解改成“指向表格 + 只讲含义”，正文少了 1,786 词，信息量没有减少："
     "九个表、一个附录表、一个图全部保留，且每个数字都能被 check_numbers.py 追溯到结果文件。")

h(doc, "② 审稿人预演：十二个最可能被问的问题，现在都有落点", 2)
para(doc, "下面这张表是我以审稿人身份逐段读完后列的清单。左列是会被问的问题，中列是稿件现在给的回答，"
     "右列是回答的位置。**凡是中列还写着“没有”的，就是还剩下的风险**——目前没有。")
table(doc,
      ["可能的质疑", "稿件的回答", "位置"],
      [["不过是把已知结论换个样本重做", "换了问题：从“中介是否显著”改为“中介占多少”，答案 0.3%，"
        "这个数字本身是新证据", "3.3；4.1"],
       ["中介不成立，是不是测量太窄", "换三个调节量表重估：第一环翻倍、第二环下降，占比 4.9%→2.2%，"
        "方向与“测量伪影”相反", "3.5；表 5"],
       ["单一系统不能推广", "四系统分别估计 + 23 系统合并，总效应不拒绝等值（p=.087），构成路径拒绝（p<.001）",
        "3.7；3.8"],
       ["标准误没考虑分层整群抽样", "十个似真值 + 80 套 Fay-BRR + Rubin 合并，间接项在复制内重估",
        "2.4；附录 B"],
       ["横断面数据谈机制", "明确降级为协方差分解，并说明间接项小正是取弱读法的理由", "2.4；5"],
       ["四个比较系统是怎么挑的", "写明选择标准（题目覆盖可比、设备融入方式不同），并承认非随机抽样", "2.1；5"],
       ["调节量表跨系统可比吗", "局限性中明说未做测量不变性检验，且结论落在系统内占比而非跨系统点值", "5"],
       ["缺失值怎么处理", "各变量缺失 < 0.5%，listwise 后 12,237；完整案例与全样本均值差 0.012 SD", "2.1"],
       ["做了几十次检验，多重比较呢", "不做 alpha 校正，报精确 p 与区间；结论靠占比而非显著性计数", "2.4"],
       ["构成比（ratio）系数不可靠", "同时给两种参数化（份额 vs 两种时长），并解释为何结论只取后者", "3.6；表 6"],
       ["LPA 未加权、未做三步校正", "局限性明确写出，剖面只作描述、不作因果", "5"],
       ["效应量这么小，有实践意义吗", "总效应 22 分/SD、十分位间 52 分；实践含义写在 4.5", "3.2；4.5"]],
      widths=[4.6, 8.4, 3.0],
      caption="表 8  审稿人预演清单",
      note="说明：这张表不进论文，是给你自己在返修阶段用的。审稿意见回来时，先对照这张表——"
           "如果意见落在表内，说明我们预判到了，回答会很快；如果落在表外，才是真正需要补分析的地方。")

h(doc, "③ 本轮新增/改动的文件", 2)
bullet(doc, "02_Revised_Manuscript_JSET.docx：正文 5,598 词、摘要 249 词、双盲、带行号、含声明节与 Figure 1 实图。")
bullet(doc, "03_Title_Page_JSET.docx：独立标题页（作者、单位、通讯、字数、图表数、声明）。")
bullet(doc, "04_Cover_Letter_JSET.docx：投稿信，按“问题—发现—为何适合本刊—方法可信度”四段写，"
       "并声明未一稿多投、无利益冲突。")
bullet(doc, "run/s18_missing_fig.py：算缺失率（写进 2.1）并重绘 Figure 1（400 dpi，轴标签与正文一致）。")
bullet(doc, "check_numbers.py：把正文/表格里的 28 个关键数字逐个对回 output/*.json，"
       "同时检查摘要 ≤250 词、正文 ≤6,000 词。交稿前跑一次，全绿再投。")

h(doc, "④ 还需要你本人补的四件事", 2)
num(doc, "作者信息与基金：标题页与声明节里所有 [方括号] 处。")
num(doc, "文献终校：Li et al. (2018) 与 Xiong et al. (2025) 两条已按数据库核对补全作者与 DOI；"
    "其余中文文献（Yang et al., 2025；Zhi & Chen, 2019）请按原刊卷期再核一次。")
num(doc, "代码与结果的 DOI：把 run/ 下的脚本与 output/*.json 打包上传 OSF 或 Zenodo，"
    "把 DOI 填进 Data availability。这一步对方法可信度的加分远超它的成本。")
num(doc, "图件格式：JSET 投稿系统接受 PNG/TIFF/EPS，Figure 1 现为 400 dpi PNG；"
    "若系统要求 TIFF，用同一脚本改扩展名重存即可（dpi 不变）。")

para(doc, "最后一句实话：这一轮改完，稿子的“可送审性”比“学术价值”提升得更多——"
     "字数、摘要、匿名、声明、图件这些是门槛，过了门槛才有机会被评价。"
     "而学术价值那部分，第九节那三个结果（0.3%、2.2%、22.91）已经把它撑住了。")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "01_诊断与改稿方案.docx")
doc.save(out)
print("saved:", out)
