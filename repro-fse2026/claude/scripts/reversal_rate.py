#!/usr/bin/env python3
"""Non-monotone reversal rate (RQ1 mechanism iii: "a larger sample can be cheaper than a
smaller one"). Reviewer-requested concrete rate (R1 #3 / R2 A1).

We build the SAME per-(sampler, level) cells as kw_cost_vs_size.py and, per family, report:

  within_strategy : over (context, strategy, level_i < level_j by sample fraction n) pairs,
                    the fraction where the LARGER sample is CHEAPER (cost_j < cost_i).
                    Pure non-monotonicity of one strategy's own size->cost curve.
  cross_strategy  : over (context, A@n_A, B@n_B) ordered pairs with n_A > n_B and A != B,
                    the fraction where the larger sample A is cheaper than the smaller B.
                    This is the paper's mechanism: cost is strategy-dependent, so a bigger
                    sample of a cheap strategy undercuts a smaller sample of a pricey one.
  ctx_has_cross   : fraction of contexts with at least one such (larger-yet-cheaper) pair.

Costs/sizes are learner-independent medians (median pct_cost / pct_n across seeds), so the
numbers are stable. Run with .venv-linux/bin/python.
"""
import argparse, csv, sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path
import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO)); sys.path.insert(0, str(REPO / "scripts"))
from cost_sampling.archive_runs import load_runs_dataset, attach_cost_dataset
from significance_flips_archive import eval_dataset
from cost_sampling.generated_sampling import (load_twins_table, load_workload_table, load_lcbench_table,
                                              subset_measured_table, budget_grid)
from significance_flips import eval_scenario
from kw_cost_vs_size import per_cell_stats


def build_items(mode, learner, eval_cap, seeds, rng, target_prop="energy", inputs="0-16", systems=None):
    """Return list of (context_label, cells) mirroring kw_cost_vs_size.main()."""
    items, min_runs = [], 1
    if mode == "icse19":
        zp = "ICPE-rawdata/NewRuns.zip"
        for c in ["LLVM", "Polly", "Dune", "Hipacc", "lrzip", "7z", "BerkeleyDBC"]:
            try:
                items.append((c, eval_dataset(load_runs_dataset(zp, c), learner, 1.0, rng, eval_cap)))
            except Exception as e:
                print(f"skip {c}: {e}", flush=True)
    elif mode == "x264":
        zp = "ICPE-rawdata/AllRuns.zip"
        lo, hi = (int(x) for x in inputs.split("-"))
        for i in range(lo, hi + 1):
            try:
                sd = load_runs_dataset(zp, f"x264_size_{i}"); td = load_runs_dataset(zp, f"x264_time_{i}")
                items.append((f"x264_{i}", eval_dataset(attach_cost_dataset(sd, td), learner, 1.0, rng, eval_cap)))
            except Exception as e:
                print(f"skip x264_{i}: {e}", flush=True)
    elif mode == "twins":
        min_runs = 10
        zp = "/tmp/twins_main.zip"
        REVISION = {"brotli": {"revision": "1.0.7"}, "PostgreSQL": {"revision": "11.2"}}
        for s in (systems or ["jump3r", "kanzi", "lrzip", "x264", "nginx", "VP8", "HSQLDB", "Apache", "exastencils"]):
            try:
                table = load_twins_table(zp, s, where=REVISION.get(s))
                cells, _ = eval_scenario(table, "performance", target_prop, budget_grid(len(table.rows)),
                                         seeds, learner, 1.0, rng, eval_cap)
                items.append((f"{s}/{target_prop}", cells))
            except Exception as e:
                print(f"skip {s}: {e}", flush=True)
    elif mode == "workload":
        min_runs = 10
        zp = "workload-impact-ICSE2023/artifact_excluding_raw_coverage.zip"
        for s in ["batik", "dconvert", "h2", "jump3r", "kanzi", "lrzip", "x264", "xz", "z3"]:
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
                    cells, _ = eval_scenario(subset, col, col, budgets, seeds, learner, 1.0, rng,
                                             eval_cap, cost_orientation=orient)
                    items.append((f"{s}|{wl}", cells))
                except Exception as e:
                    print(f"  skip {s}/{wl}: {e}", flush=True)
    else:  # lcbench
        min_runs = 10
        jp = "/private/tmp/lcbench/data_2k_lw.json"
        learner = "ridge-raw" if learner == "ridge-log" else learner
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
                cells, _ = eval_scenario(subset, "time_total", "final_val_accuracy", budgets, seeds,
                                         learner, 1.0, rng, eval_cap)
                items.append((ds, cells))
            except Exception as e:
                print(f"  skip {ds}: {e}", flush=True)
    return items, min_runs


def reversal_for_context(st, min_runs):
    """st: {(sampler, level): {err, cost, n}} for ONE context. Returns counters."""
    if min_runs > 1:
        st = {k: v for k, v in st.items() if len(v["err"]) >= min_runs}
    # within-strategy: per sampler, ordered level pairs by n
    win_tot = win_rev = 0
    by_strat = defaultdict(list)
    for (s, lv), v in st.items():
        by_strat[s].append((v["n"], v["cost"]))
    for s, pts in by_strat.items():
        pts = sorted(pts)  # by n ascending
        for (ni, ci), (nj, cj) in combinations(pts, 2):
            if nj > ni:                       # strictly larger sample
                win_tot += 1
                win_rev += int(cj < ci)       # ...yet cheaper
    # cross-strategy: ordered (A@nA, B@nB), A!=B, nA > nB, costA < costB
    cross_tot = cross_rev = 0
    pts = [(s, v["n"], v["cost"]) for (s, lv), v in st.items()]
    for (sa, na, ca), (sb, nb, cb) in combinations(pts, 2):
        if sa == sb:
            continue
        # consider the ordering where one has strictly larger n
        if na > nb:
            cross_tot += 1; cross_rev += int(ca < cb)
        elif nb > na:
            cross_tot += 1; cross_rev += int(cb < ca)
    return dict(win_tot=win_tot, win_rev=win_rev, cross_tot=cross_tot, cross_rev=cross_rev,
                ctx_has_cross=int(cross_rev > 0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["icse19", "x264", "twins", "workload", "lcbench"], required=True)
    ap.add_argument("--learner", default="ridge-log")
    ap.add_argument("--eval-cap", type=int, default=6000)
    ap.add_argument("--seeds", type=int, default=30)
    ap.add_argument("--target-prop", default="energy")
    ap.add_argument("--inputs", default="0-16")
    ap.add_argument("--systems", nargs="+", default=None, help="twins mode: explicit system list (e.g. 14-system energy)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="artifacts/reversal_rate.csv")
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    items, min_runs = build_items(args.mode, args.learner, args.eval_cap, args.seeds, rng,
                                  args.target_prop, args.inputs, args.systems)
    rows, agg = [], defaultdict(int)
    n_ctx = 0
    for label, cells in items:
        st = per_cell_stats(cells)
        c = reversal_for_context(st, min_runs)
        if c["win_tot"] == 0 and c["cross_tot"] == 0:
            continue
        n_ctx += 1
        for k in ("win_tot", "win_rev", "cross_tot", "cross_rev", "ctx_has_cross"):
            agg[k] += c[k]
        rows.append(dict(context=label, **c,
                         win_pct=round(100 * c["win_rev"] / c["win_tot"], 1) if c["win_tot"] else "",
                         cross_pct=round(100 * c["cross_rev"] / c["cross_tot"], 1) if c["cross_tot"] else ""))
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    if rows:
        with open(args.out, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    wp = 100 * agg["win_rev"] / agg["win_tot"] if agg["win_tot"] else 0.0
    cp = 100 * agg["cross_rev"] / agg["cross_tot"] if agg["cross_tot"] else 0.0
    hc = 100 * agg["ctx_has_cross"] / n_ctx if n_ctx else 0.0
    print(f"\n=== {args.mode}: {n_ctx} contexts ===")
    print(f"  WITHIN-strategy larger-yet-cheaper : {agg['win_rev']}/{agg['win_tot']} ({wp:.1f}%)")
    print(f"  CROSS-strategy  larger-yet-cheaper : {agg['cross_rev']}/{agg['cross_tot']} ({cp:.1f}%)")
    print(f"  contexts with >=1 cross reversal   : {agg['ctx_has_cross']}/{n_ctx} ({hc:.0f}%)")
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
