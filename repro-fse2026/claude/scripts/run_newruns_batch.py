#!/usr/bin/env python3
"""Run the NewRuns non-x264 systems and build a comparative report."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path
import statistics
import sys
from typing import Any
import zipfile

import numpy as np


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
    strategy_sort_key,
    strategy_summary,
    write_csv,
)
from cost_sampling.archive_runs import load_runs_dataset, load_summary_configuration_count
from cost_sampling.metrics import LEARNER_CHOICES
from cost_sampling.hypotheses import (
    aggregate_verdicts,
    evaluate_per_context_hypotheses,
    test_h3b_flip_correlation,
)
from cost_sampling.plots import (
    PALETTE,
    plot_accuracy_cost,
    plot_aggregate_rank_agreement,
    plot_calibration,
    plot_cost_distribution,
    plot_pareto_frontier_comparison,
    plot_strategy_cost_bias,
)
import matplotlib.pyplot as plt

from run_system_report import (
    DEFAULT_LAMBDAS,
    SCENARIO,
    add_scenario,
    build_context_row,
    median_by_strategy,
    write_report as write_system_report,
)


DEFAULT_CONTEXTS = ["7z", "BerkeleyDBC", "Dune", "Hipacc", "LLVM", "Polly", "lrzip"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-zip", default="ICPE-rawdata/NewRuns.zip", help="Path to NewRuns.zip.")
    parser.add_argument("--summary-zip", default="ICPE-rawdata/AllSummary.zip", help="Path to AllSummary.zip.")
    parser.add_argument("--output-dir", default="artifacts/newruns_systems", help="Output directory.")
    parser.add_argument(
        "--contexts",
        default=",".join(DEFAULT_CONTEXTS),
        help="Comma-separated NewRuns contexts. Defaults to non-x264 systems with sampled CSVs.",
    )
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


def parse_contexts(raw: str) -> list[str]:
    return [part.strip() for part in raw.split(",") if part.strip()]


def sampled_csv_counts(runs_zip: str) -> Counter[str]:
    with zipfile.ZipFile(runs_zip) as archive:
        return Counter(
            member.split("/")[1]
            for member in archive.namelist()
            if member.endswith(".csv") and member.startswith("NewRuns/") and len(member.split("/")) > 2
        )


def analyze_system(
    *,
    context: str,
    runs_zip: str,
    summary_zip: str,
    max_runs: int,
    alpha: float,
    learner: str,
    log_target: bool,
    performance_name: str,
) -> dict[str, Any]:
    dataset = load_runs_dataset(
        runs_zip,
        context,
        max_runs=max_runs,
        performance_name=performance_name,
    )
    expected_n = load_summary_configuration_count(summary_zip, context)
    records = add_scenario(evaluate_samples(dataset, alpha=alpha, log_target=log_target, learner=learner), context)
    heterogeneity = add_scenario(cost_heterogeneity_summary(dataset), context)
    summary = add_scenario(strategy_summary(records), context)
    proxy = add_scenario(proxy_summary(records), context)
    ranks = add_scenario(rank_stability(summary, DEFAULT_LAMBDAS), context)
    pareto = add_scenario(pareto_summary(summary), context)
    context_row = build_context_row(
        context=context,
        expected_n=expected_n,
        heterogeneity=heterogeneity,
        proxy=proxy,
        summary=summary,
        ranks=ranks,
        pareto=pareto,
    )
    context_row["records"] = len(records)
    context_row["strategies"] = ", ".join(sorted({row["strategy"] for row in records}, key=strategy_sort_key))
    context_row["levels"] = ", ".join(sorted({row["level"] for row in records}))
    hypothesis_rows = evaluate_per_context_hypotheses(
        scope_value=context,
        records=records,
        heterogeneity=heterogeneity,
        rank_rows=ranks,
        pareto_rows=pareto,
        cost_values=dataset.cost_values,
    )
    for row in hypothesis_rows:
        row["system"] = context
        row["cost_property"] = "performance"
        row["target_property"] = "performance"
        row["scenario"] = SCENARIO
    return {
        "records": records,
        "heterogeneity": heterogeneity,
        "summary": summary,
        "proxy": proxy,
        "ranks": ranks,
        "pareto": pareto,
        "context_row": context_row,
        "hypotheses": hypothesis_rows,
    }


def write_system_outputs(output_dir: Path, context: str, result: dict[str, Any]) -> None:
    system_dir = output_dir / context
    system_dir.mkdir(parents=True, exist_ok=True)

    write_csv(system_dir / "records.csv", result["records"])
    write_csv(system_dir / "rq1_cost_heterogeneity.csv", result["heterogeneity"])
    write_csv(system_dir / "strategy_summary.csv", result["summary"])
    write_csv(system_dir / "rq2_proxy_summary.csv", result["proxy"])
    write_csv(system_dir / "rq3_rank_stability.csv", result["ranks"])
    write_csv(system_dir / "rq4_pareto.csv", result["pareto"])
    write_csv(system_dir / "context_summary.csv", [result["context_row"]])
    write_csv(system_dir / "hypothesis_tests.csv", result["hypotheses"])

    plot_cost_distribution(result["records"], system_dir / "fig_rq1_cost_distribution.png")
    plot_strategy_cost_bias(result["summary"], system_dir / "fig_rq1_strategy_cost_bias.png")
    plot_calibration(result["records"], system_dir / "fig_rq2_size_cost_calibration.png")
    plot_aggregate_rank_agreement(
        result["ranks"],
        system_dir / "fig_rq3_rank_stability.png",
        context_label=context,
    )
    plot_accuracy_cost(result["pareto"], system_dir / "fig_rq4_accuracy_cost_frontier.png")
    plot_pareto_frontier_comparison(
        result["summary"],
        system_dir / "fig_rq4_frontier_count_vs_empirical.png",
        scenario=SCENARIO,
        scenario_label=f"{context}: cost=performance, target=performance",
    )
    write_system_report(
        system_dir / f"{context}_performance_report.md",
        context=context,
        context_row=result["context_row"],
        proxy_rows=result["proxy"],
        strategy_rows=result["summary"],
        rank_rows=result["ranks"],
    )


def plot_cost_heterogeneity_by_system(context_rows: list[dict[str, Any]], output: Path) -> None:
    rows = sorted(context_rows, key=lambda row: row["system"])
    systems = [row["system"] for row in rows]
    x = np.arange(len(rows))
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.4))
    axes[0].bar(x, [row["cost_cv"] for row in rows], color="#4C78A8")
    axes[0].set_ylabel("Per-configuration cost CV")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(systems, rotation=30, ha="right")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.8)
    axes[0].set_axisbelow(True)

    axes[1].bar(x, [row["cost_p90_over_p10"] for row in rows], color="#F58518")
    axes[1].set_yscale("log")
    axes[1].set_ylabel("p90 / p10 cost ratio (log scale)")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(systems, rotation=30, ha="right")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.8)
    axes[1].set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def plot_calibration_by_system(context_rows: list[dict[str, Any]], output: Path) -> None:
    rows = sorted(context_rows, key=lambda row: row["system"])
    systems = [row["system"] for row in rows]
    x = np.arange(len(rows))
    med = np.array([row["proxy_median_ratio"] for row in rows], dtype=float)
    q1 = np.array([row["proxy_q1_ratio"] for row in rows], dtype=float)
    q3 = np.array([row["proxy_q3_ratio"] for row in rows], dtype=float)
    yerr = np.vstack([med - q1, q3 - med])
    fig, ax = plt.subplots(figsize=(9.0, 4.6))
    ax.errorbar(x, med, yerr=yerr, fmt="o", color="#4C78A8", ecolor="#4C78A8", capsize=4)
    ax.axhline(1.0, color="#222222", linestyle="--", linewidth=1.1)
    ax.set_ylabel("Calibration ratio (%cost / %n)")
    ax.set_xticks(x)
    ax.set_xticklabels(systems, rotation=30, ha="right")
    ax.grid(axis="y", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def plot_decision_change_by_system(context_rows: list[dict[str, Any]], output: Path) -> None:
    rows = sorted(context_rows, key=lambda row: row["system"])
    systems = [row["system"] for row in rows]
    x = np.arange(len(rows))
    width = 0.36
    rank_agreement = [1.0 - row["rank_top1_flips"] / len(DEFAULT_LAMBDAS) for row in rows]
    pareto_jaccard = [row["pareto_jaccard"] for row in rows]
    fig, ax = plt.subplots(figsize=(9.4, 4.6))
    ax.bar(x - width / 2, rank_agreement, width, label="Top-1 rank agreement", color="#4C78A8")
    ax.bar(x + width / 2, pareto_jaccard, width, label="Pareto Jaccard", color="#F58518")
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Agreement under count vs measured cost")
    ax.set_xticks(x)
    ax.set_xticklabels(systems, rotation=30, ha="right")
    ax.grid(axis="y", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def plot_strategy_bias_heatmap(strategy_rows: list[dict[str, Any]], output: Path) -> None:
    systems = sorted({row["system"] for row in strategy_rows})
    strategies = sorted({row["strategy"] for row in strategy_rows}, key=strategy_sort_key)
    values = np.full((len(systems), len(strategies)), np.nan)
    grouped: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in strategy_rows:
        value = float(row["cost_over_random"])
        if np.isfinite(value) and value > 0:
            grouped[(row["system"], row["strategy"])].append(value)
    for i, system in enumerate(systems):
        for j, strategy in enumerate(strategies):
            vals = grouped.get((system, strategy), [])
            if vals:
                values[i, j] = _median(vals)

    log_values = np.log2(values)
    finite = log_values[np.isfinite(log_values)]
    vmax = max(0.25, float(np.nanmax(np.abs(finite)))) if finite.size else 1.0
    fig, ax = plt.subplots(figsize=(8.4, 5.0))
    image = ax.imshow(log_values, cmap="RdBu_r", vmin=-vmax, vmax=vmax, aspect="auto")
    ax.set_xticks(np.arange(len(strategies)))
    ax.set_xticklabels(strategies, rotation=30, ha="right")
    ax.set_yticks(np.arange(len(systems)))
    ax.set_yticklabels(systems)
    for i in range(len(systems)):
        for j in range(len(strategies)):
            if np.isfinite(values[i, j]):
                color = "white" if abs(log_values[i, j]) > 0.6 * vmax else "#111111"
                ax.text(j, i, _fmt(float(values[i, j])), ha="center", va="center", fontsize=8, color=color)
            else:
                ax.text(j, i, "-", ha="center", va="center", fontsize=8, color="#555555")
    cbar = fig.colorbar(image, ax=ax)
    cbar.set_label("log2(cost / random)")
    ax.set_title("Median strategy cost relative to random")
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def _frontier_count(row: dict[str, Any], column: str) -> int:
    return len([part for part in str(row[column]).split(",") if part.strip()])


def write_batch_report(
    output: Path,
    *,
    context_rows: list[dict[str, Any]],
    strategy_rows: list[dict[str, Any]],
    skipped: dict[str, str],
) -> None:
    rows = sorted(context_rows, key=lambda row: row["system"])
    cvs = [row["cost_cv"] for row in rows]
    p90p10 = [row["cost_p90_over_p10"] for row in rows]
    ratios = [row["proxy_median_ratio"] for row in rows]
    jaccards = [row["pareto_jaccard"] for row in rows]
    top1_flips = [row["rank_top1_flips"] for row in rows]
    tau = [row["rank_mean_kendall_tau"] for row in rows]

    strongest_bias: list[tuple[str, str, float]] = []
    for system in {row["system"] for row in strategy_rows}:
        system_rows = [row for row in strategy_rows if row["system"] == system]
        non_random = [
            (f"{row['strategy']}_{row['level']}", float(row["cost_over_random"]))
            for row in system_rows
            if row["strategy"] != "random" and np.isfinite(float(row["cost_over_random"]))
        ]
        if non_random:
            label, value = max(non_random, key=lambda item: abs(np.log2(item[1])) if item[1] > 0 else 0)
            strongest_bias.append((system, label, value))
    bias_by_system = {system: (label, value) for system, label, value in strongest_bias}

    lines = [
        "# NewRuns cross-system sampling-cost report",
        "",
        "## Scope",
        "",
        "This report systematizes the non-x264 `NewRuns.zip` systems that expose sampled configuration "
        "CSVs with a `Performance` column. Each system has one measured property, so every analysis is "
        "the diagonal scenario `cost=performance, target=performance`.",
        "",
        "The cost model is the same as in the x264 infrastructure: measured training cost is the sum of "
        "`Performance` over the configurations selected by a sampling run. The prediction target is also "
        "`Performance`, because these systems do not expose a separate size property in the sampled CSVs.",
        "",
        f"Included systems: {', '.join(row['system'] for row in rows)}.",
        "",
    ]
    if skipped:
        lines.extend(
            [
                "Skipped contexts:",
                "",
            ]
        )
        lines.extend([f"- `{context}`: {reason}" for context, reason in sorted(skipped.items())])
        lines.append("")

    lines.extend(
        [
            "## Overall conclusion",
            "",
            "The conclusion is stronger than for x264. On these NewRuns systems, measured cost is often "
            "highly heterogeneous and strategy-dependent. Sample size remains a useful coarse axis, but it "
            "is not a calibrated cost model and it can change decision-level conclusions.",
            "",
            f"Across {len(rows)} systems, cost CV ranges from {_fmt(min(cvs))} to {_fmt(max(cvs))} "
            f"(median {_fmt(_median(cvs))}), and p90/p10 cost ratio ranges from {_fmt(min(p90p10))} "
            f"to {_fmt(max(p90p10))} (median {_fmt(_median(p90p10))}). Median `%cost/%n` ranges from "
            f"{_fmt(min(ratios))} to {_fmt(max(ratios))}. Pareto Jaccard ranges from "
            f"{_fmt(min(jaccards))} to {_fmt(max(jaccards))}.",
            "",
            "## RQ1: Measured cost heterogeneity",
            "",
            "![Cost heterogeneity by system](fig_rq1_cost_heterogeneity_by_system.png)",
            "",
            "![Strategy cost bias heatmap](fig_rq1_strategy_bias_heatmap.png)",
            "",
            "| System | Reconstructed / expected configs | Cost CV | p90/p10 | Cost-over-random range | Strongest strategy-level bias |",
            "|---|---:|---:|---:|---:|---|",
        ]
    )
    for row in rows:
        expected = row["expected_configurations"]
        coverage = f"{row['reconstructed_configurations']} / {expected}" if expected is not None else str(row["reconstructed_configurations"])
        bias = bias_by_system.get(row["system"])
        bias_text = f"`{bias[0]}` = {_fmt(bias[1])}" if bias else "-"
        lines.append(
            f"| `{row['system']}` | {coverage} | {_fmt(row['cost_cv'])} | "
            f"{_fmt(row['cost_p90_over_p10'])} | {_fmt(row['cost_over_random_min'])}-"
            f"{_fmt(row['cost_over_random_max'])} | {bias_text} |"
        )

    lines.extend(
        [
            "",
            "Interpretation: the equal-cost assumption is weak for this batch. The issue is not only "
            "that configurations vary in cost; sampling strategies repeatedly select systematically "
            "cheaper or costlier regions at the same sample size.",
            "",
            "## RQ2: Sample size as cost proxy",
            "",
            "![Calibration by system](fig_rq2_calibration_by_system.png)",
            "",
            "| System | Spearman rho | Median %cost/%n | IQR %cost/%n |",
            "|---|---:|---:|---:|",
        ]
    )
    for row in rows:
        lines.append(
            f"| `{row['system']}` | {_fmt(row['proxy_spearman'])} | "
            f"{_fmt(row['proxy_median_ratio'])} | "
            f"{_fmt(row['proxy_q1_ratio'])}-{_fmt(row['proxy_q3_ratio'])} |"
        )

    lines.extend(
        [
            "",
            "Interpretation: high correlation does not imply calibration. Several systems have median "
            "ratios far from one or wide IQRs, so a count budget can overstate or understate measured "
            "measurement cost depending on the strategy.",
            "",
            "## RQ3: Ranking robustness",
            "",
            "![Decision agreement by system](fig_rq3_rq4_decision_change_by_system.png)",
            "",
            "| System | Top-1 flips / 7 cost weights | Mean Kendall tau | Mean top-3 overlap |",
            "|---|---:|---:|---:|",
        ]
    )
    for row in rows:
        lines.append(
            f"| `{row['system']}` | {row['rank_top1_flips']} / {len(DEFAULT_LAMBDAS)} | "
            f"{_fmt(row['rank_mean_kendall_tau'])} | {_fmt(row['rank_mean_top3_overlap'])} |"
        )

    lines.extend(
        [
            "",
            "Interpretation: replacing count by measured cost can change the cost-sensitive ranking. "
            "The effect varies by system, which is exactly why systematizing beyond x264 matters.",
            "",
            "## RQ4: Pareto-efficient sampling",
            "",
            "| System | Jaccard | Count frontier size | Measured frontier size | Best measured-cost simple pair |",
            "|---|---:|---:|---:|---|",
        ]
    )
    for row in rows:
        lines.append(
            f"| `{row['system']}` | {_fmt(row['pareto_jaccard'])} | "
            f"{_frontier_count(row, 'pareto_count_pairs')} | "
            f"{_frontier_count(row, 'pareto_empirical_pairs')} | "
            f"`{row['best_simple_pair']}` |"
        )

    lines.extend(
        [
            "",
            "Interpretation: the Pareto front is a compact decision-level witness. When Jaccard is below "
            "one, the measured-cost view is not just a rescaled count-cost view; it changes which "
            "sampling choices are non-dominated.",
            "",
            "## Per-system reports",
            "",
        ]
    )
    for row in rows:
        system = row["system"]
        lines.append(f"- [`{system}` report]({system}/{system}_performance_report.md)")

    lines.extend(
        [
            "",
            "## Paper-level takeaway",
            "",
            "The NewRuns systems provide stronger evidence for the paper's main claim than x264 alone. "
            "x264 showed that sample size can be a strong but incomplete proxy. NewRuns shows that the "
            "incompleteness can be large enough to affect calibration, rankings, and Pareto-efficient "
            "recommendations across multiple configurable systems.",
            "",
        ]
    )
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    requested_contexts = parse_contexts(args.contexts)
    csv_counts = sampled_csv_counts(args.runs_zip)

    all_records: list[dict[str, Any]] = []
    all_heterogeneity: list[dict[str, Any]] = []
    all_strategy: list[dict[str, Any]] = []
    all_proxy: list[dict[str, Any]] = []
    all_ranks: list[dict[str, Any]] = []
    all_pareto: list[dict[str, Any]] = []
    all_hypotheses: list[dict[str, Any]] = []
    context_rows: list[dict[str, Any]] = []
    skipped: dict[str, str] = {}

    for context in requested_contexts:
        if csv_counts.get(context, 0) == 0:
            skipped[context] = "no sampled configuration CSVs in NewRuns.zip"
            continue
        print(f"Analyzing {context} ({csv_counts[context]} sampled CSVs)")
        try:
            result = analyze_system(
                context=context,
                runs_zip=args.runs_zip,
                summary_zip=args.summary_zip,
                max_runs=args.max_runs,
                alpha=args.alpha,
                learner=args.learner,
                log_target=not args.no_log_target,
                performance_name=args.performance_name,
            )
        except Exception as exc:  # noqa: BLE001 - batch report should keep useful partial output.
            skipped[context] = str(exc)
            print(f"  skipped: {exc}")
            continue
        result["context_row"]["sampled_csvs"] = csv_counts[context]
        write_system_outputs(output_dir, context, result)
        all_records.extend(result["records"])
        all_heterogeneity.extend(result["heterogeneity"])
        all_strategy.extend(result["summary"])
        all_proxy.extend(result["proxy"])
        all_ranks.extend(result["ranks"])
        all_pareto.extend(result["pareto"])
        all_hypotheses.extend(result["hypotheses"])
        context_rows.append(result["context_row"])

    write_csv(output_dir / "records.csv", all_records)
    write_csv(output_dir / "rq1_cost_heterogeneity.csv", all_heterogeneity)
    write_csv(output_dir / "strategy_summary.csv", all_strategy)
    write_csv(output_dir / "rq2_proxy_summary.csv", all_proxy)
    write_csv(output_dir / "rq3_rank_stability.csv", all_ranks)
    write_csv(output_dir / "rq4_pareto.csv", all_pareto)
    write_csv(output_dir / "system_summary.csv", context_rows)
    write_csv(
        output_dir / "skipped_contexts.csv",
        [{"context": context, "reason": reason} for context, reason in sorted(skipped.items())],
    )

    if context_rows:
        h3b = test_h3b_flip_correlation(context_rows)
        h3b["system"] = "ALL"
        h3b["cost_property"] = "performance"
        h3b["target_property"] = "performance"
        h3b["scenario"] = "global"
        all_hypotheses.append(h3b)
    write_csv(output_dir / "hypothesis_tests.csv", all_hypotheses)
    write_csv(output_dir / "hypothesis_summary.csv", aggregate_verdicts(all_hypotheses))

    if context_rows:
        plot_cost_heterogeneity_by_system(context_rows, output_dir / "fig_rq1_cost_heterogeneity_by_system.png")
        plot_strategy_bias_heatmap(all_strategy, output_dir / "fig_rq1_strategy_bias_heatmap.png")
        plot_calibration_by_system(context_rows, output_dir / "fig_rq2_calibration_by_system.png")
        plot_decision_change_by_system(context_rows, output_dir / "fig_rq3_rq4_decision_change_by_system.png")
        write_batch_report(
            output_dir / "newruns_systems_report.md",
            context_rows=context_rows,
            strategy_rows=all_strategy,
            skipped=skipped,
        )
    print(f"Done. Outputs: {output_dir}")


if __name__ == "__main__":
    main()
