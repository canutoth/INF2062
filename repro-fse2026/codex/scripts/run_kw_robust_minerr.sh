#!/bin/zsh
cd /Users/mathieuacher/SANDBOX/cost-sampling-matters
L=artifacts/kw_robust_minerr.log; PY=.venv-linux/bin/python
echo "=== KW robust minerr started $(date) ===" >> $L
for fam in icse19 x264 workload; do
  echo "--- $fam $(date) ---" >> $L
  $PY scripts/kw_cost_vs_size.py --mode $fam --budget-policy minerr --membership-bootstrap 1000 \
      --out artifacts/kw_robust_minerr_$fam.csv >> $L 2>&1
done
echo "=== DONE $(date) ===" >> $L
