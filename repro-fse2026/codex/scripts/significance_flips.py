#!/usr/bin/env python3
"""Significance of RQ2 decision flips via test-set + seed bootstrap.

For each scenario (system x cost x target) and each accuracy-cost weight lambda,
we recompute the count-cost and measured-cost winners over ORDINARY strategies
(matching the paper), flag flips, and bootstrap whether the flip *reproduces*
under resampling of (a) the held-out evaluation configurations and (b) the
random seed for stochastic strategies.

DESIGN NOTES
- Seeds: 30 stochastic seeds per (strategy, budget). pairwise/diversity are
  deterministic by construction (1 sample); for them only the eval set is
  resampled. This is why we use a test-set bootstrap rather than seed-only
  resampling -- it gives a uniform significance axis for both kinds.
- Winner uses J = minmax(mre) + lambda * minmax(cost), argmin over (strategy,
  level), collapsed to the (strategy, level) point -- same objective as
  cost_sampling.analysis.rank_stability.
- A flip's pairwise sign is exact under fixed minmax ranges: for two points,
  sign(J(b)-J(a)) = (mre_b-mre_a)/Rmre + lam*(cost_b-cost_a)/Rcost, so we hold
  Rmre/Rcost (and Rn) at their median-candidate-set values and bootstrap the
  per-point mre/cost. p_reproduce = fraction of bootstrap replicates where the
  count side still prefers the count-winner AND the measured side prefers the
  measured-winner.
"""
import argparse, csv, json, sys
from pathlib import Path
import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from cost_sampling.generated_sampling import (
    load_twins_table, build_generated_dataset, budget_grid,
)
from cost_sampling.metrics import fit_learner, predict
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sig_core import median_decision_flips, flips_both, LAMBDAS

ORD = ["random", "balanced", "diversity", "pairwise", "pilotCost"]
DET = {"pairwise", "diversity"}
LAMBDAS = [0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 10.0]
COMBOS = [("performance", "performance"), ("performance", "energy"),
          ("energy", "energy"), ("energy", "performance")]


def rel_err(y_true, y_pred):
    return np.abs(y_true - y_pred) / np.maximum(np.abs(y_true), 1e-12)


def eval_scenario(table, cost_prop, target_prop, budgets, seeds, learner, alpha, rng, eval_cap,
                  cost_orientation="lower"):
    """Per (strategy,level): err vectors aligned to a fixed evaluation pool, plus train idx, cost, pct_n.

    To bound time/memory on large systems we evaluate MRE on a fixed random
    holdout of min(N, eval_cap) configurations (drawn once per scenario). Each
    sample's own training points falling in the pool are masked out per sample.
    """
    ds = build_generated_dataset(table, target_property=target_prop, cost_property=cost_prop,
                                 cost_orientation=cost_orientation,
                                 budgets=budgets, seeds=seeds, include_oracles=False)
    X, y, cost_values, full_cost = ds.X, ds.y, ds.cost_values, ds.full_cost
    N = len(y)
    if eval_cap and N > eval_cap:
        pool = np.sort(rng.choice(N, size=eval_cap, replace=False))
    else:
        pool = np.arange(N)
    Xp, yp = X[pool], y[pool]
    pos = {int(g): i for i, g in enumerate(pool)}  # global idx -> pool position
    cells = {}  # (strat,level) -> dict(errs=[vec over pool], valid=[bool mask], pct_cost=[], pct_n)
    for s in ds.samples:
        if s.ref.strategy not in ORD:
            continue
        idx = np.array(sorted(set(int(i) for i in s.indices)), dtype=int)
        model = fit_learner(X[idx], y[idx], learner=learner, alpha=alpha)
        err = rel_err(yp, predict(model, Xp))  # error over the fixed pool
        valid = np.ones(len(pool), dtype=bool)
        for g in idx:
            if g in pos:
                valid[pos[g]] = False
        key = (s.ref.strategy, s.ref.level)
        c = cells.setdefault(key, {"errs": [], "valid": [], "pct_cost": [], "pct_n": len(idx) / N})
        c["errs"].append(err)
        c["valid"].append(valid)
        c["pct_cost"].append(float(np.sum(cost_values[idx])) / full_cost)
    return cells, len(pool)


def median_mre(cell):
    vals = [float(err[valid].mean()) for err, valid in zip(cell["errs"], cell["valid"])]
    return float(np.median(vals))


def analyze_system(system, table, seeds, B, learner, alpha, rng, eval_cap):
    budgets = budget_grid(len(table.rows))
    flips = []
    for cost_prop, target_prop in COMBOS:
        cells, L = eval_scenario(table, cost_prop, target_prop, budgets, seeds, learner, alpha, rng, eval_cap)
        for f in flips_both(cells, system, B, rng):
            f["cost"] = cost_prop; f["target"] = target_prop
            f["det"] = (f["cw"].split("@")[0] in DET) or (f["mw"].split("@")[0] in DET)
            flips.append(f)
    return flips


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", default="/tmp/twins_main.zip")
    ap.add_argument("--systems", nargs="+", required=True)
    ap.add_argument("--seeds", type=int, default=30)
    ap.add_argument("--bootstrap", type=int, default=1000)
    ap.add_argument("--learner", default="ridge-log")
    ap.add_argument("--alpha", type=float, default=1.0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--eval-cap", type=int, default=6000, help="Max held-out configs for MRE/bootstrap (0=full).")
    ap.add_argument("--out", default="artifacts/significance_flips.csv")
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    # revisions to match the paper's revision-pinned systems
    REVISION = {"brotli": {"revision": "1.0.7"}, "PostgreSQL": {"revision": "11.2"}}
    all_flips = []
    for system in args.systems:
        try:
            table = load_twins_table(args.zip, system, where=REVISION.get(system))
        except Exception as e:
            print(f"skip {system}: {e}", flush=True); continue
        fl = analyze_system(system, table, args.seeds, args.bootstrap, args.learner, args.alpha, rng, args.eval_cap)
        all_flips.extend(fl)
        med = [f for f in fl if f["agg"] == "median"]
        print(f"{system}: {len(med)} flips (median) | on-avg(p>.5)={sum(f['p_reproduce']>0.5 for f in med)} "
              f"sig(p>=.95)={sum(f['p_reproduce']>=0.95 for f in med)}", flush=True)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(all_flips[0].keys()) if all_flips else
                           ["system","cost","target","lam","kind","cw","mw","det","p_reproduce","dMRE_pct","dCost_pct"])
        w.writeheader(); w.writerows(all_flips)
    print(f"\n=== seeds={args.seeds}, bootstrap={args.bootstrap} ===")
    for agg in ("mean", "median"):
        g = [f for f in all_flips if f["agg"] == agg]
        if not g:
            continue
        onavg = sum(f["p_reproduce"] > 0.5 for f in g)
        sig = sum(f["p_reproduce"] >= 0.95 for f in g)
        print(f"agg={agg:>6}: {len(g)} flips | flips-on-average(p>.5)={onavg} ({onavg/len(g)*100:.0f}%) | "
              f"significant(p>=.95)={sig} ({sig/len(g)*100:.0f}%)")
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
