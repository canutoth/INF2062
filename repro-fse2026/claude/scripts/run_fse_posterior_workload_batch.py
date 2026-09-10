#!/usr/bin/env python3
"""Run FSE-style posterior-bound analysis on the WORKLOAD family (ICSE'23).

Each context is one (system, workload) pair from the workload-impact artifact
(Muehlbauer et al., ICSE 2023, Zenodo 7504284). Sampling follows the public
ICSE generated-sampling protocol; posterior risk/confidence and
cost-normalized decisions follow the FSE-posterior pipeline shared with the
other corpus runners. The measured column (wall time, or throughput for h2)
serves as both the bound target and the empirical acquisition cost, matching
the public KW engine's workload mode.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
for path in (REPO_ROOT, SCRIPT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from cost_sampling.analysis import level_sort_key, write_csv
from cost_sampling.generated_sampling import (
    load_workload_table,
    parse_where,
    subset_measured_table,
)

from fse_posterior_generated_common import (
    clamp_budgets,
    parse_levels,
    run_posterior_scenario,
    slug,
    strategy_budget_trends,
    summarize_scope_levels,
    write_family_report,
)

ALL_SYSTEMS = ["batik", "dconvert", "h2", "jump3r", "kanzi", "lrzip", "x264", "xz", "z3"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--zip",
        default="workload-impact-ICSE2023/artifact_excluding_raw_coverage.zip",
        help="Path to artifact_excluding_raw_coverage.zip (Zenodo 7504284).",
    )
    parser.add_argument("--systems", nargs="+", default=["ALL"], help="Systems, or ALL for the nine-study set.")
    parser.add_argument("--workloads", default="ALL", help="Comma-separated workload names, or ALL.")
    parser.add_argument("--workload-limit", type=int, default=0, help="Optional first-N workload limit per system.")
    parser.add_argument(
        "--target-column",
        default=None,
        help="Bound target column; default picks `time`, falling back to `throughput`.",
    )
    parser.add_argument(
        "--cost-column",
        default=None,
        help="Empirical cost column; default: same as the target column.",
    )
    parser.add_argument("--levels", default="n8,n16,n32,n64", help="Comma-separated budgets, e.g. n8,n16,n32.")
    parser.add_argument("--seeds", type=int, default=30, help="Stochastic seeds per budget.")
    parser.add_argument("--output-dir", default="artifacts/fse_posterior_workload")
    parser.add_argument("--no-oracles", action="store_true", help="Skip cheap/expensive diagnostic oracles.")
    parser.add_argument("--no-srs", action="store_true")
    parser.add_argument("--srs-seeds", type=int, default=30)
    parser.add_argument("--srs-step-size", type=int, default=25)
    parser.add_argument("--srs-p-threshold", type=float, default=0.05)
    parser.add_argument("--extreme", choices=("max", "min"), default="max")
    parser.add_argument("--prior-offset", type=int, default=1)
    parser.add_argument("--epsilon-points", type=int, default=151)
    parser.add_argument("--plot-epsilon-max", type=float, default=0.15)
    parser.add_argument("--no-figures", action="store_true")
    parser.add_argument("--max-rows", type=int, default=None, help="Optional row subsample for huge tables.")
    parser.add_argument("--row-seed", type=int, default=0)
    parser.add_argument(
        "--where",
        action="append",
        default=[],
        metavar="COLUMN=VALUE",
        help="Extra row filters applied before workload splitting.",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Smoke profile: one system, three workloads, two budgets, fewer seeds.",
    )
    return parser.parse_args()


def _pick_column(labels: list[str], preferred: str | None) -> tuple[str, str]:
    """Return (column, cost_orientation) for a workload measured table."""

    if preferred is not None:
        return preferred, "inverse" if preferred == "throughput" else "lower"
    usable = [c for c in labels if c != "config_id"]
    if "time" in usable:
        return "time", "lower"
    if "throughput" in usable:
        return "throughput", "inverse"
    if not usable:
        raise ValueError("no usable label column")
    return usable[0], "lower"


def main() -> None:
    args = parse_args()
    systems = ALL_SYSTEMS if [s.upper() for s in args.systems] == ["ALL"] else args.systems
    workload_filter = (
        None
        if args.workloads.strip().upper() == "ALL"
        else {part.strip() for part in args.workloads.split(",") if part.strip()}
    )
    budgets_requested = parse_levels(args.levels)
    seeds = args.seeds
    srs_seeds = args.srs_seeds
    workload_limit = args.workload_limit
    if args.quick:
        systems = systems[:1]
        budgets_requested = budgets_requested[:2]
        seeds = min(seeds, 10)
        srs_seeds = min(srs_seeds, 10)
        if workload_limit == 0:
            workload_limit = 3

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    all_rows: dict[str, list[dict[str, Any]]] = {
        "records": [],
        "summary": [],
        "curves": [],
        "pareto": [],
        "hypotheses": [],
        "hypothesis_summary": [],
    }
    scope_rows: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    done_contexts: list[str] = []

    for system in systems:
        try:
            print(f"[workload] loading {system}", flush=True)
            table = load_workload_table(
                args.zip,
                system,
                where=parse_where(args.where),
                max_rows=args.max_rows,
                row_seed=args.row_seed,
            )
        except Exception as exc:  # noqa: BLE001
            skipped.append({"context": system, "error": str(exc)})
            print(f"[workload] skipped {system}: {exc}", flush=True)
            continue

        if "workload" not in table.rows[0]:
            skipped.append({"context": system, "error": "no workload column in merged table"})
            continue
        workloads = sorted({row["workload"] for row in table.rows})
        if workload_filter is not None:
            workloads = [w for w in workloads if w in workload_filter]
        if workload_limit > 0:
            workloads = workloads[:workload_limit]

        try:
            target_column, orientation = _pick_column(table.label_columns, args.target_column)
        except ValueError as exc:
            skipped.append({"context": system, "error": str(exc)})
            continue
        cost_column = args.cost_column or target_column

        for workload in workloads:
            context = f"{system}__{workload}"
            try:
                indices = np.asarray(
                    [idx for idx, row in enumerate(table.rows) if row["workload"] == workload],
                    dtype=int,
                )
                subset = subset_measured_table(
                    table, indices, analysis_name=f"{system}__workload_{slug(workload)}"
                )
                budgets = clamp_budgets(budgets_requested, len(subset.rows), scope=context)
                if not budgets:
                    raise ValueError("no budgets left after protocol cap")
                metadata = {
                    "family": "workload",
                    "system": system,
                    "workload": workload,
                    "target_property": target_column,
                    "cost_property": cost_column,
                }
                result = run_posterior_scenario(
                    subset,
                    scope_dir=output_dir / f"workload_{slug(context)}",
                    report_name=f"workload_{slug(context)}_fse_posterior_report.md",
                    target_property=target_column,
                    cost_property=cost_column,
                    cost_orientation=orientation,
                    budgets=budgets,
                    seeds=seeds,
                    include_oracles=not args.no_oracles,
                    include_srs=not args.no_srs,
                    srs_seeds=srs_seeds,
                    srs_step_size=args.srs_step_size,
                    srs_p_threshold=args.srs_p_threshold,
                    extreme=args.extreme,
                    prior_offset=args.prior_offset,
                    epsilon_points=args.epsilon_points,
                    plot_epsilon_max=args.plot_epsilon_max,
                    figures_enabled=not args.no_figures,
                    metadata=metadata,
                )
                for key, rows in result.items():
                    all_rows[key].extend(rows)
                scope_rows.extend(
                    summarize_scope_levels(
                        scope=context,
                        summary=result["summary"],
                        hypotheses=result["hypotheses"],
                        scope_key="context_pair",
                    )
                )
                done_contexts.append(context)
                print(f"[workload] finished {context}", flush=True)
            except Exception as exc:  # noqa: BLE001
                skipped.append({"context": context, "error": str(exc)})
                print(f"[workload] skipped {context}: {exc}", flush=True)

    trend_rows = strategy_budget_trends(all_rows["summary"], scope_key="context")
    scope_rows.sort(key=lambda row: (row["context_pair"], level_sort_key(row["level"])))
    write_csv(output_dir / "posterior_records.csv", all_rows["records"])
    write_csv(output_dir / "posterior_strategy_summary.csv", all_rows["summary"])
    write_csv(output_dir / "posterior_confidence_curves.csv", all_rows["curves"])
    write_csv(output_dir / "posterior_pareto.csv", all_rows["pareto"])
    write_csv(output_dir / "posterior_hypothesis_tests.csv", all_rows["hypotheses"])
    write_csv(output_dir / "posterior_hypothesis_summary.csv", all_rows["hypothesis_summary"])
    write_csv(output_dir / "posterior_workload_context_summary.csv", scope_rows)
    write_csv(output_dir / "posterior_workload_budget_trends.csv", trend_rows)
    write_csv(output_dir / "skipped_contexts.csv", skipped)
    write_family_report(
        output_dir / "fse_posterior_workload_report.md",
        title="FSE 2026 posterior-risk revisit on the WORKLOAD family",
        scope_noun="context",
        scope_rows=scope_rows,
        trend_rows=trend_rows,
        hypothesis_rows=all_rows["hypotheses"],
        scope_key="context_pair",
        intro_lines=[
            "This applies the FSE posterior-risk/posterior-confidence framework to the",
            "ICSE 2023 workload-impact corpus. Each context is one (system, workload)",
            "pair; the measured wall time (throughput for h2) is both the bound target",
            "and the empirical acquisition cost, so the analysis asks how posterior",
            "guarantees per cost react to workload/input context. Posterior risk is",
            "relative to the measured configuration table of that context.",
            "",
            f"Source archive: `{args.zip}`.",
            f"Systems analyzed: `{', '.join(systems)}`.",
        ],
        srs_enabled=not args.no_srs,
        srs_seeds=srs_seeds,
        include_oracles=not args.no_oracles,
    )
    print(f"Wrote WORKLOAD FSE posterior outputs to {output_dir}")
    if skipped:
        print(f"Skipped {len(skipped)} contexts; see skipped_contexts.csv")


if __name__ == "__main__":
    main()
