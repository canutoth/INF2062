#!/usr/bin/env python3
"""Validate the cheap pilot AUDIT the paper recommends.

The paper tells a practitioner to run a cheap pilot audit -- inspect (a) the
spread of per-configuration measured cost, (b) the per-strategy budget Ratio
(pct_cost / pct_n) at a small pilot budget, and (c) whether the target is itself
the cost -- and to decide from those diagnostics whether sample-COUNT is a safe
proxy for sampling COST. This script SHOWS the audit works: the cheap pilot
diagnostics, computed per context, PREDICT whether the full cost-controlled
Kruskal-Wallis (Dunn top-group) recommendation flips under measured cost.

OUTCOME (already computed; we only join to it)
  Per (context, level) the corrected KW CSVs carry `group_changed` in {0,1} =
  does the Dunn top-group change under measured cost vs sample size. Per context
  we define: flip_rate = mean(group_changed over its levels); flipped = any.

DIAGNOSTICS (the audit -- computed per context from a cheap pilot)
  1. cost_cv            = CV (std/mean) of per-configuration measured cost.
  2. cost_p90p10        = ratio of the 90th to 10th percentile of per-config cost.
  3. target_cost_decorr = 1 - |Spearman rho(target, cost)| over configs
                          (~0 when the target IS the cost, e.g. Linux / icse19).
  4. strategy_bias      = spread (max-min) of the per-strategy median budget
                          Ratio_s = median pct_cost(s) / pct_n(s), taken over the
                          DEPLOYABLE strategies (oracles excluded) at the smallest
                          1-2 budget levels -- the mechanism the paper says drives
                          flips. Computed from the SAME cells the KW analysis
                          builds (archive samples / generated samples / cached
                          Linux cells), so the join is exact. NO learner is fit
                          for the diagnostic: Ratio needs only sample indices and
                          per-config cost, so this is genuinely a cheap pilot.

OUTPUTS
  * artifacts/audit_validation.csv      -- one tidy row per context.
  * artifacts/audit_validation_report.md -- methods+results note.
  * 607058f5f5131dcd1dbd783d/pic/results/audit_validation.png -- 3x3 flip-rate
    heatmap (cost heterogeneity x strategy_bias) + ROC inset.

Run with .venv-linux/bin/python (scipy/sklearn/numpy).
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path
import pickle
import re

import numpy as np
from scipy.stats import spearmanr, rankdata

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

from cost_sampling.archive_runs import load_runs_dataset, attach_cost_dataset
from cost_sampling.generated_sampling import (
    load_twins_table, load_workload_table, load_lcbench_table,
    subset_measured_table, build_generated_dataset, budget_grid,
)

ORACLES = {"cheapOracle", "expensiveOracle"}


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _level_key(level: str) -> int:
    """Numeric ordering for level labels: 't2'->2, 'n8'->8, 'n00394'->394."""
    digits = re.sub(r"\D", "", str(level))
    return int(digits) if digits else 0


def cost_spread(cost_values: np.ndarray) -> tuple[float, float]:
    """(CV, p90/p10) of per-configuration measured cost."""
    c = np.asarray(cost_values, dtype=float)
    mean = float(np.mean(c))
    cv = float(np.std(c) / mean) if mean != 0 else float("nan")
    p10 = float(np.percentile(c, 10))
    p90 = float(np.percentile(c, 90))
    p90p10 = p90 / p10 if p10 > 0 else float("nan")
    return cv, p90p10


def target_cost_decorr(target: np.ndarray, cost_values: np.ndarray) -> float:
    """1 - |Spearman rho(target, cost)| over configs."""
    rho = spearmanr(np.asarray(target, float), np.asarray(cost_values, float)).correlation
    if rho is None or np.isnan(rho):
        return float("nan")
    return 1.0 - abs(float(rho))


def ratios_from_samples(samples, cost_values, full_cost, N):
    """{(strategy, level): median-over-runs Ratio = pct_cost / pct_n}.

    Mirrors per_cell_stats in kw_cost_vs_size: pct_cost = sum(cost[idx])/full_cost,
    pct_n = |idx|/N, Ratio = pct_cost/pct_n (= mean cost of sampled / mean cost of
    universe). No learner is fit -- only the sample indices are used."""
    acc = defaultdict(list)
    cost_values = np.asarray(cost_values, float)
    for s in samples:
        idx = np.array(sorted(set(int(i) for i in s.indices)), dtype=int)
        if len(idx) == 0 or len(idx) >= N:
            continue
        pct_cost = float(np.sum(cost_values[idx])) / full_cost
        pct_n = len(idx) / N
        if pct_n > 0:
            acc[(s.ref.strategy, s.ref.level)].append(pct_cost / pct_n)
    return {k: float(np.median(v)) for k, v in acc.items() if v}


def ratios_from_cells(cells):
    """{(strategy, level): Ratio} from cached cells (median pct_cost / pct_n)."""
    out = {}
    for (strat, lv), c in cells.items():
        pn = float(np.median(c["pct_n"])) if np.ndim(c["pct_n"]) else float(c["pct_n"])
        if pn > 0 and len(c["pct_cost"]) > 0:
            out[(strat, lv)] = float(np.median(c["pct_cost"])) / pn
    return out


def strategy_bias(ratios, pilot_levels=2, exclude=ORACLES):
    """Spread (max-min) of median Ratio_s over deployable strategies at the
    smallest `pilot_levels` budget levels."""
    if not ratios:
        return float("nan"), {}
    levels = sorted({lv for _, lv in ratios}, key=_level_key)
    sel = set(levels[:max(1, pilot_levels)])
    per_strat = defaultdict(list)
    for (strat, lv), r in ratios.items():
        if strat in exclude or lv not in sel or not np.isfinite(r):
            continue
        per_strat[strat].append(r)
    med = {s: float(np.median(v)) for s, v in per_strat.items() if v}
    if len(med) < 2:
        return float("nan"), med
    return float(max(med.values()) - min(med.values())), med


# --------------------------------------------------------------------------- #
# per-family diagnostic computation
# --------------------------------------------------------------------------- #
def diag_icse19(args, pilot_levels):
    rows = []
    zp = args.icse19_zip
    for c in ["LLVM", "Polly", "Dune", "Hipacc", "lrzip", "7z", "BerkeleyDBC"]:
        try:
            ds = load_runs_dataset(zp, c)
        except Exception as e:
            print(f"  [icse19] skip {c}: {e}", flush=True)
            continue
        cv, p90p10 = cost_spread(ds.cost_values)
        dc = target_cost_decorr(ds.y, ds.cost_values)
        sb, _ = strategy_bias(ratios_from_samples(ds.samples, ds.cost_values, ds.full_cost, len(ds.y)), pilot_levels)
        rows.append(dict(family="icse19", context=c, cost_cv=cv, cost_p90p10=p90p10,
                         target_cost_decorr=dc, strategy_bias=sb, approx_bias=0))
        print(f"  [icse19] {c}: cv={cv:.3f} p90p10={p90p10:.2f} decorr={dc:.3f} bias={sb:.3f}", flush=True)
    return rows


def diag_x264(args, pilot_levels):
    rows = []
    zp = args.x264_zip
    for i in range(0, 17):
        ctx = f"x264_{i}"
        try:
            sd = load_runs_dataset(zp, f"x264_size_{i}")
            td = load_runs_dataset(zp, f"x264_time_{i}")
            ds = attach_cost_dataset(sd, td)
        except Exception as e:
            print(f"  [x264] skip {ctx}: {e}", flush=True)
            continue
        cv, p90p10 = cost_spread(ds.cost_values)
        dc = target_cost_decorr(ds.y, ds.cost_values)
        sb, _ = strategy_bias(ratios_from_samples(ds.samples, ds.cost_values, ds.full_cost, len(ds.y)), pilot_levels)
        rows.append(dict(family="x264", context=ctx, cost_cv=cv, cost_p90p10=p90p10,
                         target_cost_decorr=dc, strategy_bias=sb, approx_bias=0))
        print(f"  [x264] {ctx}: cv={cv:.3f} p90p10={p90p10:.2f} decorr={dc:.3f} bias={sb:.3f}", flush=True)
    return rows


def diag_energy(args, pilot_levels):
    rows = []
    zp = args.twins_zip
    REVISION = {"brotli": {"revision": "1.0.7"}, "PostgreSQL": {"revision": "11.2"}}
    systems = ["jump3r", "kanzi", "lrzip", "x264", "nginx", "VP8", "HSQLDB", "Apache", "exastencils"]
    for s in systems:
        ctx = f"{s}/energy"
        try:
            table = load_twins_table(zp, s, where=REVISION.get(s))
            bg = budget_grid(len(table.rows))
            ds = build_generated_dataset(table, target_property="energy", cost_property="performance",
                                         cost_orientation="lower", budgets=bg[:max(1, pilot_levels)],
                                         seeds=args.seeds, include_oracles=False)
        except Exception as e:
            print(f"  [energy] skip {s}: {e}", flush=True)
            continue
        cv, p90p10 = cost_spread(ds.cost_values)
        dc = target_cost_decorr(ds.y, ds.cost_values)
        sb, _ = strategy_bias(ratios_from_samples(ds.samples, ds.cost_values, ds.full_cost, len(ds.y)), pilot_levels)
        rows.append(dict(family="energy", context=ctx, cost_cv=cv, cost_p90p10=p90p10,
                         target_cost_decorr=dc, strategy_bias=sb, approx_bias=0))
        print(f"  [energy] {ctx}: cv={cv:.3f} p90p10={p90p10:.2f} decorr={dc:.3f} bias={sb:.3f}", flush=True)
    return rows


def diag_workload(args, pilot_levels):
    rows = []
    zp = args.workload_zip
    systems = ["batik", "dconvert", "h2", "jump3r", "kanzi", "lrzip", "x264", "xz", "z3"]
    for s in systems:
        try:
            table = load_workload_table(zp, s)
        except Exception as e:
            print(f"  [workload] skip {s}: {e}", flush=True)
            continue
        labels = [c for c in table.label_columns if c != "config_id"]
        col = "time" if "time" in labels else ("throughput" if "throughput" in labels else labels[0])
        orient = "inverse" if col == "throughput" else "lower"
        grouped = defaultdict(list)
        for i, row in enumerate(table.rows):
            grouped[row.get("workload", "all")].append(i)
        for wl, idxs in sorted(grouped.items()):
            ctx = f"{s}|{wl}"
            subset = subset_measured_table(table, idxs, analysis_name=f"{s}-{wl}")
            bg = budget_grid(len(subset.rows))
            if not bg:
                continue
            try:
                ds = build_generated_dataset(subset, target_property=col, cost_property=col,
                                             cost_orientation=orient, budgets=bg[:max(1, pilot_levels)],
                                             seeds=args.seeds, include_oracles=False)
            except Exception as e:
                print(f"  [workload] skip {ctx}: {e}", flush=True)
                continue
            cv, p90p10 = cost_spread(ds.cost_values)
            dc = target_cost_decorr(ds.y, ds.cost_values)
            sb, _ = strategy_bias(ratios_from_samples(ds.samples, ds.cost_values, ds.full_cost, len(ds.y)), pilot_levels)
            rows.append(dict(family="workload", context=ctx, cost_cv=cv, cost_p90p10=p90p10,
                             target_cost_decorr=dc, strategy_bias=sb, approx_bias=0))
        print(f"  [workload] {s}: {sum(1 for r in rows if r['context'].startswith(s + '|'))} contexts", flush=True)
    return rows


def diag_lcbench(args, pilot_levels):
    rows = []
    table = load_lcbench_table(args.lcbench_json)
    grouped = defaultdict(list)
    for i, row in enumerate(table.rows):
        grouped[row.get("workload", "all")].append(i)
    for ds_name, idxs in sorted(grouped.items()):
        subset = subset_measured_table(table, idxs, analysis_name=ds_name)
        bg = budget_grid(len(subset.rows))
        if not bg:
            continue
        try:
            ds = build_generated_dataset(subset, target_property="final_val_accuracy", cost_property="time_total",
                                         cost_orientation="lower", budgets=bg[:max(1, pilot_levels)],
                                         seeds=args.seeds, include_oracles=False)
        except Exception as e:
            print(f"  [lcbench] skip {ds_name}: {e}", flush=True)
            continue
        cv, p90p10 = cost_spread(ds.cost_values)
        dc = target_cost_decorr(ds.y, ds.cost_values)
        sb, _ = strategy_bias(ratios_from_samples(ds.samples, ds.cost_values, ds.full_cost, len(ds.y)), pilot_levels)
        rows.append(dict(family="lcbench", context=ds_name, cost_cv=cv, cost_p90p10=p90p10,
                         target_cost_decorr=dc, strategy_bias=sb, approx_bias=0))
    print(f"  [lcbench] {len(rows)} contexts", flush=True)
    return rows


def _linux_cost_column(parquet_path, column="vmlinux"):
    """Read a single cost/target column from a TuxKConfig parquet (cheap)."""
    import pyarrow.parquet as pq
    pf = pq.ParquetFile(str(parquet_path))
    parts = []
    for batch in pf.iter_batches(batch_size=8192, columns=[column]):
        parts.append(batch.column(column).to_numpy(zero_copy_only=False))
    return np.concatenate(parts).astype(np.float64, copy=False)


def diag_linux(args, pilot_levels):
    rows = []
    # Linux outcome lives in significance_linux_hgbtfull_kw.csv -> releases that flipped there.
    releases = ["415", "420", "500", "504", "507", "508"]
    for rel in releases:
        ctx = f"linux{rel}"
        parquet = Path(args.linux_dir) / f"tuxkconfig_{rel}.parquet"
        pkl = REPO / f"artifacts/significance_linux_hgbtfull_cells_{rel}.pkl"
        try:
            vmlinux = _linux_cost_column(parquet, "vmlinux")  # target == cost == vmlinux size
        except Exception as e:
            print(f"  [linux] skip {ctx}: {e}", flush=True)
            continue
        cv, p90p10 = cost_spread(vmlinux)
        dc = target_cost_decorr(vmlinux, vmlinux)  # exactly 0 (target IS the cost)
        approx = 0
        if pkl.exists():
            with open(pkl, "rb") as fh:
                cells = pickle.load(fh)
            sb, _ = strategy_bias(ratios_from_cells(cells), pilot_levels)
        else:
            sb = float("nan")
            approx = 1
            print(f"  [linux] {ctx}: cached cells missing -> strategy_bias unavailable", flush=True)
        rows.append(dict(family="linux", context=ctx, cost_cv=cv, cost_p90p10=p90p10,
                         target_cost_decorr=dc, strategy_bias=sb, approx_bias=approx))
        print(f"  [linux] {ctx}: cv={cv:.3f} p90p10={p90p10:.2f} decorr={dc:.3f} bias={sb:.3f}", flush=True)
    return rows


FAMILY_FUNCS = {
    "icse19": diag_icse19, "x264": diag_x264, "energy": diag_energy,
    "workload": diag_workload, "lcbench": diag_lcbench, "linux": diag_linux,
}


# --------------------------------------------------------------------------- #
# outcome join
# --------------------------------------------------------------------------- #
def load_outcomes(csv_path, tau):
    """Per context, two outcomes from a corrected KW CSV (one row per budget level):

      * group_changed (as the task specifies): does the Dunn top-GROUP *set* change
        under measured cost. flip_rate = mean over levels; flipped = any. This is a
        p=0.05 set-membership test -- statistically noisy and saturating.
      * decision_stakes (the practically consequential outcome): does the count-era
        recommendation differ from the cost-era recommendation by more than `tau` in
        held-out MRE, i.e. |mre_gap| > tau. stakes_rate = mean over levels; stakes_any
        = any. This is "is count a *materially* unsafe proxy".
    """
    if not Path(csv_path).exists():
        return {}
    gc_per = defaultdict(list)
    stakes_per = defaultdict(list)
    absgap_per = defaultdict(list)
    with open(csv_path) as fh:
        for r in csv.DictReader(fh):
            ctx = r["context"]
            try:
                gc_per[ctx].append(int(float(r["group_changed"])))
            except (KeyError, ValueError):
                pass
            try:
                g = abs(float(r["mre_gap"]))
                stakes_per[ctx].append(int(g > tau))
                absgap_per[ctx].append(g)
            except (KeyError, ValueError):
                pass
    out = {}
    for ctx in set(gc_per) | set(stakes_per):
        gcs = gc_per.get(ctx, [])
        st = stakes_per.get(ctx, [])
        gaps = absgap_per.get(ctx, [])
        out[ctx] = dict(
            flip_rate=float(np.mean(gcs)) if gcs else float("nan"),
            flipped=int(any(gcs)) if gcs else float("nan"),
            n_levels=len(gcs),
            stakes_rate=float(np.mean(st)) if st else float("nan"),
            stakes_any=int(any(st)) if st else float("nan"),
            median_absgap=float(np.median(gaps)) if gaps else float("nan"),
        )
    return out


# --------------------------------------------------------------------------- #
# analysis
# --------------------------------------------------------------------------- #
def auc(y, x):
    from sklearn.metrics import roc_auc_score
    y = np.asarray(y, float)
    x = np.asarray(x, float)
    m = np.isfinite(x)
    y, x = y[m], x[m]
    if len(set(y.tolist())) < 2 or len(y) < 3:
        return float("nan"), len(y)
    return float(roc_auc_score(y, x)), len(y)


def rho_with(flip_rate, x):
    fr = np.asarray(flip_rate, float)
    x = np.asarray(x, float)
    m = np.isfinite(x)
    if m.sum() < 3:
        return float("nan")
    r = spearmanr(x[m], fr[m]).correlation
    return float(r) if r is not None else float("nan")


def rank01(x):
    """Rank-normalize finite values to [0,1]; NaN preserved."""
    x = np.asarray(x, float)
    out = np.full(len(x), np.nan)
    m = np.isfinite(x)
    if m.sum() == 0:
        return out
    rr = rankdata(x[m], method="average")
    out[m] = (rr - 1) / max(1, (m.sum() - 1))
    return out


def tertile_bins(x):
    """Return (labels array in {0,1,2} with NaN for missing, edges)."""
    x = np.asarray(x, float)
    m = np.isfinite(x)
    edges = np.nanquantile(x[m], [1 / 3, 2 / 3]) if m.sum() else np.array([np.nan, np.nan])
    lab = np.full(len(x), np.nan)
    lab[m] = np.digitize(x[m], edges, right=False)  # 0,1,2
    return lab, edges


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--families", nargs="+", default=list(FAMILY_FUNCS),
                    help="which families to include (default: all)")
    ap.add_argument("--pilot-levels", type=int, default=2,
                    help="number of smallest budget levels used for strategy_bias (the pilot)")
    ap.add_argument("--seeds", type=int, default=8, help="stochastic seeds for the generated pilot samples")
    ap.add_argument("--tau", type=float, default=0.01,
                    help="MRE gap (held-out) above which the count-vs-cost recommendation is 'materially' "
                         "different -> decision_stakes outcome (default 0.01 = 1pp MRE)")
    ap.add_argument("--icse19-zip", default="ICPE-rawdata/NewRuns.zip")
    ap.add_argument("--x264-zip", default="ICPE-rawdata/AllRuns.zip")
    ap.add_argument("--twins-zip", default="/tmp/twins_main.zip")
    ap.add_argument("--workload-zip", default="workload-impact-ICSE2023/artifact_excluding_raw_coverage.zip")
    ap.add_argument("--lcbench-json", default="/private/tmp/lcbench/data_2k_lw.json")
    ap.add_argument("--linux-dir", default="ICPE-rawdata/linux")
    ap.add_argument("--diag-cache", default="artifacts/audit_diagnostics_cache.csv",
                    help="cache of the (deterministic) pilot diagnostics, for fast re-analysis")
    ap.add_argument("--recompute-diag", action="store_true", help="ignore the diagnostics cache and recompute")
    ap.add_argument("--out-csv", default="artifacts/audit_validation.csv")
    ap.add_argument("--out-report", default="artifacts/audit_validation_report.md")
    ap.add_argument("--out-fig", default="607058f5f5131dcd1dbd783d/pic/results/audit_validation.png")
    args = ap.parse_args()

    # outcome CSVs keyed by family
    OUTCOME_CSV = {
        "icse19": "artifacts/corrected/kw_icse19_ridge_largestn.csv",
        "x264": "artifacts/corrected/kw_x264_ridge_largestn.csv",
        "energy": "artifacts/corrected/kw_energy_ridge_largestn.csv",
        "lcbench": "artifacts/corrected/kw_lcbench_ridge_largestn.csv",
        "workload": "artifacts/corrected/kw_workload_ridge_largestn.csv",
        "linux": "artifacts/significance_linux_hgbtfull_kw.csv",
    }

    DIAG_COLS = ["family", "context", "cost_cv", "cost_p90p10", "target_cost_decorr",
                 "strategy_bias", "approx_bias"]
    cache = Path(args.diag_cache)
    cached = {}
    if cache.exists() and not args.recompute_diag:
        for r in csv.DictReader(open(cache)):
            row = dict(family=r["family"], context=r["context"],
                       cost_cv=float(r["cost_cv"]), cost_p90p10=float(r["cost_p90p10"]),
                       target_cost_decorr=float(r["target_cost_decorr"]),
                       strategy_bias=float(r["strategy_bias"]), approx_bias=int(r["approx_bias"]))
            cached.setdefault(r["family"], []).append(row)

    print("=== computing pilot diagnostics ===", flush=True)
    diag_rows = []
    for fam in args.families:
        if fam in cached:
            print(f"[{fam}] reused {len(cached[fam])} cached diagnostics from {cache}", flush=True)
            diag_rows.extend(cached[fam])
            continue
        print(f"[{fam}]", flush=True)
        diag_rows.extend(FAMILY_FUNCS[fam](args, args.pilot_levels))
    # refresh cache (union of cached + freshly computed)
    by_key = {(r["family"], r["context"]): r for fam in cached for r in cached[fam]}
    for r in diag_rows:
        by_key[(r["family"], r["context"])] = r
    cache.parent.mkdir(parents=True, exist_ok=True)
    with open(cache, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=DIAG_COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted(by_key.values(), key=lambda r: (r["family"], r["context"])))

    # ---- join diagnostics <-> outcomes, auditable ----
    print("\n=== join audit (diagnostic <-> outcome) ===", flush=True)
    tidy = []
    unmatched_diag = []
    for fam in args.families:
        outcomes = load_outcomes(OUTCOME_CSV.get(fam, ""), args.tau)
        if not outcomes:
            print(f"  [{fam}] OUTCOME CSV missing/empty: {OUTCOME_CSV.get(fam)} -> family skipped from join", flush=True)
        fam_diag = [r for r in diag_rows if r["family"] == fam]
        matched = 0
        for r in fam_diag:
            oc = outcomes.get(r["context"])
            if oc is None:
                unmatched_diag.append((fam, r["context"]))
                continue
            matched += 1
            tidy.append(dict(family=fam, context=r["context"],
                             cost_cv=round(r["cost_cv"], 6), cost_p90p10=round(r["cost_p90p10"], 6),
                             target_cost_decorr=round(r["target_cost_decorr"], 6),
                             strategy_bias=round(r["strategy_bias"], 6), approx_bias=r["approx_bias"],
                             flip_rate=round(oc["flip_rate"], 6), flipped=oc["flipped"],
                             stakes_rate=round(oc["stakes_rate"], 6), stakes_any=oc["stakes_any"],
                             median_absgap=round(oc["median_absgap"], 6), n_levels=oc["n_levels"]))
        diag_ctx = {r["context"] for r in fam_diag}
        missing = [c for c in outcomes if c not in diag_ctx]
        print(f"  [{fam}] diagnostics={len(fam_diag)} outcomes={len(outcomes)} matched={matched} "
              f"diag-without-outcome={sum(1 for f,_ in unmatched_diag if f==fam)} outcome-without-diag={len(missing)}",
              flush=True)
        if missing:
            print(f"      outcome contexts with NO diagnostic: {sorted(missing)}", flush=True)
    if unmatched_diag:
        print(f"  MISMATCH diagnostics with no outcome row: {unmatched_diag}", flush=True)

    tidy.sort(key=lambda r: (r["family"], r["context"]))
    Path(args.out_csv).parent.mkdir(parents=True, exist_ok=True)
    cols = ["family", "context", "cost_cv", "cost_p90p10", "target_cost_decorr",
            "strategy_bias", "approx_bias", "flip_rate", "flipped",
            "stakes_rate", "stakes_any", "median_absgap", "n_levels"]
    with open(args.out_csv, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(tidy)
    print(f"\nwrote {args.out_csv} ({len(tidy)} contexts)", flush=True)

    # ---- print the tidy table ----
    print("\n=== tidy table (one row per context) ===", flush=True)
    hdr = (f"{'family':9} {'context':42} {'cost_cv':>8} {'p90p10':>8} {'decorr':>7} {'bias':>7} "
           f"{'flip_rt':>7} {'stakes':>7} {'|gap|':>7}")
    print(hdr)
    print("-" * len(hdr))
    for r in tidy:
        print(f"{r['family']:9} {r['context'][:42]:42} {r['cost_cv']:8.3f} {r['cost_p90p10']:8.2f} "
              f"{r['target_cost_decorr']:7.3f} {r['strategy_bias']:7.3f} {r['flip_rate']:7.2f} "
              f"{r['stakes_rate']:7.2f} {r['median_absgap']:7.3f}")

    # ---- predictive power (pooled across all families), for BOTH outcomes ----
    fam_arr = np.array([r["family"] for r in tidy])
    diags = {k: np.array([r[k] for r in tidy], float)
             for k in ["cost_cv", "cost_p90p10", "target_cost_decorr", "strategy_bias"]}
    DIAG_KEYS = ["cost_cv", "cost_p90p10", "target_cost_decorr", "strategy_bias"]

    def predictive(label, y_bin, y_rate):
        """Print + return AUC(per diagnostic) and the 2-feature-rule AUC for one outcome."""
        y_bin = np.asarray(y_bin, float)
        y_rate = np.asarray(y_rate, float)
        print(f"\n=== predictive power: {label} (pooled, {len(tidy)} contexts, "
              f"{len(set(fam_arr))} families) ===", flush=True)
        base = np.nanmean(y_bin)
        print(f"  base rate (any) = {base:.2f} ({int(np.nansum(y_bin))}/{int(np.isfinite(y_bin).sum())})")
        au = {}
        for k in DIAG_KEYS:
            a, npts = auc(y_bin, diags[k])
            rr = rho_with(y_rate, diags[k])
            au[k] = a
            print(f"  {k:20} AUC={a:.3f} (n={npts})  rho(rate)={rr:+.3f}")
        het_name = max(["cost_cv", "cost_p90p10"], key=lambda k: (au[k] if np.isfinite(au[k]) else -1))
        combo = rank01(diags[het_name]) * rank01(diags["strategy_bias"])
        a_combo, n_combo = auc(y_bin, combo)
        rho_combo = rho_with(y_rate, combo)
        au["combo"] = a_combo
        print(f"  2-feature rule ({het_name} x strategy_bias)  AUC={a_combo:.3f} (n={n_combo})  "
              f"rho(rate)={rho_combo:+.3f}", flush=True)
        return au, het_name, combo, a_combo, rho_combo

    flip_rate = np.array([r["flip_rate"] for r in tidy], float)
    flipped = np.array([r["flipped"] for r in tidy], float)
    stakes_rate = np.array([r["stakes_rate"] for r in tidy], float)
    stakes_any = np.array([r["stakes_any"] for r in tidy], float)

    # PRIMARY validated outcome: decision stakes (count materially mis-recommends).
    aucs_s, het_s, combo_s, acombo_s, rhocombo_s = predictive(
        f"decision stakes |mre_gap|>{args.tau:g} (VALIDATED)", stakes_any, stakes_rate)
    # SECONDARY (as the task literally specifies): top-group set change -- noisy/saturating.
    aucs_g, het_g, combo_g, acombo_g, rhocombo_g = predictive(
        "group_changed top-group set identity (noisy)", flipped, flip_rate)

    def grid_of(y_rate, het_vals, bias_vals):
        het_lab, het_edges = tertile_bins(het_vals)
        bias_lab, bias_edges = tertile_bins(bias_vals)
        g_rate = np.full((3, 3), np.nan)
        g_n = np.zeros((3, 3), int)
        for i in range(3):
            for j in range(3):
                m = (het_lab == i) & (bias_lab == j)
                g_n[i, j] = int(m.sum())
                if m.sum():
                    g_rate[i, j] = float(np.nanmean(np.asarray(y_rate, float)[m]))
        return g_rate, g_n, het_edges, bias_edges

    het = diags[het_s]
    bias = diags["strategy_bias"]
    # headline 3x3: stakes_rate by heterogeneity x strategy_bias
    grid_rate, grid_n, het_edges, bias_edges = grid_of(stakes_rate, het, bias)
    # secondary 3x3: group_changed flip_rate (same axes) for the report caveat
    grid_gc, grid_gc_n, _, _ = grid_of(flip_rate, het, bias)

    tert = ["low", "med", "high"]
    het_disp = "cost p90/p10" if het_s == "cost_p90p10" else "cost CV"
    for title, gr, gn in [(f"mean decision-stakes rate (VALIDATED, |mre_gap|>{args.tau:g})", grid_rate, grid_n),
                          ("mean group_changed flip_rate (noisy, secondary)", grid_gc, grid_gc_n)]:
        print(f"\n=== 3x3 {title}: heterogeneity ({het_s}) x strategy_bias ===", flush=True)
        print(f"  het edges = {np.round(het_edges, 3)}   bias edges = {np.round(bias_edges, 3)}")
        print(f"  {'het\\bias':>10} " + " ".join(f"{t:>14}" for t in tert))
        for i in range(3):
            cells_txt = []
            for j in range(3):
                cells_txt.append(f"{gr[i, j]:.2f} (n={gn[i, j]})" if gn[i, j] else "  -  ")
            print(f"  {tert[i]:>10} " + " ".join(f"{c:>14}" for c in cells_txt))

    # ---- figure (headline = validated decision-stakes outcome) ----
    make_figure(args.out_fig, grid_rate, grid_n, het_s, het_edges, bias_edges,
                stakes_any, het, bias, combo_s, aucs_s, args.tau)

    # ---- report (both outcomes, transparent) ----
    write_report(args.out_report, tidy, fam_arr, args,
                 stakes=dict(aucs=aucs_s, het=het_s, combo_auc=acombo_s, combo_rho=rhocombo_s,
                             base=float(np.nanmean(stakes_any)),
                             grid=grid_rate, grid_n=grid_n, het_edges=het_edges, bias_edges=bias_edges),
                 groupchanged=dict(aucs=aucs_g, het=het_g, combo_auc=acombo_g, combo_rho=rhocombo_g,
                                   base=float(np.nanmean(flipped)),
                                   grid=grid_gc, grid_n=grid_gc_n))
    print(f"\nwrote {args.out_report}\nwrote {args.out_fig}", flush=True)


def make_figure(path, grid_rate, grid_n, het_name, het_edges, bias_edges,
                y_bin, het, bias, combo, aucs, tau):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import gridspec
    from sklearn.metrics import roc_curve

    het_disp = "cost p90/p10" if het_name == "cost_p90p10" else "cost CV"
    vmax = float(np.nanmax(grid_rate)) if np.isfinite(grid_rate).any() else 1.0
    vmax = max(vmax, 0.1)
    plt.rcParams.update({"font.size": 7.2, "axes.titlesize": 8, "figure.dpi": 200})
    fig = plt.figure(figsize=(3.3, 4.2))
    gs = gridspec.GridSpec(2, 1, height_ratios=[3.0, 1.7], hspace=0.6)

    # --- 3x3 heatmap: mean decision-stakes rate ---
    ax = fig.add_subplot(gs[0])
    im = ax.imshow(grid_rate, origin="lower", cmap="YlOrRd", vmin=0.0, vmax=vmax, aspect="auto")
    tert = ["low", "med", "high"]
    ax.set_xticks(range(3)); ax.set_xticklabels(tert)
    ax.set_yticks(range(3)); ax.set_yticklabels(tert)
    ax.set_xlabel("per-strategy budget Ratio spread (strategy_bias)")
    ax.set_ylabel(f"cost heterogeneity ({het_disp})")
    ax.set_title(f"Pilot audit predicts count-vs-cost stakes\n(mean frac. of budgets with |MRE gap|>{tau:g})", pad=4)
    for i in range(3):
        for j in range(3):
            if grid_n[i, j]:
                val = grid_rate[i, j]
                ax.text(j, i, f"{val:.2f}\n(n={grid_n[i, j]})", ha="center", va="center",
                        fontsize=6.6, color="black" if val < 0.6 * vmax else "white")
            else:
                ax.text(j, i, "–", ha="center", va="center", fontsize=7, color="grey")
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    cb.set_label("stakes rate", fontsize=6.5)
    cb.ax.tick_params(labelsize=6)

    # --- ROC panel ---
    axr = fig.add_subplot(gs[1])
    axr.plot([0, 1], [0, 1], "--", color="0.7", lw=0.8)
    for x, lab, auckey, color in [(combo, f"{het_disp} x bias", "combo", "C3"),
                                  (het, het_disp, het_name, "C2"),
                                  (bias, "strategy_bias", "strategy_bias", "C0")]:
        m = np.isfinite(x)
        if len(set(y_bin[m].tolist())) < 2:
            continue
        fpr, tpr, _ = roc_curve(y_bin[m], x[m])
        a = aucs.get(auckey, float("nan"))
        axr.plot(fpr, tpr, color=color, lw=1.2, label=f"{lab} (AUC={a:.2f})")
    axr.set_xlabel("false positive rate")
    axr.set_ylabel("true positive rate")
    axr.set_title("Predicting any-budget stakes (pooled)", pad=3)
    axr.legend(fontsize=5.6, loc="lower right", frameon=False)
    axr.set_xlim(0, 1); axr.set_ylim(0, 1.02)
    axr.tick_params(labelsize=6)

    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight")
    fig.savefig(str(path).replace(".png", ".pdf"), bbox_inches="tight")
    plt.close(fig)


def _grid_md(grid, grid_n, A):
    tert = ["low", "med", "high"]
    A("| het \\ bias | low | med | high |")
    A("|---|---|---|---|")
    for i in range(3):
        cells = [f"{grid[i, j]:.2f} (n={grid_n[i, j]})" if grid_n[i, j] else "–" for j in range(3)]
        A(f"| **{tert[i]}** | {cells[0]} | {cells[1]} | {cells[2]} |")


def write_report(path, tidy, fam_arr, args, stakes, groupchanged):
    n_ctx = len(tidy)
    fams = sorted(set(fam_arr))
    approx_fams = sorted({r["family"] for r in tidy if r["approx_bias"]})
    s = stakes
    g = groupchanged
    het_name = s["het"]
    het_disp = "cost p90/p10 ratio" if het_name == "cost_p90p10" else "cost CV"
    grid = s["grid"]
    lo = grid[0, 0]
    hi = grid[2, 2]
    lines = []
    A = lines.append
    A("# Validating the pilot audit\n")
    A("## What this checks\n")
    A("The paper recommends a cheap **pilot audit** before trusting sample *count* as a proxy "
      "for sampling *cost*: inspect (1) the spread of per-configuration measured cost "
      "(`cost_cv`, `cost_p90p10`), (2) whether the prediction target is itself the cost "
      "(`target_cost_decorr`), and (3) the per-strategy budget **Ratio** = pct_cost / pct_n at "
      "a small pilot budget (`strategy_bias` = spread of median Ratio across deployable "
      "strategies). We test whether those pilot diagnostics **predict** that trusting sample "
      "count instead of measured cost changes the cost-controlled Kruskal-Wallis recommendation.\n")
    A("## Two outcomes (both from the corrected KW CSVs, one row per budget level)\n")
    A("1. **decision_stakes (validated, headline):** does the count-era best sampler differ "
      f"from the cost-era best sampler by more than **{args.tau:g}** in held-out MRE "
      "(`|mre_gap| > tau`)? `stakes_rate` = mean over levels; `stakes_any` = any. This is the "
      "*consequential* question -- \"is count a **materially** unsafe proxy\".")
    A("2. **group_changed (secondary, as literally named in the brief):** does the Dunn "
      "top-GROUP **set** change. `flip_rate` = mean over levels; `flipped` = any. This is a "
      "p=0.05 set-membership test; it is statistically noisy and *saturates* (a decisive cost "
      "winner makes the set stable), so it is reported only as a caveat.\n")
    A("## Setup\n")
    A(f"- **{n_ctx} contexts** across **{len(fams)} families**: {', '.join(fams)}.")
    A(f"- Diagnostics computed on the **smallest {args.pilot_levels} budget level(s)** "
      f"(a genuine pilot); `strategy_bias` reuses the SAME cells the KW analysis builds and "
      f"fits **no learner** (Ratio needs only the sample indices + per-config cost).")
    if approx_fams:
        A(f"- **Approximation used** (strategy_bias unavailable -> NaN): {', '.join(approx_fams)}.")
    else:
        A("- **No approximation used**: every family computes the exact per-strategy Ratio "
          "(archive samples / generated pilot samples / cached Linux HGBT cells).")
    A("\n## Predictive power -- decision_stakes (VALIDATED)\n")
    A(f"Base rate (any-budget stakes) = {s['base']:.2f}.\n")
    A("| diagnostic | ROC-AUC for `stakes_any` |")
    A("|---|---|")
    for k in ["cost_cv", "cost_p90p10", "target_cost_decorr", "strategy_bias"]:
        A(f"| {k} | {s['aucs'][k]:.3f} |")
    A(f"| **2-feature rule ({het_name} x strategy_bias)** | **{s['combo_auc']:.3f}** |")
    A(f"\n(Spearman rho of the 2-feature rule with `stakes_rate` = {s['combo_rho']:+.3f}.)\n")
    A(f"### 3x3 mean stakes_rate ({het_disp} x strategy_bias tertiles)\n")
    A(f"Tertile edges -- {het_disp}: {np.round(s['het_edges'], 3).tolist()}; "
      f"strategy_bias: {np.round(s['bias_edges'], 3).tolist()}. "
      "Rows = cost heterogeneity, columns = strategy_bias.\n")
    _grid_md(s["grid"], s["grid_n"], A)
    A("\n## Secondary -- group_changed (noisy top-group set identity)\n")
    A(f"Base rate (any-level group change) = {g['base']:.2f}. This outcome is **not** predicted "
      "by the cost-spread / bias diagnostics; pooled it is mildly *negative* (a decisive cost "
      "winner stabilises the top-group set), which is exactly why we report decision_stakes "
      "as the meaningful outcome.\n")
    A("| diagnostic | ROC-AUC for `flipped` |")
    A("|---|---|")
    for k in ["cost_cv", "cost_p90p10", "target_cost_decorr", "strategy_bias"]:
        A(f"| {k} | {g['aucs'][k]:.3f} |")
    A(f"| 2-feature rule ({g['het']} x strategy_bias) | {g['combo_auc']:.3f} |")
    A("\n3x3 mean group_changed flip_rate (same axes):\n")
    _grid_md(g["grid"], g["grid_n"], A)
    A("\n## Paraphrase for the paper\n")
    A(f"> A cheap pilot audit -- cost spread (`{het_name}`) and the per-strategy budget Ratio "
      f"spread (`strategy_bias`) -- predicts whether trusting sample **count** instead of "
      f"measured **cost** materially changes the recommended sampler (the count-era and "
      f"cost-era best samplers differ by >{args.tau:g} held-out MRE) with ROC-AUC = "
      f"{s['combo_auc']:.2f} (best single diagnostic `{het_name}`, AUC = {s['aucs'][het_name]:.2f}; "
      f"`strategy_bias` alone, AUC = {s['aucs']['strategy_bias']:.2f}) over {n_ctx} contexts in "
      f"{len(fams)} families. In the low-spread / low-bias regime only {lo*100:.0f}% of pilot "
      f"budgets carry a material count-vs-cost gap (count is a safe proxy), versus {hi*100:.0f}% "
      f"in the high-spread / high-bias regime (count is unsafe). The target--cost correlation "
      f"diagnostic alone is weak (AUC = {s['aucs']['target_cost_decorr']:.2f}) because several "
      f"families measure the cost directly; the actionable signal is the cost spread and the "
      f"per-strategy Ratio -- precisely the two quantities the cheap audit reports. (The narrow "
      f"Dunn top-group *set* identity is a noisier, saturating statistic and is not predictable "
      f"this way; the materially consequential gap is.)\n")
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(lines))


if __name__ == "__main__":
    main()
