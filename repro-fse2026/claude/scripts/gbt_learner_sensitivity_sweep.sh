#!/bin/bash
# Learning-algorithm sensitivity for the cost-vs-count KW re-analysis.
# Re-runs the KW top-group analysis for every NON-Linux family under sklearn HGBT
# (gradient-boosted trees), to complement the ridge-log results already on disk
# (kw_cost_vs_size_<fam>.csv). Linux is handled separately by significance_linux.py
# --learner sk-hgbt-log. Sequential, light->heavy, so the headline replications land
# first and a heavy-family failure cannot lose the earlier ones.
# Compare: top-group-change % under ridge-log vs sk-hgbt to test learner robustness.
set -u
cd /Users/mathieuacher/SANDBOX/cost-sampling-matters
PY=.venv-linux/bin/python
LOG=/tmp/gbt_kw_sweep.log
: > "$LOG"
run () { echo -e "\n>>> $1 ($(date +%H:%M:%S))" >> "$LOG"; shift; "$@" >> "$LOG" 2>&1; echo "exit=$?" >> "$LOG"; }

run icse19  $PY scripts/kw_cost_vs_size.py --mode icse19 --learner sk-hgbt-log \
    --out artifacts/kw_cost_vs_size_icse19_hgbt.csv
run x264    $PY scripts/kw_cost_vs_size.py --mode x264 --learner sk-hgbt-log \
    --out artifacts/kw_cost_vs_size_icpe20_hgbt.csv
# Generated families use --seeds 10 (not 30): GBT is ~10-50x slower per fit than ridge,
# and the KW top-group-change RATE is robust to seed count. Replications above use the
# archives' real ~100 runs (no seed param), so they stay full-fidelity.
run energy  $PY scripts/kw_cost_vs_size.py --mode twins --learner sk-hgbt-log --seeds 10 \
    --systems 7z Apache brotli exastencils HSQLDB jump3r kanzi LLVM lrzip MongoDB nginx PostgreSQL VP8 x264 \
    --out artifacts/kw_cost_vs_size_energy_hgbt.csv
run lcbench $PY scripts/kw_cost_vs_size.py --mode lcbench --learner sk-hgbt-raw --seeds 10 \
    --out artifacts/kw_cost_vs_size_lcbench_hgbt.csv
run workload $PY scripts/kw_cost_vs_size.py --mode workload --learner sk-hgbt-log --seeds 10 \
    --out artifacts/kw_cost_vs_size_workload_hgbt.csv

echo -e "\n=== GBT KW sweep DONE ($(date +%H:%M:%S)) ===" >> "$LOG"
