# 运行环境与验证记录

## 1. 环境

| 项目 | 本包实测 | 原包（Windows） |
|---|---|---|
| 系统 | macOS (darwin 25.x, arm64) | Windows |
| Python | 3.13.12 | 3.13.14 |
| numpy | 2.5.4 | 2.5.2 |
| pandas | 3.1.1 | 3.0.5 |
| scipy | 1.18.1 | 1.18.1 |
| scikit-learn | 1.9.1 | 1.9.0 |
| matplotlib | 3.11.2 | 3.11.1 |
| pyarrow | 26.0.1 | 25.0.1 |
| pyreadstat | 1.3.8 | 1.3.6 |
| python-docx | 1.2.0 | — |

版本差异未改变任何估计值：`numpy`/`pandas` 小版本升级后，主模型系数仍逐位复现（a₁ = 0.2587、d₁ = −0.0644、c = −22.1058、间接 −1.0894）。

## 2. 验证记录（2026-11-20 23:40 前后）

### 2.1 主模型复现

```
a1 = 0.2587   d1 = -0.0644   c = -22.1058   ind_total = -1.0894
```
与原投稿 `results_ref/pv_mediation.json` 一致。

### 2.2 改造后可移植性验证

修改 `common2.read_frame()` 等 6 个脚本后重跑联合检验：

```
python3 run/s15_joint_tests.py
  Entertainment -> literacy            F(3, 80) = 22.91, p < .001
  Learning -> literacy                 F(3, 80) = 10.46, p < .001
  Self-regulation -> literacy          F(3, 80) = 3.89, p = 0.012
  Serial via entertainment             F(3, 80) = 6.75, p < .001
  Serial via learning                  F(3, 80) = 5.95, p = 0.001
  All indirect                         F(3, 80) = 10.72, p < .001
```
与改造前的 `joint_tests.json` 对比：**160 个数值，0 差异**。

### 2.3 交稿门禁（在本包目录内直接运行）

```
$ python3 check_numbers.py
28 checks, 0 missing
abstract 249 words (limit 250) -> OK
main text 5601 words excluding refs/tables/legends -> OK
```

### 2.4 包内自洽性

- `check_numbers.py` 在本包目录内独立运行通过 → 说明 `run/output/*.json`、`02_Revised_Manuscript_JSET.docx`、路径约定三者一致。
- `bash -n run/run_all.sh` 语法通过。
- `run/results_ref/` 与原包 `results/` 逐文件一致（作为“改前”对照）。

## 3. 复现时的两个常见坑

1. **别忘了 `PISA_SAV`**。`s0_extract.py` 与 `s7_pv_extract.py` 都从该环境变量取原始数据路径，未设置会直接报错退出。
2. **`s15` 依赖 `s14` 的输出**。`run_all.sh` 已排好顺序，手工跑时注意先 `s14` 后 `s15`。
