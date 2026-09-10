#!/bin/bash
# Stream B (runs in parallel with the Linux full-feature stream): learner-sensitivity
# for ALL NON-Linux families across 3 metrics (KW+flip+Pareto via --all-metrics), under
# ridge (baseline completion) + RF + CART. These families are well-fit and NOT affected by
# the Linux feature-truncation bug. No set -e: each step logs and continues.
cd /Users/mathieuacher/SANDBOX/cost-sampling-matters
PY=.venv-linux/bin/python
LOG=/tmp/stream_b.log
ESYS="7z Apache brotli exastencils HSQLDB jump3r kanzi LLVM lrzip MongoDB nginx PostgreSQL VP8 x264"
say(){ echo -e "\n#### $1 ($(date '+%H:%M:%S')) ####" >> "$LOG"; }
KW(){ local out=$1 lr=$2 mode=$3; shift 3; $PY scripts/kw_cost_vs_size.py --mode $mode --learner $lr --all-metrics "$@" --out "$out" >> "$LOG" 2>&1; say "$mode/$lr exit=$?"; }
: > "$LOG"

say "complete ridge baseline (workload)"
KW artifacts/lsens_workload_ridge.csv ridge-log workload --seeds 10

say "RF all-metrics (5 families)"
KW artifacts/lsens_icse19_rf.csv   sk-rf-log icse19
KW artifacts/lsens_icpe20_rf.csv   sk-rf-log x264
KW artifacts/lsens_energy_rf.csv   sk-rf-log twins    --seeds 10 --systems $ESYS
KW artifacts/lsens_lcbench_rf.csv  sk-rf-raw lcbench  --seeds 10
KW artifacts/lsens_workload_rf.csv sk-rf-log workload --seeds 10

say "CART all-metrics (5 families)"
KW artifacts/lsens_icse19_cart.csv   cart-log icse19
KW artifacts/lsens_icpe20_cart.csv   cart-log x264
KW artifacts/lsens_energy_cart.csv   cart-log twins    --seeds 10 --systems $ESYS
KW artifacts/lsens_lcbench_cart.csv  cart-raw lcbench  --seeds 10
KW artifacts/lsens_workload_cart.csv cart-log workload --seeds 10

say "STREAM B DONE"
