#!/usr/bin/env python3
"""Run the full 2x2 x264 cost/target matrix."""

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
from cost_sampling.archive_runs import attach_cost_dataset, load_runs_dataset, load_summary_configuration_count
from cost_sampling.hypotheses import (
    aggregate_verdicts,
    evaluate_per_context_hypotheses,
    test_h5a_input_sensitivity,
    test_h5b_target_property_gap,
    test_h5c_rank_stability_compare,
)
from cost_sampling.metrics import LEARNER_CHOICES
from cost_sampling.plots import (
    plot_calibration_by_strategy,
    plot_pareto_jaccard_by_scenario,
    plot_pareto_frontier_comparison,
    plot_pareto_pair_frequencies,
    plot_rank_agreement_by_scenario,
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


PROPERTIES = ("time", "size")


SCENARIO_ORDER = [
    "cost_time__target_time",
    "cost_time__target_size",
    "cost_size__target_time",
    "cost_size__target_size",
]

SCENARIO_LABELS = {
    "cost_time__target_time": "cost=time, target=time",
    "cost_time__target_size": "cost=time, target=size",
    "cost_size__target_time": "cost=size, target=time",
    "cost_size__target_size": "cost=size, target=size",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-zip", default="ICPE-rawdata/AllRuns.zip", help="Path to AllRuns.zip.")
    parser.add_argument("--summary-zip", default="ICPE-rawdata/AllSummary.zip", help="Path to AllSummary.zip.")
    parser.add_argument("--output-dir", default="artifacts/x264_matrix", help="Output directory.")
    parser.add_argument("--max-runs", type=int, default=100, help="Maximum run id to load.")
    parser.add_argument("--alpha", type=float, default=1.0, help="Ridge regularization strength.")
    parser.add_argument("--learner", default="ridge-log", choices=LEARNER_CHOICES)
    parser.add_argument("--no-log-target", action="store_true", help="Fit the learner on raw target values.")
    parser.add_argument("--contexts", default="0-16", help="Input indices, e.g. 0-16 or 0,3,8.")
    return parser.parse_args()


def context_name(prop: str, idx: int) -> str:
    return f"x264_{prop}_{idx}"


def scenario_id(cost_prop: str, target_prop: str) -> str:
    return f"cost_{cost_prop}__target_{target_prop}"


def scenario_label(cost_prop: str, target_prop: str) -> str:
    return f"cost={cost_prop}, target={target_prop}"


def _pair(row: dict[str, Any]) -> str:
    return f"{row['strategy']}_{row['level']}"


def add_scenario(rows: list[dict[str, Any]], *, cost_prop: str, target_prop: str) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        item = dict(row)
        item["cost_property"] = cost_prop
        item["target_property"] = target_prop
        item["scenario"] = scenario_id(cost_prop, target_prop)
        out.append(item)
    return out


def build_scenario_summary(context_rows: list[dict[str, Any]], rank_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_scenario: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in context_rows:
        by_scenario[row["scenario"]].append(row)
    ranks_by_scenario: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rank_rows:
        ranks_by_scenario[row["scenario"]].append(row)

    out: list[dict[str, Any]] = []
    property_order = {name: idx for idx, name in enumerate(PROPERTIES)}
    ordered = sorted(
        by_scenario.items(),
        key=lambda item: (
            property_order[item[1][0]["cost_property"]],
            property_order[item[1][0]["target_property"]],
        ),
    )
    for scenario, rows in ordered:
        ranks = ranks_by_scenario[scenario]
        top1_flips = sum(1 for row in ranks if not row["top1_agreement"])
        total = len(ranks)
        mean_tau_by_lambda = []
        for lam in DEFAULT_LAMBDAS:
            lam_rows = [row for row in ranks if row["lambda"] == lam]
            mean_tau_by_lambda.append((lam, sum(row["kendall_tau"] for row in lam_rows) / len(lam_rows)))
        worst_lambda, worst_tau = min(mean_tau_by_lambda, key=lambda item: item[1])
        out.append(
            {
                "scenario": scenario,
                "cost_property": rows[0]["cost_property"],
                "target_property": rows[0]["target_property"],
                "contexts": len(rows),
                "rank_top1_flips": top1_flips,
                "rank_cases": total,
                "rank_top1_agreement": 1.0 - top1_flips / total,
                "rank_mean_kendall_tau": sum(row["kendall_tau"] for row in ranks) / len(ranks),
                "rank_worst_lambda": worst_lambda,
                "rank_worst_lambda_tau": worst_tau,
                "pareto_median_jaccard": _median([row["pareto_jaccard"] for row in rows]),
                "pareto_min_jaccard": min(row["pareto_jaccard"] for row in rows),
                "pareto_max_jaccard": max(row["pareto_jaccard"] for row in rows),
                "best_simple_pairs": ", ".join(
                    f"{pair}:{count}" for pair, count in Counter(row["best_simple_pair"] for row in rows).most_common()
                ),
                "count_frontier_pairs": ", ".join(
                    f"{pair}:{count}" for pair, count in count_pairs(rows, "pareto_count_pairs").most_common()
                ),
                "empirical_frontier_pairs": ", ".join(
                    f"{pair}:{count}" for pair, count in count_pairs(rows, "pareto_empirical_pairs").most_common()
                ),
            }
        )
    return out


def build_cost_property_summary(
    *,
    cost_prop: str,
    context_rows: list[dict[str, Any]],
    proxy_rows: list[dict[str, Any]],
    strategy_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    cvs = [row["cost_cv"] for row in context_rows]
    p90p10 = [row["cost_p90_over_p10"] for row in context_rows]
    proxy_all = [row for row in proxy_rows if row["strategy"] == "ALL"]
    ratios = [row["median_calibration_ratio"] for row in proxy_all]
    q1s = [row["q1_calibration_ratio"] for row in proxy_all]
    q3s = [row["q3_calibration_ratio"] for row in proxy_all]
    spearman_values = [row["spearman_n_train_cost"] for row in proxy_all]
    strategy_ratio = median_by_strategy([row for row in proxy_rows if row["strategy"] != "ALL"], "median_calibration_ratio")
    strategy_overhead = median_by_strategy(strategy_rows, "cost_over_random")
    return {
        "cost_property": cost_prop,
        "contexts": len(context_rows),
        "cost_cv_min": min(cvs),
        "cost_cv_median": _median(cvs),
        "cost_cv_max": max(cvs),
        "cost_p90_p10_min": min(p90p10),
        "cost_p90_p10_median": _median(p90p10),
        "cost_p90_p10_max": max(p90p10),
        "proxy_spearman_min": min(spearman_values),
        "proxy_spearman_median": _median(spearman_values),
        "proxy_spearman_max": max(spearman_values),
        "proxy_ratio_min": min(ratios),
        "proxy_ratio_median": _median(ratios),
        "proxy_ratio_max": max(ratios),
        "proxy_q1_min": min(q1s),
        "proxy_q3_max": max(q3s),
        "cost_over_random_min": min(row["cost_over_random"] for row in strategy_rows),
        "cost_over_random_max": max(row["cost_over_random"] for row in strategy_rows),
        "strategy_calibration_medians": "; ".join(f"{s}={_fmt(v)}" for s, v in strategy_ratio),
        "strategy_over_random_medians": "; ".join(f"{s}={_fmt(v)}" for s, v in strategy_overhead),
    }


def report_frontier_pairs(row: dict[str, Any], key: str, n_contexts: int) -> list[str]:
    pairs = []
    for part in str(row[key]).split(","):
        part = part.strip()
        if not part:
            continue
        pair, count = part.rsplit(":", 1)
        pairs.append(f"- `{pair}`: {count} / {n_contexts} contexts")
    return pairs


def write_matrix_report(
    output: Path,
    *,
    cost_summaries: list[dict[str, Any]],
    scenario_summaries: list[dict[str, Any]],
) -> None:
    by_cost = {row["cost_property"]: row for row in cost_summaries}
    lines = [
        "# x264 2x2 cost-target matrix",
        "",
        "## Scope and protocol",
        "",
        "This report separates the property used as the cost axis from the property being predicted. "
        "For every x264 input `i`, it evaluates four scenarios:",
        "",
        "- cost=time, target=time",
        "- cost=time, target=size",
        "- cost=size, target=time",
        "- cost=size, target=size",
        "",
        "Here `cost=size` means that the cost objective is the sum of selected configurations' measured "
        "output-size values. This is not elapsed acquisition time; it is a second empirical cost metric "
        "that can matter if the budget of interest is output footprint rather than measurement duration.",
        "",
        "RQ1 and RQ2 are grouped by cost property because they only ask whether the selected configurations "
        "have heterogeneous empirical cost and whether `n` is calibrated against that cost. RQ3 and RQ4 "
        "are scenario-specific because rankings and Pareto frontiers combine the cost metric with "
        "target-specific prediction error.",
        "",
        "The learner remains the current lightweight ridge/log-linear model, so this is an infrastructure "
        "and positioning result rather than the final modeling claim.",
        "",
        "## Overall result",
        "",
        "The correction matters. Cost-model validity is primarily a property of the cost axis, while "
        "strategy recommendation is a property of the cost-target pair. The same sampling run can be "
        "near-calibrated under time cost and differently calibrated under size cost, and the same cost "
        "model can produce different rankings depending on whether the target is time or size.",
        "",
        "## RQ1: Empirical cost heterogeneity by cost property",
        "",
        "![Time-cost strategy bias](fig_rq1_cost_time_strategy_bias.png)",
        "",
        "![Size-cost strategy bias](fig_rq1_cost_size_strategy_bias.png)",
        "",
    ]

    for prop in PROPERTIES:
        row = by_cost[prop]
        lines.extend(
            [
                f"### Cost = {prop}",
                "",
                f"Across {row['contexts']} inputs, per-configuration cost CV ranges from "
                f"{_fmt(row['cost_cv_min'])} to {_fmt(row['cost_cv_max'])} with median "
                f"{_fmt(row['cost_cv_median'])}. The p90/p10 cost ratio ranges from "
                f"{_fmt(row['cost_p90_p10_min'])} to {_fmt(row['cost_p90_p10_max'])} with median "
                f"{_fmt(row['cost_p90_p10_median'])}.",
                "",
                f"At fixed sample size, median strategy overhead relative to random ranges from "
                f"{_fmt(row['cost_over_random_min'])} to {_fmt(row['cost_over_random_max'])}.",
                "",
                f"Median cost-over-random by strategy: {row['strategy_over_random_medians']}.",
                "",
            ]
        )

    lines.extend(
        [
            "Interpretation: RQ1 should not be tied to the prediction target. It asks whether the chosen "
            "cost metric itself is heterogeneous across configurations and sampling strategies. Both time "
            "and size show heterogeneity, but the magnitude and strategy bias should be reported separately.",
            "",
            "## RQ2: Validity of sample size as cost proxy by cost property",
            "",
            "![Time-cost calibration by strategy](fig_rq2_cost_time_calibration_by_strategy.png)",
            "",
            "![Size-cost calibration by strategy](fig_rq2_cost_size_calibration_by_strategy.png)",
            "",
        ]
    )

    for prop in PROPERTIES:
        row = by_cost[prop]
        lines.extend(
            [
                f"### Cost = {prop}",
                "",
                f"Spearman rho between `n` and empirical cost ranges from "
                f"{_fmt(row['proxy_spearman_min'])} to {_fmt(row['proxy_spearman_max'])}, with median "
                f"{_fmt(row['proxy_spearman_median'])}. The context-level median calibration ratio "
                f"`%cost/%n` ranges from {_fmt(row['proxy_ratio_min'])} to "
                f"{_fmt(row['proxy_ratio_max'])}, with median {_fmt(row['proxy_ratio_median'])}. "
                f"The lower quartile can drop to {_fmt(row['proxy_q1_min'])}, and the upper quartile can "
                f"reach {_fmt(row['proxy_q3_max'])}.",
                "",
                f"Median calibration ratio by strategy: {row['strategy_calibration_medians']}.",
                "",
            ]
        )

    lines.extend(
        [
            "Interpretation: `n` can remain highly correlated with a cost metric while still being "
            "miscalibrated for particular strategies. That statement should be made separately for time "
            "cost and size cost.",
            "",
            "## RQ3: Robustness of conclusions by cost-target scenario",
            "",
            "The figure below keeps the four scenarios separate. Each panel averages agreement across the "
            "17 inputs only within one cost-target scenario.",
            "",
            "![Rank agreement by scenario](fig_rq3_rank_agreement_by_scenario.png)",
            "",
        ]
    )

    for row in scenario_summaries:
        lines.extend(
            [
                f"### {scenario_label(row['cost_property'], row['target_property'])}",
                "",
                f"Across {row['rank_cases']} `(input, lambda)` cases, top-1 rankings change "
                f"{row['rank_top1_flips']} times, so top-1 agreement is "
                f"{_fmt(row['rank_top1_agreement'])}. Mean Kendall tau is "
                f"{_fmt(row['rank_mean_kendall_tau'])}; the weakest lambda is "
                f"{row['rank_worst_lambda']:g} with tau {_fmt(row['rank_worst_lambda_tau'])}.",
                "",
                f"Most frequent simple best pairs: {row['best_simple_pairs']}.",
                "",
            ]
        )

    lines.extend(
        [
            "Interpretation: RQ3 cannot be answered by cost alone. The ranking objective combines prediction "
            "error with the selected cost metric, so time-prediction and size-prediction can react differently "
            "to the same cost abstraction.",
            "",
            "## RQ4: Pareto-efficient sampling by cost-target scenario",
            "",
            "For each input and scenario, each point is a `(strategy, t-level)` choice summarized by median "
            "MRE and median cost over the 100 runs. A point is Pareto-efficient if no other point is at least "
            "as good on both axes, with a strict improvement on one axis. In other words, a dominated point "
            "is worse or equal in MRE and worse or equal in cost than another available choice.",
            "",
            "The comparison asks whether the non-dominated choices change when the x-axis changes from "
            "count cost (`n / |C|`) to empirical cost (`TrainCost / FullCost`). Jaccard is the overlap between "
            "the two frontier sets:",
            "",
            "`Jaccard = |frontier_count ∩ frontier_empirical| / |frontier_count ∪ frontier_empirical|`",
            "",
            "A Jaccard value of `1` means both cost models identify exactly the same Pareto-efficient "
            "strategy-size pairs; `0` means they have no pair in common. Values around `0.4` mean that a "
            "substantial part of the decision frontier changes when measured cost replaces sample count.",
            "",
            "The first figure summarizes frontier overlap per scenario. The tradeoff-plane figures show "
            "actual Pareto fronts with cost on the x-axis and MRE on the y-axis. These plane figures use "
            "median points across the 17 inputs for readability; the reported Jaccard values and pair "
            "frequencies are computed per input before summarization.",
            "",
            "![Pareto Jaccard by scenario](fig_rq4_pareto_jaccard_by_scenario.png)",
            "",
        ]
    )

    for row in scenario_summaries:
        lines.extend(
            [
                f"### {scenario_label(row['cost_property'], row['target_property'])}",
                "",
                f"Median count-vs-empirical frontier Jaccard is {_fmt(row['pareto_median_jaccard'])} "
                f"(range {_fmt(row['pareto_min_jaccard'])}-{_fmt(row['pareto_max_jaccard'])}).",
                "",
                f"![Pareto fronts: {scenario_label(row['cost_property'], row['target_property'])}]"
                f"(fig_rq4_frontier_{row['scenario']}.png)",
                "",
                f"![Pareto pair frequencies: {scenario_label(row['cost_property'], row['target_property'])}]"
                f"(fig_rq4_pairs_{row['scenario']}.png)",
                "",
                "Count frontier concentration:",
                "",
            ]
        )
        lines.extend(report_frontier_pairs(row, "count_frontier_pairs", row["contexts"]))
        lines.extend(["", "Empirical frontier concentration:", ""])
        lines.extend(report_frontier_pairs(row, "empirical_frontier_pairs", row["contexts"]))
        lines.append("")

    lines.extend(
        [
            "RQ4 conclusion: the count-based frontier is not just a horizontally rescaled version of the "
            "empirical frontier. When empirical cost is used, fixed-size choices can move left or right "
            "depending on what they actually cost, so previously dominated points can become efficient and "
            "previously efficient points can disappear. This is the decision-level consequence of the RQ1/RQ2 "
            "calibration bias.",
            "",
            "## Paper-level takeaway",
            "",
            "The clean design is a 2x2 matrix: cost metric on one axis, prediction target on the other. "
            "RQ1 and RQ2 characterize the cost axis itself. RQ3 and RQ4 then ask how much the scientific "
            "conclusions change when that cost axis is combined with either time or size prediction error. "
            "This framing avoids conflating measurement-cost validity with target-prediction performance.",
            "",
        ]
    )
    output.write_text("\n".join(lines), encoding="utf-8")


def run_scenario(
    *,
    runs_zip: str,
    summary_zip: str,
    idx: int,
    cost_prop: str,
    target_prop: str,
    max_runs: int,
    alpha: float,
    learner: str,
    log_target: bool,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    target_context = context_name(target_prop, idx)
    cost_context = context_name(cost_prop, idx)
    target = load_runs_dataset(runs_zip, target_context, max_runs=max_runs)
    if cost_context == target_context:
        dataset = target
    else:
        cost = load_runs_dataset(runs_zip, cost_context, max_runs=max_runs)
        dataset = attach_cost_dataset(target, cost)
    expected_n = load_summary_configuration_count(summary_zip, target_context)

    records = add_scenario(
        evaluate_samples(dataset, alpha=alpha, log_target=log_target, learner=learner),
        cost_prop=cost_prop,
        target_prop=target_prop,
    )
    heterogeneity = add_scenario(cost_heterogeneity_summary(dataset), cost_prop=cost_prop, target_prop=target_prop)
    summary = add_scenario(strategy_summary(records), cost_prop=cost_prop, target_prop=target_prop)
    proxy = add_scenario(proxy_summary(records), cost_prop=cost_prop, target_prop=target_prop)
    ranks = add_scenario(rank_stability(summary, DEFAULT_LAMBDAS), cost_prop=cost_prop, target_prop=target_prop)
    pareto = add_scenario(pareto_summary(summary), cost_prop=cost_prop, target_prop=target_prop)
    context_row = build_context_row(
        target_context=target_context,
        cost_context=cost_context,
        expected_n=expected_n,
        heterogeneity=heterogeneity,
        proxy=proxy,
        summary=summary,
        ranks=ranks,
        pareto=pareto,
    )
    context_row["cost_property"] = cost_prop
    context_row["target_property"] = target_prop
    context_row["scenario"] = scenario_id(cost_prop, target_prop)
    scope = f"x264_{idx}|cost={cost_prop}|target={target_prop}"
    hypothesis_rows = evaluate_per_context_hypotheses(
        scope_value=scope,
        records=records,
        heterogeneity=heterogeneity,
        rank_rows=ranks,
        pareto_rows=pareto,
        cost_values=dataset.cost_values,
    )
    for row in hypothesis_rows:
        row["cost_property"] = cost_prop
        row["target_property"] = target_prop
        row["scenario"] = scenario_id(cost_prop, target_prop)
        row["input_index"] = idx
    return records, heterogeneity, summary, proxy, ranks, pareto, context_row, hypothesis_rows


def dedupe_cost_axis(rows: list[dict[str, Any]], keys: tuple[str, ...]) -> list[dict[str, Any]]:
    seen: set[tuple[Any, ...]] = set()
    out = []
    for row in rows:
        key = tuple(row.get(item) for item in keys)
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


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
    all_hypotheses: list[dict[str, Any]] = []
    context_rows: list[dict[str, Any]] = []

    for cost_prop in PROPERTIES:
        for target_prop in PROPERTIES:
            print(f"Scenario {scenario_label(cost_prop, target_prop)}")
            for idx in context_indices:
                print(f"  input {idx}")
                records, heterogeneity, summary, proxy, ranks, pareto, context_row, hypotheses = run_scenario(
                    runs_zip=args.runs_zip,
                    summary_zip=args.summary_zip,
                    idx=idx,
                    cost_prop=cost_prop,
                    target_prop=target_prop,
                    max_runs=args.max_runs,
                    alpha=args.alpha,
                    learner=args.learner,
                    log_target=not args.no_log_target,
                )
                all_records.extend(records)
                all_heterogeneity.extend(heterogeneity)
                all_strategy.extend(summary)
                all_proxy.extend(proxy)
                all_ranks.extend(ranks)
                all_pareto.extend(pareto)
                all_hypotheses.extend(hypotheses)
                context_rows.append(context_row)

    write_csv(output_dir / "records.csv", all_records)
    write_csv(output_dir / "rq1_cost_heterogeneity.csv", all_heterogeneity)
    write_csv(output_dir / "strategy_summary.csv", all_strategy)
    write_csv(output_dir / "rq2_proxy_summary.csv", all_proxy)
    write_csv(output_dir / "rq3_rank_stability.csv", all_ranks)
    write_csv(output_dir / "rq4_pareto.csv", all_pareto)
    write_csv(output_dir / "context_summary.csv", context_rows)

    cost_summaries: list[dict[str, Any]] = []
    for cost_prop in PROPERTIES:
        cost_context_rows = dedupe_cost_axis(
            [row for row in context_rows if row["cost_property"] == cost_prop],
            ("cost_property", "cost_context"),
        )
        cost_proxy_rows = dedupe_cost_axis(
            [row for row in all_proxy if row["cost_property"] == cost_prop],
            ("cost_property", "cost_context", "strategy"),
        )
        cost_strategy_rows = dedupe_cost_axis(
            [row for row in all_strategy if row["cost_property"] == cost_prop],
            ("cost_property", "cost_context", "strategy", "level"),
        )
        cost_summaries.append(
            build_cost_property_summary(
                cost_prop=cost_prop,
                context_rows=cost_context_rows,
                proxy_rows=cost_proxy_rows,
                strategy_rows=cost_strategy_rows,
            )
        )
        write_csv(output_dir / f"cost_{cost_prop}_rq1rq2_context_summary.csv", cost_context_rows)
        write_csv(output_dir / f"cost_{cost_prop}_rq2_proxy_summary.csv", cost_proxy_rows)
        write_csv(output_dir / f"cost_{cost_prop}_strategy_cost_summary.csv", cost_strategy_rows)
        plot_strategy_cost_bias(cost_strategy_rows, output_dir / f"fig_rq1_cost_{cost_prop}_strategy_bias.png")
        plot_calibration_by_strategy(
            cost_proxy_rows,
            output_dir / f"fig_rq2_cost_{cost_prop}_calibration_by_strategy.png",
            title=f"Cost = {cost_prop}",
        )

    scenario_summaries = build_scenario_summary(context_rows, all_ranks)
    write_csv(output_dir / "cost_property_summary.csv", cost_summaries)
    write_csv(output_dir / "scenario_summary.csv", scenario_summaries)

    # Dedupe cost-axis-only hypotheses (H1a/H1b/H2a/H2b/H2c) by (hypothesis,
    # cost_property, input_index) so each cost-axis input contributes one row,
    # not target_property duplicates.
    cost_only_h = {"H1a", "H1b", "H2a", "H2b", "H2c"}
    deduped_h: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for row in all_hypotheses:
        if row["hypothesis"] in cost_only_h:
            key = (row["hypothesis"], row.get("cost_property"), row.get("input_index"))
            if key in seen:
                continue
            seen.add(key)
            tagged = dict(row)
            tagged["scope_value"] = f"x264_{row.get('input_index')}|cost={row.get('cost_property')}"
            deduped_h.append(tagged)
        else:
            deduped_h.append(row)

    # H5a per cost-target scenario: cross-input variation in calibration ratio.
    for scenario in SCENARIO_ORDER:
        scenario_records = [row for row in all_records if row.get("scenario") == scenario]
        h5a = test_h5a_input_sensitivity(scenario_records, scope_value=scenario)
        h5a["scenario"] = scenario
        h5a["cost_property"] = scenario.split("__")[0].replace("cost_", "")
        h5a["target_property"] = scenario.split("__")[1].replace("target_", "")
        deduped_h.append(h5a)
    h5b = test_h5b_target_property_gap(scenario_summaries)
    h5b["scenario"] = "global"
    deduped_h.append(h5b)
    h5c = test_h5c_rank_stability_compare(scenario_summaries)
    h5c["scenario"] = "global"
    deduped_h.append(h5c)

    write_csv(output_dir / "hypothesis_tests.csv", deduped_h)
    write_csv(output_dir / "hypothesis_summary.csv", aggregate_verdicts(deduped_h))

    plot_rank_agreement_by_scenario(
        all_ranks,
        output_dir / "fig_rq3_rank_agreement_by_scenario.png",
        scenario_order=SCENARIO_ORDER,
        scenario_labels=SCENARIO_LABELS,
    )
    plot_pareto_jaccard_by_scenario(
        context_rows,
        output_dir / "fig_rq4_pareto_jaccard_by_scenario.png",
        scenario_order=SCENARIO_ORDER,
        scenario_labels=SCENARIO_LABELS,
    )
    for scenario in SCENARIO_ORDER:
        plot_pareto_frontier_comparison(
            all_strategy,
            output_dir / f"fig_rq4_frontier_{scenario}.png",
            scenario=scenario,
            scenario_label=SCENARIO_LABELS[scenario],
        )
        plot_pareto_pair_frequencies(
            [row for row in context_rows if row["scenario"] == scenario],
            output_dir / f"fig_rq4_pairs_{scenario}.png",
            title=SCENARIO_LABELS[scenario],
        )
    write_matrix_report(
        output_dir / "x264_matrix_report.md",
        cost_summaries=cost_summaries,
        scenario_summaries=scenario_summaries,
    )
    print(f"Done. Outputs: {output_dir}")


if __name__ == "__main__":
    main()
