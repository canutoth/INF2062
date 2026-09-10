# Learner Sensitivity Compact Pass

This directory contains a compact learner-sensitivity pass for the experiment families. It varies the prediction learner while keeping the sampling and empirical-cost protocol fixed within each family.

## Run Configuration

Command:

```bash
python3 scripts/run_learner_sensitivity.py \
  --output-dir artifacts/learner_sensitivity_compact \
  --families replication,energy,workload,lcbench,linux \
  --replication-contexts 0 \
  --newruns-contexts BerkeleyDBC,lrzip \
  --max-runs 2 \
  --seeds 2 \
  --max-budget 16 \
  --linux-levels 0.01 \
  --linux-stochastic-runs 1 \
  --linux-diversity-runs 0 \
  --linux-uncertainty-runs 0 \
  --linux-coverage-runs 0 \
  --continue-on-error
```

Learners:

- `REPLICATION`, `ENERGY`, `WORKLOAD`, `LINUX`: `ridge-log`, `rf-log`, `gbt-log`
- `LCBENCH`: `ridge-raw`, `rf-raw`, `gbt-raw`

## Main Outputs

- `learner_protocol.md`: family-by-family learner protocol.
- `learner_sensitivity_report.md`: Markdown report with aggregate results and conclusions.
- `learner_sensitivity_summary.csv`: median metrics by family, label, and learner.
- `learner_sensitivity_winners.csv`: best learner by MRE, top-1 stability, and Pareto stability.
- `learner_sensitivity_long.csv`: per-unit records used to build the aggregate summary.
- `manifest.csv`: command-level execution status.

## Status

The compact pass completed for `REPLICATION`, `ENERGY`, `WORKLOAD`, and `LCBENCH`.

`LINUX` did not complete in this local environment because Python cannot import `pyarrow`, which is needed to read the TuxKConfig parquet files. The failing command logs are under `linux/*/*/run.log`.

