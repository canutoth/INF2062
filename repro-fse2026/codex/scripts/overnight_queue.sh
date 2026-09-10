#!/bin/bash
# Overnight work queue — runs everything remaining sequentially so the machine never
# idles. Order: (0) wait for the in-flight ridge+RF all-metrics sweep, (1) Linux RF,
# (2) CART all-metrics sweep for the 5 KW families [3rd learner, bonus], (3) Linux CART.
# Each step is independent (no set -e): a failure logs and the queue continues.
# Prereqs already running: caffeinate (no sleep) + learner_sensitivity_allmetrics.sh.
cd /Users/mathieuacher/SANDBOX/cost-sampling-matters
PY=.venv-linux/bin/python
LOG=/tmp/overnight_queue.log
ESYS="7z Apache brotli exastencils HSQLDB jump3r kanzi LLVM lrzip MongoDB nginx PostgreSQL VP8 x264"
say () { echo -e "\n######## $1 ($(date '+%m-%d %H:%M:%S')) ########" >> "$LOG"; }
: > "$LOG"

say "0. waiting for ridge+RF all-metrics sweep to finish"
while pgrep -f learner_sensitivity_allmetrics >/dev/null; do sleep 120; done
say "sweep finished"

say "1. LINUX RF (all 3 metrics)"
$PY scripts/significance_linux.py --learner sk-rf-log --runs-stoch 30 --runs-other 20 \
    --bootstrap 1000 --seed 0 --out-prefix artifacts/significance_linux_rf >> "$LOG" 2>&1
say "linux RF exit=$?"

say "2. CART all-metrics sweep (5 families, 3rd learner)"
$PY scripts/kw_cost_vs_size.py --mode icse19   --learner cart-log --all-metrics \
    --out artifacts/lsens_icse19_cart.csv   >> "$LOG" 2>&1; say "icse19 cart exit=$?"
$PY scripts/kw_cost_vs_size.py --mode x264     --learner cart-log --all-metrics \
    --out artifacts/lsens_icpe20_cart.csv   >> "$LOG" 2>&1; say "x264 cart exit=$?"
$PY scripts/kw_cost_vs_size.py --mode twins    --learner cart-log --all-metrics --seeds 10 \
    --systems $ESYS --out artifacts/lsens_energy_cart.csv >> "$LOG" 2>&1; say "energy cart exit=$?"
$PY scripts/kw_cost_vs_size.py --mode lcbench  --learner cart-raw --all-metrics --seeds 10 \
    --out artifacts/lsens_lcbench_cart.csv  >> "$LOG" 2>&1; say "lcbench cart exit=$?"
$PY scripts/kw_cost_vs_size.py --mode workload --learner cart-log --all-metrics --seeds 10 \
    --out artifacts/lsens_workload_cart.csv >> "$LOG" 2>&1; say "workload cart exit=$?"

say "3. LINUX CART (all 3 metrics)"
$PY scripts/significance_linux.py --learner cart-log --runs-stoch 30 --runs-other 20 \
    --bootstrap 1000 --seed 0 --out-prefix artifacts/significance_linux_cart >> "$LOG" 2>&1
say "linux CART exit=$?"

say "ALL OVERNIGHT WORK DONE"
