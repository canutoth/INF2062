#!/bin/bash
# REPRIORITIZED overnight queue (2026-06-27). Key finding: ridge AND RF both
# catastrophically underfit Linux (~30-38% MRE); only gradient boosting fits it
# (HGBT ~7-10%, per prior works + appendix). Linux-significance HGBT does ~600
# fits/release (~19h, FEASIBLE — unlike the 44h per-run replication KW). So Linux
# HGBT is the critical experiment and gets the night; RF/CART sensitivity for the
# already-well-fit families is secondary and runs after. MRE is monitored in both
# pipelines. No set -e: each step logs and the queue continues past failures.
cd /Users/mathieuacher/SANDBOX/cost-sampling-matters
PY=.venv-linux/bin/python
LOG=/tmp/master_overnight.log
ESYS="7z Apache brotli exastencils HSQLDB jump3r kanzi LLVM lrzip MongoDB nginx PostgreSQL VP8 x264"
say(){ echo -e "\n######## $1 ($(date '+%m-%d %H:%M:%S')) ########" >> "$LOG"; }
KW(){ local out=$1 lr=$2 mode=$3; shift 3; $PY scripts/kw_cost_vs_size.py --mode $mode --learner $lr --all-metrics "$@" --out "$out" >> "$LOG" 2>&1; say "$mode/$lr exit=$?"; }
: > "$LOG"

say "A. workload ridge (finish the matched baseline)"
KW artifacts/lsens_workload_ridge.csv ridge-log workload --seeds 10

say "B. ***LINUX HGBT*** — CRITICAL (only learner that fits Linux; MRE-monitored, ~19h)"
$PY scripts/significance_linux.py --learner sk-hgbt-log --runs-stoch 30 --runs-other 20 \
    --bootstrap 1000 --seed 0 --out-prefix artifacts/significance_linux_hgbt >> "$LOG" 2>&1
say "LINUX HGBT exit=$?"

say "C. RF all-metrics sweep (other families, secondary)"
KW artifacts/lsens_icse19_rf.csv   sk-rf-log icse19
KW artifacts/lsens_icpe20_rf.csv   sk-rf-log x264
KW artifacts/lsens_energy_rf.csv   sk-rf-log twins    --seeds 10 --systems $ESYS
KW artifacts/lsens_lcbench_rf.csv  sk-rf-raw lcbench  --seeds 10
KW artifacts/lsens_workload_rf.csv sk-rf-log workload --seeds 10

say "D. CART all-metrics sweep (other families, 3rd learner)"
KW artifacts/lsens_icse19_cart.csv   cart-log icse19
KW artifacts/lsens_icpe20_cart.csv   cart-log x264
KW artifacts/lsens_energy_cart.csv   cart-log twins    --seeds 10 --systems $ESYS
KW artifacts/lsens_lcbench_cart.csv  cart-raw lcbench  --seeds 10
KW artifacts/lsens_workload_cart.csv cart-log workload --seeds 10

say "ALL DONE"
