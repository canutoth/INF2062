#!/usr/bin/env bash
set -euo pipefail

cd /Users/mathieuacher/SANDBOX/cost-sampling-matters

ROOT="artifacts/linux_hgbt_full_strategy"
LOG="$ROOT/logs/run_all.log"
mkdir -p "$ROOT/logs"

echo "[$(date)] Starting Linux HGBT all-feature full-strategy batch" >> "$LOG"
for release in 413 415 420 500 504 507 508; do
  case "$release" in
    413) parquet="ICPE-rawdata/linux/tuxkconfig_413.parquet" ;;
    415) parquet="ICPE-rawdata/linux/tuxkconfig_415.parquet" ;;
    420) parquet="ICPE-rawdata/linux/tuxkconfig_420.parquet" ;;
    500) parquet="ICPE-rawdata/linux/tuxkconfig_500.parquet" ;;
    504) parquet="ICPE-rawdata/linux/tuxkconfig_504.parquet" ;;
    507) parquet="ICPE-rawdata/linux/tuxkconfig_507.parquet" ;;
    508) parquet="ICPE-rawdata/linux/tuxkconfig_508.parquet" ;;
    *) echo "Unknown release: $release" >&2; exit 1 ;;
  esac

  out="$ROOT/linux${release}_vmlinux"
  if [[ -f "$out/strategy_summary.csv" ]]; then
    echo "[$(date)] release=$release already complete, skipping" >> "$LOG"
    continue
  fi

  echo "[$(date)] release=$release" >> "$LOG"
  .venv-linux/bin/python scripts/run_linux_kernel.py \
    --parquet "$parquet" \
    --release "$release" \
    --output-dir "$out" \
    --learner sk-hgbt-log \
    --top-k-features 0 \
    --levels 0.0108,0.0540,0.1080 \
    --stochastic-runs 3 \
    --diversity-runs 3 \
    --uncertainty-runs 3 \
    --coverage-runs 3 \
    --diversity-candidate-size 128 \
    --coverage-candidate-size 128 \
    --predict-chunk 8192 \
    >> "$LOG" 2>&1
done

echo "[$(date)] Summarizing Linux HGBT full-strategy batch" >> "$LOG"
.venv-linux/bin/python scripts/summarize_linux_hgbt_batch.py \
  --input-dir "$ROOT" \
  >> "$LOG" 2>&1

echo "[$(date)] Done" >> "$LOG"
