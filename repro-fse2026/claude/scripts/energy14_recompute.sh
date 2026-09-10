#!/usr/bin/env bash
# Energy headline switched to the 14-system set. Recompute every ENERGY-attributed number used in
# 7-threats.tex (§VII ablation) and 5-results.tex (RQ1 reversal, RQ2) at 14 systems, consistently.
# 14 systems = the all14 context set.
set +e
cd "$(dirname "$0")/.." || exit 1
PY=.venv-linux/bin/python
OUT=artifacts/energy14
mkdir -p "$OUT"
LOG="$OUT/run.log"
: > "$LOG"
SYS="7z Apache HSQLDB LLVM MongoDB PostgreSQL VP8 brotli exastencils jump3r kanzi lrzip nginx x264"
EXCL="pilotCost cheapOracle expensiveOracle"
run () { local tag="$1"; shift
  echo "=================== START $tag  $(date '+%H:%M:%S') ===================" | tee -a "$LOG"
  "$PY" "$@" 2>&1 | tee -a "$LOG"
  echo "=================== END   $tag  $(date '+%H:%M:%S') ===================" | tee -a "$LOG"; }

# 1. FULL 14-sys energy WITH Pareto (the all14 KW exists at 50% but had no --all-metrics, so no Pareto)
run energy14_full scripts/kw_cost_vs_size.py --mode twins --target-prop energy --systems $SYS \
    --learner ridge-log --budget-policy largest-n --membership-bootstrap 1000 --all-metrics \
    --out "$OUT/kw_energy14_ridge_largestn_FULL.csv"

# 2. ABLATED 14-sys energy (cost-blind random/balanced) — the §VII ablation energy figure
run energy14_abl scripts/kw_cost_vs_size.py --mode twins --target-prop energy --systems $SYS \
    --learner ridge-log --budget-policy largest-n --membership-bootstrap 1000 --all-metrics \
    --exclude $EXCL --out "$OUT/kw_energy14_ridge_largestn_ABL.csv"

# 3. REVERSAL 14-sys energy — the RQ1 cross-strategy reversal figure
run energy14_reversal scripts/reversal_rate.py --mode twins --target-prop energy --systems $SYS \
    --out "$OUT/reversal_energy14.csv"

echo "##### ENERGY14 DONE  $(date '+%Y-%m-%d %H:%M:%S') #####" | tee -a "$LOG"