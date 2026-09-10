#!/usr/bin/env bash
# Energy (twins, target=energy) corrected KW re-analysis -- runs in parallel with the main sweep
# now that /tmp/twins_main.zip is restored. Same policies/columns as overnight_kw_corrected.sh.
set +e
cd "$(dirname "$0")/.." || exit 1
PY=.venv-linux/bin/python
OUT=artifacts/corrected
mkdir -p "$OUT"
LOG="$OUT/run_energy.log"
: > "$LOG"
run () { local tag="$1"; shift
  echo "=== START $tag $(date '+%H:%M:%S') ===" | tee -a "$LOG"
  "$PY" scripts/kw_cost_vs_size.py "$@" 2>&1 | tee -a "$LOG"
  echo "=== END   $tag $(date '+%H:%M:%S') ===" | tee -a "$LOG"; }

run energy_largestn --mode twins --target-prop energy --learner ridge-log --budget-policy largest-n --membership-bootstrap 1000 --all-metrics --out "$OUT/kw_energy_ridge_largestn.csv"
run energy_minerr   --mode twins --target-prop energy --learner ridge-log --budget-policy minerr --out "$OUT/kw_energy_ridge_minerr.csv"
run energy_rf       --mode twins --target-prop energy --learner sk-rf-log --budget-policy largest-n --out "$OUT/kw_energy_sk-rf-log_largestn.csv"
run energy_cart     --mode twins --target-prop energy --learner cart-log  --budget-policy largest-n --out "$OUT/kw_energy_cart-log_largestn.csv"
echo "=== ENERGY DONE $(date '+%H:%M:%S') ===" | tee -a "$LOG"
