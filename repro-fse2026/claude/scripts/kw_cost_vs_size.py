#!/usr/bin/env python3
"""Cost-controlled re-analysis of the ICPE20/ICSE19 sampler comparison.

ICPE20/ICSE19 compare sampling strategies by prediction-error distribution over
~100 random seeds with a Kruskal-Wallis test, AT A FIXED SAMPLE SIZE (t-wise
level) -> their Tables 2-8. We reuse the SAME test, but additionally compare the
samplers AT A FIXED MEASURED-COST BUDGET, and report whether the KW-best sampler
changes. Run with .venv-linux/bin/python (has scipy).

For each (context, level L):
  SIZE view  : KW across samplers' error at level L (their cell). best = min median err.
  COST view  : budget b = median over samplers of cost(L); each sampler enters at the
               operating point it can AFFORD (median cost <= b); KW across those.
               --budget-policy largest-n (default, deployable): the largest predefined n
                   it can afford -- monotone, NON-oracular (does not peek at error).
               --budget-policy minerr (retrospective envelope, for comparison only):
                   the cheapest-error affordable level (original behaviour).
               best = min median err. (Cheap samplers can afford a bigger sample.)
  changed?   : size-best != cost-best.
  Also per comparison: evicted (size-best drops out of cost top group, R1#2),
  mre_gap (accuracy gap between size-era and cost-era pick, R1#3), and with
  --membership-bootstrap B: p_reproduce_change (top-group change survives reseeding, R1#1).
"""
import argparse, csv, sys
from pathlib import Path
import numpy as np
from scipy.stats import kruskal, rankdata, norm

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO)); sys.path.insert(0, str(REPO / "scripts"))
from cost_sampling.archive_runs import load_runs_dataset, attach_cost_dataset
from significance_flips_archive import eval_dataset
from cost_sampling.generated_sampling import (load_twins_table, load_workload_table, load_lcbench_table,
                                              subset_measured_table, build_generated_dataset, budget_grid)
from significance_flips import eval_scenario
from sig_core import flips_both, pareto_choiceset
from collections import defaultdict


def dunn_top_group(named, alpha=0.05):
    """Dunn post-hoc (Holm-adjusted) after Kruskal-Wallis. Returns (best, top_group)
    where top_group = samplers NOT significantly worse than the best (lower err = better)."""
    labels = [l for l in named if len(named[l]) > 0]
    if len(labels) < 2:
        return (labels[0] if labels else None), frozenset(labels)
    data = [np.asarray(named[l], float) for l in labels]
    allv = np.concatenate(data); N = len(allv)
    ranks = rankdata(allv)
    _, counts = np.unique(allv, return_counts=True)
    tie = float((counts ** 3 - counts).sum())
    sigma2 = (N * (N + 1) / 12.0) - tie / (12.0 * (N - 1)) if N > 1 else 0.0
    Rbar, ns, off = {}, {}, 0
    for l, d in zip(labels, data):
        Rbar[l] = ranks[off:off + len(d)].mean(); ns[l] = len(d); off += len(d)
    best = min(labels, key=lambda l: np.median(named[l]))
    others = [l for l in labels if l != best]
    pv = {}
    for l in others:
        se = np.sqrt(sigma2 * (1.0 / ns[best] + 1.0 / ns[l])) if sigma2 > 0 else 0.0
        z = abs(Rbar[best] - Rbar[l]) / se if se > 0 else 0.0
        pv[l] = 2.0 * norm.sf(z)
    order = sorted(others, key=lambda l: pv[l]); m = len(order)
    top = {best}; prev = 0.0
    for i, l in enumerate(order):
        padj = max(prev, min(1.0, (m - i) * pv[l])); prev = padj
        if padj >= alpha:
            top.add(l)
    return best, frozenset(top)


def _boot_change(size_err, cost_err, B, rng):
    """R1#1: fraction of bootstrap reps in which the Dunn top group DIFFERS between the
    size and cost views. Resample each sampler's error distribution with replacement
    (seeds), recompute both top groups, count disagreements. High value => the top-group
    change is reproducible under reseeding, not a single-draw artifact. Operating points
    are fixed (largest-n policy does not depend on error), so only errors are resampled."""
    ls = [l for l in size_err if len(size_err[l]) > 0]
    lc = [l for l in cost_err if len(cost_err[l]) > 0]
    if len(ls) < 2 or len(lc) < 2:
        return -1.0
    cnt = 0
    for _ in range(B):
        bs = {l: rng.choice(size_err[l], size=len(size_err[l]), replace=True) for l in ls}
        bc = {l: rng.choice(cost_err[l], size=len(cost_err[l]), replace=True) for l in lc}
        _, gs = dunn_top_group(bs)
        _, gc = dunn_top_group(bc)
        cnt += int(gs != gc)
    return round(cnt / B, 3)


def per_cell_stats(cells):
    """(sampler,level) -> dict(err=array over runs, cost=median cost, n=pct_n)."""
    out = {}
    for (s, lv), c in cells.items():
        errs = np.array([e[v].mean() for e, v in zip(c["errs"], c["valid"])])
        out[(s, lv)] = dict(err=errs, cost=float(np.median(c["pct_cost"])), n=float(np.median(c["pct_n"])))
    return out


def kw_p(groups):
    groups = [g for g in groups if len(g) > 0]
    if len(groups) < 2:
        return 1.0
    try:
        return float(kruskal(*groups).pvalue)
    except ValueError:
        return 1.0


def analyze(cells, context, min_runs=1, budget_policy="largest-n", membership_boot=0, rng=None):
    st = per_cell_stats(cells)
    if min_runs > 1:  # KW needs distributions; drop deterministic (1-run) samplers
        st = {k: v for k, v in st.items() if len(v["err"]) >= min_runs}
    samplers = sorted({s for s, _ in st})
    levels = sorted({lv for _, lv in st}, key=lambda lv: np.median([st[(s, lv)]["n"] for s in samplers if (s, lv) in st]))
    rows = []
    for L in levels:
        present = [s for s in samplers if (s, L) in st]
        if len(present) < 2:
            continue
        # SIZE view: samplers at level L
        size_err = {s: st[(s, L)]["err"] for s in present}
        p_size = kw_p(list(size_err.values()))
        best_size = min(present, key=lambda s: np.median(size_err[s]))
        # COST view: budget = median cost across samplers at level L
        b = float(np.median([st[(s, L)]["cost"] for s in present]))
        cost_choice, cost_err = {}, {}
        for s in samplers:
            afford = [(lv, st[(s, lv)]) for lv in levels if (s, lv) in st and st[(s, lv)]["cost"] <= b * 1.0000001]
            if not afford:
                continue
            if budget_policy == "largest-n":
                lv_star = max(afford, key=lambda kv: kv[1]["n"])           # most data affordable (non-oracular)
            else:  # "minerr": retrospective upper envelope (original; reported for comparison only)
                lv_star = min(afford, key=lambda kv: np.median(kv[1]["err"]))
            cost_choice[s] = lv_star[0]; cost_err[s] = lv_star[1]["err"]
        if len(cost_err) < 2:
            continue
        p_cost = kw_p(list(cost_err.values()))
        best_cost = min(cost_err, key=lambda s: np.median(cost_err[s]))
        # Dunn post-hoc top-groups (samplers statistically tied with the best)
        _, grp_size = dunn_top_group(size_err)
        _, grp_cost = dunn_top_group(cost_err)
        # R1#2 "evicted": the source-study recommendation (size-best) drops out of the cost top group
        evicted = int(best_size not in grp_cost)
        # R1#3 effect size: accuracy gap between the size-era pick and the cost-era pick
        mre_best_size = float(np.median(size_err[best_size]))
        mre_best_cost = float(np.median(cost_err[best_cost]))
        # equal-budget gap: at the cost budget, accuracy gain of the cost-pick over the
        # count-pick (both under cost affordability); >= 0, "what you gain by switching"
        eqb = (float(np.median(cost_err[best_size])) - mre_best_cost) if best_size in cost_err else None
        # R1#1 membership-change bootstrap (only when grp differs; else cheap to skip)
        p_repro = _boot_change(size_err, cost_err, membership_boot, rng) if membership_boot else -1.0
        rows.append(dict(context=context, level=L,
                         best_size=best_size, p_size=round(p_size, 4),
                         best_cost=best_cost, p_cost=round(p_cost, 4),
                         best_cost_level=cost_choice.get(best_cost, ""),
                         changed=int(best_size != best_cost),
                         topgroup_size="|".join(sorted(grp_size)),
                         topgroup_cost="|".join(sorted(grp_cost)),
                         group_changed=int(grp_size != grp_cost),
                         evicted=evicted,
                         p_reproduce_change=round(p_repro, 3),
                         # ACCURACY MONITOR: catch a catastrophic-fit learner (e.g. ridge on Linux)
                         best_mre=round(mre_best_size, 4),
                         mre_best_cost=round(mre_best_cost, 4),
                         mre_gap=round(mre_best_size - mre_best_cost, 4),
                         mre_eqbudget_gap=round(eqb, 4) if eqb is not None else "",
                         median_mre=round(float(np.median([np.median(size_err[s]) for s in present])), 4)))
    return rows


def _level_decision(errs, costs, samplers, levels, L):
    """One (context, level) decision from per-cell error arrays + costs.
    errs/costs keyed by (sampler, level). Returns size/cost Dunn groups, winners,
    eviction (size-winner not in cost top-group) and the equal-budget MRE gap."""
    present = [s for s in samplers if (s, L) in errs]
    if len(present) < 2:
        return None
    size_err = {s: errs[(s, L)] for s in present}
    best_size = min(present, key=lambda s: np.median(size_err[s]))
    _, grp_size = dunn_top_group(size_err)
    b = float(np.median([costs[(s, L)] for s in present]))
    cost_err = {}
    for s in samplers:
        afford = [errs[(s, lv)] for lv in levels if (s, lv) in errs and costs[(s, lv)] <= b * 1.0000001]
        if not afford:
            continue
        cost_err[s] = min(afford, key=lambda a: np.median(a))
    if len(cost_err) < 2:
        return None
    best_cost = min(cost_err, key=lambda s: np.median(cost_err[s]))
    _, grp_cost = dunn_top_group(cost_err)
    dMRE = (float(np.median(cost_err[best_size]) - np.median(cost_err[best_cost]))
            if best_size in cost_err else None)
    return dict(best_size=best_size, best_cost=best_cost, grp_size=grp_size, grp_cost=grp_cost,
                group_changed=int(grp_size != grp_cost), best_changed=int(best_size != best_cost),
                evicted=int(best_size not in grp_cost), dMRE=dMRE)


def analyze_robust(cells, context, B=1000, rng=None, min_runs=1):
    """Point estimate + seed bootstrap of the top-group membership change. For each
    (context, level) resample each sampler's per-seed errors with replacement B times
    and recompute the size/cost Dunn groups, reporting how often the change reproduces.
    Also reports eviction (the size-recommended sampler dropping out of the cost top
    group) and the equal-budget MRE gap as an effect size."""
    if rng is None:
        rng = np.random.default_rng(0)
    st = per_cell_stats(cells)
    if min_runs > 1:
        st = {k: v for k, v in st.items() if len(v["err"]) >= min_runs}
    samplers = sorted({s for s, _ in st})
    levels = sorted({lv for _, lv in st}, key=lambda lv: np.median([st[(s, lv)]["n"] for s in samplers if (s, lv) in st]))
    errs0 = {k: np.asarray(v["err"], float) for k, v in st.items()}
    costs = {k: v["cost"] for k, v in st.items()}
    rows = []
    for L in levels:
        d = _level_decision(errs0, costs, samplers, levels, L)
        if d is None:
            continue
        gc = ev = bc = 0
        for _ in range(B):
            errs_b = {k: a[rng.integers(0, len(a), len(a))] for k, a in errs0.items()}
            db = _level_decision(errs_b, costs, samplers, levels, L)
            if db is None:
                continue
            gc += db["group_changed"]; ev += db["evicted"]; bc += db["best_changed"]
        rows.append(dict(context=context, level=L, best_size=d["best_size"], best_cost=d["best_cost"],
                         group_changed=d["group_changed"], p_groupchange=round(gc / B, 3),
                         evicted=d["evicted"], p_evict=round(ev / B, 3),
                         best_changed=d["best_changed"], p_bestchange=round(bc / B, 3),
                         dMRE=round(d["dMRE"], 5) if d["dMRE"] is not None else "",
                         topgroup_size="|".join(sorted(d["grp_size"])),
                         topgroup_cost="|".join(sorted(d["grp_cost"]))))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["icse19", "x264", "twins", "workload", "lcbench"], required=True)
    ap.add_argument("--zip", default=None)
    ap.add_argument("--contexts", nargs="+", default=None)
    ap.add_argument("--inputs", default="0-16")
    ap.add_argument("--systems", nargs="+", default=None, help="twins mode: energy systems")
    ap.add_argument("--target-prop", default="energy", help="twins mode target property")
    ap.add_argument("--seeds", type=int, default=30, help="twins mode stochastic seeds")
    ap.add_argument("--learner", default="ridge-log")
    ap.add_argument("--eval-cap", type=int, default=6000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--budget-policy", choices=["largest-n", "minerr"], default="largest-n",
                    help="operating point at a budget: largest-n (deployable, non-oracular) | "
                         "minerr (retrospective upper envelope; original, for comparison)")
    ap.add_argument("--membership-bootstrap", type=int, default=0,
                    help="bootstrap reps for the Dunn top-group CHANGE (R1#1); 0=off")
    ap.add_argument("--exclude", nargs="+", default=[],
                    help="strategy names to drop from the candidate set (construct-validity sensitivity, e.g. pilotCost)")
    ap.add_argument("--all-metrics", action="store_true",
                    help="also emit flip (<out>_flip.csv) and Pareto (<out>_pareto.csv) from the same cells")
    ap.add_argument("--bootstrap", type=int, default=1000, help="bootstrap reps for flip/Pareto (--all-metrics)")
    ap.add_argument("--out", default="artifacts/kw_cost_vs_size.csv")
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    items = []          # (label, cells)
    min_runs = 1        # archives: every sampler has ~100 runs
    if args.mode == "icse19":
        zp = args.zip or "ICPE-rawdata/NewRuns.zip"
        for c in (args.contexts or ["LLVM", "Polly", "Dune", "Hipacc", "lrzip", "7z", "BerkeleyDBC"]):
            try:
                items.append((c, eval_dataset(load_runs_dataset(zp, c), args.learner, 1.0, rng, args.eval_cap)))
            except Exception as e:
                print(f"skip {c}: {e}")
    elif args.mode == "x264":
        zp = args.zip or "ICPE-rawdata/AllRuns.zip"
        idxs = range(int(args.inputs.split("-")[0]), int(args.inputs.split("-")[1]) + 1) if "-" in args.inputs \
            else [int(x) for x in args.inputs.split(",")]
        for i in idxs:
            try:
                sd = load_runs_dataset(zp, f"x264_size_{i}"); td = load_runs_dataset(zp, f"x264_time_{i}")
                items.append((f"x264_{i}", eval_dataset(attach_cost_dataset(sd, td), args.learner, 1.0, rng, args.eval_cap)))
            except Exception as e:
                print(f"skip x264_{i}: {e}")
    elif args.mode == "twins":  # generated families: STOCHASTIC samplers only (deterministic have 1 run)
        min_runs = 10
        zp = args.zip or "/tmp/twins_main.zip"
        REVISION = {"brotli": {"revision": "1.0.7"}, "PostgreSQL": {"revision": "11.2"}}
        systems = args.systems or ["jump3r", "kanzi", "lrzip", "x264", "nginx", "VP8", "HSQLDB", "Apache", "exastencils"]
        for s in systems:
            try:
                table = load_twins_table(zp, s, where=REVISION.get(s))
                budgets = budget_grid(len(table.rows))
                cells, _ = eval_scenario(table, "performance", args.target_prop, budgets, args.seeds,
                                         args.learner, 1.0, rng, args.eval_cap)
                items.append((f"{s}/{args.target_prop}", cells))
            except Exception as e:
                print(f"skip {s}: {e}")
    elif args.mode == "workload":  # ICSE'23 workload-impact: one context per (system, workload)
        min_runs = 10
        zp = args.zip or "workload-impact-ICSE2023/artifact_excluding_raw_coverage.zip"
        systems = args.systems or ["batik", "dconvert", "h2", "jump3r", "kanzi", "lrzip", "x264", "xz", "z3"]
        for s in systems:
            try:
                table = load_workload_table(zp, s)
            except Exception as e:
                print(f"skip {s}: {e}"); continue
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
                    cells, _ = eval_scenario(subset, col, col, budgets, args.seeds, args.learner, 1.0, rng,
                                             args.eval_cap, cost_orientation=orient)
                    items.append((f"{s}|{wl}", cells))
                except Exception as e:
                    print(f"  skip {s}/{wl}: {e}")
    else:  # lcbench: one context per OpenML dataset; raw target (accuracy bounded)
        min_runs = 10
        jp = args.zip or "/private/tmp/lcbench/data_2k_lw.json"
        # default ridge-raw; respect an explicit --learner (use a -raw variant for bounded accuracy)
        learner = "ridge-raw" if args.learner == "ridge-log" else args.learner
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
                                         learner, 1.0, rng, args.eval_cap)
                items.append((ds, cells))
            except Exception as e:
                print(f"  skip {ds}: {e}")
    if args.exclude:
        print(f"EXCLUDING samplers from candidate set: {args.exclude}", flush=True)
    allrows, flips_all, paretos_all = [], [], []
    for label, cells in items:
        if args.exclude:
            cells = {k: v for k, v in cells.items() if k[0] not in set(args.exclude)}
        rows = analyze(cells, label, min_runs=min_runs, budget_policy=args.budget_policy,
                       membership_boot=args.membership_bootstrap, rng=rng)
        allrows.extend(rows)
        if args.all_metrics:
            # flip + Pareto use the FULL candidate set (deterministic samplers included),
            # same cells the KW analysis was built from -> all three metrics, one build.
            flips_all.extend(flips_both(cells, label, args.bootstrap, rng))
            pr = pareto_choiceset(cells, label, args.bootstrap, rng, agg="mean")
            if pr:
                paretos_all.append(pr)
        print(f"{label}: {len(rows)} comparisons | best changes {sum(r['changed'] for r in rows)} | "
              f"top-group changes {sum(r['group_changed'] for r in rows)}", flush=True)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    if allrows:
        with open(args.out, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(allrows[0].keys())); w.writeheader(); w.writerows(allrows)
    n = len(allrows)
    if n:
        ch = sum(r["changed"] for r in allrows)
        gch = sum(r["group_changed"] for r in allrows)
        ev = sum(r["evicted"] for r in allrows)
        both_sig = sum(r["p_size"] < .05 and r["p_cost"] < .05 for r in allrows)
        print(f"\n=== {args.mode} [budget-policy={args.budget_policy}]: {n} (context,level) sampler comparisons ===")
        print(f"  KW significant (p<.05) under BOTH views: {both_sig}/{n}")
        print(f"  BEST sampler changes under cost:        {ch}/{n} ({ch/n*100:.0f}%)")
        print(f"  TOP-GROUP (Dunn) changes under cost:     {gch}/{n} ({gch/n*100:.0f}%)")
        print(f"  PRIOR-REC EVICTED from cost top-group:  {ev}/{n} ({ev/n*100:.0f}%)")
        if args.membership_bootstrap:
            rob = sum(1 for r in allrows if r["group_changed"] and r["p_reproduce_change"] >= .95)
            denom = gch if gch else 1
            print(f"  TOP-GROUP change ROBUST (boot p>=.95):  {rob}/{gch} of changed ({rob/denom*100:.0f}%)")
    if args.all_metrics:
        base = args.out[:-4] if args.out.endswith(".csv") else args.out
        def _dump(rows, path):
            if rows:
                with open(path, "w", newline="") as fh:
                    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), extrasaction="ignore")
                    w.writeheader(); w.writerows(rows)
        _dump(flips_all, base + "_flip.csv")
        _dump(paretos_all, base + "_pareto.csv")
        fl_med = [f for f in flips_all if f.get("agg") == "median"]
        print(f"  FLIP (median): {len(fl_med)} flips, robust(p>=.95)={sum(float(f['p_reproduce']) >= .95 for f in fl_med)}")
        if paretos_all:
            pd = sum(p["p_differ"] >= .95 for p in paretos_all)
            print(f"  PARETO: {pd}/{len(paretos_all)} scenarios robustly differ")
        print(f"wrote {base}_flip.csv and {base}_pareto.csv", flush=True)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
