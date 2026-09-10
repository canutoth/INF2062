#!/usr/bin/env python3
"""Run all x264_size_* contexts with x264_time_* as empirical cost."""

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
from cost_sampling.archive_runs import attach_cost_dataset, load_runs_dataset, load_summary_configuration_count
from cost_sampling.metrics import LEARNER_CHOICES
from cost_sampling.plots import (
    plot_aggregate_rank_agreement,
    plot_context_sensitivity,
    plot_strategy_cost_bias,
)


DEFAULT_LAMBDAS = [0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 10.0]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-zip", default="ICPE-rawdata/AllRuns.zip", help="Path to AllRuns.zip.")
    parser.add_argument("--summary-zip", default="ICPE-rawdata/AllSummary.zip", help="Path to AllSummary.zip.")
    parser.add_argument("--output-dir", default="artifacts/x264_size_all", help="Output directory.")
    parser.add_argument("--max-runs", type=int, default=100, help="Maximum run id to load.")
    parser.add_argument("--alpha", type=float, default=1.0, help="Ridge regularization strength.")
    parser.add_argument("--learner", default="ridge-log", choices=LEARNER_CHOICES)
    parser.add_argument("--no-log-target", action="store_true", help="Fit the learner on raw size values.")
    parser.add_argument("--contexts", default="0-16", help="Input indices, e.g. 0-16 or 0,3,8.")
    return parser.parse_args()


def parse_context_indices(raw: str) -> list[int]:
    indices: list[int] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo, hi = part.split("-", 1)
            indices.extend(range(int(lo), int(hi) + 1))
        else:
            indices.append(int(part))
    return sorted(set(indices))


def _fmt(value: float) -> str:
    return f"{value:.4g}"


def _median(values: list[float]) -> float:
    return float(statistics.median(values))


def _pair(row: dict[str, Any]) -> str:
    return f"{row['strategy']}_{row['level']}"


def build_context_row(
    *,
    target_context: str,
    cost_context: str,
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
    best_time = min(summary, key=lambda row: row["median_mre"] + row["median_pct_cost"])
    return {
        "target_context": target_context,
        "cost_context": cost_context,
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
        "best_simple_pair": _pair(best_time),
        "best_simple_mre": best_time["median_mre"],
        "best_simple_pct_cost": best_time["median_pct_cost"],
    }


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


def write_aggregate_report(
    output: Path,
    *,
    context_rows: list[dict[str, Any]],
    proxy_rows: list[dict[str, Any]],
    strategy_rows: list[dict[str, Any]],
    rank_rows: list[dict[str, Any]],
) -> None:
    cvs = [row["cost_cv"] for row in context_rows]
    p90p10 = [row["cost_p90_over_p10"] for row in context_rows]
    spearman_values = [row["proxy_spearman"] for row in context_rows]
    ratio_values = [row["proxy_median_ratio"] for row in context_rows]
    q1_values = [row["proxy_q1_ratio"] for row in context_rows]
    q3_values = [row["proxy_q3_ratio"] for row in context_rows]
    overhead_min = min(row["cost_over_random_min"] for row in context_rows)
    overhead_max = max(row["cost_over_random_max"] for row in context_rows)
    top1_flips = sum(row["rank_top1_flips"] for row in context_rows)
    total_rank_cases = len(context_rows) * len(DEFAULT_LAMBDAS)
    top1_agreement = 1.0 - top1_flips / total_rank_cases
    mean_tau_by_lambda = []
    for lam in DEFAULT_LAMBDAS:
        rows = [row for row in rank_rows if row["lambda"] == lam]
        mean_tau_by_lambda.append((lam, sum(row["kendall_tau"] for row in rows) / len(rows)))
    worst_lambda, worst_tau = min(mean_tau_by_lambda, key=lambda item: item[1])
    count_frontier = count_pairs(context_rows, "pareto_count_pairs")
    empirical_frontier = count_pairs(context_rows, "pareto_empirical_pairs")
    pareto_jaccards = [row["pareto_jaccard"] for row in context_rows]
    strategy_ratio = median_by_strategy([row for row in proxy_rows if row["strategy"] != "ALL"], "median_calibration_ratio")
    strategy_overhead = median_by_strategy(strategy_rows, "cost_over_random")

    lines = [
        "# x264_size_* with empirical x264_time_* acquisition cost",
        "",
        "## Scope and protocol",
        "",
        "This batch analyzes the 17 `x264_size_i` contexts. For each input `i`, the target is output size "
        "from `x264_size_i`, while empirical training cost is the encoding time of the same configurations "
        f"from `x264_time_i`. Each context uses {len(DEFAULT_LAMBDAS)} lambda values and the available "
        "100 runs for six strategies at `t1`, `t2`, and `t3` sample sizes.",
        "",
        "The learner is the current lightweight ridge/log-linear model. The results are good for validating "
        "the infrastructure and studying cost-model behavior, but they should later be replicated with the "
        "paper's final learner.",
        "",
        "## Overall result",
        "",
        "Sample size is a strong but incomplete proxy. It ranks broad cost levels well because `t1`, `t2`, "
        "and `t3` differ substantially in size, but it misses systematic strategy bias at fixed size. "
        "The most important empirical signal is therefore not that `%n` is useless; it is that `%n` is "
        "too coarse to explain which strategies are cheap or expensive once `n` is held constant.",
        "",
        "## RQ1: Empirical cost heterogeneity",
        "",
        f"Across the 17 inputs, per-configuration time-cost CV ranges from {_fmt(min(cvs))} to "
        f"{_fmt(max(cvs))} with median {_fmt(_median(cvs))}. The p90/p10 cost ratio ranges from "
        f"{_fmt(min(p90p10))} to {_fmt(max(p90p10))} with median {_fmt(_median(p90p10))}. "
        "So individual configurations are not equal-cost measurements.",
        "",
        f"At fixed sample size, median strategy overhead relative to random ranges from "
        f"{_fmt(overhead_min)} to {_fmt(overhead_max)} across all contexts, strategies, and levels. "
        "This directly violates the count-cost abstraction: two samples with the same `n` can have "
        "substantially different acquisition time.",
        "",
        "Median cost-over-random by strategy across all inputs and levels:",
        "",
    ]
    lines.extend([f"- `{strategy}`: {_fmt(value)}" for strategy, value in strategy_overhead])
    lines.extend(
        [
            "",
            "## RQ2: Validity of sample size as cost proxy",
            "",
            f"Spearman rho between `n` and empirical `TrainCost` is high in every context "
            f"(range {_fmt(min(spearman_values))}-{_fmt(max(spearman_values))}, "
            f"median {_fmt(_median(spearman_values))}). This means sample size is useful for ranking "
            "large jumps in effort.",
            "",
            f"Calibration is much less clean. The context-level median `%cost/%n` ratio ranges from "
            f"{_fmt(min(ratio_values))} to {_fmt(max(ratio_values))}; the lower quartile of ratios can "
            f"drop to {_fmt(min(q1_values))}, and the upper quartile can reach {_fmt(max(q3_values))}. "
            "A high correlation therefore coexists with biased budgets.",
            "",
            "Median calibration ratio by strategy:",
            "",
        ]
    )
    lines.extend([f"- `{strategy}`: {_fmt(value)}" for strategy, value in strategy_ratio])
    lines.extend(
        [
            "",
            "Interpretation: `random` and `divDistBased` are close to calibrated on median, `distBased` "
            "is slightly above size cost, `solverBased` is median-neutral but can have high upper-tail "
            "cost in some inputs, `twise` is systematically costlier, and `henard` is systematically "
            "cheaper than its sample size suggests. This is exactly the distinction the paper should emphasize: "
            "sample size can be correlated with cost without being an unbiased cost model.",
            "",
            "## RQ3: Robustness of conclusions to the cost model",
            "",
            f"Across {total_rank_cases} `(context, lambda)` ranking cases, the top-1 strategy-size pair "
            f"changes {top1_flips} times, so top-1 agreement is {_fmt(top1_agreement)}. "
            f"The lowest mean Kendall tau occurs at lambda={worst_lambda:g} with tau={_fmt(worst_tau)}.",
            "",
            "This suggests that conclusions are often stable when accuracy dominates, but agreement degrades "
            "once cost has substantial weight. Put differently: if a paper makes claims under a cost-sensitive "
            "objective, replacing `n` by measured time can change the recommended strategy.",
            "",
            "## RQ4: Pareto-efficient sampling under empirical cost",
            "",
            f"Count-frontier overlap with the empirical frontier has median Jaccard "
            f"{_fmt(_median(pareto_jaccards))} across inputs. The count frontier is concentrated on:",
            "",
        ]
    )
    lines.extend([f"- `{pair}`: {count} / {len(context_rows)} contexts" for pair, count in count_frontier.most_common()])
    lines.extend(["", "The empirical frontier additionally favors cheaper fixed-size points:"])
    lines.extend([f"- `{pair}`: {count} / {len(context_rows)} contexts" for pair, count in empirical_frontier.most_common()])
    lines.extend(
        [
            "",
            "Interpretation: the empirical frontier is more decision-relevant because it exposes low-time "
            "training sets that count-cost Pareto analysis hides. This is particularly visible for cheaper "
            "`t1` and `t2` points.",
            "",
            "## RQ5: Context sensitivity",
            "",
            f"The effect is present across all 17 inputs, but its magnitude varies. Cost CV ranges over "
            f"{_fmt(max(cvs) - min(cvs))} absolute points, and context-level median calibration ratio spans "
            f"{_fmt(max(ratio_values) - min(ratio_values))}. Rank sensitivity is also context-dependent: "
            f"some inputs have no top-1 flips, while the maximum is "
            f"{max(row['rank_top1_flips'] for row in context_rows)} / {len(DEFAULT_LAMBDAS)} lambda values.",
            "",
            "This supports the paper's intended positioning: cost-model validity is not a universal property "
            "of configurable-system sampling. It depends on input/workload, strategy, and the chosen "
            "accuracy-cost decision rule.",
            "",
            "## Paper-level takeaway",
            "",
            "For `x264_size_*`, using `n` alone is empirically defensible as a rough first-order effort axis, "
            "but not as a fully calibrated cost model. The strongest claim supported by this PoC is nuanced: "
            "count-based effort often preserves broad trends, yet it can hide fixed-size cost bias and alter "
            "cost-sensitive recommendations. That is a solid empirical gap for the paper.",
            "",
        ]
    )
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    context_indices = parse_context_indices(args.contexts)

    all_records: list[dict[str, Any]] = []
    all_heterogeneity: list[dict[str, Any]] = []
    all_strategy: list[dict[str, Any]] = []
    all_proxy: list[dict[str, Any]] = []
    all_ranks: list[dict[str, Any]] = []
    all_pareto: list[dict[str, Any]] = []
    context_rows: list[dict[str, Any]] = []

    for idx in context_indices:
        target_context = f"x264_size_{idx}"
        cost_context = f"x264_time_{idx}"
        print(f"Analyzing {target_context} with costs from {cost_context}")
        target = load_runs_dataset(args.runs_zip, target_context, max_runs=args.max_runs)
        cost = load_runs_dataset(args.runs_zip, cost_context, max_runs=args.max_runs)
        dataset = attach_cost_dataset(target, cost)
        expected_n = load_summary_configuration_count(args.summary_zip, target_context)

        records = evaluate_samples(
            dataset,
            alpha=args.alpha,
            log_target=not args.no_log_target,
            learner=args.learner,
        )
        heterogeneity = cost_heterogeneity_summary(dataset)
        summary = strategy_summary(records)
        proxy = proxy_summary(records)
        ranks = rank_stability(summary, DEFAULT_LAMBDAS)
        pareto = pareto_summary(summary)

        all_records.extend(records)
        all_heterogeneity.extend(heterogeneity)
        all_strategy.extend(summary)
        all_proxy.extend(proxy)
        all_ranks.extend(ranks)
        all_pareto.extend(pareto)
        context_rows.append(
            build_context_row(
                target_context=target_context,
                cost_context=cost_context,
                expected_n=expected_n,
                heterogeneity=heterogeneity,
                proxy=proxy,
                summary=summary,
                ranks=ranks,
                pareto=pareto,
            )
        )

    write_csv(output_dir / "records.csv", all_records)
    write_csv(output_dir / "rq1_cost_heterogeneity.csv", all_heterogeneity)
    write_csv(output_dir / "strategy_summary.csv", all_strategy)
    write_csv(output_dir / "rq2_proxy_summary.csv", all_proxy)
    write_csv(output_dir / "rq3_rank_stability.csv", all_ranks)
    write_csv(output_dir / "rq4_pareto.csv", all_pareto)
    write_csv(output_dir / "context_summary.csv", context_rows)

    plot_strategy_cost_bias(all_strategy, output_dir / "fig_rq1_strategy_cost_bias.png")
    plot_aggregate_rank_agreement(
        all_ranks,
        output_dir / "fig_rq3_aggregate_rank_agreement.png",
        context_label="x264_size contexts",
    )
    plot_context_sensitivity(
        context_rows,
        output_dir / "fig_rq5_context_sensitivity.png",
        context_prefix="x264_size_",
    )
    write_aggregate_report(
        output_dir / "x264_size_report.md",
        context_rows=context_rows,
        proxy_rows=all_proxy,
        strategy_rows=all_strategy,
        rank_rows=all_ranks,
    )

    print(f"Done. Outputs: {output_dir}")


if __name__ == "__main__":
    main()
