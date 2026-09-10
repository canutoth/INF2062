#!/usr/bin/env python3
"""Significance of RQ2 flips for the REPLICATION families (ICPE archives).

Same bootstrap core as scripts/significance_flips.py, but samples come from the
real sampling-run archives (AllRuns/NewRuns) via load_runs_dataset -- each
(strategy, level) has multiple real run_ids that serve as the seed-resampling
pool, on top of the test-set bootstrap. Cost = measured performance of the
sampled configs (cost_values); count cost = n/|C|.
"""
import argparse, csv, sys
from pathlib import Path
from collections import defaultdict
import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from cost_sampling.archive_runs import load_runs_dataset
from cost_sampling.metrics import fit_learner, predict
from sig_core import median_decision_flips, flips_both, LAMBDAS


def rel_err(yt, yp):
    return np.abs(yt - yp) / np.maximum(np.abs(yt), 1e-12)


def eval_dataset(ds, learner, alpha, rng, eval_cap):
    X, y, cost_values, full_cost = ds.X, ds.y, ds.cost_values, ds.full_cost
    N = len(y)
    pool = np.sort(rng.choice(N, size=eval_cap, replace=False)) if (eval_cap and N > eval_cap) else np.arange(N)
    Xp, yp = X[pool], y[pool]
    posmap = {int(g): i for i, g in enumerate(pool)}
    cells = {}
    for s in ds.samples:
        idx = np.array(sorted(set(int(i) for i in s.indices)), dtype=int)
        if len(idx) == 0 or len(idx) >= N:
            continue
        model = fit_learner(X[idx], y[idx], learner=learner, alpha=alpha)
        err = rel_err(yp, predict(model, Xp))
        valid = np.ones(len(pool), dtype=bool)
        for g in idx:
            if g in posmap:
                valid[posmap[g]] = False
        key = (s.ref.strategy, s.ref.level)
        c = cells.setdefault(key, {"errs": [], "valid": [], "pct_cost": [], "pct_n": []})
        c["errs"].append(err); c["valid"].append(valid)
        c["pct_cost"].append(float(np.sum(cost_values[idx])) / full_cost)
        c["pct_n"].append(len(idx) / N)
    return cells


def flips(cells, context, B, rng):
    return flips_both(cells, context, B, rng)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", default="ICPE-rawdata/NewRuns.zip")
    ap.add_argument("--contexts", nargs="+", required=True)
    ap.add_argument("--bootstrap", type=int, default=1000)
    ap.add_argument("--learner", default="ridge-log")
    ap.add_argument("--alpha", type=float, default=1.0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--eval-cap", type=int, default=6000)
    ap.add_argument("--max-runs", type=int, default=None)
    ap.add_argument("--out", default="artifacts/significance_flips_replication.csv")
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    allf = []
    for ctx in args.contexts:
        try:
            ds = load_runs_dataset(args.zip, ctx, max_runs=args.max_runs)
        except Exception as e:
            print(f"skip {ctx}: {e}", flush=True); continue
        cells = eval_dataset(ds, args.learner, args.alpha, rng, args.eval_cap)
        nruns = {k: len(cells[k]["errs"]) for k in cells}
        fl = flips(cells, ctx, args.bootstrap, rng)
        allf.extend(fl)
        rob = sum(f["p_reproduce"] >= 0.95 for f in fl)
        print(f"{ctx}: {len(cells)} (strat,level) cells, runs/cell~{np.median(list(nruns.values())):.0f}, "
              f"{len(fl)} flips, {rob} robust (p>=0.95)", flush=True)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(allf[0].keys()) if allf else
                           ["system","lam","kind","cw","mw","p_reproduce","dMRE_pct","dCost_pct"])
        w.writeheader(); w.writerows(allf)
    n = len(allf)
    if n:
        rob = sum(f["p_reproduce"] >= 0.95 for f in allf)
        ps = np.array([f["p_reproduce"] for f in allf])
        print(f"\n=== bootstrap={args.bootstrap} ===\ntotal flips: {n}")
        print(f"  robust (p>=0.95): {rob} ({rob/n*100:.0f}%)   median p={np.median(ps):.2f}")
        print(f"  p<.5: {(ps<.5).sum()}  .5-.95: {((ps>=.5)&(ps<.95)).sum()}  >=.95: {(ps>=.95).sum()}")
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
