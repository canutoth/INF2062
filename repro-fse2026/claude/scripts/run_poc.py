#!/usr/bin/env python3
"""Run the x264 empirical sampling-cost proof of concept."""

from __future__ import annotations

import argparse
from pathlib import Path
import statistics
import sys


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
    plot_accuracy_cost,
    plot_calibration,
    plot_cost_distribution,
    plot_rank_stability,
)


DEFAULT_LAMBDAS = [0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 10.0]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--context", default="x264_time_0", help="AllRuns/AllSummary context to analyze.")
    parser.add_argument(
        "--cost-context",
        default=None,
        help="Optional context that provides empirical acquisition cost. "
        "Defaults to the target context, except x264_size_i infers x264_time_i.",
    )
    parser.add_argument("--runs-zip", default="ICPE-rawdata/AllRuns.zip", help="Path to AllRuns.zip.")
    parser.add_argument("--summary-zip", default="ICPE-rawdata/AllSummary.zip", help="Path to AllSummary.zip.")
    parser.add_argument("--output-dir", default=None, help="Output directory; defaults to artifacts/poc_<context>.")
    parser.add_argument("--max-runs", type=int, default=100, help="Maximum run id to load.")
    parser.add_argument("--alpha", type=float, default=1.0, help="Ridge regularization strength.")
    parser.add_argument("--learner", default="ridge-log", choices=LEARNER_CHOICES)
    parser.add_argument("--no-log-target", action="store_true", help="Fit the learner on the raw target instead of log(target).")
    return parser.parse_args()


def infer_cost_context(context: str, explicit_cost_context: str | None) -> str | None:
    if explicit_cost_context:
        return explicit_cost_context
    if context.startswith("x264_size_"):
        return context.replace("x264_size_", "x264_time_", 1)
    return None


def _fmt(value: float) -> str:
    return f"{value:.4g}"


def write_markdown_summary(
    output: Path,
    *,
    context: str,
    cost_context: str,
    expected_n: int | None,
    heterogeneity: list[dict],
    proxy: list[dict],
    summary: list[dict],
    ranks: list[dict],
    pareto: list[dict],
) -> None:
    h = heterogeneity[0]
    overall_proxy = next(row for row in proxy if row["strategy"] == "ALL")
    empirical_frontier = [f"{row['strategy']}_{row['level']}" for row in pareto if row["pareto_empirical"]]
    count_frontier = [f"{row['strategy']}_{row['level']}" for row in pareto if row["pareto_count"]]
    rank_flips = [row for row in ranks if row["top1_agreement"] == 0]
    best_time = min(summary, key=lambda row: row["median_mre"] + row["median_pct_cost"])

    lines = [
        f"# Proof of concept: {context}",
        "",
        "## Data",
        "",
        f"- Prediction target context: `{context}`",
        f"- Empirical acquisition-cost context: `{cost_context}`",
        f"- Reconstructed configurations: {h['n_configurations']}"
        + (f" / {expected_n} listed in AllSummary" if expected_n is not None else ""),
        f"- Full empirical cost: {_fmt(h['full_cost'])}",
        f"- Per-configuration cost CV: {_fmt(h['cv_cost'])}",
        f"- p90/p10 per-configuration cost ratio: {_fmt(h['p90_over_p10'])}",
        "",
        "## RQ snapshots",
        "",
        f"- RQ1: median fixed-size overhead vs random ranges from "
        f"{_fmt(min(row['cost_over_random'] for row in summary))} to "
        f"{_fmt(max(row['cost_over_random'] for row in summary))}.",
        f"- RQ2: Spearman rho(n, TrainCost) = {_fmt(overall_proxy['spearman_n_train_cost'])}; "
        f"median calibration ratio = {_fmt(overall_proxy['median_calibration_ratio'])}.",
        f"- RQ3: top-1 strategy-size pair changes for {len(rank_flips)} / {len(ranks)} lambda values.",
        f"- RQ4: empirical frontier = {', '.join(empirical_frontier)}.",
        f"- Count frontier = {', '.join(count_frontier)}.",
        "",
        "## Useful first read",
        "",
        f"The lowest simple combined median MRE + empirical-cost point is "
        f"{best_time['strategy']}_{best_time['level']} "
        f"(MRE={_fmt(best_time['median_mre'])}, cost={_fmt(100 * best_time['median_pct_cost'])}% of full cost).",
        "",
        "Generated files in this directory contain the raw records, strategy summaries, "
        "rank stability sweep, Pareto labels, and figures.",
        "",
    ]
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    cost_context = infer_cost_context(args.context, args.cost_context)
    output_name = f"poc_{args.context}" if cost_context in (None, args.context) else f"poc_{args.context}_cost_{cost_context}"
    output_dir = Path(args.output_dir or f"artifacts/{output_name}")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading {args.context} from {args.runs_zip}")
    dataset = load_runs_dataset(args.runs_zip, args.context, max_runs=args.max_runs)
    if cost_context is not None and cost_context != args.context:
        print(f"Loading acquisition costs from {cost_context}")
        cost_dataset = load_runs_dataset(args.runs_zip, cost_context, max_runs=args.max_runs)
        dataset = attach_cost_dataset(dataset, cost_dataset)
    expected_n = load_summary_configuration_count(args.summary_zip, args.context)
    if expected_n is not None and expected_n != len(dataset.y):
        print(f"warning: reconstructed {len(dataset.y)} configs, summary lists {expected_n}")

    run_ids = sorted({sample.ref.run_id for sample in dataset.samples})
    strategies = sorted({sample.ref.strategy for sample in dataset.samples})
    levels = sorted({sample.ref.level for sample in dataset.samples})
    print(
        f"Loaded {len(dataset.samples)} samples over {len(run_ids)} runs, "
        f"{len(strategies)} strategies, {len(levels)} levels, {len(dataset.y)} configurations."
    )

    print(f"Evaluating samples with learner={args.learner}")
    records = evaluate_samples(dataset, alpha=args.alpha, log_target=not args.no_log_target, learner=args.learner)
    heterogeneity = cost_heterogeneity_summary(dataset)
    summary = strategy_summary(records)
    proxy = proxy_summary(records)
    ranks = rank_stability(summary, DEFAULT_LAMBDAS)
    pareto = pareto_summary(summary)

    write_csv(output_dir / "records.csv", records)
    write_csv(output_dir / "rq1_cost_heterogeneity.csv", heterogeneity)
    write_csv(output_dir / "strategy_summary.csv", summary)
    write_csv(output_dir / "rq2_proxy_summary.csv", proxy)
    write_csv(output_dir / "rq3_rank_stability.csv", ranks)
    write_csv(output_dir / "rq4_pareto.csv", pareto)

    print("Writing figures")
    plot_cost_distribution(records, output_dir / "fig_rq1_cost_distribution.png")
    plot_calibration(records, output_dir / "fig_rq2_size_cost_calibration.png")
    plot_accuracy_cost(pareto, output_dir / "fig_rq4_accuracy_cost_frontier.png")
    plot_rank_stability(ranks, output_dir / "fig_rq3_rank_stability.png")

    write_markdown_summary(
        output_dir / "summary.md",
        context=args.context,
        cost_context=dataset.effective_cost_context,
        expected_n=expected_n,
        heterogeneity=heterogeneity,
        proxy=proxy,
        summary=summary,
        ranks=ranks,
        pareto=pareto,
    )

    medians = [row["median_calibration_ratio"] for row in summary]
    print(f"Done. Outputs: {output_dir}")
    print(
        "Calibration ratio by strategy-size pair: "
        f"median={statistics.median(medians):.3f}, min={min(medians):.3f}, max={max(medians):.3f}"
    )


if __name__ == "__main__":
    main()
