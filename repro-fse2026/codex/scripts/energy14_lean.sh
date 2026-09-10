#!/usr/bin/env bash
# Lean 14-system energy recompute: only the TWO genuinely-needed new numbers (full 50% / Pareto 80%
# are already in-paper). Ablated FIRST (the §VII figure), then reversal (the RQ1 figure).
set +e
cd "$(dirname "$0")/.." || exit 1
PY=.venv-linux/bin/python
OUT=artifacts/energy14
mkdir -p "$OUT"
LOG="$OUT/lean.log"
: > "$LOG"
SYS="7z Apache HSQLDB LLVM MongoDB PostgreSQL VP8 brotli exastencils jump3r kanzi lrzip nginx x264"
run () { local tag="$1"; shift
  echo "=================== START $tag  $(date '+%H:%M:%S') ===================" | tee -a "$LOG"
  "$PY" "$@" 2>&1 | tee -a "$LOG"
  echo "=================== END   $tag  $(date '+%H:%M:%S') ===================" | tee -a "$LOG"; }

run energy14_abl scripts/kw_cost_vs_size.py --mode twins --target-prop energy --systems $SYS \
    --learner ridge-log --budget-policy largest-n --membership-bootstrap 1000 --all-metrics \
    --exclude pilotCost cheapOracle expensiveOracle --out "$OUT/kw_energy14_ridge_largestn_ABL.csv"

run energy14_reversal scripts/reversal_rate.py --mode twins --target-prop energy --systems $SYS \
    --out "$OUT/reversal_energy14.csv"

echo "##### ENERGY14 LEAN DONE  $(date '+%Y-%m-%d %H:%M:%S') #####" | tee -a "$LOG"