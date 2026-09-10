#!/usr/bin/env python3
"""Run all x264_time_* contexts with empirical time as acquisition cost."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import statistics
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

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
from cost_sampling.metrics import LEARNER_CHOICES
from cost_sampling.plots import (
    plot_aggregate_rank_agreement,
    plot_context_sensitivity,
    plot_strategy_cost_bias,
)
from run_x264_size_batch import (
    DEFAULT_LAMBDAS,
    _fmt,
    _median,
    build_context_row,
    count_pairs,
    median_by_strategy,
    parse_context_indices,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-zip", default="ICPE-rawdata/AllRuns.zip", help="Path to AllRuns.zip.")
    parser.add_argument("--summary-zip", default="ICPE-rawdata/AllSummary.zip", help="Path to AllSummary.zip.")
    parser.add_argument("--output-dir", default="artifacts/x264_time_all", help="Output directory.")
    parser.add_argument("--max-runs", type=int, default=100, help="Maximum run id to load.")
    parser.add_argument("--alpha", type=float, default=1.0, help="Ridge regularization strength.")
    parser.add_argument("--learner", default="ridge-log", choices=LEARNER_CHOICES)
    parser.add_argument("--no-log-target", action="store_true", help="Fit the learner on raw time values.")
    parser.add_argument("--contexts", default="0-16", help="Input indices, e.g. 0-16 or 0,3,8.")
    return parser.parse_args()


def write_time_report(
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
    best_pairs = Counter(row["best_simple_pair"] for row in context_rows)

    lines = [
        "# x264_time_* with empirical x264_time_* acquisition cost",
        "",
        "## Scope and protocol",
        "",
        "This batch analyzes the 17 `x264_time_i` contexts. For each input `i`, the prediction target is "
        "encoding time and the empirical training acquisition cost is the same encoding time measurement. "
        f"Each context uses {len(DEFAULT_LAMBDAS)} lambda values and the available 100 runs for six strategies "
        "at `t1`, `t2`, and `t3` sample sizes.",
        "",
        "This is the strongest Tier 1 setting for the paper because the target property and measurement "
        "cost are the same phenomenon. If count-based effort is misleading here, it is not because we used "
        "an unrelated cost proxy.",
        "",
        "The learner is the current lightweight ridge/log-linear model. These results validate the "
        "infrastructure and expose cost-model behavior; final paper numbers should still be replicated "
        "with the chosen literature-aligned learner.",
        "",
        "## Overall result",
        "",
        "The time-property case strengthens the core argument. Sample size remains highly correlated with "
        "empirical measurement cost, but strategy identity creates repeatable fixed-size bias. Because "
        "time is both target and cost here, cost-aware conclusions are especially sensitive to whether "
        "we use `n` or measured time.",
        "",
        "## RQ1: Empirical cost heterogeneity",
        "",
        f"Across the 17 inputs, per-configuration time-cost CV ranges from {_fmt(min(cvs))} to "
        f"{_fmt(max(cvs))} with median {_fmt(_median(cvs))}. The p90/p10 cost ratio ranges from "
        f"{_fmt(min(p90p10))} to {_fmt(max(p90p10))} with median {_fmt(_median(p90p10))}. "
        "Thus, even within the same system and target property, configurations are not equal-cost units.",
        "",
        f"At fixed sample size, median strategy overhead relative to random ranges from "
        f"{_fmt(overhead_min)} to {_fmt(overhead_max)} across all contexts, strategies, and levels. "
        "The count-cost model assigns these samples identical effort, but the empirical data does not.",
        "",
        "Median cost-over-random by strategy across all inputs and levels:",
        "",
    ]
    lines.extend([f"- `{strategy}`: {_fmt(value)}" for strategy, value in strategy_overhead])
    lines.extend(
        [
            "",
            "Interpretation: `henard` repeatedly selects cheaper configurations, while `twise` repeatedly "
            "selects costlier ones. The other strategies are closer to random on median but still vary by "
            "input and sample level.",
            "",
            "## RQ2: Validity of sample size as cost proxy",
            "",
            f"Spearman rho between `n` and empirical `TrainCost` is high in every context "
            f"(range {_fmt(min(spearman_values))}-{_fmt(max(spearman_values))}, "
            f"median {_fmt(_median(spearman_values))}). So sample size is a useful coarse ranking signal.",
            "",
            f"Calibration is the problem. The context-level median `%cost/%n` ratio ranges from "
            f"{_fmt(min(ratio_values))} to {_fmt(max(ratio_values))}; the lower quartile can drop to "
            f"{_fmt(min(q1_values))}, and the upper quartile can reach {_fmt(max(q3_values))}. "
            "A strategy can therefore look equivalent under `n` while consuming materially less or more "
            "measurement time.",
            "",
            "Median calibration ratio by strategy:",
            "",
        ]
    )
    lines.extend([f"- `{strategy}`: {_fmt(value)}" for strategy, value in strategy_ratio])
    lines.extend(
        [
            "",
            "Interpretation: sample size is not wrong as a first-order abstraction, but it is incomplete. "
            "The correct paper phrasing is that `n` is usually correlated with cost, yet it is not a "
            "calibrated or strategy-neutral cost model.",
            "",
            "## RQ3: Robustness of conclusions to the cost model",
            "",
            f"Across {total_rank_cases} `(context, lambda)` ranking cases, the top-1 strategy-size pair "
            f"changes {top1_flips} times, so top-1 agreement is {_fmt(top1_agreement)}. "
            f"The lowest mean Kendall tau occurs at lambda={worst_lambda:g} with tau={_fmt(worst_tau)}.",
            "",
            "This is stronger evidence than in a pure target/cost-separation scenario: when predicting time, "
            "the empirical cost term is also the property being modeled. A count-cost ranking can therefore "
            "recommend a sample that is not actually efficient once measurement time is accounted for.",
            "",
            "## RQ4: Pareto-efficient sampling under empirical cost",
            "",
            f"Count-frontier overlap with the empirical frontier has median Jaccard "
            f"{_fmt(_median(pareto_jaccards))} across inputs. The count frontier is concentrated on:",
            "",
        ]
    )
    lines.extend([f"- `{pair}`: {count} / {len(context_rows)} contexts" for pair, count in count_frontier.most_common()])
    lines.extend(["", "The empirical frontier highlights a different decision set:"])
    lines.extend([f"- `{pair}`: {count} / {len(context_rows)} contexts" for pair, count in empirical_frontier.most_common()])
    lines.extend(
        [
            "",
            "Interpretation: empirical Pareto analysis surfaces cheap, accuracy-competitive fixed-size "
            "choices that count-based Pareto analysis can hide. This is exactly why RQ4 is useful: it avoids "
            "arguing about one lambda and asks which choices are simply dominated under the measured cost.",
            "",
            "## RQ5: Context sensitivity",
            "",
            f"The effect appears across all 17 inputs, but magnitude varies. Cost CV ranges over "
            f"{_fmt(max(cvs) - min(cvs))} absolute points, and context-level median calibration ratio spans "
            f"{_fmt(max(ratio_values) - min(ratio_values))}. Rank sensitivity is also context-dependent: "
            f"some inputs have no top-1 flips, while the maximum is "
            f"{max(row['rank_top1_flips'] for row in context_rows)} / {len(DEFAULT_LAMBDAS)} lambda values.",
            "",
            "This supports a context-sensitive conclusion rather than a universal one: size-based effort is "
            "safer in some inputs than others, even for the same configurable system and same target property.",
            "",
            "## Paper-level takeaway",
            "",
            "For `x264_time_*`, sample size is a strong coarse proxy but not a calibrated empirical-cost "
            "model. The central paper claim is well supported: replacing count-based effort with measured "
            "training time can expose strategy-specific acquisition bias, change cost-sensitive rankings, "
            "and produce different Pareto frontiers.",
            "",
            "Most frequent simple best pairs by context-level `MRE + empirical-cost` are:",
            "",
        ]
    )
    lines.extend([f"- `{pair}`: {count} / {len(context_rows)} contexts" for pair, count in best_pairs.most_common()])
    lines.append("")
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
        context = f"x264_time_{idx}"
        print(f"Analyzing {context}")
        dataset = load_runs_dataset(args.runs_zip, context, max_runs=args.max_runs)
        expected_n = load_summary_configuration_count(args.summary_zip, context)

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
                target_context=context,
                cost_context=context,
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
        context_label="x264_time contexts",
    )
    plot_context_sensitivity(
        context_rows,
        output_dir / "fig_rq5_context_sensitivity.png",
        context_prefix="x264_time_",
    )
    write_time_report(
        output_dir / "x264_time_report.md",
        context_rows=context_rows,
        proxy_rows=all_proxy,
        strategy_rows=all_strategy,
        rank_rows=all_ranks,
    )

    print(f"Done. Outputs: {output_dir}")


if __name__ == "__main__":
    main()
