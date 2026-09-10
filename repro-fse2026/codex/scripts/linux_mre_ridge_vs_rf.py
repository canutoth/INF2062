#!/usr/bin/env python3
"""Does RF fix Linux MRE? Direct check on one release: sample at the experiment's
fractions, fit ridge-log and sk-rf-log on the SAME sample, MRE on a held-out pool.
Prior works: trees ~5-8% on Linux size, linear ~30%+. Expect RF << ridge here."""
import numpy as np, sys, time
sys.path.insert(0, "."); sys.path.insert(0, "scripts")
from cost_sampling.linux_data import load_linux_dataset
from cost_sampling.metrics import fit_learner, predict

rel = sys.argv[1] if len(sys.argv) > 1 else "420"
LEARNERS = sys.argv[2].split(",") if len(sys.argv) > 2 else ["ridge-log", "sk-rf-log"]
REPS = int(sys.argv[3]) if len(sys.argv) > 3 else 2
FRACS = [0.01, 0.05, 0.10, 0.20]
ds = load_linux_dataset(f"ICPE-rawdata/linux/tuxkconfig_{rel}.parquet", context=f"linux{rel}")
X, y = np.asarray(ds.X, float), np.asarray(ds.y, float)
N = len(y); rng = np.random.default_rng(0)
ECAP = 5000
pool = np.sort(rng.choice(N, size=min(ECAP, N), replace=False))
Xp, yp = X[pool], y[pool]; pset = set(pool.tolist())
print(f"linux{rel}: N={N}  features={X.shape[1]}  (holdout {len(pool)}) learners={LEARNERS}", flush=True)
for frac in FRACS:
    n = int(frac * N)
    for lr in LEARNERS:
        mres = []; t0 = time.time()
        for _ in range(2):
            idx = rng.choice(N, size=n, replace=False)
            m = fit_learner(X[idx], y[idx], learner=lr)
            p = predict(m, Xp)
            mres.append(float(np.mean(np.abs(yp - p) / np.maximum(np.abs(yp), 1e-12))))
        print(f"  frac={frac*100:4.0f}%  n={n:6d}  {lr:11s}: MRE={np.mean(mres)*100:5.1f}%   ({(time.time()-t0)/2:.0f}s/fit)", flush=True)
print("DONE", flush=True)
