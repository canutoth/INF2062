#!/usr/bin/env python3
"""Significance of RQ2 flips for REPLICATION-ICPE20 (x264), all 4 cost/target combos.

Per input i: target=size (x264_size_i), cost=time (x264_time_i). The asymmetric
time-cost/size-target case is the one most relevant to the original Figure 4.
Reuses the archive bootstrap core (eval_dataset, flips).
"""
import argparse, csv, sys
from pathlib import Path
import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO)); sys.path.insert(0, str(REPO / "scripts"))
from cost_sampling.archive_runs import load_runs_dataset, attach_cost_dataset
from significance_flips_archive import eval_dataset, flips


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", default="ICPE-rawdata/AllRuns.zip")
    ap.add_argument("--inputs", default="0-16")
    ap.add_argument("--bootstrap", type=int, default=1000)
    ap.add_argument("--learner", default="ridge-log")
    ap.add_argument("--alpha", type=float, default=1.0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--eval-cap", type=int, default=6000)
    ap.add_argument("--max-runs", type=int, default=None)
    ap.add_argument("--out", default="artifacts/significance_flips_replication_icpe20.csv")
    args = ap.parse_args()
    if "-" in args.inputs:
        lo, hi = args.inputs.split("-"); inputs = list(range(int(lo), int(hi) + 1))
    else:
        inputs = [int(x) for x in args.inputs.split(",")]
    rng = np.random.default_rng(args.seed)
    allf = []
    for i in inputs:
        try:
            size_ds = load_runs_dataset(args.zip, f"x264_size_{i}", max_runs=args.max_runs)
            time_ds = load_runs_dataset(args.zip, f"x264_time_{i}", max_runs=args.max_runs)
        except Exception as e:
            print(f"skip input {i}: {e}", flush=True); continue
        combos = {
            "size/size": size_ds,
            "time/time": time_ds,
            "timecost-sizetarget": attach_cost_dataset(size_ds, time_ds),
            "sizecost-timetarget": attach_cost_dataset(time_ds, size_ds),
        }
        for label, ds in combos.items():
            cells = eval_dataset(ds, args.learner, args.alpha, rng, args.eval_cap)
            fl = flips(cells, f"x264_{i}", args.bootstrap, rng)
            for f in fl:
                f["combo"] = label
            allf.extend(fl)
        nf = sum(1 for f in allf if f["system"] == f"x264_{i}")
        rob = sum(1 for f in allf if f["system"] == f"x264_{i}" and f["p_reproduce"] >= 0.95)
        print(f"x264_{i}: {nf} flips, {rob} robust", flush=True)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    fields = ["system", "combo", "agg", "lam", "kind", "cw", "mw", "p_reproduce", "dMRE_pct", "dCost_pct"]
    with open(args.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader(); w.writerows(allf)
    n = len(allf)
    if n:
        ps = np.array([f["p_reproduce"] for f in allf])
        rob = int((ps >= 0.95).sum())
        print(f"\n=== ICPE20 x264, bootstrap={args.bootstrap} ===\ntotal flips: {n}")
        print(f"  robust (p>=0.95): {rob} ({rob/n*100:.0f}%)   median p={np.median(ps):.2f}")
        # asymmetric (time-cost/size-target) vs symmetric
        asym = [f for f in allf if f["combo"] in ("timecost-sizetarget", "sizecost-timetarget")]
        sym = [f for f in allf if f["combo"] in ("size/size", "time/time")]
        for name, grp in [("asymmetric (target!=cost)", asym), ("symmetric (target=cost)", sym)]:
            if grp:
                g = np.array([f["p_reproduce"] for f in grp])
                print(f"  {name}: {len(grp)} flips, {int((g>=.95).sum())} robust, median p={np.median(g):.2f}")
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
