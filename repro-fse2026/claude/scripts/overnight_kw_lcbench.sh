#!/usr/bin/env bash
# Restore LCBench data_2k_lw.json from figshare (disk-safe) and run the corrected KW
# re-analysis. Same policies/columns as the other corrected sweeps. The LCBench loader
# remaps ridge-log -> ridge-raw internally (bounded accuracy target).
set +e
cd "$(dirname "$0")/.." || exit 1
PY=.venv-linux/bin/python
OUT=artifacts/corrected
LOG="$OUT/run_lcbench.log"
mkdir -p "$OUT" /private/tmp/lcbench
: > "$LOG"

JSON=/private/tmp/lcbench/data_2k_lw.json
ZIP=/private/tmp/lcbench/data_2k_lw.zip
if [ ! -s "$JSON" ]; then
  echo "Downloading data_2k_lw.zip (339M) from figshare ..." | tee -a "$LOG"
  curl -fL --retry 3 --retry-delay 5 --max-time 1800 -o "$ZIP" https://ndownloader.figshare.com/files/21188598
  rc=$?; echo "download exit=$rc size=$(du -h "$ZIP" 2>/dev/null | cut -f1)" | tee -a "$LOG"
  if [ $rc -ne 0 ]; then echo "FATAL: download failed (rc=$rc)" | tee -a "$LOG"; exit 1; fi
  if ! unzip -tq "$ZIP" >/dev/null 2>&1; then echo "FATAL: zip integrity check failed" | tee -a "$LOG"; rm -f "$ZIP"; exit 1; fi
  echo "Extracting ..." | tee -a "$LOG"
  ( cd /private/tmp/lcbench && unzip -o -q data_2k_lw.zip )
  found=$(find /private/tmp/lcbench -name "data_2k_lw.json" -type f 2>/dev/null | head -1)
  if [ -n "$found" ] && [ "$found" != "$JSON" ]; then mv "$found" "$JSON"; fi
  rm -f "$ZIP"   # free 339M immediately
fi
if [ ! -s "$JSON" ]; then echo "FATAL: $JSON missing" | tee -a "$LOG"; exit 1; fi
echo "Validating JSON ($(du -h "$JSON" | cut -f1)) ..." | tee -a "$LOG"
"$PY" -c "import json; d=json.load(open('$JSON')); print('json OK,', len(d), 'datasets')" 2>&1 | tee -a "$LOG"
if [ ${PIPESTATUS[0]} -ne 0 ]; then echo "FATAL: JSON invalid" | tee -a "$LOG"; exit 1; fi

run () { local tag="$1"; shift
  echo "=== START $tag $(date '+%H:%M:%S') ===" | tee -a "$LOG"
  "$PY" scripts/kw_cost_vs_size.py "$@" 2>&1 | tee -a "$LOG"
  echo "=== END   $tag $(date '+%H:%M:%S') ===" | tee -a "$LOG"; }

run lcbench_largestn --mode lcbench --learner ridge-log --budget-policy largest-n --membership-bootstrap 1000 --all-metrics --out "$OUT/kw_lcbench_ridge_largestn.csv"
run lcbench_minerr   --mode lcbench --learner ridge-log --budget-policy minerr --out "$OUT/kw_lcbench_ridge_minerr.csv"
run lcbench_rf       --mode lcbench --learner sk-rf-log --budget-policy largest-n --out "$OUT/kw_lcbench_sk-rf-log_largestn.csv"
run lcbench_cart     --mode lcbench --learner cart-log  --budget-policy largest-n --out "$OUT/kw_lcbench_cart-log_largestn.csv"
echo "=== LCBENCH DONE $(date '+%H:%M:%S') ===" | tee -a "$LOG"
