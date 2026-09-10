#!/usr/bin/env python3
"""Linux learner bakeoff on ONE (small) release: which learner actually fits Linux
binary size? Tests ridge, RF(sqrt) [current], RF(all-features) [hypothesis: sqrt
starves the additive size fn], HGBT, GBT — at the experiment's sampling fractions.
Target: prior works ~5-8%. log-target everywhere (predict log y, exp back)."""
import numpy as np, sys, time
sys.path.insert(0, "."); sys.path.insert(0, "scripts")
from cost_sampling.linux_data import load_linux_dataset
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge

rel = sys.argv[1] if len(sys.argv) > 1 else "420"
TOPK = None if (len(sys.argv) > 2 and sys.argv[2] in ("all", "none", "None")) else 512
FRACS = [0.01, 0.05, 0.20]
ds = load_linux_dataset(f"ICPE-rawdata/linux/tuxkconfig_{rel}.parquet", context=f"linux{rel}", top_k_features=TOPK)
X, y = np.asarray(ds.X, float), np.asarray(ds.y, float)
N = len(y); rng = np.random.default_rng(0)
pool = np.sort(rng.choice(N, size=min(5000, N), replace=False))
Xp, yp = X[pool], y[pool]
print(f"linux{rel}: N={N}  features={X.shape[1]}  holdout={len(pool)}\n", flush=True)

def mre(t, p): return float(np.mean(np.abs(t - p) / np.maximum(np.abs(t), 1e-12)))

LEARNERS = {
    "ridge(alpha=1)":   lambda: Ridge(alpha=1.0),
    "RF(sqrt)[current]": lambda: RandomForestRegressor(n_estimators=200, max_features="sqrt", n_jobs=-1, random_state=1729),
    "RF(all-features)":  lambda: RandomForestRegressor(n_estimators=200, max_features=None, n_jobs=-1, random_state=1729),
    "RF(max_feat=0.5)":  lambda: RandomForestRegressor(n_estimators=200, max_features=0.5, n_jobs=-1, random_state=1729),
    "HGBT":              lambda: HistGradientBoostingRegressor(max_iter=300, learning_rate=0.08, max_leaf_nodes=31, random_state=4242),
    "GBT(classic)":      lambda: GradientBoostingRegressor(n_estimators=300, learning_rate=0.05, max_depth=5, subsample=0.8, max_features="sqrt", random_state=4242),
}
for name, factory in LEARNERS.items():
    for frac in FRACS:
        n = int(frac * N)
        idx = rng.choice(N, size=n, replace=False)
        t0 = time.time()
        est = factory(); est.fit(X[idx], np.log(y[idx]))
        pred = np.exp(est.predict(Xp))
        print(f"  {name:20s} frac={frac*100:4.0f}% n={n:6d}: MRE={mre(yp, pred)*100:5.1f}%  ({time.time()-t0:4.0f}s)", flush=True)
    print(flush=True)
print("DONE", flush=True)
