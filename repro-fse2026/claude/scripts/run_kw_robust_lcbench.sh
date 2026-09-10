#!/bin/zsh
cd /Users/mathieuacher/SANDBOX/cost-sampling-matters
L=artifacts/kw_robust_lcbench.log; PY=.venv-linux/bin/python
echo "=== lcbench extract+robust started $(date) ===" >> $L
mkdir -p /private/tmp/lcbench_x
unzip -o artifacts/_lcbench/dl.bin -d /private/tmp/lcbench_x >> $L 2>&1
JSON=$(find /private/tmp/lcbench_x -name "*.json" | head -1)
echo "json: $JSON ($(du -h $JSON 2>/dev/null | cut -f1))" >> $L
$PY scripts/kw_cost_vs_size.py --mode lcbench --zip "$JSON" --budget-policy minerr \
    --membership-bootstrap 1000 --out artifacts/kw_robust_minerr_lcbench.csv >> $L 2>&1
rm -f artifacts/_lcbench/dl.bin
echo "=== lcbench DONE $(date) ===" >> $L
