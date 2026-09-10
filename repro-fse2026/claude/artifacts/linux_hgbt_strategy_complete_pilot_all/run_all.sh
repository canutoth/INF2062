#!/usr/bin/env bash
set -euo pipefail

cd /Users/mathieuacher/SANDBOX/cost-sampling-matters

OUT_ROOT="artifacts/linux_hgbt_strategy_complete_pilot_all"
LOG="$OUT_ROOT/run_all.log"

parquet_for_release() {
  case "$1" in
    413) echo "ICPE-rawdata/linux/tuxkconfig_413.parquet" ;;
    415) echo "ICPE-rawdata/linux/tuxkconfig_415.parquet" ;;
    420) echo "ICPE-rawdata/linux/tuxkconfig_420.parquet" ;;
    500) echo "ICPE-rawdata/linux/tuxkconfig_500.parquet" ;;
    504) echo "ICPE-rawdata/linux/tuxkconfig_504.parquet" ;;
    507) echo "ICPE-rawdata/linux/tuxkconfig_507.parquet" ;;
    508) echo "ICPE-rawdata/linux/tuxkconfig_508.parquet" ;;
    *) echo "unknown release: $1" >&2; return 1 ;;
  esac
}

{
  echo "[$(date)] Starting Linux HGBT strategy-complete one-budget pilot"
  for release in 413 415 420 500 504 507 508; do
    parquet="$(parquet_for_release "$release")"
    echo "[$(date)] release=$release"
    .venv-linux/bin/python scripts/run_linux_kernel.py \
      --parquet "$parquet" \
      --release "$release" \
      --output-dir "$OUT_ROOT/linux${release}_vmlinux" \
      --learner sk-hgbt-log \
      --top-k-features 0 \
      --levels 0.0108 \
      --stochastic-runs 1 \
      --diversity-runs 1 \
      --uncertainty-runs 1 \
      --coverage-runs 1 \
      --diversity-candidate-size 64 \
      --coverage-candidate-size 64 \
      --predict-chunk 8192
  done
  echo "[$(date)] Done"
} >> "$LOG" 2>&1
