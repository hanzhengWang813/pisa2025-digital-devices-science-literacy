# PISA 2025 — Digital device use and scientific literacy

Analysis code and results for a secondary analysis of **PISA 2025** student data,
examining how learning-oriented and entertainment-oriented digital device use
relate to scientific literacy, with self-regulation as a candidate mediator.

- Sample: 12,385 15-year-old students in B-S-J-Z (Beijing–Shanghai–Jiangsu–Zhejiang), China; 12,237 enter the models after listwise deletion.
- Pooled cross-system estimates use 23 education systems.
- Estimation: 10 plausible values × 80 Fay–BRR replicate weights, combined with Rubin's rules.

This repository contains the code that produces every number in the manuscript.
**It does not contain the manuscript or the raw data** — see [Data](#data).

---

## Repository layout

| Path | Contents |
|---|---|
| `run/*.py` | 27 analysis scripts, from the raw `.sav` to `output/*.json` |
| `run/output/*.json` | Results of the current (recomputed) models — the source for every number in the text |
| `run/output/fig/fig1_pub.png` | Publication Figure 1 (400 dpi) |
| `run/results_ref/` | Results of the original submission, kept for before/after comparison — **do not overwrite** |
| `run/run_all.sh` | Ordered execution of steps 2–4 below (`set -e`) |
| `build_manuscript.py` | Builds the manuscript `.docx` |
| `build_report.py` | Builds the Chinese diagnostic report `.docx` |
| `build_frontmatter.py` | Builds title page and cover letter `.docx` |
| `docx_helpers.py` | Word formatting utilities (fonts, tables, line numbers, page numbers) |
| `check_numbers.py` | Pre-submission gate: 28 numeric assertions + abstract and main-text word limits |
| `retrim*.py` | Mechanical text-replacement scripts used in this revision round; already executed, kept for provenance |
| `archive/build_manuscript.bak.py` | Generator snapshot before trimming |

---

## Reproducing

```bash
# 0) environment
python3 -m pip install -r requirements.txt

# 1) point to the raw data
export PISA_SAV=/path/to/CY09_MS_STU_PUF.sav

# 2) extract analysis data (~6-10 min for a 1.9 GB .sav)
python3 run/s0_extract.py            # -> run/output/analysis.parquet
python3 run/s7_pv_extract.py         # -> run/output/pv.parquet

# 3) exploratory models (the original submission's analyses)
python3 run/s1_constructs.py
python3 run/s2_mediation.py
python3 run/s3_moderation.py
python3 run/s4_multigroup.py
python3 run/s5_lpa.py
python3 run/s6_figures.py
python3 run/s8_rcs.py
python3 run/s9_interaction.py
python3 run/s12_corr_inference.py

# 4) design-based re-estimation (the results the manuscript reports)
python3 run/s7b_pv_models.py         # main model: PV + BRR + Rubin
python3 run/s10_robust_dual.py       # eight robustness specifications
python3 run/s11_interaction_ci.py    # interaction intervals
python3 run/s13_composition.py       # composition (share vs. hours)
python3 run/s14_multisystem_pv.py    # four education systems
python3 run/s15_joint_tests.py       # joint Wald tests (needs s14 output)
python3 run/s16_pooled_pv.py         # 23 systems pooled
python3 run/s17_altmediator.py       # alternative moderator scales
python3 run/s18_missing_fig.py       # missingness + Figure 1

# 5) documents
python3 build_manuscript.py
python3 build_report.py
python3 build_frontmatter.py

# 6) pre-submission gate
python3 check_numbers.py             # exits 0 only if 28/28 and word limits pass
```

`run/run_all.sh` chains steps 2–4 in order. Indicative runtimes (macOS, Apple
silicon): `s0_extract` 6–10 min; `s14` and `s16` 1–3 min each; most others
under 1 min.

---

## Data

- **Raw data**: OECD PISA 2025 student questionnaire and cognitive data
  (`CY09_MS_STU_PUF.sav`). Publicly available from the OECD; **not redistributed
  here** — download it and set `PISA_SAV` as above.
- **Derived data** (`analysis.parquet` 755,721 × 153, `pv.parquet` 755,721 × 10)
  are reproducible from step 2 and therefore not included.
- `run/results_ref/` holds the *original submission's* result files and is the
  only record of the before/after comparison. Leave it untouched when re-running.

---

## Which file produces which number

| Manuscript location | Quantity | File |
|---|---|---|
| Table 1 | Descriptives and correlations | `results_ref/desc_cn.csv`, `corr_cn.csv`, `corr_design_inference.csv` |
| Table 2 | c = −22.11, c′ = −21.02 (95.1%), indirect −1.09 (4.9%), serial path 0.3% | `output/pv_mediation.json` |
| Figure 1 | Dose–response curves | `output/fig/fig1_pub.png`, `results_ref/rcs_results.json` |
| Tables 3–4 | Four profiles, entropy = .877 | `results_ref/lpa_results.json`, `lpa_profiles.csv` |
| Table 5 | SELFREG α = .80; GOALSET d₁ = −0.147, b₃ = 7.98, serial −0.303, share 2.2% | `output/altmediator.json` |
| Table 6 | Share −0.62 per 10 pp (p = .155), total hours −3.31 (p = .003), learning +0.55 (n.s.), entertainment −4.62 (p < .001) | `output/composition.json` |
| Table 7 | Four systems: c, c′, b₃, d₁, b₁ | `output/multisystem_pv.json` |
| Table 8 | 23 systems pooled: c = −20.07, c′ = −20.36, net indirect +0.29 (−1.5%) | `output/pooled_pv.json` |
| Table 9 | Eight robustness specifications | `output/robustness_dual.json` |
| Table B1 | Per-system 95% intervals | `output/multisystem_pv.json` |
| Section 3.7 | F(3, 80) = 2.27 (total), 0.75 (direct), 22.91 (entertainment → literacy) | `output/joint_tests.json` |
| Section 2.1 | Missingness < 0.5% per variable; complete-case mean difference 0.012 SD | `output/missing.json` |

---

## Verification performed

1. **Main model reproduces digit for digit**: a₁ = 0.2587, d₁ = −0.0644, c = −22.1058, indirect −1.0894.
2. **Number consistency**: `check_numbers.py` traces 28 reported values back to `output/*.json`; currently 28/28.
3. **Length compliance**: abstract 249 words, main text 5,601 words excluding references, tables and legends.
4. **Portability**: after refactoring the I/O layer, `s15_joint_tests.py` reproduces `joint_tests.json` with **0 differences across 160 values**.

---

## Known limitations (also stated in the manuscript)

- **The legacy weighted-bootstrap implementation is flawed** (weights applied twice, so intervals can exclude the point estimate). All intervals reported here use PV + BRR + Rubin; the bootstrap helper is retained in `common2.py` but no reported conclusion depends on it.
- **The four-system joint test treats systems as independent samples.** It is used only to ask whether effects are equal, not as a precise between-system test.
- **No measurement invariance testing across systems** (2025 technical-report parameters were not available). Conclusions are therefore about within-system shares, not cross-system point comparisons.

---

## Citation

If you use this code, please cite the paper. PISA 2025 data should be cited
according to the OECD's citation guidelines. A Zenodo DOI will be added on
acceptance.
