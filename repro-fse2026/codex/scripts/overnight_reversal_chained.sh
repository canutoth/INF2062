#!/usr/bin/env bash
# Chained AFTER the ablation batch (waits for its DONE marker to avoid CPU contention), then
# computes the non-monotone reversal rate on the heavy-tailed GENERATED families, where the
# "a larger sample can be cheaper than a smaller one" claim (RQ1 mechanism iii) should actually
# show up. Archive families (icse19 ~0.8%, x264 0%) are already computed and reported separately.
set +e
cd "$(dirname "$0")/.." || exit 1
ABL_LOG=artifacts/ablation/run.log
echo "[reversal-chain] waiting for ablation batch to finish ($(date '+%H:%M:%S')) ..."
until grep -q "ABLATION BATCH DONE" "$ABL_LOG" 2>/dev/null; do sleep 60; done
echo "[reversal-chain] ablation done; starting reversal ($(date '+%H:%M:%S'))"
PY=.venv-linux/bin/python
OUT=artifacts/reversal
mkdir -p "$OUT"
LOG="$OUT/run.log"
: > "$LOG"
run () { local tag="$1"; shift
  echo "=== START $tag $(date '+%H:%M:%S') ===" | tee -a "$LOG"
  "$PY" scripts/reversal_rate.py "$@" 2>&1 | tee -a "$LOG"
  echo "=== END   $tag $(date '+%H:%M:%S') ===" | tee -a "$LOG"; }
# archive families (fast) re-run here too so every family lands in one place / one seed
run icse19   --mode icse19   --out "$OUT/reversal_icse19.csv"
run x264     --mode x264     --out "$OUT/reversal_x264.csv"
run energy   --mode twins    --target-prop energy --out "$OUT/reversal_energy.csv"
run workload --mode workload --out "$OUT/reversal_workload.csv"
run lcbench  --mode lcbench  --out "$OUT/reversal_lcbench.csv"
echo "##### REVERSAL BATCH DONE $(date '+%Y-%m-%d %H:%M:%S') #####" | tee -a "$LOG"