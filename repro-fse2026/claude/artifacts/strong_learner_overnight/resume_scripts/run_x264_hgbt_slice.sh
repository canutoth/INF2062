#!/usr/bin/env bash
set -euo pipefail

cd /Users/mathieuacher/SANDBOX/cost-sampling-matters

LOG="artifacts/strong_learner_overnight/replication/sk-hgbt-log/x264_matrix_slice_tmux.log"
{
  echo "[$(date)] Starting bounded x264 HGBT matrix slice"
  .venv-linux/bin/python scripts/run_x264_matrix.py \
    --max-runs 30 \
    --contexts 0-2 \
    --learner sk-hgbt-log \
    --output-dir artifacts/strong_learner_overnight/replication/sk-hgbt-log/x264_matrix_slice
  echo "[$(date)] Done"
} >> "$LOG" 2>&1
