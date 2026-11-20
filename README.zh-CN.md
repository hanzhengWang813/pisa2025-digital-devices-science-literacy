# PISA 2025 修订版代码包（2026-11-20）

本仓库配套一篇尚未发表的稿件（数字设备使用与科学素养，PISA 2025）。
**稿件本身、标题页与投稿信不在本仓库中**——仅公开代码、结果与文档生成脚本。

English version: [`README.md`](README.md)

---

## 1. 包里有什么

| 目录 / 文件 | 内容 | 说明 |
|---|---|---|
| `run/*.py` | 27 个分析脚本 | 从原始 `.sav` 到 `output/*.json` 的全部计算 |
| `run/output/*.json` | 复算后的结果文件 | 正文每个数字的出处 |
| `run/output/fig/fig1_pub.png` | 稿件 Figure 1 | 400 dpi |
| `run/results_ref/` | 原投稿的结果文件 | 用于对照“改了什么”，**不要覆盖** |
| `build_manuscript.py` | 英文稿生成器 | 生成稿件 docx（输出文件不在本仓库） |
| `build_report.py` | 中文诊断报告生成器 | 生成诊断报告 docx（输出文件不在本仓库） |
| `build_frontmatter.py` | 标题页与投稿信生成器 | 生成标题页与投稿信（输出文件不在本仓库） |
| `docx_helpers.py` | Word 排版工具函数 | 字体、表格、行号、页码 |
| `check_numbers.py` | 交稿前数字与字数门禁 | 28 项断言，全绿才投 |
| `retrim*.py` | 本轮改稿用的机械替换脚本 | 已执行完毕，保留供追溯 |
| `archive/build_manuscript.bak.py` | 压缩前的生成器备份 | 需要回看原段落时用 |

**未包含**：原始数据 `CY09_MS_STU_PUF.sav`（1.9 GB）与派生的 `analysis.parquet`、`pv.parquet`（共 190 MB）。原因见 §4，两条命令即可重建。

---

## 2. 本轮（第三轮）代码改动清单

### 2.1 新增 6 个分析脚本（`run/s13`–`s18`，共 624 行）

| 脚本 | 解决的问题 | 输出 | 对应正文 |
|---|---|---|---|
| `s13_composition.py` | 把娱乐／学习时长当作“份额”而非绝对时长，检验构成效应是否稳健 | `composition.json` | 3.6，Table 6 |
| `s14_multisystem_pv.py` | 四经济体改用 10 个似真值 × 80 套 Fay-BRR × Rubin 合并重估（原稿用解析标准误） | `multisystem_pv.json` | 3.7，Table 7，Table B1 |
| `s15_joint_tests.py` | 四经济体**联合** Wald 检验 `F(3,80)`，而非逐个看系数是否显著 | `joint_tests.json` | 3.7 正文 |
| `s16_pooled_pv.py` | 23 个经济体合并估计（组内标准化），给跨系统结论一个正式区间 | `pooled_pv.json` | 3.8，Table 8 |
| `s17_altmediator.py` | 换两个调节量表（GOALSET、COGABIL）重估，检验结论是否依赖 SELFREG 的测量宽度 | `altmediator.json` | 3.5，Table 5 |
| `s18_missing_fig.py` | 缺失率与完整案例偏差；重绘出版级 Figure 1 | `missing.json`、`fig/fig1_pub.png` | 2.1，Figure 1 |

### 2.2 修改 6 个已有脚本（**只改可移植性，不改变任何数值**）

| 脚本 | 改动 | 改动行数 |
|---|---|---|
| `common2.py` | ① 新增 `read_frame()`：`parquet` 优先、`pkl` 回退；② `OUT` 默认改为脚本同级 `output/`，可用 `PISA_OUT2` 覆盖；③ `setup_font()` 增加 macOS/Linux 中文字体回退 | 22 |
| `s0_extract.py` | 原始数据路径改为环境变量 `PISA_SAV`（缺失时报错并给出提示）；写出时 `parquet` 失败自动退回 `pkl`；缺失码可直接读 `.sav` 自带值标签 | 34 |
| `s7_pv_extract.py` | 同上：`PISA_SAV` 环境变量、相对 `OUT`、经 `read_frame()` 对齐校验 | 19 |
| `s7b_pv_models.py` | 读 PV 改用 `C.read_frame()` | 2 |
| `s10_robust_dual.py` | 读 PV 改用 `C.read_frame()` | 2 |
| `s11_interaction_ci.py` | 读 PV 改用 `C.read_frame()` | 2 |

> 验证：改造后重跑 `s15_joint_tests.py`，`joint_tests.json` 与原结果**160 个数值 0 差异**。其余脚本的改动均在数据读写层，不触及估计式。

### 2.3 文档生成器与工具

| 文件 | 本轮变化 |
|---|---|
| `build_manuscript.py` | 重写摘要（321→249 词）；改写 2.2/2.3 方法；新增 3.5–3.10 六节结果；重写讨论 4.3、局限、结论；新增 Appendix B（Table B1）；表 1 第 2 行改为 −0.86/0.96；全稿匿名化；嵌入 Figure 1；补 Statements and Declarations 节；参考文献改 APA 7（补全作者与 DOI） |
| `build_report.py` | 第九节改写为四件事的复算结果；新增第十三节（合规对照表 + 十二问审稿人预演表）；表 3 全部换成 s14 设计基础值；表号重编为表 7／表 8 |
| `docx_helpers.py` | 新增 `add_line_numbers()`，全文连续行号（Springer 初投要求） |
| `check_numbers.py` | 本轮新增，28 项断言 + 摘要 ≤250 词 + 正文 ≤6,000 词门禁 |
| `build_frontmatter.py` | 本轮新增，输出独立标题页与投稿信 |

### 2.4 未改动的脚本（15 个）

`build_html.py`、`repro_1docx.py`、`repro_paper.py`、`run_robustness_dual.py`、`s1_constructs.py`、`s2_mediation.py`、`s3_moderation.py`、`s4_multigroup.py`、`s5_lpa.py`、`s6_figures.py`、`s8_rcs.py`、`s8_rcs_fig_en.py`、`s9_interaction.py`、`s12_corr_inference.py`、`verify_paper.py`。
以上与原始包**逐字节比对无差异**（27 = 6 新增 + 6 修改 + 15 未动）。

---

## 3. 复现步骤

```bash
# 0) 环境
python3 -m pip install -r requirements.txt

# 1) 指向原始数据
export PISA_SAV=/path/to/CY09_MS_STU_PUF.sav

# 2) 抽取分析数据（约 6–10 分钟，1.9GB .sav）
python3 run/s0_extract.py            # -> run/output/analysis.parquet
python3 run/s7_pv_extract.py         # -> run/output/pv.parquet

# 3) 探索性分析（原投稿的分析，结果落在 results_ref 同名的 json）
python3 run/s1_constructs.py
python3 run/s2_mediation.py
python3 run/s3_moderation.py
python3 run/s4_multigroup.py
python3 run/s5_lpa.py
python3 run/s6_figures.py
python3 run/s8_rcs.py
python3 run/s9_interaction.py
python3 run/s12_corr_inference.py

# 4) 设计基础重估（本轮新增，正文主要结论都出自这几步）
python3 run/s7b_pv_models.py         # 主模型：PV + BRR + Rubin
python3 run/s10_robust_dual.py       # 八种稳健性设定
python3 run/s11_interaction_ci.py    # 交互项区间
python3 run/s13_composition.py       # 构成比
python3 run/s14_multisystem_pv.py    # 四经济体
python3 run/s15_joint_tests.py       # 联合检验（依赖 s14 输出）
python3 run/s16_pooled_pv.py         # 23 经济体合并
python3 run/s17_altmediator.py       # 替代调节量表
python3 run/s18_missing_fig.py       # 缺失率 + Figure 1

# 5) 生成文档
python3 build_manuscript.py          # -> 稿件 docx（不入库）
python3 build_report.py              # -> 诊断报告 docx（不入库）
python3 build_frontmatter.py         # -> 03、04

# 6) 交稿前门禁
python3 check_numbers.py             # 28/28，摘要与正文词数达标才退出 0
```

`run/run_all.sh` 是上面 2–4 步的顺序版（`set -e`，任一步失败即停）。

单步耗时参考（macOS，M 系列）：`s0_extract` 6–10 min；`s14`/`s16` 各 1–3 min；其余多在 1 min 内。

---

## 4. 数据

- 原始数据：OECD **PISA 2025** 学生问卷与认知数据（`CY09_MS_STU_PUF.sav`，B-S-J-Z 中国 + 其他经济体）。公开数据，需自行从 OECD 下载，本包不附带。
- 派生数据（可重建，故未打包）：`analysis.parquet`（755,721 × 153）、`pv.parquet`（755,721 × 10）。重建只需 §3 的第 2 步。
- 分析样本：中国四省市（B-S-J-Z）12,385 人；进入模型 12,237 人（listwise）。
- `run/results_ref/` 是**原投稿**的结果文件，请勿覆盖：它是“改前 vs 改后”的唯一凭据。

---

## 5. 正文数字 ← 结果文件

| 稿件位置 | 数字 | 文件 |
|---|---|---|
| Table 1 | 描述统计与相关 | `results_ref/desc_cn.csv`、`corr_cn.csv`、`corr_design_inference.csv` |
| Table 2 / 3.2–3.3 | c = −22.11、c′ = −21.02（95.1%）、间接 −1.09（4.9%）、串联 0.3% | `output/pv_mediation.json` |
| Figure 1 / 3.1 | 剂量反应曲线 | `output/fig/fig1_pub.png`、`results_ref/rcs_results.json` |
| Table 3–4 / 3.4 | 4 剖面、entropy = .877 | `results_ref/lpa_results.json`、`lpa_profiles.csv` |
| Table 5 / 3.5 | SELFREG α=.80；GOALSET d₁=−0.147、b₃=7.98、串联 −0.303、占比 2.2% | `output/altmediator.json` |
| Table 6 / 3.6 | 份额 −0.62/10pp（p=.155）、总时长 −3.31（p=.003）、学习 +0.55（n.s.）、娱乐 −4.62（p<.001） | `output/composition.json` |
| Table 7 / 3.7 | 四经济体 c、c′、b₃、d₁、b₁ | `output/multisystem_pv.json` |
| 3.7 正文 | F(3,80) = 2.27（总效应）、0.75（直接）、22.91（娱乐→素养） | `output/joint_tests.json` |
| Table 8 / 3.8 | 23 经济体 c = −20.07、c′ = −20.36、净间接 +0.29（−1.5%） | `output/pooled_pv.json` |
| Table 9 / 3.10 | 八种稳健性设定 | `output/robustness_dual.json` |
| Table B1 | 分系统 95% 区间 | `output/multisystem_pv.json` |
| 2.1 | 各变量缺失 <0.5%；完整案例均值差 0.012 SD | `output/missing.json` |

---

## 6. 已做的验证

1. **主模型逐位复现**：a₁ = 0.2587、d₁ = −0.0644、c = −22.1058、间接 −1.0894，与原稿一致。
2. **数字一致性**：`check_numbers.py` 把 28 个关键数字回对 `output/*.json`，当前 28/28 通过。
3. **字数合规**：摘要 249 词（≤250）、正文 5,601 词（≤6,000）。
4. **可移植性**：改造后重跑 `s15`，160 个输出数值 0 差异。

## 7. 需要留意的三处（已写入稿件局限，不是隐藏问题）

- **加权 bootstrap 的旧实现有缺陷**（`pr ∝ W` 又乘 `W`，等于权重平方，区间不含点估计）。本轮所有区间改用 PV + BRR + Rubin，不依赖该实现；`common2.py` 中的 bootstrap 函数保留未删，但正文结论不再引用。
- **四经济体的联合检验把四个系统当独立样本**，只用于“能否拒绝等值”，不宜读成精确的组间检验。
- **跨系统未做测量不变性检验**（网络受限，未取得 2025 版技术报告的参数）。因此结论落在“系统内占比”，不主张跨系统点值可比。

---

## 8. 引用

若使用本代码，请引用稿件本身；PISA 2025 数据请按 OECD 的引用规范标注。本仓库为代码存档；录用后将在 Zenodo 打 tag 取得 DOI 并回填。
