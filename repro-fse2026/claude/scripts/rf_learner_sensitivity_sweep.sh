#!/bin/bash
# Learning-algorithm sensitivity for the cost-vs-count KW re-analysis, under RANDOM
# FOREST (sk-rf), a strong, widely-used performance-prediction baseline. Chosen over
# GBT/HGBT because HGBT (max_iter=300) is ~24x slower per fit here (15.9s vs 0.67s),
# making the per-run KW fits (~10k/replication family) infeasible (~44h) under HGBT
# but ~2h under RF. Complements the ridge-log results on disk (kw_cost_vs_size_<fam>.csv).
# Linux is handled separately (significance_linux.py: ridge-log done + HGBT running).
# Sequential, light->heavy. Replications use the archives' ~100 real runs (full fidelity);
# generated families use --seeds 10 (KW top-group-change RATE is robust to seed count).
set -u
cd /Users/mathieuacher/SANDBOX/cost-sampling-matters
PY=.venv-linux/bin/python
LOG=/tmp/rf_kw_sweep.log
: > "$LOG"
run () { echo -e "\n>>> $1 ($(date +%H:%M:%S))" >> "$LOG"; shift; "$@" >> "$LOG" 2>&1; echo "exit=$?" >> "$LOG"; }

run icse19   $PY scripts/kw_cost_vs_size.py --mode icse19 --learner sk-rf-log \
    --out artifacts/kw_cost_vs_size_icse19_rf.csv
run x264     $PY scripts/kw_cost_vs_size.py --mode x264 --learner sk-rf-log \
    --out artifacts/kw_cost_vs_size_icpe20_rf.csv
run energy   $PY scripts/kw_cost_vs_size.py --mode twins --learner sk-rf-log --seeds 10 \
    --systems 7z Apache brotli exastencils HSQLDB jump3r kanzi LLVM lrzip MongoDB nginx PostgreSQL VP8 x264 \
    --out artifacts/kw_cost_vs_size_energy_rf.csv
run lcbench  $PY scripts/kw_cost_vs_size.py --mode lcbench --learner sk-rf-raw --seeds 10 \
    --out artifacts/kw_cost_vs_size_lcbench_rf.csv
run workload $PY scripts/kw_cost_vs_size.py --mode workload --learner sk-rf-log --seeds 10 \
    --out artifacts/kw_cost_vs_size_workload_rf.csv

echo -e "\n=== RF KW sweep DONE ($(date +%H:%M:%S)) ===" >> "$LOG"
