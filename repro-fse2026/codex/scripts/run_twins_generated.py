#!/usr/bin/env python3
"""Run generated-sampling protocol on one TwinsOrFalseFriends system."""

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
from cost_sampling.generated_sampling import (
    build_generated_dataset,
    budget_grid,
    load_twins_table,
    parse_where,
)
from cost_sampling.metrics import LEARNER_CHOICES
from cost_sampling.plots import (
    plot_accuracy_cost,
    plot_calibration,
    plot_pareto_frontier_comparison,
    plot_pareto_jaccard_by_scenario,
    plot_rank_agreement_by_scenario,
    plot_strategy_cost_bias,
)


DEFAULT_LAMBDAS = [0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 10.0]
DEFAULT_PROPERTIES = ["performance", "energy"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--zip",
        default="/private/tmp/TwinsOrFalseFriends-ICSE2023.zip",
        help="Path to AI-4-SE/TwinsOrFalseFriends-ICSE2023.zip.",
    )
    parser.add_argument("--system", default="HSQLDB", help="System under data/<system>/measurements.csv.")
    parser.add_argument("--output-dir", default=None, help="Output directory.")
    parser.add_argument("--seeds", type=int, default=30, help="Stochastic seeds per budget.")
    parser.add_argument("--max-budget", type=int, default=256, help="Maximum generated sample size.")
    parser.add_argument(
        "--max-rows",
        type=int,
        default=None,
        help="Deterministically subsample this many rows after filters. Use only for exploratory large-system passes.",
    )
    parser.add_argument("--row-seed", type=int, default=0, help="Seed for --max-rows subsampling.")
    parser.add_argument("--alpha", type=float, default=1.0, help="Ridge regularization strength.")
    parser.add_argument(
        "--learner",
        choices=LEARNER_CHOICES,
        default="ridge-log",
        help="Learner used to estimate the prediction target from sampled configurations.",
    )
    parser.add_argument("--no-log-target", action="store_true", help="Fit on raw target values.")
    parser.add_argument(
        "--cost-orientation",
        action="append",
        default=[],
        metavar="PROPERTY=lower|inverse",
        help="Cost-axis orientation override. Use inverse for throughput-like cost properties.",
    )
    parser.add_argument(
        "--where",
        action="append",
        default=[],
        metavar="COLUMN=VALUE",
        help="Filter rows before sampling, e.g. --where revision=2.2.0.",
    )
    parser.add_argument("--no-oracles", action="store_true", help="Skip cheap/expensive diagnostic oracles.")
    parser.add_argument(
        "--progress-every",
        type=int,
        default=100,
        help="Print progress every N sample evaluations; use 0 to disable.",
    )
    return parser.parse_args()


def _fmt(value: float) -> str:
    return f"{value:.4g}"


def _median(values: list[float]) -> float:
    return float(statistics.median(values))


def _scenario(cost: str, target: str) -> str:
    return f"cost_{cost}__target_{target}"


def _scenario_label(cost: str, target: str) -> str:
    return f"cost={cost}, target={target}"


def _learner_description(learner: str) -> str:
    descriptions = {
        "ridge-log": "ridge regression trained on log-transformed targets",
        "ridge-raw": "ridge regression trained on raw targets",
        "cart-log": "a lightweight CART-style regression tree trained on log-transformed targets",
        "cart-raw": "a lightweight CART-style regression tree trained on raw targets",
        "rf-log": "a dependency-free random forest trained on log-transformed targets",
        "rf-raw": "a dependency-free random forest trained on raw targets",
        "gbt-log": "dependency-free gradient boosted regression trees trained on log-transformed targets",
        "gbt-raw": "dependency-free gradient boosted regression trees trained on raw targets",
    }
    return descriptions.get(learner, learner)


def _pair(row: dict[str, Any]) -> str:
    return f"{row['strategy']}_{row['level']}"


def _add_metadata(rows: list[dict[str, Any]], *, system: str, cost: str, target: str) -> list[dict[str, Any]]:
    scenario = _scenario(cost, target)
    out = []
    for row in rows:
        item = dict(row)
        item["system"] = system
        item["cost_property"] = cost
        item["target_property"] = target
        item["scenario"] = scenario
        out.append(item)
    return out


def _parse_orientation(items: list[str]) -> dict[str, str]:
    out = {prop: "lower" for prop in DEFAULT_PROPERTIES}
    for item in items:
        if "=" not in item:
            raise ValueError(f"Expected PROPERTY=ORIENTATION, got {item!r}")
        prop, orientation = item.split("=", 1)
        if orientation not in {"lower", "inverse"}:
            raise ValueError(f"Unsupported orientation {orientation!r}; use lower or inverse.")
        out[prop] = orientation
    return out


def _count_pairs(rows: list[dict[str, Any]], column: str) -> Counter[str]:
    counter: Counter[str] = Counter()
    for row in rows:
        for pair in str(row[column]).split(","):
            pair = pair.strip()
            if pair:
                counter[pair] += 1
    return counter


def _median_by_strategy(rows: list[dict[str, Any]], column: str) -> list[tuple[str, float]]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        grouped[str(row["strategy"])].append(float(row[column]))
    return sorted((strategy, _median(values)) for strategy, values in grouped.items())


def _build_scenario_row(
    *,
    system: str,
    cost: str,
    target: str,
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
    empirical = {_pair(row) for row in pareto if row["pareto_empirical"]}
    count = {_pair(row) for row in pareto if row["pareto_count"]}
    union = empirical | count
    best = min(summary, key=lambda row: row["median_mre"] + row["median_pct_cost"])
    return {
        "system": system,
        "cost_property": cost,
        "target_property": target,
        "scenario": _scenario(cost, target),
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
        "pareto_count_n": len(count),
        "pareto_empirical_n": len(empirical),
        "pareto_overlap_n": len(count & empirical),
        "pareto_jaccard": len(count & empirical) / len(union) if union else 1.0,
        "pareto_count_pairs": ", ".join(sorted(count)),
        "pareto_empirical_pairs": ", ".join(sorted(empirical)),
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
    feature_count: int,
    label_columns: list[str],
    context_columns: list[str],
    budgets: list[int],
    seeds: int,
    learner: str,
    scenario_rows: list[dict[str, Any]],
    proxy_rows: list[dict[str, Any]],
    strategy_rows: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Generated sampling on TwinsOrFalseFriends `{system}`",
        "",
        "## Scope",
        "",
        f"Source archive: `{source_zip}`",
        "",
        f"Source member: `{source_member}`",
        "",
        f"The table has {scenario_rows[0]['n_configurations']} rows, {feature_count} encoded feature columns, "
        f"and labels `{', '.join(label_columns)}`.",
        "",
        f"Context columns excluded from features: `{', '.join(context_columns) if context_columns else 'none'}`.",
        "",
        f"Generated budgets: `{', '.join(str(n) for n in budgets)}` with {seeds} stochastic seeds.",
        "",
        f"Current learner: `{learner}` ({_learner_description(learner)}).",
        "",
        "Interpretation note: these results test the sampling-cost protocol, not the final learner choice. "
        "The learner is now a command-line parameter, so the same generated samples can be rerun with CART "
        "or raw-target ridge. A full replication with stepwise linear regression and a literature-aligned "
        "CART implementation should be reported as a learner-robustness extension.",
        "",
        "The protocol uses random, feature-balanced, diversity, pairwise-coverage, and pilot-cost-aware "
        "sampling. Cheap-first and expensive-first are diagnostic oracles when enabled.",
        "",
        "## RQ1/RQ2: cost properties",
        "",
    ]
    for cost in DEFAULT_PROPERTIES:
        row = next(item for item in scenario_rows if item["cost_property"] == cost and item["target_property"] == cost)
        cost_proxy = [item for item in proxy_rows if item["cost_property"] == cost and item["target_property"] == cost]
        strategy_ratio = _median_by_strategy([item for item in cost_proxy if item["strategy"] != "ALL"], "median_calibration_ratio")
        lines.extend(
            [
                f"### Cost = `{cost}`",
                "",
                "**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. "
                f"For `{cost}`, CV={_fmt(row['cost_cv'])}, p90/p10={_fmt(row['cost_p90_over_p10'])}, "
                f"and strategy cost-over-random spans {_fmt(row['cost_over_random_min'])}-"
                f"{_fmt(row['cost_over_random_max'])}.",
                "",
                "**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. "
                f"Spearman rho={_fmt(row['proxy_spearman'])}; median `%cost/%n`="
                f"{_fmt(row['proxy_median_ratio'])} with IQR {_fmt(row['proxy_q1_ratio'])}-"
                f"{_fmt(row['proxy_q3_ratio'])}.",
                "",
                f"Cost heterogeneity: CV={_fmt(row['cost_cv'])}, p90/p10={_fmt(row['cost_p90_over_p10'])}. "
                f"Sample-size proxy: Spearman rho={_fmt(row['proxy_spearman'])}, median `%cost/%n`="
                f"{_fmt(row['proxy_median_ratio'])} (IQR {_fmt(row['proxy_q1_ratio'])}-"
                f"{_fmt(row['proxy_q3_ratio'])}).",
                "",
                f"Strategy cost-over-random range: {_fmt(row['cost_over_random_min'])}-"
                f"{_fmt(row['cost_over_random_max'])}. Median calibration by strategy:",
                "",
            ]
        )
        lines.extend([f"- `{strategy}`: {_fmt(value)}" for strategy, value in strategy_ratio])
        lines.extend(
            [
                "",
                f"![Calibration for {cost}](fig_rq2_calibration_cost_{cost}.png)",
                "",
                f"![Strategy cost bias for {cost}](fig_rq1_strategy_cost_bias_{cost}.png)",
                "",
            ]
        )

    changed_rank = [row for row in scenario_rows if float(row["rank_top1_agreement"]) < 1.0]
    changed_pareto = [row for row in scenario_rows if float(row["pareto_jaccard"]) < 1.0]
    total_scenarios = len(scenario_rows)
    if len(changed_rank) == total_scenarios:
        rq3_answer = "replacing count cost with empirical cost changes the cost-sensitive ranking in all scenarios"
    elif changed_rank:
        rq3_answer = (
            "replacing count cost with empirical cost changes the cost-sensitive ranking in "
            f"{len(changed_rank)} of {total_scenarios} scenarios"
        )
    else:
        rq3_answer = "the top recommendation is stable under count and empirical cost for all scenarios"
    if len(changed_pareto) == total_scenarios:
        rq4_answer = "replacing count cost with empirical cost changes the non-dominated sampling choices in all scenarios"
    elif changed_pareto:
        rq4_answer = (
            "replacing count cost with empirical cost changes the non-dominated sampling choices in "
            f"{len(changed_pareto)} of {total_scenarios} scenarios"
        )
    else:
        rq4_answer = "the count-cost and empirical-cost Pareto sets are identical for all scenarios"

    lines.extend(["## RQ3/RQ4: cost-target scenarios", ""])
    lines.extend(
        [
            f"**RQ3 answer:** {rq3_answer}.",
            "",
            f"**RQ4 answer:** {rq4_answer}.",
            "",
        ]
    )
    lines.append("| Scenario | Top-1 agreement | Mean tau | Pareto Jaccard | Best simple pair |")
    lines.append("|---|---:|---:|---:|---|")
    for row in scenario_rows:
        lines.append(
            f"| `{_scenario_label(row['cost_property'], row['target_property'])}` | "
            f"{_fmt(row['rank_top1_agreement'])} | {_fmt(row['rank_mean_kendall_tau'])} | "
            f"{_fmt(row['pareto_jaccard'])} | `{row['best_simple_pair']}` |"
        )
    lines.extend(
        [
            "",
            "![Rank agreement by scenario](fig_rq3_rank_agreement_by_scenario.png)",
            "",
            "![Pareto Jaccard by scenario](fig_rq4_pareto_jaccard_by_scenario.png)",
            "",
            "The Pareto-front figures below show the direct count-cost vs empirical-cost decision comparison.",
            "",
        ]
    )
    for row in scenario_rows:
        scenario = row["scenario"]
        lines.extend(
            [
                f"### {_scenario_label(row['cost_property'], row['target_property'])}",
                "",
                f"RQ3 detail: top-1 agreement is {_fmt(row['rank_top1_agreement'])}; "
                f"{row['rank_top1_flips']} of {len(DEFAULT_LAMBDAS)} lambda settings select a different "
                "top recommendation under empirical cost than under count cost.",
                "",
                f"RQ4 detail: Pareto Jaccard is {_fmt(row['pareto_jaccard'])}; "
                f"count cost selects {row['pareto_count_n']} non-dominated pairs and empirical cost selects "
                f"{row['pareto_empirical_n']}.",
                "",
                f"![Pareto frontier {scenario}](fig_rq4_frontier_{scenario}.png)",
                "",
            ]
        )
    lines.extend(
        [
            "## Interpretation",
            "",
            "This is a generated-sampling replication point: the dataset supplies measured configurations and labels, "
            "but not sample traces. Therefore, conclusions should be compared to precomputed ICPE/Kaltenecker "
            "results by protocol-aware facets, not by aggregating all rows into one table.",
            "",
            "For paper writing, use this as the first proof that the same RQ machinery works when we must generate "
            "common strategies and a common budget grid ourselves.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir or f"artifacts/twins_{args.system}_generated")
    output_dir.mkdir(parents=True, exist_ok=True)

    where = parse_where(args.where)
    orientations = _parse_orientation(args.cost_orientation)
    table = load_twins_table(args.zip, args.system, where=where, max_rows=args.max_rows, row_seed=args.row_seed)
    budgets = budget_grid(len(table.rows), max_absolute=args.max_budget)

    all_records: list[dict[str, Any]] = []
    all_heterogeneity: list[dict[str, Any]] = []
    all_summary: list[dict[str, Any]] = []
    all_proxy: list[dict[str, Any]] = []
    all_ranks: list[dict[str, Any]] = []
    all_pareto: list[dict[str, Any]] = []
    scenario_rows: list[dict[str, Any]] = []

    mre_cache: dict[tuple[Any, ...], float] = {}

    for cost in DEFAULT_PROPERTIES:
        print(f"Generating samples: system={args.system} cost={cost}", flush=True)
        base_dataset = build_generated_dataset(
            table,
            target_property=DEFAULT_PROPERTIES[0],
            cost_property=cost,
            cost_orientation=orientations.get(cost, "lower"),
            budgets=budgets,
            seeds=args.seeds,
            include_oracles=not args.no_oracles,
        )
        samples = base_dataset.samples
        for target in DEFAULT_PROPERTIES:
            print(f"Running generated protocol: system={args.system} cost={cost} target={target}", flush=True)
            dataset = base_dataset if target == DEFAULT_PROPERTIES[0] else build_generated_dataset(
                table,
                target_property=target,
                cost_property=cost,
                cost_orientation=orientations.get(cost, "lower"),
                budgets=budgets,
                seeds=args.seeds,
                include_oracles=not args.no_oracles,
                samples=samples,
            )
            records = _add_metadata(
                evaluate_samples(
                    dataset,
                    alpha=args.alpha,
                    log_target=not args.no_log_target,
                    learner=args.learner,
                    mre_cache=mre_cache,
                    mre_cache_prefix=(target,),
                    progress_label=f"{args.system} cost={cost} target={target}",
                    progress_every=args.progress_every,
                ),
                system=args.system,
                cost=cost,
                target=target,
            )
            heterogeneity = _add_metadata(cost_heterogeneity_summary(dataset), system=args.system, cost=cost, target=target)
            summary = _add_metadata(strategy_summary(records), system=args.system, cost=cost, target=target)
            proxy = _add_metadata(proxy_summary(records), system=args.system, cost=cost, target=target)
            ranks = _add_metadata(rank_stability(summary, DEFAULT_LAMBDAS), system=args.system, cost=cost, target=target)
            pareto = _add_metadata(pareto_summary(summary), system=args.system, cost=cost, target=target)

            scenario_rows.append(
                _build_scenario_row(
                    system=args.system,
                    cost=cost,
                    target=target,
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

    write_csv(output_dir / "records.csv", all_records)
    write_csv(output_dir / "rq1_cost_heterogeneity.csv", all_heterogeneity)
    write_csv(output_dir / "strategy_summary.csv", all_summary)
    write_csv(output_dir / "rq2_proxy_summary.csv", all_proxy)
    write_csv(output_dir / "rq3_rank_stability.csv", all_ranks)
    write_csv(output_dir / "rq4_pareto.csv", all_pareto)
    write_csv(output_dir / "scenario_summary.csv", scenario_rows)

    for cost in DEFAULT_PROPERTIES:
        calibration_records = [
            row for row in all_records if row["cost_property"] == cost and row["target_property"] == cost
        ]
        cost_summary = [
            row for row in all_summary if row["cost_property"] == cost and row["target_property"] == cost
        ]
        plot_calibration(calibration_records, output_dir / f"fig_rq2_calibration_cost_{cost}.png")
        plot_strategy_cost_bias(cost_summary, output_dir / f"fig_rq1_strategy_cost_bias_{cost}.png")

    scenario_order = [_scenario(cost, target) for cost in DEFAULT_PROPERTIES for target in DEFAULT_PROPERTIES]
    scenario_labels = {
        _scenario(cost, target): _scenario_label(cost, target)
        for cost in DEFAULT_PROPERTIES
        for target in DEFAULT_PROPERTIES
    }
    plot_rank_agreement_by_scenario(
        all_ranks,
        output_dir / "fig_rq3_rank_agreement_by_scenario.png",
        scenario_order=scenario_order,
        scenario_labels=scenario_labels,
    )
    plot_pareto_jaccard_by_scenario(
        scenario_rows,
        output_dir / "fig_rq4_pareto_jaccard_by_scenario.png",
        scenario_order=scenario_order,
        scenario_labels=scenario_labels,
    )
    for cost in DEFAULT_PROPERTIES:
        for target in DEFAULT_PROPERTIES:
            scenario = _scenario(cost, target)
            plot_pareto_frontier_comparison(
                all_summary,
                output_dir / f"fig_rq4_frontier_{scenario}.png",
                scenario=scenario,
                scenario_label=f"{args.system}: {_scenario_label(cost, target)}",
            )
            plot_accuracy_cost(
                [row for row in all_pareto if row["scenario"] == scenario],
                output_dir / f"fig_rq4_accuracy_cost_{scenario}.png",
            )

    _write_report(
        output_dir / f"{args.system}_generated_report.md",
        system=args.system,
        source_zip=args.zip,
        source_member=table.source_member,
        feature_count=len(table.feature_names),
        label_columns=table.label_columns,
        context_columns=table.context_columns,
        budgets=budgets,
        seeds=args.seeds,
        learner=args.learner if not args.no_log_target else args.learner.replace("-log", "-raw"),
        scenario_rows=scenario_rows,
        proxy_rows=all_proxy,
        strategy_rows=all_summary,
    )
    print(f"Done. Outputs: {output_dir}")


if __name__ == "__main__":
    main()
