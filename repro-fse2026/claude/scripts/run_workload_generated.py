#!/usr/bin/env python3
"""Run the generated-sampling protocol on the ICSE 2023 workload-impact archive."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
import re
import statistics
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from cost_sampling.analysis import (
    cost_heterogeneity_summary,
    evaluate_samples,
    pareto_summary,
    proxy_summary,
    rank_stability,
    strategy_summary,
    write_csv,
)
from cost_sampling.generated_sampling import (
    build_generated_dataset,
    budget_grid,
    load_workload_table,
    parse_where,
    subset_measured_table,
)
from cost_sampling.hypotheses import test_h5a_input_sensitivity
from cost_sampling.metrics import LEARNER_CHOICES
from cost_sampling.plots import (
    plot_accuracy_cost,
    plot_aggregate_rank_agreement,
    plot_calibration,
    plot_calibration_by_strategy,
    plot_strategy_cost_bias,
)


DEFAULT_LAMBDAS = [0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 10.0]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--zip",
        default="/private/tmp/artifact_excluding_raw_coverage.zip",
        help="Path to the ICSE 2023 workload-impact archive.",
    )
    parser.add_argument("--system", default="xz", help="System name, for example xz.")
    parser.add_argument(
        "--workload",
        action="append",
        default=[],
        help="Restrict to one or more workload values. Repeat the flag to select multiple workloads.",
    )
    parser.add_argument("--target-column", default="performance", help="Prediction target column.")
    parser.add_argument("--cost-column", default="performance", help="Empirical cost column.")
    parser.add_argument(
        "--cost-orientation",
        choices=["lower", "inverse"],
        default="lower",
        help="Use inverse for throughput-like cost columns.",
    )
    parser.add_argument("--output-dir", default=None, help="Output directory.")
    parser.add_argument("--seeds", type=int, default=30, help="Stochastic seeds per budget.")
    parser.add_argument("--max-budget", type=int, default=256, help="Maximum generated sample size.")
    parser.add_argument(
        "--max-rows",
        type=int,
        default=None,
        help="Optional deterministic row cap for exploratory pilots.",
    )
    parser.add_argument("--row-seed", type=int, default=0, help="Seed for --max-rows subsampling.")
    parser.add_argument("--alpha", type=float, default=1.0, help="Ridge regularization strength.")
    parser.add_argument(
        "--learner",
        choices=LEARNER_CHOICES,
        default="ridge-log",
        help="Learner used to estimate the prediction target.",
    )
    parser.add_argument("--no-oracles", action="store_true", help="Skip cheap/expensive diagnostic oracles.")
    parser.add_argument(
        "--progress-every",
        type=int,
        default=100,
        help="Print progress every N sample evaluations; use 0 to disable.",
    )
    parser.add_argument(
        "--where",
        action="append",
        default=[],
        metavar="COLUMN=VALUE",
        help="Additional row filters applied before workload slicing.",
    )
    return parser.parse_args()


def _fmt(value: float) -> str:
    return f"{value:.4g}"


def _median(values: list[float]) -> float:
    return float(statistics.median(values))


def _slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")
    return slug or "value"


def _pair(row: dict[str, Any]) -> str:
    return f"{row['strategy']}_{row['level']}"


def _add_metadata(
    rows: list[dict[str, Any]],
    *,
    system: str,
    workload: str,
    target: str,
    cost: str,
) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        item = dict(row)
        item["system"] = system
        item["workload"] = workload
        item["target_property"] = target
        item["cost_property"] = cost
        out.append(item)
    return out


def _workload_row(
    *,
    system: str,
    workload: str,
    target: str,
    cost: str,
    heterogeneity: list[dict[str, Any]],
    proxy: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    ranks: list[dict[str, Any]],
    pareto: list[dict[str, Any]],
    budgets: list[int],
    seeds: int,
) -> dict[str, Any]:
    h = heterogeneity[0]
    overall_proxy = next(row for row in proxy if row["strategy"] == "ALL")
    count_pairs = {_pair(row) for row in pareto if row["pareto_count"]}
    empirical_pairs = {_pair(row) for row in pareto if row["pareto_empirical"]}
    union = count_pairs | empirical_pairs
    best = min(summary, key=lambda row: row["median_mre"] + row["median_pct_cost"])
    return {
        "system": system,
        "workload": workload,
        "target_property": target,
        "cost_property": cost,
        "analysis_context": h["target_context"],
        "n_configurations": h["n_configurations"],
        "budgets": " ".join(str(n) for n in budgets),
        "seeds": seeds,
        "full_cost": h["full_cost"],
        "cost_cv": h["cv_cost"],
        "cost_p90_over_p10": h["p90_over_p10"],
        "proxy_spearman": overall_proxy["spearman_n_train_cost"],
        "proxy_median_ratio": overall_proxy["median_calibration_ratio"],
        "proxy_q1_ratio": overall_proxy["q1_calibration_ratio"],
        "proxy_q3_ratio": overall_proxy["q3_calibration_ratio"],
        "cost_over_random_min": min(row["cost_over_random"] for row in summary),
        "cost_over_random_max": max(row["cost_over_random"] for row in summary),
        "rank_top1_flips": sum(1 for row in ranks if not row["top1_agreement"]),
        "rank_top1_agreement": sum(row["top1_agreement"] for row in ranks) / len(ranks),
        "rank_mean_kendall_tau": sum(row["kendall_tau"] for row in ranks) / len(ranks),
        "rank_mean_top3_overlap": sum(row["top3_overlap"] for row in ranks) / len(ranks),
        "pareto_count_n": len(count_pairs),
        "pareto_empirical_n": len(empirical_pairs),
        "pareto_overlap_n": len(count_pairs & empirical_pairs),
        "pareto_jaccard": len(count_pairs & empirical_pairs) / len(union) if union else 1.0,
        "best_simple_pair": _pair(best),
        "best_simple_mre": best["median_mre"],
        "best_simple_pct_cost": best["median_pct_cost"],
    }


def _write_report(
    path: Path,
    *,
    system: str,
    source_zip: str,
    source_member: str,
    target_column: str,
    cost_column: str,
    workloads: list[str],
    feature_count: int,
    workload_rows: list[dict[str, Any]],
    h5a_row: dict[str, Any] | None,
) -> None:
    lines = [
        f"# Generated sampling pilot on workload-impact `{system}`",
        "",
        "## Scope",
        "",
        f"Source archive: `{source_zip}`",
        "",
        f"Source member(s): `{source_member}`",
        "",
        f"Target column: `{target_column}`. Cost column: `{cost_column}`.",
        "",
        f"Workloads analyzed: `{', '.join(workloads)}`",
        "",
        f"Encoded feature columns: `{feature_count}`.",
        "",
        "This pilot reuses the Twins-style generated-sampling protocol on the measured configuration universe "
        "provided by the ICSE 2023 workload dataset. Each workload is treated as a separate context.",
        "",
        "## Workload summary",
        "",
        "| Workload | Cost CV | Spearman rho | Median %cost/%n | Top-1 flips | Pareto Jaccard | Best simple pair |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in workload_rows:
        lines.append(
            f"| `{row['workload']}` | {_fmt(row['cost_cv'])} | {_fmt(row['proxy_spearman'])} | "
            f"{_fmt(row['proxy_median_ratio'])} | {row['rank_top1_flips']} / {len(DEFAULT_LAMBDAS)} | "
            f"{_fmt(row['pareto_jaccard'])} | `{row['best_simple_pair']}` |"
        )

    strongest_cv = max(workload_rows, key=lambda row: float(row["cost_cv"]))
    strongest_flip = max(workload_rows, key=lambda row: int(row["rank_top1_flips"]))
    weakest_proxy = min(workload_rows, key=lambda row: float(row["proxy_spearman"]))
    lines.extend(
        [
            "",
            "## Readout",
            "",
            f"Highest heterogeneity: `{strongest_cv['workload']}` with CV={_fmt(strongest_cv['cost_cv'])}.",
            "",
            f"Least count-stable workload: `{strongest_flip['workload']}` with "
            f"{strongest_flip['rank_top1_flips']} top-1 flips out of {len(DEFAULT_LAMBDAS)} lambda settings.",
            "",
            f"Weakest rank-proxy workload: `{weakest_proxy['workload']}` with "
            f"Spearman rho={_fmt(weakest_proxy['proxy_spearman'])}.",
            "",
        ]
    )
    if h5a_row is not None:
        lines.extend(
            [
                "## H5a",
                "",
                f"Verdict: `{h5a_row['verdict']}`. {h5a_row['notes']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Files",
            "",
            "- `records.csv`: one row per sampled run.",
            "- `workload_summary.csv`: one row per workload context.",
            "- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.",
            "- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir or f"artifacts/workload_{args.system}_pilot")
    output_dir.mkdir(parents=True, exist_ok=True)

    where = parse_where(args.where)
    table = load_workload_table(
        args.zip,
        args.system,
        where=where,
        max_rows=args.max_rows,
        row_seed=args.row_seed,
    )
    if args.target_column not in table.rows[0]:
        raise SystemExit(f"Missing target column {args.target_column!r} in merged table.")
    if args.cost_column not in table.rows[0]:
        raise SystemExit(f"Missing cost column {args.cost_column!r} in merged table.")

    workload_column = next((column for column in table.context_columns if column.lower() == "workload"), None)
    if workload_column is None and table.context_columns:
        workload_column = table.context_columns[0]
    if workload_column is None:
        workload_values = ["all"]
        workload_to_indices = {"all": list(range(len(table.rows)))}
    else:
        grouped: dict[str, list[int]] = defaultdict(list)
        for idx, row in enumerate(table.rows):
            grouped[row[workload_column]].append(idx)
        requested = set(args.workload)
        workload_values = sorted(requested) if requested else sorted(grouped)
        missing = [value for value in workload_values if value not in grouped]
        if missing:
            raise SystemExit(f"Unknown workload values for {args.system}: {', '.join(missing)}")
        workload_to_indices = {value: grouped[value] for value in workload_values}

    all_records: list[dict[str, Any]] = []
    all_heterogeneity: list[dict[str, Any]] = []
    all_summary: list[dict[str, Any]] = []
    all_proxy: list[dict[str, Any]] = []
    all_ranks: list[dict[str, Any]] = []
    all_pareto: list[dict[str, Any]] = []
    workload_rows: list[dict[str, Any]] = []
    mre_cache: dict[tuple[Any, ...], float] = {}

    for workload in workload_values:
        indices = workload_to_indices[workload]
        analysis_name = f"{args.system}__workload_{_slug(workload)}"
        subset = subset_measured_table(table, indices, analysis_name=analysis_name)
        budgets = budget_grid(len(subset.rows), max_absolute=args.max_budget)
        if not budgets:
            print(f"Skipping workload={workload}: not enough rows for generated budgets.", flush=True)
            continue
        print(
            f"Running generated protocol: system={args.system} workload={workload} rows={len(subset.rows)}",
            flush=True,
        )
        dataset = build_generated_dataset(
            subset,
            target_property=args.target_column,
            cost_property=args.cost_column,
            cost_orientation=args.cost_orientation,
            budgets=budgets,
            seeds=args.seeds,
            include_oracles=not args.no_oracles,
        )
        records = _add_metadata(
            evaluate_samples(
                dataset,
                alpha=args.alpha,
                learner=args.learner,
                mre_cache=mre_cache,
                mre_cache_prefix=(workload, args.target_column, args.cost_column),
                progress_label=f"{args.system} workload={workload}",
                progress_every=args.progress_every,
            ),
            system=args.system,
            workload=workload,
            target=args.target_column,
            cost=args.cost_column,
        )
        heterogeneity = _add_metadata(
            cost_heterogeneity_summary(dataset),
            system=args.system,
            workload=workload,
            target=args.target_column,
            cost=args.cost_column,
        )
        summary = _add_metadata(strategy_summary(records), system=args.system, workload=workload, target=args.target_column, cost=args.cost_column)
        proxy = _add_metadata(proxy_summary(records), system=args.system, workload=workload, target=args.target_column, cost=args.cost_column)
        ranks = _add_metadata(rank_stability(summary, DEFAULT_LAMBDAS), system=args.system, workload=workload, target=args.target_column, cost=args.cost_column)
        pareto = _add_metadata(pareto_summary(summary), system=args.system, workload=workload, target=args.target_column, cost=args.cost_column)

        workload_rows.append(
            _workload_row(
                system=args.system,
                workload=workload,
                target=args.target_column,
                cost=args.cost_column,
                heterogeneity=heterogeneity,
                proxy=proxy,
                summary=summary,
                ranks=ranks,
                pareto=pareto,
                budgets=budgets,
                seeds=args.seeds,
            )
        )
        all_records.extend(records)
        all_heterogeneity.extend(heterogeneity)
        all_summary.extend(summary)
        all_proxy.extend(proxy)
        all_ranks.extend(ranks)
        all_pareto.extend(pareto)

        fig_slug = _slug(workload)
        plot_calibration(records, output_dir / f"fig_rq2_calibration_{fig_slug}.png")
        plot_strategy_cost_bias(summary, output_dir / f"fig_rq1_strategy_cost_bias_{fig_slug}.png")
        plot_accuracy_cost(pareto, output_dir / f"fig_rq4_accuracy_cost_{fig_slug}.png")

    if not workload_rows:
        raise SystemExit("No workload contexts were analyzed.")

    write_csv(output_dir / "records.csv", all_records)
    write_csv(output_dir / "rq1_cost_heterogeneity.csv", all_heterogeneity)
    write_csv(output_dir / "strategy_summary.csv", all_summary)
    write_csv(output_dir / "rq2_proxy_summary.csv", all_proxy)
    write_csv(output_dir / "rq3_rank_stability.csv", all_ranks)
    write_csv(output_dir / "rq4_pareto.csv", all_pareto)
    write_csv(output_dir / "workload_summary.csv", workload_rows)

    h5a_row = test_h5a_input_sensitivity(all_records, scope_value=f"{args.system}|cost={args.cost_column}|target={args.target_column}")
    write_csv(output_dir / "h5_workload_sensitivity.csv", [h5a_row])

    plot_calibration_by_strategy(
        all_proxy,
        output_dir / "fig_rq2_calibration_by_strategy.png",
        title=f"{args.system}: calibration across workloads",
    )
    plot_aggregate_rank_agreement(
        all_ranks,
        output_dir / "fig_rq3_rank_agreement_by_workload.png",
        context_label="workloads",
    )

    _write_report(
        output_dir / "pilot_report.md",
        system=args.system,
        source_zip=args.zip,
        source_member=table.source_member,
        target_column=args.target_column,
        cost_column=args.cost_column,
        workloads=[row["workload"] for row in workload_rows],
        feature_count=len(table.feature_names),
        workload_rows=workload_rows,
        h5a_row=h5a_row if len(workload_rows) >= 3 else None,
    )


if __name__ == "__main__":
    main()
