#!/usr/bin/env python3
"""Bootstrapped Pareto choice-set significance for the GENERATED families
(energy / workload / lcbench). One row per scenario (lambda-free). Reuses
eval_scenario + sig_core.pareto_choiceset."""
import argparse, csv, sys
from pathlib import Path
from collections import defaultdict
import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO)); sys.path.insert(0, str(REPO / "scripts"))
from cost_sampling.generated_sampling import (load_twins_table, load_workload_table, load_lcbench_table,
                                              subset_measured_table, budget_grid)
from significance_flips import eval_scenario
from sig_core import pareto_choiceset

ENERGY_SYS = ["7z", "Apache", "brotli", "exastencils", "HSQLDB", "jump3r", "kanzi", "LLVM",
              "lrzip", "MongoDB", "nginx", "PostgreSQL", "VP8", "x264"]
WL_SYS = ["batik", "dconvert", "h2", "jump3r", "kanzi", "lrzip", "x264", "xz", "z3"]
COMBOS = [("performance", "performance"), ("performance", "energy"),
          ("energy", "energy"), ("energy", "performance")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", choices=["energy", "workload", "lcbench"], required=True)
    ap.add_argument("--zip", default=None)
    ap.add_argument("--seeds", type=int, default=30)
    ap.add_argument("--bootstrap", type=int, default=1000)
    ap.add_argument("--eval-cap", type=int, default=6000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    rows = []

    if args.family == "energy":
        zp = args.zip or "/tmp/twins_main.zip"
        REV = {"brotli": {"revision": "1.0.7"}, "PostgreSQL": {"revision": "11.2"}}
        for s in ENERGY_SYS:
            try:
                table = load_twins_table(zp, s, where=REV.get(s))
            except Exception as e:
                print(f"skip {s}: {e}", flush=True); continue
            budgets = budget_grid(len(table.rows))
            for cost_p, target_p in COMBOS:
                try:
                    cells, _ = eval_scenario(table, cost_p, target_p, budgets, args.seeds, "ridge-log", 1.0, rng, args.eval_cap)
                    r = pareto_choiceset(cells, s, args.bootstrap, rng, agg="mean", combo=f"{cost_p[:4]}/{target_p[:4]}")
                    if r:
                        rows.append(r)
                except Exception as e:
                    print(f"  skip {s} {cost_p}/{target_p}: {e}", flush=True)
            print(f"{s}: done", flush=True)
    elif args.family == "workload":
        zp = args.zip or "workload-impact-ICSE2023/artifact_excluding_raw_coverage.zip"
        for s in WL_SYS:
            try:
                table = load_workload_table(zp, s)
            except Exception as e:
                print(f"skip {s}: {e}", flush=True); continue
            labels = [c for c in table.label_columns if c != "config_id"]
            col = "time" if "time" in labels else ("throughput" if "throughput" in labels else labels[0])
            orient = "inverse" if col == "throughput" else "lower"
            grouped = defaultdict(list)
            for i, row in enumerate(table.rows):
                grouped[row.get("workload", "all")].append(i)
            for wl, idxs in sorted(grouped.items()):
                subset = subset_measured_table(table, idxs, analysis_name=f"{s}-{wl}")
                budgets = budget_grid(len(subset.rows))
                if not budgets:
                    continue
                try:
                    cells, _ = eval_scenario(subset, col, col, budgets, args.seeds, "ridge-log", 1.0, rng,
                                             args.eval_cap, cost_orientation=orient)
                    r = pareto_choiceset(cells, f"{s}|{wl}", args.bootstrap, rng, agg="mean")
                    if r:
                        rows.append(r)
                except Exception as e:
                    print(f"  skip {s}/{wl}: {e}", flush=True)
            print(f"{s}: done", flush=True)
    else:  # lcbench
        jp = args.zip or "/private/tmp/lcbench/data_2k_lw.json"
        table = load_lcbench_table(jp)
        grouped = defaultdict(list)
        for i, row in enumerate(table.rows):
            grouped[row.get("workload", "all")].append(i)
        for ds, idxs in sorted(grouped.items()):
            subset = subset_measured_table(table, idxs, analysis_name=ds)
            budgets = budget_grid(len(subset.rows))
            if not budgets:
                continue
            try:
                cells, _ = eval_scenario(subset, "time_total", "final_val_accuracy", budgets, args.seeds,
                                         "ridge-raw", 1.0, rng, args.eval_cap)
                r = pareto_choiceset(cells, ds, args.bootstrap, rng, agg="mean")
                if r:
                    rows.append(r)
                    print(f"{ds}: jacc={r['jaccard']} p_differ={r['p_differ']:.2f}", flush=True)
            except Exception as e:
                print(f"  skip {ds}: {e}", flush=True)

    out = args.out or f"artifacts/significance_pareto_{args.family}.csv"
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    if rows:
        with open(out, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
        rob = sum(r["p_differ"] >= 0.95 for r in rows)
        print(f"\n{args.family.upper()} Pareto: {len(rows)} scenarios, choice-set robustly differs in "
              f"{rob} ({rob/len(rows)*100:.0f}%); median Jaccard={np.median([r['jaccard'] for r in rows]):.2f}")
    print(f"wrote {out}", flush=True)


if __name__ == "__main__":
    main()
