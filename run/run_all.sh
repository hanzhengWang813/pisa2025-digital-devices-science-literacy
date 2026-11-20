#!/usr/bin/env bash
# 一键复现：按依赖顺序跑完分析（第 2–4 步）。任一步失败即停。
# 用法：
#   export PISA_SAV=/path/to/CY09_MS_STU_PUF.sav
#   bash run/run_all.sh
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

if [ -z "${PISA_SAV:-}" ]; then
  echo "请先设置 PISA_SAV 指向 CY09_MS_STU_PUF.sav" >&2
  exit 1
fi

run() {
  echo ""
  echo "==> $1"
  /usr/bin/time -p python3 "$1" 2>&1 | tail -5 || { echo "失败：$1" >&2; exit 1; }
}

# 2) 抽取分析数据（慢：读 1.9GB .sav）
run s0_extract.py
run s7_pv_extract.py

# 3) 探索性分析（原投稿口径）
for f in s1_constructs.py s2_mediation.py s3_moderation.py s4_multigroup.py \
         s5_lpa.py s6_figures.py s8_rcs.py s9_interaction.py s12_corr_inference.py; do
  run "$f"
done

# 4) 设计基础重估（PV + BRR + Rubin；正文主要结论）
for f in s7b_pv_models.py s10_robust_dual.py s11_interaction_ci.py \
         s13_composition.py s14_multisystem_pv.py s15_joint_tests.py \
         s16_pooled_pv.py s17_altmediator.py s18_missing_fig.py; do
  run "$f"
done

echo ""
echo "完成。下一步："
echo "  python3 ../build_manuscript.py && python3 ../build_report.py && python3 ../check_numbers.py"
