#!/bin/zsh
cd /Users/mathieuacher/SANDBOX/cost-sampling-matters
L=artifacts/kw_robust.log; PY=.venv-linux/bin/python
echo "=== KW robustness (R1#1/2/3) started $(date) ===" >> $L
for fam in icse19 x264; do
  echo "--- $fam $(date) ---" >> $L
  $PY scripts/kw_cost_vs_size.py --mode $fam --membership-bootstrap 1000 \
      --out artifacts/kw_robust_$fam.csv >> $L 2>&1
done
echo "=== KW robustness replications DONE $(date) ===" >> $L
