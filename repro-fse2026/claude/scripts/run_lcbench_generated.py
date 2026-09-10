#!/usr/bin/env python3
"""Run the generated-sampling protocol on an LCBench JSON benchmark."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
import re
import statistics
import sys
from typing import Any

import numpy as np


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
    load_lcbench_table,
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
        "--json",
        default="/private/tmp/lcbench/six_datasets_lw.json",
        help="Path to an LCBench JSON file.",
    )
    parser.add_argument(
        "--dataset",
        action="append",
        default=[],
        help="Restrict to one or more OpenML datasets. Repeat the flag to select multiple datasets.",
    )
    parser.add_argument("--target-column", default="final_val_accuracy", help="Prediction target column.")
    parser.add_argument("--cost-column", default="time_total", help="Measured cost column.")
    parser.add_argument(
        "--cost-orientation",
        choices=["lower", "inverse"],
        default="lower",
        help="Use inverse only for benefit-like cost columns.",
    )
    parser.add_argument(
        "--runtime-mode",
        choices=["last", "sum"],
        default="last",
        help="How to flatten the runtime learning curve into a scalar acquisition cost.",
    )
    parser.add_argument("--output-dir", default=None, help="Output directory.")
    parser.add_argument("--seeds", type=int, default=10, help="Stochastic seeds per budget.")
    parser.add_argument("--max-budget", type=int, default=64, help="Maximum generated sample size.")
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
        default="ridge-raw",
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
    workload: str,
    target: str,
    cost: str,
) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        item = dict(row)
        item["system"] = "lcbench"
        item["workload"] = workload
        item["target_property"] = target
        item["cost_property"] = cost
        out.append(item)
    return out


def _workload_row(
    *,
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
        "system": "lcbench",
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
    source_json: str,
    target_column: str,
    cost_column: str,
    workloads: list[str],
    feature_count: int,
    workload_rows: list[dict[str, Any]],
    h5a_row: dict[str, Any] | None,
) -> None:
    lines = [
        "# Generated sampling pilot on LCBench",
        "",
        "## Scope",
        "",
        f"Source JSON: `{source_json}`",
        "",
        f"Target column: `{target_column}`. Cost column: `{cost_column}`.",
        "",
        f"OpenML datasets analyzed: `{', '.join(workloads)}`",
        "",
        f"Encoded hyperparameter columns: `{feature_count}`.",
        "",
        "LCBench is treated as a workload-style benchmark: each OpenML dataset is a distinct context,",
        "the sampled objects are hyperparameter configurations, and acquisition cost is the cumulative",
        "training runtime of a configuration on that dataset.",
        "",
        "## Per-dataset summary",
        "",
        "| Dataset | Cost CV | Spearman(n,cost) | Median %cost/%n | Top-1 flips / 7 | Pareto Jaccard |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in workload_rows:
        lines.append(
            f"| `{row['workload']}` | {_fmt(float(row['cost_cv']))} | {_fmt(float(row['proxy_spearman']))} | "
            f"{_fmt(float(row['proxy_median_ratio']))} | {int(row['rank_top1_flips'])}/7 | {_fmt(float(row['pareto_jaccard']))} |"
        )
    if h5a_row is not None:
        lines.extend(
            [
                "",
                "## H5a-style context sensitivity",
                "",
                f"p-value: `{_fmt(float(h5a_row['p_value']))}`; ratio spread: `{_fmt(float(h5a_row['effect_value']))}`; "
                f"verdict: `{h5a_row['verdict']}`.",
            ]
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    source_json = Path(args.json)
    output_dir = Path(args.output_dir) if args.output_dir else REPO_ROOT / "artifacts" / "lcbench_six_datasets_pilot"
    output_dir.mkdir(parents=True, exist_ok=True)

    table = load_lcbench_table(
        source_json,
        datasets=args.dataset or None,
        where=parse_where(args.where),
        max_rows=args.max_rows,
        row_seed=args.row_seed,
        runtime_mode=args.runtime_mode,
    )
    workloads = sorted({row["workload"] for row in table.rows})

    all_records: list[dict[str, Any]] = []
    all_heterogeneity: list[dict[str, Any]] = []
    all_strategy_summary: list[dict[str, Any]] = []
    all_proxy_summary: list[dict[str, Any]] = []
    all_ranks: list[dict[str, Any]] = []
    all_pareto: list[dict[str, Any]] = []
    workload_rows: list[dict[str, Any]] = []
    mre_cache: dict[tuple[Any, ...], float] = {}

    for workload in workloads:
        indices = np.asarray([idx for idx, row in enumerate(table.rows) if row["workload"] == workload], dtype=int)
        analysis_name = f"lcbench__workload_{_slug(workload)}"
        subset = subset_measured_table(table, indices, analysis_name=analysis_name)
        budgets = [n for n in budget_grid(len(subset.rows)) if n <= args.max_budget]
        if not budgets:
            raise ValueError(f"No valid budget grid for workload {workload!r}.")
        dataset = build_generated_dataset(
            subset,
            target_property=args.target_column,
            cost_property=args.cost_column,
            cost_orientation=args.cost_orientation,
            seeds=args.seeds,
            budgets=budgets,
            include_oracles=not args.no_oracles,
        )
        records = evaluate_samples(
            dataset,
            alpha=args.alpha,
            learner=args.learner,
            mre_cache=mre_cache,
            mre_cache_prefix=(workload, args.target_column, args.cost_column),
            progress_label=f"lcbench workload={workload}",
            progress_every=args.progress_every,
        )
        heterogeneity = cost_heterogeneity_summary(dataset)
        summary = strategy_summary(records)
        proxy = proxy_summary(records)
        ranks = rank_stability(summary, DEFAULT_LAMBDAS)
        pareto = pareto_summary(summary)

        records = _add_metadata(records, workload=workload, target=args.target_column, cost=args.cost_column)
        heterogeneity = _add_metadata(heterogeneity, workload=workload, target=args.target_column, cost=args.cost_column)
        summary = _add_metadata(summary, workload=workload, target=args.target_column, cost=args.cost_column)
        proxy = _add_metadata(proxy, workload=workload, target=args.target_column, cost=args.cost_column)
        ranks = _add_metadata(ranks, workload=workload, target=args.target_column, cost=args.cost_column)
        pareto = _add_metadata(pareto, workload=workload, target=args.target_column, cost=args.cost_column)

        all_records.extend(records)
        all_heterogeneity.extend(heterogeneity)
        all_strategy_summary.extend(summary)
        all_proxy_summary.extend(proxy)
        all_ranks.extend(ranks)
        all_pareto.extend(pareto)
        workload_rows.append(
            _workload_row(
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

        plot_strategy_cost_bias(
            summary,
            output_dir / f"fig_rq1_strategy_cost_bias_{_slug(workload)}.png",
        )
        plot_calibration(
            records,
            output_dir / f"fig_rq2_calibration_{_slug(workload)}.png",
        )
        plot_accuracy_cost(
            pareto,
            output_dir / f"fig_rq4_accuracy_cost_{_slug(workload)}.png",
        )

    h5a_row = test_h5a_input_sensitivity(
        [
            {
                "target_context": row["workload"],
                "calibration_ratio": float(row["calibration_ratio"]),
            }
            for row in all_records
        ],
        scope_value="lcbench|datasets",
    )
    h5a_summary = [
        {
            "scope": h5a_row["scope"],
            "scope_value": h5a_row["scope_value"],
            "statistic": h5a_row["statistic"],
            "statistic_value": h5a_row["statistic_value"],
            "p_value": h5a_row["p_value"],
            "effect": h5a_row["effect"],
            "effect_value": h5a_row["effect_value"],
            "effect_label": h5a_row["effect_label"],
            "verdict": h5a_row["verdict"],
            "notes": h5a_row["notes"],
        }
    ]

    write_csv(output_dir / "records.csv", all_records)
    write_csv(output_dir / "rq1_cost_heterogeneity.csv", all_heterogeneity)
    write_csv(output_dir / "strategy_summary.csv", all_strategy_summary)
    write_csv(output_dir / "rq2_proxy_summary.csv", all_proxy_summary)
    write_csv(output_dir / "rq3_rank_stability.csv", all_ranks)
    write_csv(output_dir / "rq4_pareto.csv", all_pareto)
    write_csv(output_dir / "workload_summary.csv", workload_rows)
    write_csv(output_dir / "h5_workload_sensitivity.csv", h5a_summary)

    plot_calibration_by_strategy(
        all_proxy_summary,
        output_dir / "fig_rq2_calibration_by_strategy.png",
        title="LCBench: calibration by strategy across OpenML datasets",
    )
    plot_aggregate_rank_agreement(
        all_ranks,
        output_dir / "fig_rq3_rank_agreement_by_workload.png",
        context_label="OpenML datasets",
    )

    _write_report(
        output_dir / "pilot_report.md",
        source_json=str(source_json),
        target_column=args.target_column,
        cost_column=args.cost_column,
        workloads=workloads,
        feature_count=len(table.feature_columns),
        workload_rows=workload_rows,
        h5a_row=h5a_row,
    )
    print(f"Wrote LCBench generated-sampling outputs to {output_dir}")


if __name__ == "__main__":
    main()
