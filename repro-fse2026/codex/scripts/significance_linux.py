#!/usr/bin/env python3
"""Linux (TuxKConfig) — flip + KW + Pareto from one eval pass per release.

Replicates run_linux_kernel's pool sampling (random/balanced/diversity/
uncertainty/coverage), evaluates per-config errors on a capped holdout, builds
cells, and computes: top-1 flip (sig_core), KW best/top-group (kw_cost_vs_size),
and Pareto choice-set (sig_core). target=cost=vmlinux size (storage-bound).
Run with .venv-linux/bin/python (scipy for KW).
"""
import argparse, csv, pickle, sys
from pathlib import Path
import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO)); sys.path.insert(0, str(REPO / "scripts"))
from cost_sampling.linux_data import load_linux_dataset
from cost_sampling.metrics import fit_learner, predict
from cost_sampling.pool_samplers import (random_sample, balanced_sample, diversity_sample,
                                         uncertainty_sample, coverage_sample)
from sig_core import flips_both, pareto_choiceset
from kw_cost_vs_size import analyze as kw_analyze

LEVELS = [0.01, 0.02, 0.05, 0.10, 0.20]
RELEASES = ["413", "415", "420", "500", "504", "507", "508"]


def rel_err(yt, yp):
    return np.abs(yt - yp) / np.maximum(np.abs(yt), 1e-12)


def build_cells(ds, runs_stoch, runs_other, learner, alpha, rng, eval_cap, div_max_n=1851):
    X, y, cost_values, full_cost = ds.X, ds.y, ds.cost_values, ds.full_cost
    N = X.shape[0]
    pool = np.sort(rng.choice(N, size=eval_cap, replace=False)) if N > eval_cap else np.arange(N)
    Xp, yp = X[pool], y[pool]
    posmap = {int(g): i for i, g in enumerate(pool)}
    cells = {}

    def add(strategy, n, idx):
        idx = np.array(sorted(set(int(i) for i in idx)), dtype=int)
        if len(idx) == 0 or len(idx) >= N:
            return
        model = fit_learner(X[idx], y[idx], learner=learner, alpha=alpha)
        err = rel_err(yp, predict(model, Xp))
        valid = np.ones(len(pool), bool)
        for g in idx:
            if g in posmap:
                valid[posmap[g]] = False
        key = (strategy, f"n{n:05d}")
        c = cells.setdefault(key, {"errs": [], "valid": [], "pct_cost": [], "pct_n": len(idx) / N})
        c["errs"].append(err); c["valid"].append(valid)
        c["pct_cost"].append(float(np.sum(cost_values[idx])) / full_cost)

    for frac in LEVELS:
        n = int(round(frac * N))
        for r in range(runs_stoch):
            add("random", n, random_sample(n, pool_size=N, rng=rng))
            add("balanced", n, balanced_sample(n, active_options=ds.active_options, rng=rng))
        if n <= div_max_n:
            for r in range(runs_other):
                add("diversity", n, diversity_sample(n, X=X, rng=rng, candidate_size=512))
        for r in range(runs_other):
            add("uncertainty", n, uncertainty_sample(n, X=X, y=y, rng=rng, seed_fraction=0.25,
                                                     alpha=alpha, log_target=True))
            add("coverage", n, coverage_sample(n, X=X, rng=rng, candidate_size=512))
    return cells


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="ICPE-rawdata/linux")
    ap.add_argument("--releases", nargs="+", default=RELEASES)
    ap.add_argument("--runs-stoch", type=int, default=30)
    ap.add_argument("--runs-other", type=int, default=20)
    ap.add_argument("--bootstrap", type=int, default=1000)
    ap.add_argument("--learner", default="ridge-log")
    ap.add_argument("--alpha", type=float, default=1.0)
    ap.add_argument("--eval-cap", type=int, default=6000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--top-k-features", type=int, default=0,
                    help="keep top-k Linux options (0 = ALL ~9645 features). The pipeline "
                         "default of 512 crippled BOTH the learner AND the feature-based "
                         "samplers (balanced/diversity/uncertainty/coverage) — use 0.")
    ap.add_argument("--out-prefix", default="artifacts/significance_linux")
    ap.add_argument("--reuse-cells", action="store_true",
                    help="load cached _cells_<rel>.pkl instead of re-fitting (for fast re-aggregation)")
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    flips, kws, paretos, kws_xal, costsize, mre_rows = [], [], [], [], [], []
    for rel in args.releases:
        pkl = f"{args.out_prefix}_cells_{rel}.pkl"
        if args.reuse_cells and Path(pkl).exists():
            with open(pkl, "rb") as fh:
                cells = pickle.load(fh)
            print(f"linux{rel}: reused cached cells from {pkl} (no re-fit)", flush=True)
        else:
            pq = f"{args.data_dir}/tuxkconfig_{rel}.parquet"
            try:
                ds = load_linux_dataset(pq, context=f"linux{rel}",
                                        top_k_features=(args.top_k_features if args.top_k_features > 0 else None))
            except Exception as e:
                print(f"skip {rel}: {e}", flush=True); continue
            print(f"linux{rel}: loaded {ds.X.shape[0]} configs x {ds.X.shape[1]} features "
                  f"(top_k={args.top_k_features or 'ALL'})", flush=True)
            cells = build_cells(ds, args.runs_stoch, args.runs_other, args.learner, args.alpha, rng, args.eval_cap)
            # serialize cells so any later re-analysis (e.g. exclude-a-sampler) is instant, no re-fit
            Path(args.out_prefix).parent.mkdir(parents=True, exist_ok=True)
            with open(pkl, "wb") as fh:
                pickle.dump(cells, fh)
        for f in flips_both(cells, f"linux{rel}", args.bootstrap, rng):
            flips.append(f)
        # budget_policy defaults to "largest-n" (non-oracular, C2); pass the bootstrap so
        # Linux gets p_reproduce_change (R1#1) and evicted (R1#2) like the other families.
        krows = kw_analyze(cells, f"linux{rel}", min_runs=10,
                           membership_boot=args.bootstrap, rng=rng)
        kws.extend(krows)
        # EXCLUDE active learning (uncertainty): does the non-AL field reshuffle MORE under cost?
        cells_xal = {k: v for k, v in cells.items() if k[0] != "uncertainty"}
        kws_xal.extend(kw_analyze(cells_xal, f"linux{rel}", min_runs=10))
        # per-sampler measured cost at equal sample size (verify: does uncertainty pick expensive configs?)
        for lv in sorted({lv for _, lv in cells}):
            row = {"context": f"linux{rel}", "level": lv}
            for s in sorted({st for st, _ in cells}):
                c = cells.get((s, lv))
                if c is not None:
                    row[f"{s}_cost"] = round(float(np.mean(c["pct_cost"])), 6)
            costsize.append(row)
        # ACCURACY MONITOR: median MRE per (sampler, level) from the same cells, so a
        # catastrophic-fit learner (e.g. ridge-log on Linux ~36%) is caught live.
        for (s, lv), c in cells.items():
            runs = [float(np.asarray(e)[np.asarray(v)].mean()) for e, v in zip(c["errs"], c["valid"])]
            mre_rows.append({"context": f"linux{rel}", "learner": args.learner, "sampler": s,
                             "level": lv, "pct_n": round(float(np.median(c["pct_n"])) if np.ndim(c["pct_n"]) else float(c["pct_n"]), 4),
                             "median_mre": round(float(np.median(runs)), 4)})
        rel_mre = [r["median_mre"] for r in mre_rows if r["context"] == f"linux{rel}"]
        pr = pareto_choiceset(cells, f"linux{rel}", args.bootstrap, rng, agg="mean")
        if pr:
            paretos.append(pr)
        fl_med = [f for f in flips if f["system"] == f"linux{rel}" and f["agg"] == "median"]
        mre_flag = " **CATASTROPHIC MRE**" if rel_mre and np.median(rel_mre) > 0.20 else ""
        print(f"linux{rel}: MRE med={np.median(rel_mre)*100:.0f}% [{min(rel_mre)*100:.0f}-{max(rel_mre)*100:.0f}%]{mre_flag} | "
              f"flips(med)={len(fl_med)} sig={sum(x['p_reproduce']>=0.95 for x in fl_med)} | KW comps={len(krows)} "
              f"grp-change={sum(r['group_changed'] for r in krows)} | pareto p_differ={pr['p_differ'] if pr else '—'}", flush=True)

    def dump(rows, path):
        if rows:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), extrasaction="ignore")
                w.writeheader(); w.writerows(rows)
    dump(flips, f"{args.out_prefix}_flips.csv")
    dump(kws, f"{args.out_prefix}_kw.csv")
    dump(paretos, f"{args.out_prefix}_pareto.csv")
    dump(kws_xal, f"{args.out_prefix}_kw_excl_uncertainty.csv")
    dump(mre_rows, f"{args.out_prefix}_mre.csv")
    if mre_rows:
        allm = [r["median_mre"] for r in mre_rows]
        print(f"\nACCURACY ({args.learner}): median MRE {np.median(allm)*100:.1f}% "
              f"[{min(allm)*100:.0f}–{max(allm)*100:.0f}%]"
              f"{'  ** CATASTROPHIC — learner unfit for Linux **' if np.median(allm) > 0.20 else '  (acceptable)'}")
    if costsize:
        keys = []
        for r in costsize:
            for k in r:
                if k not in keys:
                    keys.append(k)
        with open(f"{args.out_prefix}_costsize.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=keys); w.writeheader(); w.writerows(costsize)
    if kws:
        gc = sum(r["group_changed"] for r in kws)
        ev = sum(r["evicted"] for r in kws)
        rob = sum(1 for r in kws if r["group_changed"] and r.get("p_reproduce_change", -1) >= .95)
        print(f"\nLINUX KW [largest-n]: {len(kws)} comparisons, top-group changes {gc} "
              f"({gc/len(kws)*100:.0f}%) | evicted {ev} ({ev/len(kws)*100:.0f}%) | "
              f"change robust(boot>=.95) {rob}/{gc}")
    if kws_xal:
        gx = sum(r["group_changed"] for r in kws_xal)
        print(f"LINUX KW (excl. active learning): {len(kws_xal)} comps, top-group changes {gx} ({gx/len(kws_xal)*100:.0f}%)")
    if paretos:
        pd = sum(p["p_differ"] >= 0.95 for p in paretos)
        print(f"LINUX Pareto: choice-set robustly differs in {pd}/{len(paretos)} releases")
    print("wrote", args.out_prefix, "*.csv", flush=True)


if __name__ == "__main__":
    main()
