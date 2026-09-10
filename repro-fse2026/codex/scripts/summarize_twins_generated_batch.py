#!/usr/bin/env python3
"""Rewrite a Twins generated-sampling batch report with RQ-level synthesis."""

from __future__ import annotations

import argparse
import csv
import math
import os
from pathlib import Path
import sys
import tempfile
from collections import defaultdict
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


SCENARIO_ORDER = [
    ("performance", "performance"),
    ("performance", "energy"),
    ("energy", "performance"),
    ("energy", "energy"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default="artifacts/twins_generated_quick")
    parser.add_argument("--output", default=None, help="Report path; defaults to <input-dir>/twins_generated_batch_report.md")
    return parser.parse_args()


def _read_csv(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _float(row: dict[str, Any], key: str, default: float = float("nan")) -> float:
    try:
        return float(row.get(key, default))
    except (TypeError, ValueError):
        return default


def _int(row: dict[str, Any], key: str, default: int = 0) -> int:
    try:
        return int(float(row.get(key, default)))
    except (TypeError, ValueError):
        return default


def _coerce_scenarios(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
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
                item[key] = _int(item, key)
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
                item[key] = _float(item, key)
        out.append(item)
    return out


def _fmt(value: Any, digits: int = 4) -> str:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not math.isfinite(x):
        return "--"
    return f"{x:.{digits}g}"


def _row_range(rows: list[dict[str, Any]], key: str) -> tuple[float, float]:
    values = [_float(row, key) for row in rows]
    values = [value for value in values if math.isfinite(value)]
    return (min(values), max(values)) if values else (float("nan"), float("nan"))


def _scenario_label(cost: str, target: str) -> str:
    return f"{cost}->{target}"


def _scenario_long_label(cost: str, target: str) -> str:
    return f"cost={cost}, target={target}"


def _context_order(system_rows: list[dict[str, Any]], scenario_rows: list[dict[str, Any]]) -> list[str]:
    ordered = [row["analysis_context"] for row in system_rows if row.get("analysis_context")]
    if ordered:
        return ordered
    return sorted({row["analysis_context"] for row in scenario_rows})


def _make_matrix(
    scenario_rows: list[dict[str, Any]],
    contexts: list[str],
    *,
    key: str,
) -> np.ndarray:
    by_cell = {
        (row["analysis_context"], row["cost_property"], row["target_property"]): _float(row, key)
        for row in scenario_rows
    }
    matrix = np.full((len(contexts), len(SCENARIO_ORDER)), np.nan)
    for i, context in enumerate(contexts):
        for j, (cost, target) in enumerate(SCENARIO_ORDER):
            matrix[i, j] = by_cell.get((context, cost, target), np.nan)
    return matrix


def _plot_heatmap(
    matrix: np.ndarray,
    contexts: list[str],
    *,
    title: str,
    output: Path,
    vmin: float = 0.0,
    vmax: float = 1.0,
) -> None:
    fig, ax = plt.subplots(figsize=(8.6, max(4.8, 0.34 * len(contexts) + 1.6)))
    cmap = plt.get_cmap("viridis")
    image = ax.imshow(matrix, aspect="auto", cmap=cmap, vmin=vmin, vmax=vmax)
    ax.set_yticks(np.arange(len(contexts)))
    ax.set_yticklabels(contexts)
    ax.set_xticks(np.arange(len(SCENARIO_ORDER)))
    ax.set_xticklabels([_scenario_label(cost, target) for cost, target in SCENARIO_ORDER], rotation=20, ha="right")
    ax.set_title(title)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = matrix[i, j]
            if math.isfinite(value):
                color = "white" if value < 0.45 else "black"
                ax.text(j, i, f"{value:.2f}", ha="center", va="center", fontsize=7, color=color)
    fig.colorbar(image, ax=ax, fraction=0.03, pad=0.02)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def _plot_cost_proxy_figures(output_dir: Path, scenario_rows: list[dict[str, Any]], contexts: list[str]) -> None:
    diagonal = [
        row for row in scenario_rows if row["cost_property"] == row["target_property"]
    ]
    if not diagonal:
        return
    x = np.arange(len(contexts))
    width = 0.36
    by_cell = {
        (row["analysis_context"], row["cost_property"]): row
        for row in diagonal
    }

    fig, ax = plt.subplots(figsize=(10.2, 4.8))
    for offset, cost, color in [(-width / 2, "performance", "#4C78A8"), (width / 2, "energy", "#F58518")]:
        values = [_float(by_cell.get((context, cost), {}), "proxy_spearman") for context in contexts]
        ax.bar(x + offset, values, width=width, label=cost, color=color)
    ax.axhline(0.7, color="#333333", linewidth=1.0, linestyle="--", label="rho=0.7")
    ax.set_xticks(x)
    ax.set_xticklabels(contexts, rotation=45, ha="right")
    ax.set_ylim(0.0, 1.03)
    ax.set_ylabel("Spearman rho(n, TrainCost)")
    ax.set_title("RQ2: sample-size ordering quality by cost property")
    ax.grid(axis="y", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, ncols=3)
    fig.tight_layout()
    fig.savefig(output_dir / "fig_rq2_proxy_spearman_by_system_cost.png", dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10.2, 4.8))
    for offset, cost, color in [(-width / 2, "performance", "#4C78A8"), (width / 2, "energy", "#F58518")]:
        values = [_float(by_cell.get((context, cost), {}), "proxy_median_ratio") for context in contexts]
        ax.bar(x + offset, values, width=width, label=cost, color=color)
    ax.axhline(1.0, color="#333333", linewidth=1.0, linestyle="--", label="perfect calibration")
    ax.set_xticks(x)
    ax.set_xticklabels(contexts, rotation=45, ha="right")
    ax.set_ylabel("Median (%TrainCost / %n)")
    ax.set_title("RQ2: sample-size calibration by cost property")
    ax.grid(axis="y", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, ncols=3)
    fig.tight_layout()
    fig.savefig(output_dir / "fig_rq2_median_calibration_by_system_cost.png", dpi=200)
    plt.close(fig)


def _plot_batch_ranges(output_dir: Path, system_rows: list[dict[str, Any]], scenario_rows: list[dict[str, Any]], contexts: list[str]) -> None:
    rows_by_context = {
        context: [row for row in scenario_rows if row["analysis_context"] == context]
        for context in contexts
    }
    cv_ranges = [_row_range(rows_by_context[context], "cost_cv") for context in contexts]
    top_ranges = [_row_range(rows_by_context[context], "rank_top1_agreement") for context in contexts]
    jac_ranges = [_row_range(rows_by_context[context], "pareto_jaccard") for context in contexts]
    order = sorted(range(len(contexts)), key=lambda idx: cv_ranges[idx][1], reverse=True)
    labels = [contexts[idx] for idx in order]
    y = list(range(len(labels)))

    fig, ax = plt.subplots(figsize=(8.6, max(4.8, 0.35 * len(labels) + 1.2)))
    for pos, idx in enumerate(order):
        lo, hi = cv_ranges[idx]
        ax.plot([lo, hi], [pos, pos], color="#4C78A8", linewidth=5, solid_capstyle="round")
        ax.scatter([lo, hi], [pos, pos], color="#1f3b57", s=18, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel("Cost CV range across cost-target scenarios")
    ax.grid(axis="x", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(output_dir / "fig_cost_cv_range_by_system.png", dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8.6, max(4.8, 0.35 * len(labels) + 1.2)))
    height = 0.34
    for pos, idx in enumerate(order):
        top_lo, top_hi = top_ranges[idx]
        jac_lo, jac_hi = jac_ranges[idx]
        ax.plot([top_lo, top_hi], [pos - height / 2, pos - height / 2], color="#F58518", linewidth=4, solid_capstyle="round")
        ax.plot([jac_lo, jac_hi], [pos + height / 2, pos + height / 2], color="#54A24B", linewidth=4, solid_capstyle="round")
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlim(-0.02, 1.02)
    ax.set_xlabel("Agreement range across scenarios")
    ax.grid(axis="x", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    handles = [
        plt.Line2D([0], [0], color="#F58518", linewidth=4, label="Top-1 agreement"),
        plt.Line2D([0], [0], color="#54A24B", linewidth=4, label="Pareto Jaccard"),
    ]
    ax.legend(handles=handles, frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(output_dir / "fig_decision_agreement_by_system.png", dpi=200)
    plt.close(fig)


def _plot_all(output_dir: Path, system_rows: list[dict[str, Any]], scenario_rows: list[dict[str, Any]]) -> None:
    contexts = _context_order(system_rows, scenario_rows)
    if not contexts:
        return
    _plot_batch_ranges(output_dir, system_rows, scenario_rows, contexts)
    _plot_cost_proxy_figures(output_dir, scenario_rows, contexts)
    top_matrix = _make_matrix(scenario_rows, contexts, key="rank_top1_agreement")
    jac_matrix = _make_matrix(scenario_rows, contexts, key="pareto_jaccard")
    _plot_heatmap(
        top_matrix,
        contexts,
        title="RQ3: top-1 agreement between count and empirical cost",
        output=output_dir / "fig_rq3_top1_agreement_heatmap.png",
    )
    _plot_heatmap(
        jac_matrix,
        contexts,
        title="RQ4: Pareto-front Jaccard between count and empirical cost",
        output=output_dir / "fig_rq4_pareto_jaccard_heatmap.png",
    )


def _hypothesis_index(input_dir: Path) -> dict[str, dict[str, Any]]:
    rows = _read_csv(input_dir / "hypothesis_summary.csv")
    return {row["hypothesis"]: row for row in rows}


def _hypothesis_sentence(hypotheses: dict[str, dict[str, Any]], h_id: str) -> str:
    row = hypotheses.get(h_id)
    if not row:
        return "not computed"
    return f"{row['global_verdict']}; {row['supports']}/{row['scopes']} supporting scopes"


def _h1b_caveat(hypotheses: dict[str, dict[str, Any]]) -> str:
    row = hypotheses.get("H1b")
    if not row:
        return ""
    if row.get("supports") == "0" and row.get("inconclusive") == row.get("scopes"):
        return " The quick batch is underpowered for the fixed-n strategy-effect test, so H1b remains a rerun-with-more-seeds item even when cost-over-random ranges are visibly wide."
    return ""


def _write_report(
    output: Path,
    *,
    input_dir: Path,
    system_rows: list[dict[str, Any]],
    scenario_rows: list[dict[str, Any]],
) -> None:
    contexts = _context_order(system_rows, scenario_rows)
    rows_by_context = {
        context: [row for row in scenario_rows if row["analysis_context"] == context]
        for context in contexts
    }
    hypotheses = _hypothesis_index(input_dir)

    diagonal = [row for row in scenario_rows if row["cost_property"] == row["target_property"]]
    cost_contexts = {(row["analysis_context"], row["cost_property"]) for row in diagonal}
    cv_values = [_float(row, "cost_cv") for row in diagonal]
    rho_values = [_float(row, "proxy_spearman") for row in diagonal]
    ratio_values = [_float(row, "proxy_median_ratio") for row in diagonal]
    high_cv = [row for row in diagonal if _float(row, "cost_cv") >= 0.4]
    high_rho = [row for row in diagonal if _float(row, "proxy_spearman") >= 0.7]
    miscalibrated_like = [row for row in diagonal if abs(_float(row, "proxy_median_ratio") - 1.0) >= 0.05]
    scenarios_with_flips = [row for row in scenario_rows if _int(row, "rank_top1_flips") > 0]
    scenarios_changed_frontier = [row for row in scenario_rows if _float(row, "pareto_jaccard") < 0.999]

    strongest = sorted(diagonal, key=lambda row: _float(row, "cost_cv"), reverse=True)[:4]
    weakest = sorted(diagonal, key=lambda row: _float(row, "cost_cv"))[:4]
    most_stable_rank = sorted(scenario_rows, key=lambda row: _float(row, "rank_top1_agreement"), reverse=True)[:4]
    least_stable_rank = sorted(scenario_rows, key=lambda row: _float(row, "rank_top1_agreement"))[:4]
    lowest_jaccard = sorted(scenario_rows, key=lambda row: _float(row, "pareto_jaccard"))[:4]

    seed_values = sorted({_int(row, "seeds") for row in scenario_rows if _int(row, "seeds")})
    max_budget_values = sorted({row.get("budgets", "") for row in scenario_rows if row.get("budgets")})
    row_cap_values = sorted({_int(row, "row_cap") for row in scenario_rows})
    capped_contexts = sorted({row["analysis_context"] for row in scenario_rows if _int(row, "row_cap") > 0})
    max_seed = max(seed_values) if seed_values else 0
    if max_seed >= 100 and not capped_contexts:
        caveat_lines = [
            "This folder is a stronger representative pass: at least 100 stochastic seeds, no row caps, and larger budget grids on the selected systems.",
            "It is appropriate for representative paper evidence, but it is not a full 14-system Twins pass; cite the selected-system scope explicitly.",
        ]
    explain_lines: list[str] = []
    if (input_dir / "fig_explain_strategy_calibration_heatmap.png").exists():
        example_rows = []
        for context in ("brotli_1.0.7", "jump3r", "PostgreSQL_11.2"):
            folder = next((row["report"].split("/", 1)[0] for row in system_rows if row.get("analysis_context") == context and "/" in row.get("report", "")), None)
            if folder:
                example = Path(folder) / "fig_explain_cost_error_cost_performance__target_energy.png"
                if (input_dir / example).exists():
                    example_rows.append((context, str(example)))
        brotli_folder = next((row["report"].split("/", 1)[0] for row in system_rows if row.get("analysis_context") == "brotli_1.0.7" and "/" in row.get("report", "")), None)
        brotli_fixed = Path(brotli_folder) / "fig_explain_fixed_n8_cost_performance__target_energy_deployable.png" if brotli_folder else None
        brotli_path = Path(brotli_folder) / "fig_explain_strategy_budget_path_cost_performance__target_energy_deployable.png" if brotli_folder else None
        brotli_n8_text = ""
        if brotli_folder:
            brotli_rows = [
                row
                for row in _read_csv(input_dir / brotli_folder / "strategy_summary.csv")
                if row.get("cost_property") == "performance" and row.get("target_property") == "energy" and row.get("level") == "n8"
            ]
            by_strategy = {row["strategy"]: row for row in brotli_rows}
            if "pairwise" in by_strategy:
                comparison = []
                for strategy in ("random", "balanced", "pilotCost"):
                    row = by_strategy.get(strategy)
                    if row:
                        comparison.append(
                            f"`{strategy}` cost `{_fmt(100 * _float(row, 'median_pct_cost'))}%`, MRE `{_fmt(row.get('median_mre'))}`"
                        )
                pairwise = by_strategy["pairwise"]
                if comparison:
                    brotli_n8_text = (
                        f" At `n=8`, `pairwise` uses `{_fmt(100 * _float(pairwise, 'median_pct_cost'))}%` "
                        f"of the full performance cost and has median MRE `{_fmt(pairwise.get('median_mre'))}`; "
                        f"the deployable alternatives are {', '.join(comparison)}."
                    )
        explain_lines = [
            "",
            "## Explanatory Bias Figures",
            "",
            "These figures explain the mechanism behind the RQ results: heavy-tailed cost distributions, strategy calibration bias, and samples that move into costly regions without proportionally improving MRE.",
            "",
            "![Strategy calibration heatmap](fig_explain_strategy_calibration_heatmap.png)",
            "",
            "Per-system `fig_explain_cost_error_*.png` plots are the detailed run-level view: each point is one generated sample run at one budget. They are useful for seeing stochastic spread and cost-distribution overlap, but a strategy can appear many times because it is evaluated at several `n` levels and seeds.",
            "",
            "Per-system `fig_explain_strategy_budget_path_*.png` plots are the aggregated alternative: one point per strategy and budget, using median cost fraction and median MRE, with points connected to show each strategy's budget trajectory.",
            "",
            "Per-system `fig_explain_fixed_n8_*.png` plots fix the budget at `n=8`: one point per strategy, with IQR error bars over seeds for stochastic strategies and single markers for deterministic strategies. These are the clearest figures when the goal is to compare where each strategy operates under the same sample size.",
            "",
        ]
        if brotli_fixed and (input_dir / brotli_fixed).exists():
            explain_lines.extend(
                [
                    "Brotli is the cleanest caricatural example. For cost=`performance`, target=`energy`, and deployable strategies only, `pairwise` at `n=8` sits far above and to the right of the other strategies: it spends a much larger fraction of the full empirical cost while producing much worse MRE." + brotli_n8_text,
                    "",
                    f"![Brotli fixed n8 deployable]({brotli_fixed})",
                    "",
                ]
            )
        if brotli_path and (input_dir / brotli_path).exists():
            explain_lines.extend(
                [
                    "The corresponding trajectory view keeps all budget levels but aggregates runs, making it explicit that the bad `pairwise` behavior is budget-dependent rather than a plotting artifact.",
                    "",
                    f"![Brotli strategy-budget path deployable]({brotli_path})",
                    "",
                ]
            )
        for context, path in example_rows:
            explain_lines.append(f"- `{context}` example: [{path}]({path})")
        explain_lines.append("")
    else:
        caveat_lines = [
            "This folder is an exploratory broad pass. Use it to select representative systems and figures.",
            "For final claims, rerun selected systems or the whole batch with more seeds, larger budgets, and no row cap where feasible.",
        ]

    lines = [
        "# TwinsOrFalseFriends Generated-Sampling Batch",
        "",
        "## Scope",
        "",
        "This report summarizes the generated-sampling protocol over the TwinsOrFalseFriends performance/energy data.",
        "Unlike the ICPE x264 and Kaltenecker/NewRuns tiers, this dataset has no precomputed sampling traces; samples are generated from the measured configuration universe.",
        "",
        f"Systems covered: `{len(contexts)}`. Cost-target scenarios: `{len(scenario_rows)}`.",
        f"Seeds per stochastic strategy: `{', '.join(str(v) for v in seed_values) if seed_values else 'unknown'}`.",
        f"Budget grids observed: `{'; '.join(max_budget_values[:3])}{' ...' if len(max_budget_values) > 3 else ''}`.",
        f"Row-capped systems: `{', '.join(capped_contexts) if capped_contexts else 'none'}`.",
        "",
        "RQ1 and RQ2 are grouped by cost property because they only concern acquisition cost.",
        "RQ3 and RQ4 are grouped by cost-target scenario because accuracy depends on the prediction target.",
        "",
        "## RQ Answers",
        "",
        "### RQ1: Empirical Cost Heterogeneity",
        "",
        "**Answer:** empirical acquisition cost is heterogeneous across Twins systems and cost properties, but the magnitude is system-dependent.",
        f"Across {len(cost_contexts)} system-cost contexts, CV spans {_fmt(min(cv_values))}-{_fmt(max(cv_values))}; {len(high_cv)} contexts have CV >= 0.4.",
        f"Hypothesis checks: H1a is {_hypothesis_sentence(hypotheses, 'H1a')}; H1b is {_hypothesis_sentence(hypotheses, 'H1b')}.{_h1b_caveat(hypotheses)}",
        "",
        "Strongest heterogeneity examples:",
        "",
    ]
    for row in strongest:
        lines.append(
            f"- `{row['analysis_context']}` cost=`{row['cost_property']}`: "
            f"CV={_fmt(row['cost_cv'])}, p90/p10={_fmt(row['cost_p90_over_p10'])}."
        )
    lines.extend(["", "Lowest-heterogeneity contrasts:", ""])
    for row in weakest:
        lines.append(
            f"- `{row['analysis_context']}` cost=`{row['cost_property']}`: "
            f"CV={_fmt(row['cost_cv'])}, p90/p10={_fmt(row['cost_p90_over_p10'])}."
        )
    lines.extend(
        [
            "",
            "![Cost CV range by system](fig_cost_cv_range_by_system.png)",
            "",
            "### RQ2: Sample Size as a Cost Proxy",
            "",
            "**Answer:** sample size is often a useful rank proxy, but it is not sufficient as a calibrated cost model.",
            f"Spearman rho spans {_fmt(min(rho_values))}-{_fmt(max(rho_values))}; {len(high_rho)}/{len(cost_contexts)} contexts have rho >= 0.7.",
            f"Median calibration `%TrainCost/%n` spans {_fmt(min(ratio_values))}-{_fmt(max(ratio_values))}; {len(miscalibrated_like)}/{len(cost_contexts)} contexts deviate by at least 5%.",
            f"Hypothesis checks: H2a is {_hypothesis_sentence(hypotheses, 'H2a')}; H2b is {_hypothesis_sentence(hypotheses, 'H2b')}; H2c is {_hypothesis_sentence(hypotheses, 'H2c')}.",
            "",
            "Interpretation: high rho means larger samples usually cost more, but calibration and strategy bias still matter for budget claims.",
            "",
            "![Sample-size ordering by system and cost](fig_rq2_proxy_spearman_by_system_cost.png)",
            "",
            "![Median calibration by system and cost](fig_rq2_median_calibration_by_system_cost.png)",
            "",
            "### RQ3: Ranking Robustness",
            "",
            "**Answer:** replacing count cost with empirical cost frequently changes the best cost-accuracy choice.",
            f"Top-1 recommendations differ in {len(scenarios_with_flips)}/{len(scenario_rows)} scenarios.",
            f"Hypothesis checks: H3a is {_hypothesis_sentence(hypotheses, 'H3a')}; H3b is {_hypothesis_sentence(hypotheses, 'H3b')}.",
            "",
            "Least stable ranking scenarios:",
            "",
        ]
    )
    for row in least_stable_rank:
        lines.append(
            f"- `{row['analysis_context']}` {_scenario_long_label(row['cost_property'], row['target_property'])}: "
            f"top-1 agreement={_fmt(row['rank_top1_agreement'])}, flips={row['rank_top1_flips']}/7, tau={_fmt(row['rank_mean_kendall_tau'])}."
        )
    lines.extend(["", "Most stable ranking scenarios:", ""])
    for row in most_stable_rank:
        lines.append(
            f"- `{row['analysis_context']}` {_scenario_long_label(row['cost_property'], row['target_property'])}: "
            f"top-1 agreement={_fmt(row['rank_top1_agreement'])}, flips={row['rank_top1_flips']}/7."
        )
    lines.extend(
        [
            "",
            "![RQ3 top-1 agreement heatmap](fig_rq3_top1_agreement_heatmap.png)",
            "",
            "### RQ4: Pareto-Efficient Sampling",
            "",
            "**Answer:** Pareto conclusions are even more sensitive than scalar top-1 rankings.",
            f"Count-cost and empirical-cost frontiers differ in {len(scenarios_changed_frontier)}/{len(scenario_rows)} scenarios.",
            f"Hypothesis checks: H4a is {_hypothesis_sentence(hypotheses, 'H4a')}; H4b is {_hypothesis_sentence(hypotheses, 'H4b')}.",
            "",
            "Largest frontier disagreements:",
            "",
        ]
    )
    for row in lowest_jaccard:
        lines.append(
            f"- `{row['analysis_context']}` {_scenario_long_label(row['cost_property'], row['target_property'])}: "
            f"Pareto Jaccard={_fmt(row['pareto_jaccard'])}, count={row['pareto_count_n']}, empirical={row['pareto_empirical_n']}."
        )
    lines.extend(
        [
            "",
            "![RQ4 Pareto Jaccard heatmap](fig_rq4_pareto_jaccard_heatmap.png)",
            "",
            "For intuitive paper figures, use the per-system `fig_rq4_frontier_*.png` files: they show MRE against count-cost and empirical-cost frontiers on the same plane.",
            "",
            *explain_lines,
            "## System Coverage",
            "",
            "| System | Filter | Rows used | Row cap | Report |",
            "|---|---|---:|---:|---|",
        ]
    )
    for row in system_rows:
        lines.append(
            f"| `{row['system']}` | `{row.get('filter') or 'none'}` | {row.get('rows_used', '--')} | "
            f"{row.get('row_cap') or 'none'} | [{row['report']}]({row['report']}) |"
        )
    lines.extend(
        [
            "",
            "## Scenario Ranges",
            "",
            "![Decision agreement by system](fig_decision_agreement_by_system.png)",
            "",
            "| System | Cost CV range | Spearman rho range | Median ratio range | Top-1 agreement range | Pareto Jaccard range |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for context in contexts:
        rows = rows_by_context[context]
        cv_min, cv_max = _row_range(rows, "cost_cv")
        rho_min, rho_max = _row_range(rows, "proxy_spearman")
        ratio_min, ratio_max = _row_range(rows, "proxy_median_ratio")
        top_min, top_max = _row_range(rows, "rank_top1_agreement")
        jac_min, jac_max = _row_range(rows, "pareto_jaccard")
        lines.append(
            f"| `{context}` | {_fmt(cv_min)}-{_fmt(cv_max)} | {_fmt(rho_min)}-{_fmt(rho_max)} | "
            f"{_fmt(ratio_min)}-{_fmt(ratio_max)} | {_fmt(top_min)}-{_fmt(top_max)} | {_fmt(jac_min)}-{_fmt(jac_max)} |"
        )
    lines.extend(
        [
            "",
            "## Files To Use",
            "",
            f"- `scenario_summary.csv`: compact table for all {len(scenario_rows)} cost-target scenarios.",
            "- `hypothesis_tests.csv` and `hypothesis_summary.csv`: formal H1--H4 verdicts.",
            "- `twins_hypothesis_report.md`: readable hypothesis-test synthesis.",
            "- Per-system folders: detailed RQ reports and the Pareto-front figures for each scenario.",
            "",
            "## Caveat",
            "",
            *caveat_lines,
            "",
        ]
    )
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir)
    system_rows = _read_csv(input_dir / "system_summary.csv")
    scenario_rows = _coerce_scenarios(_read_csv(input_dir / "scenario_summary.csv"))
    if not scenario_rows:
        raise SystemExit(f"No scenario rows found in {input_dir / 'scenario_summary.csv'}")
    _plot_all(input_dir, system_rows, scenario_rows)
    output = Path(args.output) if args.output else input_dir / "twins_generated_batch_report.md"
    _write_report(output, input_dir=input_dir, system_rows=system_rows, scenario_rows=scenario_rows)
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
