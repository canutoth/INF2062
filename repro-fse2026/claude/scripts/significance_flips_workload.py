#!/usr/bin/env python3
"""Flip-significance for the WORKLOAD family (ICSE 2023 workload-impact archive).

One context per (system, workload), target=cost=time (symmetric perf/perf). Reuses
the generated eval (eval_scenario) and the shared median/mean-decision core.
"""
import argparse, csv, sys
from pathlib import Path
from collections import defaultdict
import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO)); sys.path.insert(0, str(REPO / "scripts"))
from cost_sampling.generated_sampling import load_workload_table, subset_measured_table, budget_grid
from significance_flips import eval_scenario
from sig_core import flips_both

WL_SYSTEMS = ["batik", "dconvert", "h2", "jump3r", "kanzi", "lrzip", "x264", "xz", "z3"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", default="workload-impact-ICSE2023/artifact_excluding_raw_coverage.zip")
    ap.add_argument("--systems", nargs="+", default=WL_SYSTEMS)
    ap.add_argument("--column", default="time", help="target=cost column")
    ap.add_argument("--seeds", type=int, default=30)
    ap.add_argument("--bootstrap", type=int, default=1000)
    ap.add_argument("--learner", default="ridge-log")
    ap.add_argument("--eval-cap", type=int, default=6000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="artifacts/significance_flips_workload.csv")
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    allf = []
    for system in args.systems:
        try:
            table = load_workload_table(args.zip, system)
        except Exception as e:
            print(f"skip {system}: {e}", flush=True); continue
        # detect the measured metric column per system (time, else throughput, else first label)
        labels = [c for c in table.label_columns if c != "config_id"]
        col = "time" if "time" in labels else ("throughput" if "throughput" in labels else (labels[0] if labels else None))
        if col is None:
            print(f"skip {system}: no metric column in {table.label_columns}", flush=True); continue
        orientation = "inverse" if col == "throughput" else "lower"  # throughput is benefit-like
        grouped = defaultdict(list)
        for i, row in enumerate(table.rows):
            grouped[row.get("workload", "all")].append(i)
        nctx = 0
        for workload, idxs in sorted(grouped.items()):
            subset = subset_measured_table(table, idxs, analysis_name=f"{system}-{workload}")
            budgets = budget_grid(len(subset.rows))
            if not budgets:
                continue
            try:
                cells, _ = eval_scenario(subset, col, col, budgets, args.seeds,
                                         args.learner, 1.0, rng, args.eval_cap, cost_orientation=orientation)
            except Exception as e:
                print(f"  skip {system}/{workload}: {e}", flush=True); continue
            for f in flips_both(cells, f"{system}|{workload}", args.bootstrap, rng):
                f["system"] = system; f["workload"] = workload
                allf.append(f)
            nctx += 1
        med = [f for f in allf if f.get("system") == system and f["agg"] == "median"]
        print(f"{system}: {nctx} workloads | {len(med)} flips(median) "
              f"on-avg={sum(x['p_reproduce']>0.5 for x in med)} sig={sum(x['p_reproduce']>=0.95 for x in med)}", flush=True)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    if allf:
        cols = ["system", "workload", "agg", "lam", "kind", "cw", "mw", "p_reproduce", "dMRE_pct", "dCost_pct"]
        with open(args.out, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(allf)
    for agg in ("mean", "median"):
        g = [f for f in allf if f["agg"] == agg]
        if g:
            print(f"agg={agg:>6}: {len(g)} flips | on-avg(p>.5)={sum(f['p_reproduce']>0.5 for f in g)} | sig(p>=.95)={sum(f['p_reproduce']>=0.95 for f in g)}")
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
