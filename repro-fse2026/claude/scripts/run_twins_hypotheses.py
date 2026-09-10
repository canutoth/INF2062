#!/usr/bin/env python3
"""Compute H1--H4 hypothesis verdicts for a Twins generated-sampling batch.

The generated Twins protocol has two cost properties (`performance`, `energy`)
and two prediction targets. We therefore keep the hypothesis scopes aligned
with the RQ structure:

* H1/H2 are evaluated per system and cost property.
* H3/H4 are evaluated per system, cost property, and prediction target.
* H3b is evaluated once across all cost-target scenarios.

Diagnostic oracle strategies are excluded from the main H1/H2 verdicts because
they use true cost labels, but they are retained in the per-strategy
calibration appendix.
"""

from __future__ import annotations

import argparse
import csv
import math
import os
from pathlib import Path
import sys
import tempfile
from collections import Counter, defaultdict
from typing import Any

import numpy as np


_cache_root = Path(tempfile.gettempdir()) / "cost_sampling_cache"
(_cache_root / "matplotlib").mkdir(parents=True, exist_ok=True)
(_cache_root / "fontconfig").mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_cache_root / "matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(_cache_root / "fontconfig"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from cost_sampling.analysis import write_csv
from cost_sampling.hypotheses import (
    aggregate_verdicts,
    bootstrap_median_ci,
    test_h1a_cost_heterogeneity,
    test_h1b_strategy_effect,
    test_h2a_correlation,
    test_h2b_calibration_offset,
    test_h2c_calibration_strategy_dep,
    test_h3a_rank_flips,
    test_h3b_flip_correlation,
    test_h4a_h4b_pareto,
)


ORACLE_STRATEGIES = {"cheapOracle", "expensiveOracle"}
VERDICT_ORDER = ["supports", "refutes", "inconclusive"]
VERDICT_COLORS = {
    "supports": "#54A24B",
    "refutes": "#E45756",
    "inconclusive": "#9D9DA1",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        default="artifacts/twins_generated_quick",
        help="Twins generated batch directory.",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Where to write hypothesis outputs. Defaults to --input-dir.",
    )
    parser.add_argument(
        "--include-oracles-main",
        action="store_true",
        help="Include cheap/expensive diagnostic oracles in aggregate H1/H2 tests.",
    )
    return parser.parse_args()


def _read_csv(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _to_float(row: dict[str, Any], key: str, default: float = float("nan")) -> float:
    try:
        return float(row.get(key, default))
    except (TypeError, ValueError):
        return default


def _to_int(row: dict[str, Any], key: str, default: int = 0) -> int:
    try:
        return int(float(row.get(key, default)))
    except (TypeError, ValueError):
        return default


def _coerce_records(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        for key in ("run", "n"):
            if key in item:
                item[key] = _to_int(item, key)
        for key in ("pct_n", "train_cost", "pct_cost", "calibration_ratio", "mre"):
            if key in item:
                item[key] = _to_float(item, key)
        out.append(item)
    return out


def _coerce_heterogeneity(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["n_configurations"] = _to_int(item, "n_configurations")
        for key in (
            "full_cost",
            "min_cost",
            "q1_cost",
            "median_cost",
            "mean_cost",
            "q3_cost",
            "max_cost",
            "std_cost",
            "cv_cost",
            "p90_over_p10",
        ):
            if key in item:
                item[key] = _to_float(item, key)
        out.append(item)
    return out


def _coerce_ranks(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["lambda"] = _to_float(item, "lambda")
        item["top1_agreement"] = _to_int(item, "top1_agreement")
        item["top3_overlap"] = _to_float(item, "top3_overlap")
        item["kendall_tau"] = _to_float(item, "kendall_tau")
        item["mean_abs_rank_difference"] = _to_float(item, "mean_abs_rank_difference")
        out.append(item)
    return out


def _coerce_pareto(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["n"] = _to_int(item, "n")
        item["pareto_count"] = _to_int(item, "pareto_count")
        item["pareto_empirical"] = _to_int(item, "pareto_empirical")
        for key in ("pct_n", "median_pct_cost", "median_train_cost", "median_mre"):
            if key in item:
                item[key] = _to_float(item, key)
        out.append(item)
    return out


def _coerce_scenario(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        for key in (
            "n_configurations",
            "seeds",
            "rank_top1_flips",
            "pareto_count_n",
            "pareto_empirical_n",
            "pareto_overlap_n",
            "row_cap",
        ):
            if key in item:
                item[key] = _to_int(item, key)
        for key in (
            "full_cost",
            "cost_cv",
            "cost_p90_over_p10",
            "proxy_spearman",
            "proxy_median_ratio",
            "proxy_q1_ratio",
            "proxy_q3_ratio",
            "cost_over_random_min",
            "cost_over_random_max",
            "rank_top1_agreement",
            "rank_mean_kendall_tau",
            "rank_mean_top3_overlap",
            "pareto_jaccard",
            "best_simple_mre",
            "best_simple_pct_cost",
        ):
            if key in item:
                item[key] = _to_float(item, key)
        out.append(item)
    return out


def _fmt(value: Any, digits: int = 3) -> str:
    if value is None:
        return "--"
    if isinstance(value, str):
        return value
    try:
        x = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not math.isfinite(x):
        return "--"
    return f"{x:.{digits}g}"


def _fmt_p(value: float) -> str:
    if not math.isfinite(value):
        return "--"
    if value < 1e-12:
        return "<1e-12"
    if value < 1e-3:
        return f"{value:.2e}"
    return f"{value:.3g}"


def _scenario_label(row: dict[str, Any]) -> str:
    return f"{row['analysis_context']}|cost={row['cost_property']}|target={row['target_property']}"


def _context_dirs(input_dir: Path) -> list[tuple[str, Path]]:
    if (input_dir / "records.csv").exists():
        return [(input_dir.name, input_dir)]
    summary = _read_csv(input_dir / "system_summary.csv")
    if summary:
        out = []
        for row in summary:
            report = row.get("report", "")
            folder = report.split("/", 1)[0] if "/" in report else row.get("analysis_context", "")
            if folder:
                out.append((row.get("analysis_context", folder), input_dir / folder))
        return out
    out = []
    for path in sorted(input_dir.iterdir()):
        if path.is_dir() and (path / "records.csv").exists():
            out.append((path.name, path))
    return out


def _calibration_test(
    records: list[dict[str, Any]],
    *,
    analysis_context: str,
    cost_property: str,
    strategy: str,
) -> dict[str, Any]:
    ratios = np.array(
        [
            r["calibration_ratio"]
            for r in records
            if r.get("strategy") == strategy and math.isfinite(r.get("calibration_ratio", float("nan")))
        ],
        dtype=float,
    )
    if ratios.size < 10:
        return {
            "analysis_context": analysis_context,
            "cost_property": cost_property,
            "strategy": strategy,
            "n_records": int(ratios.size),
            "median_ratio": float("nan"),
            "ci_low": float("nan"),
            "ci_high": float("nan"),
            "deviation": float("nan"),
            "verdict": "inconclusive",
        }
    ci = bootstrap_median_ci(ratios)
    median = ci["median"]
    deviation = abs(median - 1.0)
    excludes_one = (ci["ci_low"] > 1.0) or (ci["ci_high"] < 1.0)
    if excludes_one and deviation >= 0.05:
        verdict = "miscalibrated"
    elif (not excludes_one) and deviation < 0.05:
        verdict = "calibrated"
    else:
        verdict = "inconclusive"
    return {
        "analysis_context": analysis_context,
        "cost_property": cost_property,
        "strategy": strategy,
        "n_records": int(ratios.size),
        "median_ratio": float(median),
        "ci_low": float(ci["ci_low"]),
        "ci_high": float(ci["ci_high"]),
        "deviation": float(deviation),
        "verdict": verdict,
    }


def _strategy_calibration_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(row["cost_property"], row["strategy"])].append(row)
    out = []
    for (cost, strategy), items in sorted(grouped.items()):
        verdicts = Counter(row["verdict"] for row in items)
        medians = [
            float(row["median_ratio"])
            for row in items
            if math.isfinite(float(row.get("median_ratio", float("nan"))))
        ]
        deviations = [
            float(row["deviation"])
            for row in items
            if math.isfinite(float(row.get("deviation", float("nan"))))
        ]
        out.append(
            {
                "cost_property": cost,
                "strategy": strategy,
                "scopes": len(items),
                "calibrated": verdicts.get("calibrated", 0),
                "miscalibrated": verdicts.get("miscalibrated", 0),
                "inconclusive": verdicts.get("inconclusive", 0),
                "median_of_medians": float(np.median(medians)) if medians else float("nan"),
                "median_abs_deviation": float(np.median(deviations)) if deviations else float("nan"),
            }
        )
    return out


def _plot_hypothesis_verdicts(summary_rows: list[dict[str, Any]], output: Path) -> None:
    if not summary_rows:
        return
    labels = [row["hypothesis"] for row in summary_rows]
    x = np.arange(len(labels))
    bottom = np.zeros(len(labels))
    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    for verdict in VERDICT_ORDER:
        values = np.array([int(row.get(verdict, 0)) for row in summary_rows], dtype=float)
        ax.bar(x, values, bottom=bottom, label=verdict, color=VERDICT_COLORS[verdict])
        bottom += values
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Number of scopes")
    ax.set_title("Hypothesis verdicts by scope")
    ax.legend(frameon=False, ncols=3, loc="upper right")
    ax.grid(axis="y", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def _write_report(
    output: Path,
    *,
    input_dir: Path,
    hypothesis_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    calibration_summary: list[dict[str, Any]],
    scenario_rows: list[dict[str, Any]],
    include_oracles_main: bool,
) -> None:
    by_h = {row["hypothesis"]: row for row in summary_rows}

    def verdict_cell(h_id: str) -> str:
        row = by_h.get(h_id)
        if not row:
            return "--"
        return f"{row['global_verdict']} ({row['supports']} support, {row['refutes']} refute, {row['inconclusive']} inconclusive)"

    def row_for(h_id: str) -> dict[str, Any] | None:
        return next((row for row in hypothesis_rows if row["hypothesis"] == h_id and row["scope"] == "global"), None)

    h3b = row_for("H3b")
    by_h = {row["hypothesis"]: row for row in summary_rows}
    h1b_summary = by_h.get("H1b", {})
    h1b_rows = [row for row in hypothesis_rows if row["hypothesis"] == "H1b"]
    h1b_large_effects = sum(
        1 for row in h1b_rows if math.isfinite(float(row.get("effect_value", float("nan")))) and float(row["effect_value"]) >= 0.14
    )
    h1b_near_significant = sum(
        1 for row in h1b_rows if math.isfinite(float(row.get("p_value", float("nan")))) and float(row["p_value"]) < 0.10
    )
    scenario_count = len(scenario_rows)
    contexts = sorted({row.get("analysis_context", "") for row in scenario_rows if row.get("analysis_context")})
    seed_values = sorted({int(row.get("seeds", 0)) for row in scenario_rows if int(row.get("seeds", 0)) > 0})
    row_caps = sorted({int(row.get("row_cap", 0)) for row in scenario_rows if int(row.get("row_cap", 0)) > 0})
    scope_note = (
        f"This run has {', '.join(str(seed) for seed in seed_values)} stochastic seeds"
        if seed_values
        else "The seed count is not recorded in the scenario summary"
    )
    if row_caps:
        scope_note += f" and row caps {', '.join(str(cap) for cap in row_caps)}."
    else:
        scope_note += " and no row cap recorded in the scenario summary."
    if len(contexts) == 1:
        h3b_scope_note = "H3b is descriptive only for this single-system report; use the broad batch for the cross-system H3b claim."
    else:
        h3b_scope_note = "H3b is evaluated across the cost-target scenarios in this batch."

    if str(h1b_summary.get("global_verdict", "")).startswith("supported"):
        h1b_interpretation = (
            f"Formal strategy-cost effects are supported in {h1b_summary.get('supports', 0)}/{h1b_summary.get('scopes', len(h1b_rows))} scopes; "
            f"{h1b_large_effects}/{len(h1b_rows)} scopes have large eta^2."
        )
        h1b_rq_sentence = "H1b also supports strategy-induced cost differences at fixed n."
    else:
        h1b_interpretation = (
            f"Underpowered in this run: {h1b_large_effects}/{len(h1b_rows)} scopes have large eta^2, "
            f"but only {h1b_near_significant}/{len(h1b_rows)} reach p<0.10."
        )
        h1b_rq_sentence = (
            "H1b should be treated as inconclusive in this run because the fixed-n group test lacks enough "
            "statistical support, despite large observed effect sizes."
        )
    scenario_with_flips = sum(1 for row in scenario_rows if int(row.get("rank_top1_flips", 0)) > 0)
    frontier_changes = sum(1 for row in scenario_rows if float(row.get("pareto_jaccard", 1.0)) < 0.999)
    cost_contexts = sorted({(row["analysis_context"], row["cost_property"]) for row in scenario_rows})
    strong_cv = {
        (row["analysis_context"], row["cost_property"])
        for row in scenario_rows
        if row["cost_property"] == row["target_property"] and float(row.get("cost_cv", 0.0)) >= 0.4
    }
    high_rho = {
        (row["analysis_context"], row["cost_property"])
        for row in scenario_rows
        if row["cost_property"] == row["target_property"] and float(row.get("proxy_spearman", 0.0)) >= 0.7
    }
    median_ratios = [
        float(row["proxy_median_ratio"])
        for row in scenario_rows
        if row["cost_property"] == row["target_property"] and math.isfinite(float(row.get("proxy_median_ratio", float("nan"))))
    ]
    ratio_min = min(median_ratios) if median_ratios else float("nan")
    ratio_max = max(median_ratios) if median_ratios else float("nan")

    top_examples = sorted(
        [
            row
            for row in scenario_rows
            if row["cost_property"] == row["target_property"]
        ],
        key=lambda row: float(row.get("cost_cv", 0.0)),
        reverse=True,
    )[:5]
    stable_examples = sorted(
        [
            row
            for row in scenario_rows
            if row["cost_property"] == row["target_property"]
        ],
        key=lambda row: float(row.get("cost_cv", 0.0)),
    )[:5]

    lines = [
        "# TwinsOrFalseFriends Generated-Sampling Hypothesis Checks",
        "",
        "## Scope",
        "",
        f"Input batch: `{input_dir}`.",
        "",
        "The tests reuse the H1a--H4b operationalization in `cost_sampling/hypotheses.py`.",
        "For this 2x2 performance/energy setting, scopes are deliberately not aggregated:",
        "",
        "- H1/H2 are tested per system and cost property.",
        "- H3/H4 are tested per system, cost property, and prediction target.",
        "- H3b is a single cross-scenario correlation between cost CV and top-1 rank flips.",
        "",
        (
            "The main H1/H2 tests include the diagnostic cheap/expensive oracles."
            if include_oracles_main
            else "The main H1/H2 tests exclude the diagnostic cheap/expensive oracles; oracle calibration is reported separately."
        ),
        "",
        scope_note,
        h3b_scope_note,
        "",
        "## Verdict Summary",
        "",
        "![Hypothesis verdicts](fig_twins_hypothesis_verdicts.png)",
        "",
        "| Hypothesis | RQ | Scope | Verdict summary | Interpretation |",
        "|---|---|---|---|---|",
        f"| H1a | RQ1 | system-cost | {verdict_cell('H1a')} | Per-configuration acquisition cost is usually heterogeneous. Strong-CV contexts: {len(strong_cv)}/{len(cost_contexts)}. |",
        f"| H1b | RQ1 | system-cost | {verdict_cell('H1b')} | {h1b_interpretation} |",
        f"| H2a | RQ2 | system-cost | {verdict_cell('H2a')} | n is often rank-correlated with TrainCost; strong rho contexts: {len(high_rho)}/{len(cost_contexts)}. |",
        f"| H2b | RQ2 | system-cost | {verdict_cell('H2b')} | Aggregate median calibration is conditional, with context medians spanning {_fmt(ratio_min)}-{_fmt(ratio_max)}. |",
        f"| H2c | RQ2 | system-cost | {verdict_cell('H2c')} | Calibration depends on strategy, so a single global ratio is not enough. |",
        f"| H3a | RQ3 | system-cost-target | {verdict_cell('H3a')} | Count-cost and empirical-cost rankings disagree in {scenario_with_flips}/{scenario_count} scenarios. |",
        f"| H3b | RQ3 | global scenarios | {verdict_cell('H3b')} | Cross-scenario CV-to-flip relation: rho={_fmt(h3b['statistic_value'] if h3b else float('nan'))}, p={_fmt_p(h3b['p_value'] if h3b else float('nan'))}. |",
        f"| H4a | RQ4 | system-cost-target | {verdict_cell('H4a')} | At least one pair flips Pareto status in most or all scenarios. |",
        f"| H4b | RQ4 | system-cost-target | {verdict_cell('H4b')} | Count and empirical Pareto frontiers differ in {frontier_changes}/{scenario_count} scenarios. |",
        "",
        "## RQ-Level Synthesis",
        "",
        "**RQ1.** The equal-cost-per-configuration assumption is not credible for Twins overall.",
        f"H1a gives the formal support. {h1b_rq_sentence}",
        "The strongest cost heterogeneity appears in:",
        "",
    ]
    for row in top_examples:
        lines.append(
            f"- `{row['analysis_context']}` cost=`{row['cost_property']}`: "
            f"CV={_fmt(row['cost_cv'])}, p90/p10={_fmt(row['cost_p90_over_p10'])}."
        )
    lines.extend(
        [
            "",
            "The lowest-heterogeneity contrasts are:",
            "",
        ]
    )
    for row in stable_examples:
        lines.append(
            f"- `{row['analysis_context']}` cost=`{row['cost_property']}`: "
            f"CV={_fmt(row['cost_cv'])}, p90/p10={_fmt(row['cost_p90_over_p10'])}."
        )
    lines.extend(
        [
            "",
            "**RQ2.** Sample size is a useful ordering proxy in many contexts, but not a complete cost model.",
            f"The median calibration ratios across system-cost contexts span {_fmt(ratio_min)}-{_fmt(ratio_max)}, "
            "and H2c shows that strategy-specific calibration must be reported.",
            "",
            "**RQ3.** The cost model changes cost-sensitive strategy rankings.",
            f"Top-1 recommendations change in {scenario_with_flips}/{scenario_count} cost-target scenarios under the lambda sweep.",
            "This is why performance/energy cost and performance/energy targets should be kept faceted.",
            "",
            "**RQ4.** The Pareto-front conclusion is stronger than the scalar-ranking conclusion.",
            f"Empirical-cost and count-cost frontiers differ in {frontier_changes}/{scenario_count} scenarios.",
            "For paper figures, prefer the per-system frontier plots because the x-axis is an actual cost fraction and the y-axis is MRE.",
            "",
            "## Per-Strategy Calibration Appendix",
            "",
            "This table aggregates per-system bootstrap checks of the median calibration ratio by strategy and cost property.",
            "The verdict is `miscalibrated` when the 95% bootstrap CI excludes 1 and the median deviation is at least 5%.",
            "With limited stochastic repetition, deterministic strategies and oracles often have fewer than ten records per system-cost context, so `inconclusive` here usually means insufficient bootstrap sample size rather than evidence of calibration.",
            "",
            "| Cost | Strategy | Scopes | Calibrated | Miscalibrated | Inconclusive | Median ratio | Median abs deviation |",
            "|---|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in calibration_summary:
        lines.append(
            f"| `{row['cost_property']}` | `{row['strategy']}` | {row['scopes']} | "
            f"{row['calibrated']} | {row['miscalibrated']} | {row['inconclusive']} | "
            f"{_fmt(row['median_of_medians'])} | {_fmt(row['median_abs_deviation'])} |"
        )
    lines.extend(
        [
            "",
            "## Output Files",
            "",
            "- `hypothesis_tests.csv`: one row per formal H1--H4 test scope.",
            "- `hypothesis_summary.csv`: support/refute/inconclusive counts per hypothesis.",
            "- `strategy_calibration_tests.csv`: per-system, per-cost, per-strategy bootstrap calibration checks.",
            "- `strategy_calibration_summary.csv`: aggregate strategy-calibration table.",
            "- `fig_twins_hypothesis_verdicts.png`: stacked verdict-count figure.",
            "",
        ]
    )
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir) if args.output_dir else input_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    hypothesis_rows: list[dict[str, Any]] = []
    strategy_calibration_rows: list[dict[str, Any]] = []

    for analysis_context, context_dir in _context_dirs(input_dir):
        records = _coerce_records(_read_csv(context_dir / "records.csv"))
        heterogeneity = _coerce_heterogeneity(_read_csv(context_dir / "rq1_cost_heterogeneity.csv"))
        rank_rows = _coerce_ranks(_read_csv(context_dir / "rq3_rank_stability.csv"))
        pareto_rows = _coerce_pareto(_read_csv(context_dir / "rq4_pareto.csv"))
        if not records:
            continue

        cost_properties = sorted({row["cost_property"] for row in records})
        target_properties = sorted({row["target_property"] for row in records})

        for cost in cost_properties:
            # H1/H2 depend only on the cost axis. Use the diagonal target to
            # avoid duplicating the same TrainCost rows under both targets.
            cost_records = [
                row
                for row in records
                if row["cost_property"] == cost
                and row["target_property"] == cost
                and (args.include_oracles_main or row["strategy"] not in ORACLE_STRATEGIES)
            ]
            h_rows = [
                row
                for row in heterogeneity
                if row["cost_property"] == cost and row["target_property"] == cost
            ]
            scope = f"{analysis_context}|cost={cost}"
            if h_rows:
                hypothesis_rows.append(test_h1a_cost_heterogeneity(h_rows[0], scope_value=scope))
            hypothesis_rows.append(test_h1b_strategy_effect(cost_records, scope_value=scope))
            hypothesis_rows.append(test_h2a_correlation(cost_records, scope_value=scope))
            hypothesis_rows.append(test_h2b_calibration_offset(cost_records, scope_value=scope))
            hypothesis_rows.append(test_h2c_calibration_strategy_dep(cost_records, scope_value=scope))

            all_cost_records = [
                row for row in records if row["cost_property"] == cost and row["target_property"] == cost
            ]
            for strategy in sorted({row["strategy"] for row in all_cost_records}):
                strategy_calibration_rows.append(
                    _calibration_test(
                        all_cost_records,
                        analysis_context=analysis_context,
                        cost_property=cost,
                        strategy=strategy,
                    )
                )

        for cost in cost_properties:
            for target in target_properties:
                scenario_ranks = [
                    row for row in rank_rows if row["cost_property"] == cost and row["target_property"] == target
                ]
                scenario_pareto = [
                    row for row in pareto_rows if row["cost_property"] == cost and row["target_property"] == target
                ]
                scope = f"{analysis_context}|cost={cost}|target={target}"
                hypothesis_rows.append(test_h3a_rank_flips(scenario_ranks, scope_value=scope))
                h4a, h4b = test_h4a_h4b_pareto(scenario_pareto, scope_value=scope)
                hypothesis_rows.append(h4a)
                hypothesis_rows.append(h4b)

    scenario_rows = _coerce_scenario(_read_csv(input_dir / "scenario_summary.csv"))
    for row in scenario_rows:
        row.setdefault("analysis_context", input_dir.name)
    if scenario_rows:
        h3b = test_h3b_flip_correlation(scenario_rows)
        h3b["scope_value"] = "all_twins_cost_target_scenarios"
        h3b_contexts = {row.get("analysis_context", "") for row in scenario_rows}
        if len(h3b_contexts) < 4:
            h3b["verdict"] = "inconclusive"
            h3b["effect_label"] = "single-system descriptive"
        h3b["notes"] = (
            f"Spearman(CV, top1 flips) rho={h3b['statistic_value']:.3g} "
            f"across n={len(scenario_rows)} cost-target scenarios"
            + ("; single-system scope is too small for the cross-system H3b claim" if len(h3b_contexts) < 4 else "")
        )
        hypothesis_rows.append(h3b)

    summary_rows = aggregate_verdicts(hypothesis_rows)
    calibration_summary = _strategy_calibration_summary(strategy_calibration_rows)

    write_csv(output_dir / "hypothesis_tests.csv", hypothesis_rows)
    write_csv(output_dir / "hypothesis_summary.csv", summary_rows)
    write_csv(output_dir / "strategy_calibration_tests.csv", strategy_calibration_rows)
    write_csv(output_dir / "strategy_calibration_summary.csv", calibration_summary)
    _plot_hypothesis_verdicts(summary_rows, output_dir / "fig_twins_hypothesis_verdicts.png")
    _write_report(
        output_dir / "twins_hypothesis_report.md",
        input_dir=input_dir,
        hypothesis_rows=hypothesis_rows,
        summary_rows=summary_rows,
        calibration_summary=calibration_summary,
        scenario_rows=scenario_rows,
        include_oracles_main=args.include_oracles_main,
    )
    print(f"Wrote hypothesis outputs to {output_dir}")


if __name__ == "__main__":
    main()
