#!/usr/bin/env bash
# Overnight corrected KW re-analysis for the ICSE-2027 reviewer responses.
#   C2  : non-oracular budget policy (largest affordable n) -- the deployable headline
#   minerr : retrospective upper envelope, run alongside for the "holds under both policies" claim
#   R1#1: --membership-bootstrap -> p_reproduce_change (top-group change survives reseeding)
#   R1#2: evicted column (source-study recommendation drops out of cost top group)
#   R1#3: mre_gap column (accuracy gap between size-era and cost-era pick)
# Families with data present now: icse19, x264, workload. energy added later if archive restored.
# Replications run FIRST (strongest thread). Continues past any single-family failure.
set +e
cd "$(dirname "$0")/.." || exit 1
PY=.venv-linux/bin/python
OUT=artifacts/corrected
mkdir -p "$OUT"
LOG="$OUT/run.log"
BOOT_REPL=1000      # replications are small + fast
BOOT_HEAVY=500      # workload has many comparisons
: > "$LOG"
run () {  # run <tag> <args...>
  local tag="$1"; shift
  echo "=================== START $tag  $(date '+%H:%M:%S') ===================" | tee -a "$LOG"
  "$PY" scripts/kw_cost_vs_size.py "$@" 2>&1 | tee -a "$LOG"
  echo "=================== END   $tag  $(date '+%H:%M:%S') ===================" | tee -a "$LOG"
}

echo "##### PHASE 1: largest-n (deployable) + membership bootstrap, primary learner ridge-log #####" | tee -a "$LOG"
run icse19_largestn  --mode icse19   --learner ridge-log --budget-policy largest-n --membership-bootstrap $BOOT_REPL  --all-metrics --out "$OUT/kw_icse19_ridge_largestn.csv"
run x264_largestn    --mode x264      --learner ridge-log --budget-policy largest-n --membership-bootstrap $BOOT_REPL  --all-metrics --out "$OUT/kw_x264_ridge_largestn.csv"
run workload_largestn --mode workload --learner ridge-log --budget-policy largest-n --membership-bootstrap $BOOT_HEAVY --all-metrics --out "$OUT/kw_workload_ridge_largestn.csv"

echo "##### PHASE 2: minerr (retrospective envelope) for the side-by-side policy comparison #####" | tee -a "$LOG"
run icse19_minerr    --mode icse19   --learner ridge-log --budget-policy minerr --out "$OUT/kw_icse19_ridge_minerr.csv"
run x264_minerr      --mode x264      --learner ridge-log --budget-policy minerr --out "$OUT/kw_x264_ridge_minerr.csv"
run workload_minerr  --mode workload  --learner ridge-log --budget-policy minerr --out "$OUT/kw_workload_ridge_minerr.csv"

echo "##### PHASE 3: learner robustness under the corrected largest-n policy (RF, CART) #####" | tee -a "$LOG"
for lr in sk-rf-log cart-log; do
  run icse19_$lr   --mode icse19   --learner $lr --budget-policy largest-n --out "$OUT/kw_icse19_${lr}_largestn.csv"
  run x264_$lr     --mode x264      --learner $lr --budget-policy largest-n --out "$OUT/kw_x264_${lr}_largestn.csv"
  run workload_$lr --mode workload  --learner $lr --budget-policy largest-n --out "$OUT/kw_workload_${lr}_largestn.csv"
done

echo "##### ALL DONE  $(date '+%H:%M:%S') #####" | tee -a "$LOG"
