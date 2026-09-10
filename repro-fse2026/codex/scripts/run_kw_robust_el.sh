#!/bin/zsh
cd /Users/mathieuacher/SANDBOX/cost-sampling-matters
L=artifacts/kw_robust_el.log; PY=.venv-linux/bin/python
echo "=== energy+lcbench robust minerr started $(date) ===" >> $L
echo "--- energy $(date) ---" >> $L
$PY scripts/kw_cost_vs_size.py --mode twins --zip /private/tmp/twins_main.zip \
    --budget-policy minerr --membership-bootstrap 1000 \
    --out artifacts/kw_robust_minerr_energy.csv >> $L 2>&1
echo "--- lcbench download $(date) ---" >> $L
mkdir -p /private/tmp/lcbench
curl -sL https://ndownloader.figshare.com/files/21188598 -o /private/tmp/lcbench/data_2k_lw.json
file /private/tmp/lcbench/data_2k_lw.json >> $L 2>&1; ls -la /private/tmp/lcbench/data_2k_lw.json >> $L 2>&1
echo "--- lcbench $(date) ---" >> $L
$PY scripts/kw_cost_vs_size.py --mode lcbench --zip /private/tmp/lcbench/data_2k_lw.json \
    --budget-policy minerr --membership-bootstrap 1000 \
    --out artifacts/kw_robust_minerr_lcbench.csv >> $L 2>&1
echo "=== DONE $(date) ===" >> $L
