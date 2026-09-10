#!/usr/bin/env python3
"""Equal-measured-spend comparison on LCBench measured pools.

Companion to `run_energy_equal_spend.py`. LCBench is the weak
cost-target-coupling case (cost = training runtime, target = final
validation accuracy), so the tail-avoidance mechanism that sinks pilotCost
on the ENERGY family predicts a much smaller penalty here: cheap
configurations are not systematically depleted of high-accuracy ones, so
pilotCost's volume advantage at equal spend should (partially) pay off.

Checkpointed per dataset: rerun after a kill to resume.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any, Callable

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
for path in (REPO_ROOT, SCRIPT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from cost_sampling.analysis import write_csv
from cost_sampling.generated_sampling import (
    _balanced_sample,
    _diversity_sample,
    _pair_sets,
    _pairwise_sample,
    _pilot_cost_sample,
    _value_codes,
    budget_grid,
    load_lcbench_table,
    oriented_cost,
    subset_measured_table,
)
from cost_sampling.srs import srs_indices

from run_energy_equal_spend import affordable_sample, posterior_risk


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", default="/private/tmp/lcbench/data_2k_lw.json")
    parser.add_argument("--datasets", default="ALL")
    parser.add_argument("--target-column", default="final_val_accuracy")
    parser.add_argument("--cost-column", default="time_total")
    parser.add_argument("--runtime-mode", choices=("last", "sum"), default="last")
    parser.add_argument("--ref-levels", default="8,16,32,64")
    parser.add_argument("--seeds", type=int, default=30)
    parser.add_argument("--srs-seeds", type=int, default=30)
    parser.add_argument("--output-dir", default="artifacts/fse_posterior_lcbench_equal_spend")
    parser.add_argument("--quick", action="store_true", help="Three datasets, two budgets, 10 seeds.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ref_levels = [int(x) for x in args.ref_levels.split(",")]
    seeds, srs_seeds = args.seeds, args.srs_seeds
    dataset_filter = None if args.datasets.strip().upper() == "ALL" else {
        d.strip() for d in args.datasets.split(",") if d.strip()
    }
    limit = 0
    if args.quick:
        ref_levels = ref_levels[:2]
        seeds = min(seeds, 10)
        srs_seeds = min(srs_seeds, 10)
        limit = 3

    output_dir = Path(args.output_dir)
    parts_dir = output_dir / "parts"
    parts_dir.mkdir(parents=True, exist_ok=True)

    print("[eqspend-lc] loading LCBench JSON (large)", flush=True)
    table = load_lcbench_table(args.json, runtime_mode=args.runtime_mode)
    workloads = sorted({row["workload"] for row in table.rows})
    if dataset_filter is not None:
        workloads = [w for w in workloads if w in dataset_filter]
    if limit:
        workloads = workloads[:limit]

    skipped: list[dict[str, Any]] = []
    for workload in workloads:
        slug = "".join(ch if ch.isalnum() else "_" for ch in workload).strip("_")
        part_path = parts_dir / f"{slug}.csv"
        if part_path.exists():
            print(f"[eqspend-lc] {workload} already done (checkpoint), skipping", flush=True)
            continue
        try:
            indices = np.asarray(
                [i for i, row in enumerate(table.rows) if row["workload"] == workload], dtype=int
            )
            subset = subset_measured_table(table, indices, analysis_name=f"lcbench__{slug}")
            y = np.asarray([float(row[args.target_column]) for row in subset.rows])
            raw_cost = np.asarray([float(row[args.cost_column]) for row in subset.rows])
            cost_values = oriented_cost(raw_cost, "lower")
            mean_cost = float(np.mean(cost_values))
            n_configs = len(subset.rows)
            n_cap = max(budget_grid(n_configs), default=0)
            if n_cap == 0:
                raise ValueError("no valid budget grid")
            value_codes = _value_codes(subset.raw_feature_values)
            pair_sets = _pair_sets(value_codes)
            print(f"[eqspend-lc] {workload} (pool {n_configs}, cap {n_cap})", flush=True)

            builders: dict[str, tuple[bool, Callable[[int, int], np.ndarray]]] = {
                "random": (True, lambda n, s: np.sort(
                    np.random.default_rng(s).choice(n_configs, size=n, replace=False))),
                "balanced": (True, lambda n, s: np.asarray(
                    _balanced_sample(value_codes, n, np.random.default_rng(s)), dtype=int)),
                "pilotCost": (True, lambda n, s: np.asarray(
                    _pilot_cost_sample(subset.X, cost_values, n, np.random.default_rng(s)), dtype=int)),
                "diversity": (False, lambda n, s: np.asarray(
                    _diversity_sample(subset.X, n, np.random.default_rng(0)), dtype=int)),
                "pairwise": (False, lambda n, s: np.asarray(
                    _pairwise_sample(pair_sets, n, np.random.default_rng(0)), dtype=int)),
                "SRSSampling": (True, lambda n, s: srs_indices(
                    subset.X, y, n, rng=s + 1, extreme="max")),
            }

            part_records: list[dict[str, Any]] = []
            for n_ref in ref_levels:
                if n_ref > n_cap:
                    continue
                budget = n_ref * mean_cost
                for strategy, (stochastic, build) in builders.items():
                    strat_seeds = (srs_seeds if strategy == "SRSSampling" else seeds) if stochastic else 1
                    for seed in range(strat_seeds):
                        idx, n_aff, spent, cap_hit = affordable_sample(
                            lambda n, _s=seed, _b=build: _b(n, _s), cost_values, budget, n_cap
                        )
                        part_records.append(
                            {
                                "workload": workload,
                                "scenario": f"lcbench__{slug}",
                                "ref_level": f"n{n_ref}",
                                "budget": budget,
                                "strategy": strategy,
                                "seed": seed,
                                "afforded_n": n_aff,
                                "spent": spent,
                                "budget_utilization": spent / budget if budget else float("nan"),
                                "cap_hit": int(cap_hit),
                                "posterior_risk": posterior_risk(y, idx),
                                "n_configurations": n_configs,
                            }
                        )
                print(f"[eqspend-lc]   n{n_ref} done", flush=True)
            write_csv(part_path, part_records)
            print(f"[eqspend-lc] finished {workload}", flush=True)
        except Exception as exc:  # noqa: BLE001
            skipped.append({"scope": workload, "error": str(exc)})
            print(f"[eqspend-lc] skipped {workload}: {exc}", flush=True)

    import pandas as pd

    part_frames = [pd.read_csv(p) for p in sorted(parts_dir.glob("*.csv"))]
    if not part_frames:
        raise SystemExit("No records produced.")
    df = pd.concat(part_frames, ignore_index=True)
    df.to_csv(output_dir / "equal_spend_records.csv", index=False)
    write_csv(output_dir / "skipped_scopes.csv", skipped)

    grouped = (
        df.groupby(["scenario", "ref_level", "strategy"])
        .agg(
            median_risk=("posterior_risk", "median"),
            mean_risk=("posterior_risk", "mean"),
            median_afforded_n=("afforded_n", "median"),
            cap_hits=("cap_hit", "sum"),
            runs=("seed", "count"),
            median_utilization=("budget_utilization", "median"),
        )
        .reset_index()
    )
    grouped.to_csv(output_dir / "equal_spend_strategy_summary.csv", index=False)

    scope_rows = []
    for (scenario, level), sub in grouped.groupby(["scenario", "ref_level"]):
        sub = sub.set_index("strategy")
        winner = sub["median_risk"].idxmin()
        rnd = sub.loc["random"] if "random" in sub.index else None
        pc = sub.loc["pilotCost"] if "pilotCost" in sub.index else None
        srs = sub.loc["SRSSampling"] if "SRSSampling" in sub.index else None
        scope_rows.append(
            {
                "scenario": scenario,
                "ref_level": level,
                "equal_spend_winner": winner,
                "winner_median_risk": float(sub.loc[winner, "median_risk"]),
                "random_risk": float(rnd["median_risk"]) if rnd is not None else float("nan"),
                "pilotCost_risk": float(pc["median_risk"]) if pc is not None else float("nan"),
                "srs_risk": float(srs["median_risk"]) if srs is not None else float("nan"),
                "pilotCost_beats_random": int(pc is not None and rnd is not None and pc["median_risk"] < rnd["median_risk"]),
                "srs_beats_random": int(srs is not None and rnd is not None and srs["median_risk"] < rnd["median_risk"]),
                "pilotCost_n_multiplier": float(pc["median_afforded_n"] / rnd["median_afforded_n"]) if pc is not None and rnd is not None and rnd["median_afforded_n"] else float("nan"),
                "pilotCost_cap_hits": int(pc["cap_hits"]) if pc is not None else 0,
            }
        )
    scope_df = pd.DataFrame(scope_rows).sort_values(["scenario", "ref_level"])
    scope_df.to_csv(output_dir / "equal_spend_scope_summary.csv", index=False)

    n_scopes = len(scope_df)
    pc_beats = int(scope_df["pilotCost_beats_random"].sum())
    srs_beats = int(scope_df["srs_beats_random"].sum())
    win_counts = scope_df["equal_spend_winner"].value_counts()
    lines = [
        "# Equal-measured-spend comparison (LCBench)",
        "",
        "Same protocol as the ENERGY equal-spend experiment; LCBench is the",
        "weak cost-target-coupling case (cost = runtime, target = accuracy),",
        "testing the mechanism prediction that pilotCost's equal-spend penalty",
        "shrinks or disappears when the outcome-relevant information is not",
        "concentrated in the expensive tail.",
        "",
        f"Scopes (dataset x budget level): {n_scopes}.",
        f"pilotCost beats random at equal spend in {pc_beats}/{n_scopes} scopes "
        f"(median affordable-n multiplier {scope_df['pilotCost_n_multiplier'].median():.2f}x; "
        f"capped in {int((scope_df['pilotCost_cap_hits'] > 0).sum())} scopes).",
        f"SRS beats random at equal spend in {srs_beats}/{n_scopes} scopes.",
        "",
        "Equal-spend winners:",
        "",
    ]
    for strategy, count in win_counts.items():
        lines.append(f"- `{strategy}`: {int(count)}/{n_scopes}")
    (output_dir / "equal_spend_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote LCBench equal-spend outputs to {output_dir}")


if __name__ == "__main__":
    main()
