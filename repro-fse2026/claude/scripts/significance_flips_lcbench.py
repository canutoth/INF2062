#!/usr/bin/env python3
"""Flip-significance for the LCBENCH family (OpenML datasets, real-runtime HPO).

One context per OpenML dataset (exposed as 'workload'); target=final_val_accuracy,
cost=time_total, learner=ridge-raw (accuracy is bounded, no log target). Reuses the
generated eval + shared median/mean-decision core. LCBench is external-validation
scope (see significance_decisions.md C5) but kept in per the user.
"""
import argparse, csv, sys
from pathlib import Path
from collections import defaultdict
import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO)); sys.path.insert(0, str(REPO / "scripts"))
from cost_sampling.generated_sampling import load_lcbench_table, subset_measured_table, budget_grid
from significance_flips import eval_scenario
from sig_core import flips_both


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default="/private/tmp/lcbench/data_2k_lw.json")
    ap.add_argument("--target", default="final_val_accuracy")
    ap.add_argument("--cost", default="time_total")
    ap.add_argument("--learner", default="ridge-raw")
    ap.add_argument("--seeds", type=int, default=30)
    ap.add_argument("--bootstrap", type=int, default=1000)
    ap.add_argument("--eval-cap", type=int, default=6000)
    ap.add_argument("--limit", type=int, default=0, help="process only first N datasets (0=all)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="artifacts/significance_flips_lcbench.csv")
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    print("loading LCBench JSON (large)…", flush=True)
    table = load_lcbench_table(args.json)
    grouped = defaultdict(list)
    for i, row in enumerate(table.rows):
        grouped[row.get("workload", "all")].append(i)
    datasets = sorted(grouped)
    if args.limit:
        datasets = datasets[:args.limit]
    print(f"{len(datasets)} datasets", flush=True)
    allf = []
    for ds in datasets:
        subset = subset_measured_table(table, grouped[ds], analysis_name=ds)
        budgets = budget_grid(len(subset.rows))
        if not budgets:
            continue
        cells, _ = eval_scenario(subset, args.cost, args.target, budgets, args.seeds,
                                 args.learner, 1.0, rng, args.eval_cap)
        for f in flips_both(cells, ds, args.bootstrap, rng):
            f["dataset"] = ds
            allf.append(f)
        med = [f for f in allf if f.get("dataset") == ds and f["agg"] == "median"]
        print(f"{ds}: {len(med)} flips(median) on-avg={sum(x['p_reproduce']>0.5 for x in med)} "
              f"sig={sum(x['p_reproduce']>=0.95 for x in med)}", flush=True)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    if allf:
        cols = ["dataset", "agg", "lam", "kind", "cw", "mw", "p_reproduce", "dMRE_pct", "dCost_pct"]
        with open(args.out, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(allf)
    for agg in ("mean", "median"):
        g = [f for f in allf if f["agg"] == agg]
        if g:
            print(f"agg={agg:>6}: {len(g)} flips | on-avg(p>.5)={sum(f['p_reproduce']>0.5 for f in g)} | sig(p>=.95)={sum(f['p_reproduce']>=0.95 for f in g)}")
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
