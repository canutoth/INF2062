#!/bin/zsh
# Overnight Linux finisher: wait for the running full-feature HGBT job (PID 18025,
# building releases 413+415), then build the one missing release (507) and
# re-aggregate ALL 7 releases from cached cells into the corrected results.
cd /Users/mathieuacher/SANDBOX/cost-sampling-matters
LOG=artifacts/overnight_linux.log
PY=.venv-linux/bin/python
echo "=== overnight Linux orchestration started $(date) ===" >> $LOG

# 1. wait for the in-flight HGBT job (413+415) to finish so we don't thrash CPU
while kill -0 18025 2>/dev/null; do sleep 300; done
echo "$(date) PID 18025 finished. Cached HGBT cells present:" >> $LOG
ls -1 artifacts/significance_linux_hgbtfull_cells_*.pkl >> $LOG 2>&1

# 2. build the missing release (507) + reuse the other six, aggregate all seven
$PY scripts/significance_linux.py \
  --releases 413 415 420 500 504 507 508 --reuse-cells \
  --top-k-features 0 --learner sk-hgbt-log \
  --runs-stoch 15 --runs-other 10 --bootstrap 1000 --seed 0 --eval-cap 4000 \
  --out-prefix artifacts/significance_linux_hgbtfull >> $LOG 2>&1
echo "$(date) 7-release corrected aggregate written" >> $LOG

# 3. old-vs-corrected comparison summary
$PY - >> $LOG 2>&1 <<'PY'
import csv
def summ(f):
    rows=list(csv.DictReader(open(f)))
    gc=sum(1 for r in rows if str(r.get('group_changed','')).lower() in ('true','1'))
    ch=sum(1 for r in rows if str(r.get('changed','')).lower() in ('true','1'))
    return len(rows),ch,gc
print("\n===== LINUX: OLD (crippled 512-feat ridge) vs CORRECTED (full-feat HGBT) =====")
for tag,f in [('OLD       ','artifacts/significance_linux_kw.csv'),
              ('CORRECTED ','artifacts/significance_linux_hgbtfull_kw.csv')]:
    try:
        n,ch,gc=summ(f); print(f'{tag} KW: {n} comps | best-sampler {ch} ({round(100*ch/max(n,1))}%) | top-group {gc} ({round(100*gc/max(n,1))}%)')
    except Exception as e: print(f'{tag} {e}')
try:
    pr=list(csv.DictReader(open('artifacts/significance_linux_hgbtfull_pareto.csv')))
    dif=sum(1 for r in pr if float(r.get('p_differ',0))>=0.95)
    print(f'CORRECTED Pareto: {dif}/{len(pr)} releases robustly differ (p>=.95); jaccards=', [round(float(r["jaccard"]),2) for r in pr])
    mre=list(csv.DictReader(open('artifacts/significance_linux_hgbtfull_mre.csv')))
    import statistics as st
    by20=[float(r['median_mre']) for r in mre if abs(float(r['level'])-0.20)<1e-9]
    if by20: print(f'CORRECTED MRE @20% budget: median {round(100*st.median(by20))}%  (sanity: should be ~7-10%, not ~30%)')
except Exception as e: print('pareto/mre:', e)
PY
echo "$(date) OVERNIGHT LINUX DONE" >> $LOG
