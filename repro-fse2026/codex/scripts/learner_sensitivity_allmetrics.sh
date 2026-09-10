#!/bin/bash
# Learning-algorithm sensitivity across ALL THREE metrics (KW top-group, top-1 flip,
# Pareto choice-set) for every non-Linux family, under ridge-log AND Random Forest,
# via kw_cost_vs_size.py --all-metrics (builds cells ONCE per family, emits all three:
# <out>.csv = KW, <out>_flip.csv, <out>_pareto.csv). Matched code path => clean
# ridge-vs-RF comparison. GBT/HGBT omitted (does not scale: ~24x slower per fit).
# Linux is covered separately by significance_linux.py (ridge done; RF to run).
# Ridge runs first (fast) to land the full baseline; RF second (the time cost).
# Replications use the archives' ~100 real runs; generated families use --seeds 10.
set -u
cd /Users/mathieuacher/SANDBOX/cost-sampling-matters
PY=.venv-linux/bin/python
LOG=/tmp/lsens_am.log
: > "$LOG"
run () { echo -e "\n>>> $1 ($(date +%H:%M:%S))" >> "$LOG"; shift; "$@" >> "$LOG" 2>&1; echo "exit=$?" >> "$LOG"; }
ESYS="7z Apache brotli exastencils HSQLDB jump3r kanzi LLVM lrzip MongoDB nginx PostgreSQL VP8 x264"

for spec in "ridge-log:ridge-raw:ridge" "sk-rf-log:sk-rf-raw:rf"; do
  LOGl=${spec%%:*}; rest=${spec#*:}; RAW=${rest%%:*}; tag=${rest##*:}
  run "icse19-$tag"   $PY scripts/kw_cost_vs_size.py --mode icse19   --learner $LOGl --all-metrics \
      --out artifacts/lsens_icse19_${tag}.csv
  run "x264-$tag"     $PY scripts/kw_cost_vs_size.py --mode x264     --learner $LOGl --all-metrics \
      --out artifacts/lsens_icpe20_${tag}.csv
  run "energy-$tag"   $PY scripts/kw_cost_vs_size.py --mode twins    --learner $LOGl --all-metrics --seeds 10 \
      --systems $ESYS --out artifacts/lsens_energy_${tag}.csv
  run "lcbench-$tag"  $PY scripts/kw_cost_vs_size.py --mode lcbench  --learner $RAW  --all-metrics --seeds 10 \
      --out artifacts/lsens_lcbench_${tag}.csv
  run "workload-$tag" $PY scripts/kw_cost_vs_size.py --mode workload --learner $LOGl --all-metrics --seeds 10 \
      --out artifacts/lsens_workload_${tag}.csv
done
echo -e "\n=== lsens all-metrics DONE ($(date +%H:%M:%S)) ===" >> "$LOG"
