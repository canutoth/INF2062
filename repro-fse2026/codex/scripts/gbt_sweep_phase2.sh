#!/bin/bash
# Operational continuation of gbt_learner_sensitivity_sweep.sh for THIS run only:
# phase-1 already started icse19 (left running); this resumes with x264 (full) then
# the generated families at --seeds 10. Waits for icse19 so only one GBT job runs at a
# time (alongside the separate Linux-HGBT job). The canonical reproducible script is
# gbt_learner_sensitivity_sweep.sh; this file just avoids re-running icse19.
set -u
cd /Users/mathieuacher/SANDBOX/cost-sampling-matters
PY=.venv-linux/bin/python
LOG=/tmp/gbt_kw_phase2.log
: > "$LOG"
run () { echo -e "\n>>> $1 ($(date +%H:%M:%S))" >> "$LOG"; shift; "$@" >> "$LOG" 2>&1; echo "exit=$?" >> "$LOG"; }

echo "waiting for icse19 CSV (phase-1 still finishing it)..." >> "$LOG"
while [ ! -f artifacts/kw_cost_vs_size_icse19_hgbt.csv ]; do sleep 30; done
echo "icse19 done -> starting x264 ($(date +%H:%M:%S))" >> "$LOG"

run x264    $PY scripts/kw_cost_vs_size.py --mode x264 --learner sk-hgbt-log \
    --out artifacts/kw_cost_vs_size_icpe20_hgbt.csv
run energy  $PY scripts/kw_cost_vs_size.py --mode twins --learner sk-hgbt-log --seeds 10 \
    --systems 7z Apache brotli exastencils HSQLDB jump3r kanzi LLVM lrzip MongoDB nginx PostgreSQL VP8 x264 \
    --out artifacts/kw_cost_vs_size_energy_hgbt.csv
run lcbench $PY scripts/kw_cost_vs_size.py --mode lcbench --learner sk-hgbt-raw --seeds 10 \
    --out artifacts/kw_cost_vs_size_lcbench_hgbt.csv
run workload $PY scripts/kw_cost_vs_size.py --mode workload --learner sk-hgbt-log --seeds 10 \
    --out artifacts/kw_cost_vs_size_workload_hgbt.csv
echo -e "\n=== phase2 DONE ($(date +%H:%M:%S)) ===" >> "$LOG"
