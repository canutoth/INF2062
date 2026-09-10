#!/usr/bin/env python3
"""Sanity check: is RF's accuracy (MRE) in-line with ridge (close or better)?
Direct micro-benchmark: for a representative table per family, draw a sample, fit
ridge and RF on the SAME sample, measure MRE on the held-out rest, average over reps.
RF should be <= ridge (or within ~5%); a much worse RF would make the learner
sensitivity an unfair comparison."""
import numpy as np, sys
sys.path.insert(0, "."); sys.path.insert(0, "scripts")
from cost_sampling.generated_sampling import (load_twins_table, load_workload_table, load_lcbench_table,
                                              subset_measured_table, _column_values)
from cost_sampling.metrics import fit_learner, predict
from collections import defaultdict


def compare(name, X, y, pair, sizes=(50, 200, 500), reps=8):
    X = np.asarray(X, float); y = np.asarray(y, float); N = len(y)
    rng = np.random.default_rng(0)
    for n in sizes:
        if n >= N:
            continue
        res = defaultdict(list)
        for _ in range(reps):
            idx = rng.choice(N, size=n, replace=False)
            mask = np.ones(N, bool); mask[idx] = False
            for lr in pair:
                m = fit_learner(X[idx], y[idx], learner=lr)
                p = predict(m, X[mask])
                res[lr].append(float(np.mean(np.abs(y[mask] - p) / np.maximum(np.abs(y[mask]), 1e-12))))
        rg, rf = np.mean(res[pair[0]]), np.mean(res[pair[1]])
        verdict = "RF<=ridge OK" if rf <= rg * 1.05 else "** RF WORSE **"
        print(f"{name:22s} n={n:4d}: ridge={rg:.4f}  RF={rf:.4f}  {verdict} ({rf/rg:.2f}x)", flush=True)


t = load_twins_table("/tmp/twins_main.zip", "x264")
compare("ENERGY/x264(energy)", t.X, _column_values(t, "energy"), ["ridge-log", "sk-rf-log"])
compare("ENERGY/x264(perf)", t.X, _column_values(t, "performance"), ["ridge-log", "sk-rf-log"])

tb = load_lcbench_table("/private/tmp/lcbench/data_2k_lw.json"); g = defaultdict(list)
for i, r in enumerate(tb.rows): g[r.get("workload", "all")].append(i)
d = sorted(g)[0]; sub = subset_measured_table(tb, g[d], analysis_name=d)
compare(f"LCBENCH/{d[:12]}", sub.X, _column_values(sub, "final_val_accuracy"), ["ridge-raw", "sk-rf-raw"])

tw = load_workload_table("workload-impact-ICSE2023/artifact_excluding_raw_coverage.zip", "kanzi")
labels = [c for c in tw.label_columns if c != "config_id"]
col = "time" if "time" in labels else ("throughput" if "throughput" in labels else labels[0])
g = defaultdict(list)
for i, r in enumerate(tw.rows): g[r.get("workload", "all")].append(i)
wl = sorted(g)[0]; sub = subset_measured_table(tw, g[wl], analysis_name=f"k-{wl}")
compare(f"WORKLOAD/kanzi", sub.X, _column_values(sub, col), ["ridge-log", "sk-rf-log"])
print("DONE", flush=True)
