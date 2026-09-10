#!/usr/bin/env bash
set -euo pipefail

cd /Users/mathieuacher/SANDBOX/cost-sampling-matters

LOG="artifacts/strong_learner_overnight/replication/sk-hgbt-log/newruns_missing_tmux.log"
{
  echo "[$(date)] Starting missing NewRuns HGBT contexts"
  .venv-linux/bin/python scripts/run_newruns_batch.py \
    --max-runs 100 \
    --learner sk-hgbt-log \
    --contexts Hipacc,LLVM,Polly,lrzip \
    --output-dir artifacts/strong_learner_overnight/replication/sk-hgbt-log/newruns
  echo "[$(date)] Aggregating NewRuns HGBT contexts"
  .venv-linux/bin/python scripts/aggregate_newruns_from_contexts.py \
    --output-dir artifacts/strong_learner_overnight/replication/sk-hgbt-log/newruns
  echo "[$(date)] Done"
} >> "$LOG" 2>&1
