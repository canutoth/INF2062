#!/usr/bin/env bash
# RESUME after the overnight batch was killed (~11:06). Already DONE: energy + workload ablated
# Phase-1 (artifacts/ablation/kw_{energy,workload}_ridge_largestn_ABL*.csv). This script runs the
# MISSING work in PRIORITY order so the reviewer-critical results land first even if killed again.
set +e
cd "$(dirname "$0")/.." || exit 1
PY=.venv-linux/bin/python
OUT=artifacts/ablation
ROUT=artifacts/reversal
mkdir -p "$OUT" "$ROUT"
LOG="$OUT/resume.log"
: > "$LOG"
EXCL="pilotCost cheapOracle expensiveOracle"
run () { local tag="$1"; shift
  echo "=================== START $tag  $(date '+%Y-%m-%d %H:%M:%S') ===================" | tee -a "$LOG"
  "$PY" "$@" 2>&1 | tee -a "$LOG"
  echo "=================== END   $tag  $(date '+%Y-%m-%d %H:%M:%S') ===================" | tee -a "$LOG"; }

echo "##### CORE 1: lcbench ablated (completes the ablation trio) #####" | tee -a "$LOG"
run lcbench_abl_largestn scripts/kw_cost_vs_size.py --mode lcbench --learner ridge-log \
    --budget-policy largest-n --membership-bootstrap 1000 --all-metrics --exclude $EXCL \
    --out "$OUT/kw_lcbench_ridge_largestn_ABL.csv"

echo "##### CORE 2: reversal on energy (heavy-tailed; the key larger-yet-cheaper number) #####" | tee -a "$LOG"
run reversal_energy scripts/reversal_rate.py --mode twins --target-prop energy --out "$ROUT/reversal_energy.csv"

echo "##### SECONDARY: reversal on the remaining families #####" | tee -a "$LOG"
run reversal_workload scripts/reversal_rate.py --mode workload --out "$ROUT/reversal_workload.csv"
run reversal_lcbench  scripts/reversal_rate.py --mode lcbench  --out "$ROUT/reversal_lcbench.csv"
run reversal_icse19   scripts/reversal_rate.py --mode icse19   --out "$ROUT/reversal_icse19.csv"
run reversal_x264     scripts/reversal_rate.py --mode x264     --out "$ROUT/reversal_x264.csv"

echo "##### SECONDARY: budget-rule sensitivity (minerr) ablated, all 3 generated families #####" | tee -a "$LOG"
run energy_abl_minerr   scripts/kw_cost_vs_size.py --mode twins    --target-prop energy --learner ridge-log --budget-policy minerr --exclude $EXCL --out "$OUT/kw_energy_ridge_minerr_ABL.csv"
run workload_abl_minerr scripts/kw_cost_vs_size.py --mode workload                      --learner ridge-log --budget-policy minerr --exclude $EXCL --out "$OUT/kw_workload_ridge_minerr_ABL.csv"
run lcbench_abl_minerr  scripts/kw_cost_vs_size.py --mode lcbench                       --learner ridge-log --budget-policy minerr --exclude $EXCL --out "$OUT/kw_lcbench_ridge_minerr_ABL.csv"

echo "##### SECONDARY: learner robustness (sk-rf) ablated, all 3 generated families #####" | tee -a "$LOG"
run energy_abl_rf   scripts/kw_cost_vs_size.py --mode twins    --target-prop energy --learner sk-rf-log --budget-policy largest-n --exclude $EXCL --out "$OUT/kw_energy_sk-rf-log_largestn_ABL.csv"
run workload_abl_rf scripts/kw_cost_vs_size.py --mode workload                      --learner sk-rf-log --budget-policy largest-n --exclude $EXCL --out "$OUT/kw_workload_sk-rf-log_largestn_ABL.csv"
run lcbench_abl_rf  scripts/kw_cost_vs_size.py --mode lcbench                       --learner sk-rf-log --budget-policy largest-n --exclude $EXCL --out "$OUT/kw_lcbench_sk-rf-log_largestn_ABL.csv"

echo "##### RESUME BATCH DONE  $(date '+%Y-%m-%d %H:%M:%S') #####" | tee -a "$LOG"