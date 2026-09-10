#!/usr/bin/env python3
"""Run a single non-x264 ICPE-style system from NewRuns.zip."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path
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
from cost_sampling.archive_runs import load_runs_dataset, load_summary_configuration_count
from cost_sampling.hypotheses import evaluate_per_context_hypotheses
from cost_sampling.metrics import LEARNER_CHOICES
from cost_sampling.plots import (
    plot_accuracy_cost,
    plot_aggregate_rank_agreement,
    plot_calibration,
    plot_cost_distribution,
    plot_pareto_frontier_comparison,
    plot_strategy_cost_bias,
)


DEFAULT_LAMBDAS = [0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 10.0]
SCENARIO = "cost_performance__target_performance"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--context", default="BerkeleyDBC", help="System/context name inside NewRuns.zip.")
    parser.add_argument("--runs-zip", default="ICPE-rawdata/NewRuns.zip", help="Path to NewRuns.zip.")
    parser.add_argument("--summary-zip", default="ICPE-rawdata/AllSummary.zip", help="Path to AllSummary.zip.")
    parser.add_argument("--output-dir", default=None, help="Output directory.")
    parser.add_argument("--max-runs", type=int, default=100, help="Maximum run id to load.")
    parser.add_argument("--alpha", type=float, default=1.0, help="Ridge regularization strength.")
    parser.add_argument("--learner", default="ridge-log", choices=LEARNER_CHOICES)
    parser.add_argument("--no-log-target", action="store_true", help="Fit the learner on raw target values.")
    parser.add_argument("--performance-name", default="Performance", help="Performance column in sampled CSVs.")
    return parser.parse_args()


def _fmt(value: float) -> str:
    return f"{value:.4g}"


def _median(values: list[float]) -> float:
    return float(statistics.median(values))


def _pair(row: dict[str, Any]) -> str:
    return f"{row['strategy']}_{row['level']}"


def add_scenario(rows: list[dict[str, Any]], context: str) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        item = dict(row)
        item["system"] = context
        item["cost_property"] = "performance"
        item["target_property"] = "performance"
        item["scenario"] = SCENARIO
        out.append(item)
    return out


def count_pairs(rows: list[dict[str, Any]], column: str) -> Counter[str]:
    counter: Counter[str] = Counter()
    for row in rows:
        for pair in str(row[column]).split(","):
            pair = pair.strip()
            if pair:
                counter[pair] += 1
    return counter


def median_by_strategy(rows: list[dict[str, Any]], column: str) -> list[tuple[str, float]]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        grouped[row["strategy"]].append(float(row[column]))
    return sorted((strategy, _median(values)) for strategy, values in grouped.items())


def build_context_row(
    *,
    context: str,
    expected_n: int | None,
    heterogeneity: list[dict[str, Any]],
    proxy: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    ranks: list[dict[str, Any]],
    pareto: list[dict[str, Any]],
) -> dict[str, Any]:
    h = heterogeneity[0]
    overall_proxy = next(row for row in proxy if row["strategy"] == "ALL")
    empirical = {_pair(row) for row in pareto if row["pareto_empirical"]}
    count = {_pair(row) for row in pareto if row["pareto_count"]}
    union = empirical | count
    best = min(summary, key=lambda row: row["median_mre"] + row["median_pct_cost"])
    row = {
        "system": context,
        "target_context": context,
        "cost_context": context,
        "expected_configurations": expected_n,
        "reconstructed_configurations": h["n_configurations"],
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
        "rank_mean_kendall_tau": sum(row["kendall_tau"] for row in ranks) / len(ranks),
        "rank_mean_top3_overlap": sum(row["top3_overlap"] for row in ranks) / len(ranks),
        "pareto_count_n": len(count),
        "pareto_empirical_n": len(empirical),
        "pareto_overlap_n": len(count & empirical),
        "pareto_jaccard": len(count & empirical) / len(union) if union else 1.0,
        "pareto_count_pairs": ", ".join(sorted(count)),
        "pareto_empirical_pairs": ", ".join(sorted(empirical)),
        "best_simple_pair": _pair(best),
        "best_simple_mre": best["median_mre"],
        "best_simple_pct_cost": best["median_pct_cost"],
        "cost_property": "performance",
        "target_property": "performance",
        "scenario": SCENARIO,
    }
    return row


def write_report(
    output: Path,
    *,
    context: str,
    context_row: dict[str, Any],
    proxy_rows: list[dict[str, Any]],
    strategy_rows: list[dict[str, Any]],
    rank_rows: list[dict[str, Any]],
) -> None:
    strategy_ratio = median_by_strategy(
        [row for row in proxy_rows if row["strategy"] != "ALL"],
        "median_calibration_ratio",
    )
    strategy_overhead = median_by_strategy(strategy_rows, "cost_over_random")
    top1_flips = sum(1 for row in rank_rows if not row["top1_agreement"])
    top1_agreement = 1.0 - top1_flips / len(rank_rows)
    mean_tau_by_lambda = []
    for lam in DEFAULT_LAMBDAS:
        rows = [row for row in rank_rows if row["lambda"] == lam]
        mean_tau_by_lambda.append((lam, sum(row["kendall_tau"] for row in rows) / len(rows)))
    worst_lambda, worst_tau = min(mean_tau_by_lambda, key=lambda item: item[1])
    count_frontier = count_pairs([context_row], "pareto_count_pairs")
    empirical_frontier = count_pairs([context_row], "pareto_empirical_pairs")

    coverage = ""
    expected = context_row["expected_configurations"]
    if expected is not None:
        coverage = (
            f"The sampled CSVs reconstruct {context_row['reconstructed_configurations']} of "
            f"{expected} configurations."
        )
    else:
        coverage = f"The sampled CSVs reconstruct {context_row['reconstructed_configurations']} configurations."

    lines = [
        f"# {context} sampling-cost report",
        "",
        "## Scope and protocol",
        "",
        f"This report extends the infrastructure beyond x264 using `{context}` from `NewRuns.zip`. "
        "The archive exposes sampled configuration CSVs for this system. The only available measured "
        "property is `Performance`, so this is the single diagonal scenario: empirical performance is "
        "both the cost of measuring a selected configuration and the target being predicted.",
        "",
        f"{coverage} The current learner remains the lightweight ridge/log-linear model.",
        "",
        "Because there is no separate size property here, this report is not a 2x2 matrix. It is the "
        "non-x264 analogue of the `cost=performance, target=performance` case.",
        "",
        "## RQ1: Empirical cost heterogeneity",
        "",
        "![Cost distribution by strategy and level](fig_rq1_cost_distribution.png)",
        "",
        "![Strategy cost bias](fig_rq1_strategy_cost_bias.png)",
        "",
        f"Per-configuration empirical cost is heterogeneous: CV is {_fmt(context_row['cost_cv'])}, "
        f"and the p90/p10 cost ratio is {_fmt(context_row['cost_p90_over_p10'])}. At fixed sample size, "
        f"strategy overhead relative to random ranges from {_fmt(context_row['cost_over_random_min'])} "
        f"to {_fmt(context_row['cost_over_random_max'])}.",
        "",
        "Median cost-over-random by strategy:",
        "",
    ]
    lines.extend([f"- `{strategy}`: {_fmt(value)}" for strategy, value in strategy_overhead])
    lines.extend(
        [
            "",
            "Interpretation: even on this non-x264 system, `n` does not force all strategies at the same "
            "level to consume the same empirical cost. The strength of the bias depends on which regions "
            "of the configuration space the strategy selects.",
            "",
            "## RQ2: Sample size as cost proxy",
            "",
            "![Sample-size calibration](fig_rq2_size_cost_calibration.png)",
            "",
            f"Spearman rho between `n` and empirical `TrainCost` is "
            f"{_fmt(context_row['proxy_spearman'])}. The median calibration ratio `%cost/%n` is "
            f"{_fmt(context_row['proxy_median_ratio'])}, with IQR "
            f"{_fmt(context_row['proxy_q1_ratio'])}-{_fmt(context_row['proxy_q3_ratio'])}.",
            "",
            "Median calibration ratio by strategy:",
            "",
        ]
    )
    lines.extend([f"- `{strategy}`: {_fmt(value)}" for strategy, value in strategy_ratio])
    lines.extend(
        [
            "",
            "Interpretation: sample size is useful as a first-order axis only if one is satisfied with "
            "coarse ordering. Calibration and strategy-specific bias still need to be checked.",
            "",
            "## RQ3: Ranking robustness",
            "",
            "![Rank agreement](fig_rq3_rank_stability.png)",
            "",
            f"Across {len(rank_rows)} lambda values, the top-1 recommendation changes {top1_flips} times, "
            f"so top-1 agreement is {_fmt(top1_agreement)}. Mean Kendall tau is "
            f"{_fmt(context_row['rank_mean_kendall_tau'])}; the weakest lambda is "
            f"{worst_lambda:g} with tau {_fmt(worst_tau)}.",
            "",
            "Interpretation: this directly tests whether a count-cost conclusion survives when empirical "
            "cost replaces sample size in the same accuracy-cost objective.",
            "",
            "## RQ4: Pareto-efficient sampling",
            "",
            "![Empirical accuracy-cost frontier](fig_rq4_accuracy_cost_frontier.png)",
            "",
            "![Count vs empirical Pareto fronts](fig_rq4_frontier_count_vs_empirical.png)",
            "",
            f"Count-vs-empirical frontier Jaccard is {_fmt(context_row['pareto_jaccard'])}. "
            "The count-cost frontier contains:",
            "",
        ]
    )
    lines.extend([f"- `{pair}`" for pair in sorted(count_frontier)])
    lines.extend(["", "The empirical-cost frontier contains:", ""])
    lines.extend([f"- `{pair}`" for pair in sorted(empirical_frontier)])
    lines.extend(
        [
            "",
            "Interpretation: the Pareto comparison is the decision-level check. If the two lists differ, "
            "then replacing count cost by empirical cost changes which sampling choices are non-dominated.",
            "",
            "## Takeaway",
            "",
            f"`{context}` gives a useful non-x264 replication point. It does not support the full "
            "time/size matrix because the archive exposes one `Performance` property, but it does let us "
            "test the central cost-proxy claim on another configurable system using the same code path.",
            "",
        ]
    )
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir or f"artifacts/{args.context}_performance")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Analyzing {args.context} from {args.runs_zip}")
    dataset = load_runs_dataset(
        args.runs_zip,
        args.context,
        max_runs=args.max_runs,
        performance_name=args.performance_name,
    )
    expected_n = load_summary_configuration_count(args.summary_zip, args.context)

    records = add_scenario(
        evaluate_samples(dataset, alpha=args.alpha, log_target=not args.no_log_target, learner=args.learner),
        args.context,
    )
    heterogeneity = add_scenario(cost_heterogeneity_summary(dataset), args.context)
    summary = add_scenario(strategy_summary(records), args.context)
    proxy = add_scenario(proxy_summary(records), args.context)
    ranks = add_scenario(rank_stability(summary, DEFAULT_LAMBDAS), args.context)
    pareto = add_scenario(pareto_summary(summary), args.context)
    context_row = build_context_row(
        context=args.context,
        expected_n=expected_n,
        heterogeneity=heterogeneity,
        proxy=proxy,
        summary=summary,
        ranks=ranks,
        pareto=pareto,
    )

    write_csv(output_dir / "records.csv", records)
    write_csv(output_dir / "rq1_cost_heterogeneity.csv", heterogeneity)
    write_csv(output_dir / "strategy_summary.csv", summary)
    write_csv(output_dir / "rq2_proxy_summary.csv", proxy)
    write_csv(output_dir / "rq3_rank_stability.csv", ranks)
    write_csv(output_dir / "rq4_pareto.csv", pareto)
    write_csv(output_dir / "context_summary.csv", [context_row])
    hypothesis_rows = evaluate_per_context_hypotheses(
        scope_value=args.context,
        records=records,
        heterogeneity=heterogeneity,
        rank_rows=ranks,
        pareto_rows=pareto,
        cost_values=dataset.cost_values,
    )
    for row in hypothesis_rows:
        row["system"] = args.context
        row["scenario"] = SCENARIO
    write_csv(output_dir / "hypothesis_tests.csv", hypothesis_rows)

    plot_cost_distribution(records, output_dir / "fig_rq1_cost_distribution.png")
    plot_strategy_cost_bias(summary, output_dir / "fig_rq1_strategy_cost_bias.png")
    plot_calibration(records, output_dir / "fig_rq2_size_cost_calibration.png")
    plot_aggregate_rank_agreement(ranks, output_dir / "fig_rq3_rank_stability.png", context_label=args.context)
    plot_accuracy_cost(pareto, output_dir / "fig_rq4_accuracy_cost_frontier.png")
    plot_pareto_frontier_comparison(
        summary,
        output_dir / "fig_rq4_frontier_count_vs_empirical.png",
        scenario=SCENARIO,
        scenario_label=f"{args.context}: cost=performance, target=performance",
    )
    write_report(
        output_dir / f"{args.context}_performance_report.md",
        context=args.context,
        context_row=context_row,
        proxy_rows=proxy,
        strategy_rows=summary,
        rank_rows=ranks,
    )
    print(f"Done. Outputs: {output_dir}")


if __name__ == "__main__":
    main()
