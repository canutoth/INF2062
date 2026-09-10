#!/usr/bin/env python3
"""Run FSE-style posterior-bound analysis on the ENERGY (Twins) family.

Each scenario is one (system, cost property, target property) combination on a
TwinsOrFalseFriends measured table. Sampling follows the public ICSE
generated-sampling protocol (`cost_sampling.generated_sampling`); posterior
risk/confidence and cost-normalized decisions follow the FSE-posterior
pipeline shared with the other corpus runners.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
for path in (REPO_ROOT, SCRIPT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from cost_sampling.analysis import level_sort_key, write_csv
from cost_sampling.generated_sampling import load_twins_table, parse_where

from fse_posterior_generated_common import (
    clamp_budgets,
    parse_levels,
    run_posterior_scenario,
    slug,
    strategy_budget_trends,
    summarize_scope_levels,
    write_family_report,
)

ALL_SYSTEMS = [
    "7z",
    "Apache",
    "HSQLDB",
    "LLVM",
    "MongoDB",
    "PostgreSQL",
    "VP8",
    "brotli",
    "exastencils",
    "jump3r",
    "kanzi",
    "lrzip",
    "nginx",
    "x264",
]
# Same revision pinning as the public ICSE KW engine (kw_cost_vs_size.py).
REVISION_FILTERS: dict[str, dict[str, str]] = {
    "brotli": {"revision": "1.0.7"},
    "PostgreSQL": {"revision": "11.2"},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--zip",
        default="data/curated/energy/twins_energy_subset.zip",
        help="Path to the TwinsOrFalseFriends archive (curated subset or twins_main.zip).",
    )
    parser.add_argument(
        "--systems",
        nargs="+",
        default=["ALL"],
        help="Systems under data/<system>/measurements.csv, or ALL.",
    )
    parser.add_argument("--target-props", default="energy,performance", help="Comma-separated target properties.")
    parser.add_argument("--cost-props", default="energy,performance", help="Comma-separated cost properties.")
    parser.add_argument("--levels", default="n8,n16,n32,n64", help="Comma-separated budgets, e.g. n8,n16,n32.")
    parser.add_argument("--seeds", type=int, default=30, help="Stochastic seeds per budget.")
    parser.add_argument("--output-dir", default="artifacts/fse_posterior_energy")
    parser.add_argument("--cost-orientation", choices=("lower", "inverse"), default="lower")
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
        help="Extra row filters applied to every system (overrides revision pinning).",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Smoke profile: two systems, two budgets, fewer seeds.",
    )
    return parser.parse_args()


def _split(raw: str) -> list[str]:
    return [part.strip() for part in raw.split(",") if part.strip()]


def main() -> None:
    args = parse_args()
    systems = ALL_SYSTEMS if [s.upper() for s in args.systems] == ["ALL"] else args.systems
    target_props = _split(args.target_props)
    cost_props = _split(args.cost_props)
    budgets_requested = parse_levels(args.levels)
    seeds = args.seeds
    srs_seeds = args.srs_seeds
    if args.quick:
        systems = systems[:2]
        budgets_requested = budgets_requested[:2]
        seeds = min(seeds, 10)
        srs_seeds = min(srs_seeds, 10)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    extra_where = parse_where(args.where)

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
    done_scenarios: list[str] = []

    for system in systems:
        where = {**REVISION_FILTERS.get(system, {}), **extra_where}
        try:
            print(f"[energy] loading {system} (where={where or 'none'})", flush=True)
            table = load_twins_table(
                args.zip,
                system,
                where=where,
                max_rows=args.max_rows,
                row_seed=args.row_seed,
            )
        except Exception as exc:  # noqa: BLE001
            skipped.append({"scenario": system, "error": str(exc)})
            print(f"[energy] skipped {system}: {exc}", flush=True)
            continue

        available = set(table.rows[0].keys())
        for cost_prop in cost_props:
            for target_prop in target_props:
                scenario = f"{system}__cost_{cost_prop}__target_{target_prop}"
                if cost_prop not in available or target_prop not in available:
                    skipped.append(
                        {
                            "scenario": scenario,
                            "error": f"missing column(s); labels are {table.label_columns}",
                        }
                    )
                    print(f"[energy] skipped {scenario}: missing columns", flush=True)
                    continue
                try:
                    budgets = clamp_budgets(budgets_requested, len(table.rows), scope=scenario)
                    if not budgets:
                        raise ValueError("no budgets left after protocol cap")
                    metadata = {
                        "family": "energy",
                        "system": system,
                        "target_property": target_prop,
                        "cost_property": cost_prop,
                    }
                    result = run_posterior_scenario(
                        table,
                        scope_dir=output_dir / f"twins_{slug(scenario)}",
                        report_name=f"twins_{slug(scenario)}_fse_posterior_report.md",
                        target_property=target_prop,
                        cost_property=cost_prop,
                        cost_orientation=args.cost_orientation,
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
                            scope=scenario,
                            summary=result["summary"],
                            hypotheses=result["hypotheses"],
                            scope_key="scenario",
                        )
                    )
                    done_scenarios.append(scenario)
                    print(f"[energy] finished {scenario}", flush=True)
                except Exception as exc:  # noqa: BLE001
                    skipped.append({"scenario": scenario, "error": str(exc)})
                    print(f"[energy] skipped {scenario}: {exc}", flush=True)

    trend_rows = strategy_budget_trends(all_rows["summary"], scope_key="context")
    scope_rows.sort(key=lambda row: (row["scenario"], level_sort_key(row["level"])))
    write_csv(output_dir / "posterior_records.csv", all_rows["records"])
    write_csv(output_dir / "posterior_strategy_summary.csv", all_rows["summary"])
    write_csv(output_dir / "posterior_confidence_curves.csv", all_rows["curves"])
    write_csv(output_dir / "posterior_pareto.csv", all_rows["pareto"])
    write_csv(output_dir / "posterior_hypothesis_tests.csv", all_rows["hypotheses"])
    write_csv(output_dir / "posterior_hypothesis_summary.csv", all_rows["hypothesis_summary"])
    write_csv(output_dir / "posterior_energy_scenario_summary.csv", scope_rows)
    write_csv(output_dir / "posterior_energy_budget_trends.csv", trend_rows)
    write_csv(output_dir / "skipped_contexts.csv", skipped)
    write_family_report(
        output_dir / "fse_posterior_energy_report.md",
        title="FSE 2026 posterior-risk revisit on the ENERGY (Twins) family",
        scope_noun="scenario",
        scope_rows=scope_rows,
        trend_rows=trend_rows,
        hypothesis_rows=all_rows["hypotheses"],
        scope_key="scenario",
        intro_lines=[
            "This applies the FSE posterior-risk/posterior-confidence framework to the",
            "TwinsOrFalseFriends energy corpus. Each scenario is one (system, cost property,",
            "target property) combination; acquisition cost is the measured cost property",
            "(energy or runtime), so the same sampling question is asked under a different",
            "notion of cost. Posterior risk is relative to the measured configuration table.",
            "",
            f"Source archive: `{args.zip}`.",
            f"Systems analyzed: `{', '.join(systems)}`.",
            f"Cost properties: `{', '.join(cost_props)}`; target properties: `{', '.join(target_props)}`.",
        ],
        srs_enabled=not args.no_srs,
        srs_seeds=srs_seeds,
        include_oracles=not args.no_oracles,
    )
    print(f"Wrote ENERGY FSE posterior outputs to {output_dir}")
    if skipped:
        print(f"Skipped {len(skipped)} scenarios; see skipped_contexts.csv")


if __name__ == "__main__":
    main()
