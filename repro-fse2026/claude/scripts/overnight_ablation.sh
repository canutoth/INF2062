#!/usr/bin/env bash
# Overnight ABLATION batch (reviewer-requested: "show the effect is not just pilotCost/oracles").
# For each GENERATED family (energy/twins, workload, lcbench) we re-run the cost-controlled KW /
# Pareto / flip analysis with the cost-aware sampler (pilotCost) AND both oracles removed from the
# candidate set, leaving only the cost-BLIND deployable samplers {balanced, random}. Compare the
# top-group-change %, robust subset, eviction, and Pareto p_differ against the FULL-candidate-set
# baselines already in artifacts/corrected/kw_<fam>_ridge_largestn*.csv.
#
# Phases (critical first; set +e so one failure never kills the batch):
#   1. ablated largest-n (headline policy) + membership bootstrap + all-metrics, ridge   <- THE ablation
#   2. ablated minerr (retrospective envelope) KW-only, ridge                            <- budget sensitivity
#   3. ablated largest-n KW-only, sk-rf-log                                              <- learner robustness of the ablation
set +e
cd "$(dirname "$0")/.." || exit 1
PY=.venv-linux/bin/python
OUT=artifacts/ablation
mkdir -p "$OUT"
LOG="$OUT/run.log"
: > "$LOG"
EXCL="pilotCost cheapOracle expensiveOracle"
BOOT_E=1000   # energy: few comparisons, cheap
BOOT_W=500    # workload: many comparisons
BOOT_L=1000   # lcbench

run () {  # run <tag> <args...>
  local tag="$1"; shift
  echo "=================== START $tag  $(date '+%Y-%m-%d %H:%M:%S') ===================" | tee -a "$LOG"
  "$PY" scripts/kw_cost_vs_size.py "$@" 2>&1 | tee -a "$LOG"
  echo "=================== END   $tag  $(date '+%Y-%m-%d %H:%M:%S') ===================" | tee -a "$LOG"
}

echo "##### PHASE 1: ABLATED largest-n + bootstrap + all-metrics (ridge) #####" | tee -a "$LOG"
run energy_abl_largestn   --mode twins    --target-prop energy --learner ridge-log --budget-policy largest-n \
    --membership-bootstrap $BOOT_E --all-metrics --exclude $EXCL --out "$OUT/kw_energy_ridge_largestn_ABL.csv"
run workload_abl_largestn --mode workload                      --learner ridge-log --budget-policy largest-n \
    --membership-bootstrap $BOOT_W --all-metrics --exclude $EXCL --out "$OUT/kw_workload_ridge_largestn_ABL.csv"
run lcbench_abl_largestn  --mode lcbench                       --learner ridge-log --budget-policy largest-n \
    --membership-bootstrap $BOOT_L --all-metrics --exclude $EXCL --out "$OUT/kw_lcbench_ridge_largestn_ABL.csv"

echo "##### PHASE 2: ABLATED minerr (budget-rule sensitivity), KW-only (ridge) #####" | tee -a "$LOG"
run energy_abl_minerr   --mode twins    --target-prop energy --learner ridge-log --budget-policy minerr \
    --exclude $EXCL --out "$OUT/kw_energy_ridge_minerr_ABL.csv"
run workload_abl_minerr --mode workload                      --learner ridge-log --budget-policy minerr \
    --exclude $EXCL --out "$OUT/kw_workload_ridge_minerr_ABL.csv"
run lcbench_abl_minerr  --mode lcbench                       --learner ridge-log --budget-policy minerr \
    --exclude $EXCL --out "$OUT/kw_lcbench_ridge_minerr_ABL.csv"

echo "##### PHASE 3: ABLATED largest-n, learner robustness (sk-rf-log) #####" | tee -a "$LOG"
run energy_abl_rf   --mode twins    --target-prop energy --learner sk-rf-log --budget-policy largest-n \
    --exclude $EXCL --out "$OUT/kw_energy_sk-rf-log_largestn_ABL.csv"
run workload_abl_rf --mode workload                      --learner sk-rf-log --budget-policy largest-n \
    --exclude $EXCL --out "$OUT/kw_workload_sk-rf-log_largestn_ABL.csv"
run lcbench_abl_rf  --mode lcbench                       --learner sk-rf-log --budget-policy largest-n \
    --exclude $EXCL --out "$OUT/kw_lcbench_sk-rf-log_largestn_ABL.csv"

echo "##### ABLATION BATCH DONE  $(date '+%Y-%m-%d %H:%M:%S') #####" | tee -a "$LOG"
