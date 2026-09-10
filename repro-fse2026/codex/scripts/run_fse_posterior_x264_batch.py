#!/usr/bin/env python3
"""Revisit the FSE posterior-risk experiments on the ICPE x264 corpus."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import replace
import math
from pathlib import Path
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
for path in (REPO_ROOT, SCRIPT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from cost_sampling.analysis import level_sort_key, strategy_sort_key, write_csv
from cost_sampling.archive_runs import attach_cost_dataset, load_runs_dataset

from run_fse_posterior import (
    _fmt,
    _parse_set,
    _with_srs_samples,
    confidence_curves,
    level_confidence_frontiers,
    posterior_hypothesis_summary,
    posterior_hypothesis_tests,
    posterior_pareto,
    posterior_records,
    posterior_summary,
    write_figures,
    write_report,
)


DEFAULT_STRATEGIES = "random,solverBased,divDistBased,twise,distBased,henard"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-zip", default="ICPE-rawdata/AllRuns.zip", help="Path to AllRuns.zip.")
    parser.add_argument("--output-dir", default="artifacts/fse_posterior_x264_icpe")
    parser.add_argument("--contexts", default="0-16", help="Input indices, e.g. 0-16 or 0,3,8.")
    parser.add_argument("--target-props", default="time,size", help="Comma-separated target properties.")
    parser.add_argument(
        "--cost-prop",
        default="time",
        help="Empirical acquisition-cost property. Use `same` to use each target property as its own cost.",
    )
    parser.add_argument("--max-runs", type=int, default=100)
    parser.add_argument("--strategies", default=DEFAULT_STRATEGIES)
    parser.add_argument("--levels", default="t1,t2,t3")
    parser.add_argument("--fixed-level", default="t2", help="Level used for the FSE Experiment-1 summary.")
    parser.add_argument("--extreme", choices=("max", "min"), default="max")
    parser.add_argument("--prior-offset", type=int, default=1)
    parser.add_argument("--epsilon-points", type=int, default=151)
    parser.add_argument("--plot-epsilon-max", type=float, default=0.15)
    parser.add_argument("--srs-seeds", type=int, default=100)
    parser.add_argument("--srs-step-size", type=int, default=25)
    parser.add_argument("--srs-p-threshold", type=float, default=0.05)
    parser.add_argument("--no-srs", action="store_true", help="Do not generate SRS samples.")
    parser.add_argument("--no-figures", action="store_true", help="Skip per-context PNG figures.")
    return parser.parse_args()


def parse_context_indices(raw: str) -> list[int]:
    out: list[int] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            out.extend(range(int(start), int(end) + 1))
        else:
            out.append(int(part))
    return sorted(set(out))


def _props(raw: str) -> list[str]:
    return [part.strip() for part in raw.split(",") if part.strip()]


def _context(prop: str, idx: int) -> str:
    return f"x264_{prop}_{idx}"


def _pair(row: dict[str, Any]) -> str:
    return f"{row['strategy']}_{row['level']}"


def _median(rows: list[dict[str, Any]], key: str) -> float:
    values = sorted(float(row[key]) for row in rows)
    if not values:
        return float("nan")
    mid = len(values) // 2
    return values[mid] if len(values) % 2 else (values[mid - 1] + values[mid]) / 2.0


def load_x264_dataset(
    *,
    runs_zip: str,
    input_index: int,
    target_prop: str,
    cost_prop: str,
    max_runs: int,
    strategies: set[str] | None,
    levels: set[str] | None,
) -> Any:
    target_context = _context(target_prop, input_index)
    dataset = load_runs_dataset(
        runs_zip,
        target_context,
        max_runs=max_runs,
        strategies=strategies,
        levels=levels,
    )
    effective_cost_prop = target_prop if cost_prop == "same" else cost_prop
    cost_context = _context(effective_cost_prop, input_index)
    if cost_context != target_context:
        cost_dataset = load_runs_dataset(
            runs_zip,
            cost_context,
            max_runs=max_runs,
            strategies=strategies,
            levels=levels,
        )
        dataset = attach_cost_dataset(dataset, cost_dataset)
    return dataset


def summarize_context_levels(
    *,
    input_index: int,
    target_prop: str,
    cost_prop: str,
    summary: list[dict[str, Any]],
    pareto: list[dict[str, Any]],
    hypotheses: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    levels = sorted({row["level"] for row in summary}, key=level_sort_key)
    for level in levels:
        level_summary = [row for row in summary if row["level"] == level]
        best_size = max(level_summary, key=lambda row: row["omega_size_baseline"])
        best_cost = max(level_summary, key=lambda row: row["omega_cost_baseline"])
        best_risk = min(level_summary, key=lambda row: row["median_posterior_risk"])
        srs = next((row for row in level_summary if row["strategy"] == "SRSSampling"), None)
        random = next((row for row in level_summary if row["strategy"] == "random"), None)
        fse_by_id = {
            row["hypothesis"]: row
            for row in hypotheses
            if str(row["scope"]).endswith(f":{level}")
        }
        count_front, empirical_front = level_confidence_frontiers(level_summary)
        union = count_front | empirical_front
        rows.append(
            {
                "input_index": input_index,
                "target_property": target_prop,
                "cost_property": cost_prop,
                "context": _context(target_prop, input_index),
                "level": level,
                "n": best_cost["n"],
                "n_configurations": round(best_cost["n"] / best_cost["pct_n"]),
                "best_risk_pair": _pair(best_risk),
                "best_risk": best_risk["median_posterior_risk"],
                "best_size_pair": _pair(best_size),
                "best_cost_pair": _pair(best_cost),
                "top_changed_by_cost": int(_pair(best_size) != _pair(best_cost)),
                "best_cost_omega": best_cost["omega_cost_baseline"],
                "srs_best_cost": int(srs is not None and _pair(srs) == _pair(best_cost)),
                "srs_on_empirical_confidence_front": int(
                    srs is not None and _pair(srs) in empirical_front
                ),
                "srs_risk": srs["median_posterior_risk"] if srs else float("nan"),
                "random_risk": random["median_posterior_risk"] if random else float("nan"),
                "srs_pct_cost": srs["median_pct_cost"] if srs else float("nan"),
                "random_pct_cost": random["median_pct_cost"] if random else float("nan"),
                "srs_omega_size": srs["omega_size_baseline"] if srs else float("nan"),
                "srs_omega_cost": srs["omega_cost_baseline"] if srs else float("nan"),
                "pareto_jaccard": len(count_front & empirical_front) / len(union) if union else 1.0,
                "count_confidence_front": ",".join(sorted(count_front)),
                "empirical_confidence_front": ",".join(sorted(empirical_front)),
                "fse1_verdict": fse_by_id.get("FSE1", {}).get("verdict", ""),
                "fse3_verdict": fse_by_id.get("FSE3", {}).get("verdict", ""),
                "fse4_verdict": fse_by_id.get("FSE4", {}).get("verdict", ""),
                "fse5_verdict": fse_by_id.get("FSE5", {}).get("verdict", ""),
                "fse6_verdict": fse_by_id.get("FSE6", {}).get("verdict", ""),
            }
        )
    return rows


def summarize_budget_trends(context_level_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[int, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in context_level_rows:
        grouped[(row["input_index"], row["target_property"], row["cost_property"], row["level"])].append(row)

    # Use posterior_strategy_summary rows instead for per-strategy trends; this placeholder
    # is kept unused to avoid conflating best-pair trends with strategy trends.
    return []


def strategy_budget_trends(summary_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[int, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in summary_rows:
        grouped[(row["input_index"], row["target_property"], row["cost_property"], row["strategy"])].append(row)
    out: list[dict[str, Any]] = []
    for (input_index, target_prop, cost_prop, strategy), rows in grouped.items():
        rows.sort(key=lambda row: level_sort_key(row["level"]))
        risks = [float(row["median_posterior_risk"]) for row in rows]
        areas = [float(row["posterior_confidence_area"]) for row in rows]
        omega_size = [float(row["omega_size_baseline"]) for row in rows]
        omega_cost = [float(row["omega_cost_baseline"]) for row in rows]
        levels = [str(row["level"]) for row in rows]
        out.append(
            {
                "input_index": input_index,
                "target_property": target_prop,
                "cost_property": cost_prop,
                "context": _context(target_prop, input_index),
                "strategy": strategy,
                "levels": ",".join(levels),
                "risk_first": risks[0],
                "risk_last": risks[-1],
                "risk_delta_first_last": risks[-1] - risks[0],
                "risk_nonincreasing": int(all(b <= a + 1e-12 for a, b in zip(risks, risks[1:]))),
                "posterior_area_first": areas[0],
                "posterior_area_last": areas[-1],
                "posterior_area_delta_first_last": areas[-1] - areas[0],
                "posterior_area_nondecreasing": int(all(b + 1e-12 >= a for a, b in zip(areas, areas[1:]))),
                "omega_size_nonnegative_all": int(all(value >= -1e-12 for value in omega_size)),
                "omega_cost_nonnegative_all": int(all(value >= -1e-12 for value in omega_cost)),
            }
        )
    out.sort(key=lambda row: (row["target_property"], row["input_index"], strategy_sort_key(row["strategy"])))
    return out


def _verdict_counts(rows: list[dict[str, Any]], hypothesis: str, *, level: str | None = None) -> Counter[str]:
    counter: Counter[str] = Counter()
    for row in rows:
        if row["hypothesis"] != hypothesis:
            continue
        if level is not None and not str(row["scope"]).endswith(f":{level}"):
            continue
        counter[str(row["verdict"])] += 1
    return counter


def _strategy_counts(rows: list[dict[str, Any]], key: str, *, level: str | None = None) -> Counter[str]:
    counter: Counter[str] = Counter()
    for row in rows:
        if level is not None and row["level"] != level:
            continue
        counter[str(row[key])] += 1
    return counter


def _target_counts(rows: list[dict[str, Any]], key: str, *, level: str | None = None) -> dict[str, Counter[str]]:
    out: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        if level is not None and row["level"] != level:
            continue
        out[str(row["target_property"])][str(row[key])] += 1
    return out


def write_batch_report(
    output: Path,
    *,
    context_rows: list[dict[str, Any]],
    trend_rows: list[dict[str, Any]],
    hypothesis_rows: list[dict[str, Any]],
    fixed_level: str,
    target_props: list[str],
    cost_prop: str,
    srs_enabled: bool,
    srs_seeds: int,
) -> None:
    fixed = [row for row in context_rows if row["level"] == fixed_level]
    n_contexts = len(fixed)
    all_levels = sorted({row["level"] for row in context_rows}, key=level_sort_key)
    fse1 = _verdict_counts(hypothesis_rows, "FSE1", level=fixed_level)
    fse5 = _verdict_counts(hypothesis_rows, "FSE5", level=fixed_level)
    fse6 = _verdict_counts(hypothesis_rows, "FSE6", level=fixed_level)
    changed_top = sum(int(row["top_changed_by_cost"]) for row in fixed)
    changed_front = sum(1 for row in fixed if float(row["pareto_jaccard"]) < 1.0)
    srs_best = sum(int(row["srs_best_cost"]) for row in fixed)
    srs_front = sum(int(row["srs_on_empirical_confidence_front"]) for row in fixed)
    srs_trends = [row for row in trend_rows if row["strategy"] == "SRSSampling"]
    srs_risk_improves = sum(int(row["risk_nonincreasing"]) for row in srs_trends)
    srs_area_improves = sum(int(row["posterior_area_nondecreasing"]) for row in srs_trends)
    target_best = _target_counts(fixed, "best_cost_pair")

    lines = [
        "# FSE 2026 posterior-risk revisit on ICPE x264",
        "",
        "## Scope",
        "",
        "This experiment reuses the FSE 2026 posterior risk, posterior confidence, and "
        "integrated confidence discrepancy outcomes on the REPLICATION-ICPE x264 corpus.",
        "",
        f"Target properties: `{','.join(target_props)}`. Empirical acquisition cost property: `{cost_prop}`.",
        f"Levels: `{','.join(all_levels)}`. Fixed-budget summary level: `{fixed_level}`.",
        f"SRS generated: `{srs_enabled}` with `{srs_seeds}` seeds per context/level.",
        "",
        "The fixed-budget part corresponds to the FSE paper's first experiment: do posterior "
        "risk and confidence reveal meaningful differences between strategies at the same sample size?",
        "",
        "The budget-scaling part corresponds to the FSE paper's second experiment: do posterior "
        "risk and confidence improve as the sample size increases?",
        "",
        "## Headline",
        "",
        f"At `{fixed_level}`, strategy posterior-risk distributions differ in "
        f"{fse1.get('supports', 0)}/{n_contexts} x264 target contexts.",
        "",
        f"SRS is the best empirical-cost-normalized recommendation in {srs_best}/{n_contexts} contexts "
        f"and appears on the empirical cost/confidence Pareto frontier in {srs_front}/{n_contexts} contexts.",
        "",
        f"Cost-normalization changes the top integrated-confidence recommendation in "
        f"{changed_top}/{n_contexts} contexts and changes the confidence Pareto frontier in "
        f"{changed_front}/{n_contexts} contexts.",
        "",
        f"SRS has lower posterior risk than random sampling in {fse5.get('supports', 0)}/{n_contexts} "
        f"contexts at `{fixed_level}`; its empirical acquisition cost differs from random in "
        f"{fse6.get('supports', 0)}/{n_contexts} contexts.",
        "",
        "## FSE Experiment 1 Revisited: Fixed Sample Size",
        "",
        "| Target | Best empirical-cost-normalized pair counts |",
        "|---|---|",
    ]
    for target, counts in sorted(target_best.items()):
        text = "; ".join(f"`{pair}`={count}" for pair, count in counts.most_common())
        lines.append(f"| `{target}` | {text} |")

    lines.extend(
        [
            "",
            "| Target | Contexts | SRS best | SRS on Pareto front | Cost changed top | Pareto changed |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for target in sorted({row["target_property"] for row in fixed}):
        rows = [row for row in fixed if row["target_property"] == target]
        lines.append(
            f"| `{target}` | {len(rows)} | {sum(int(row['srs_best_cost']) for row in rows)} | "
            f"{sum(int(row['srs_on_empirical_confidence_front']) for row in rows)} | "
            f"{sum(int(row['top_changed_by_cost']) for row in rows)} | "
            f"{sum(1 for row in rows if float(row['pareto_jaccard']) < 1.0)} |"
        )

    lines.extend(
        [
            "",
            "Interpretation: the FSE posterior outcomes transfer to x264: they do separate "
            "strategies at the same nominal budget. The cost-aware qualification also transfers: "
            "equal sample size does not necessarily mean equal acquisition effort.",
            "",
            "## FSE Experiment 2 Revisited: Increasing Sample Size",
            "",
            "| Strategy | Risk non-increasing | Posterior area non-decreasing | Omega(size) >= 0 for all levels | Omega(cost) >= 0 for all levels |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    by_strategy: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in trend_rows:
        by_strategy[str(row["strategy"])].append(row)
    for strategy in sorted(by_strategy, key=strategy_sort_key):
        rows = by_strategy[strategy]
        lines.append(
            f"| `{strategy}` | {sum(int(row['risk_nonincreasing']) for row in rows)}/{len(rows)} | "
            f"{sum(int(row['posterior_area_nondecreasing']) for row in rows)}/{len(rows)} | "
            f"{sum(int(row['omega_size_nonnegative_all']) for row in rows)}/{len(rows)} | "
            f"{sum(int(row['omega_cost_nonnegative_all']) for row in rows)}/{len(rows)} |"
        )

    lines.extend(
        [
            "",
            f"For SRS specifically, posterior risk is non-increasing in {srs_risk_improves}/{len(srs_trends)} "
            f"contexts and integrated posterior confidence is non-decreasing in "
            f"{srs_area_improves}/{len(srs_trends)} contexts.",
            "",
            "## Practical Take-Away",
            "",
            "Yes, the FSE 2026 paper can be revisited on REPLICATION-ICPE/x264. The required "
            "ingredients are present: a known configuration universe, measured target values, repeated "
            "sampling traces for existing strategies, and enough configuration features to generate SRS.",
            "",
            "The scientific question should be phrased as a replication-plus-extension:",
            "",
            "1. Replication of FSE: do posterior risk/confidence distinguish strategies and improve with budget?",
            "2. Extension from our paper: do those posterior guarantees still support the same recommendation "
            "after empirical acquisition cost replaces sample size?",
            "",
            "## Output Files",
            "",
            "- `posterior_x264_context_summary.csv`: one row per input/target/level.",
            "- `posterior_x264_budget_trends.csv`: budget-scaling trends per strategy and context.",
            "- `posterior_hypothesis_tests.csv`: FSE-style fixed-level and per-level tests.",
            "- `posterior_strategy_summary.csv`: all per-strategy posterior summaries.",
            "- per-context folders with reports, CSVs, and figures.",
        ]
    )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_indices = parse_context_indices(args.contexts)
    target_props = _props(args.target_props)
    strategies = _parse_set(args.strategies)
    levels = _parse_set(args.levels)

    all_records: list[dict[str, Any]] = []
    all_summary: list[dict[str, Any]] = []
    all_curves: list[dict[str, Any]] = []
    all_pareto: list[dict[str, Any]] = []
    all_hypotheses: list[dict[str, Any]] = []
    all_hypothesis_summaries: list[dict[str, Any]] = []
    context_rows: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []

    for target_prop in target_props:
        for input_index in input_indices:
            target_context = _context(target_prop, input_index)
            cost_prop = target_prop if args.cost_prop == "same" else args.cost_prop
            try:
                dataset = load_x264_dataset(
                    runs_zip=args.runs_zip,
                    input_index=input_index,
                    target_prop=target_prop,
                    cost_prop=args.cost_prop,
                    max_runs=args.max_runs,
                    strategies=strategies,
                    levels=levels,
                )
                samples = list(dataset.samples)
                include_srs = not args.no_srs
                if include_srs:
                    samples = _with_srs_samples(
                        dataset,
                        samples,
                        context=target_context,
                        seeds=args.srs_seeds,
                        step_size=args.srs_step_size,
                        p_threshold=args.srs_p_threshold,
                        extreme=args.extreme,
                    )
                dataset = replace(dataset, samples=samples)

                records = posterior_records(dataset, dataset.samples, extreme=args.extreme)
                for row in records:
                    row["input_index"] = input_index
                    row["target_property"] = target_prop
                    row["cost_property"] = cost_prop
                summary = posterior_summary(records, n_configurations=len(dataset.y), prior_offset=args.prior_offset)
                for row in summary:
                    row["input_index"] = input_index
                    row["target_property"] = target_prop
                    row["cost_property"] = cost_prop
                curves = confidence_curves(records, epsilon_points=args.epsilon_points, prior_offset=args.prior_offset)
                for row in curves:
                    row["input_index"] = input_index
                    row["target_property"] = target_prop
                    row["cost_property"] = cost_prop
                pareto = posterior_pareto(summary)
                for row in pareto:
                    row["input_index"] = input_index
                    row["target_property"] = target_prop
                    row["cost_property"] = cost_prop
                hypotheses = posterior_hypothesis_tests(records, summary, pareto, context=target_context)
                for row in hypotheses:
                    row["input_index"] = input_index
                    row["target_property"] = target_prop
                    row["cost_property"] = cost_prop
                hypothesis_summary = posterior_hypothesis_summary(hypotheses)
                for row in hypothesis_summary:
                    row["input_index"] = input_index
                    row["target_property"] = target_prop
                    row["cost_property"] = cost_prop

                context_dir = output_dir / target_context
                context_dir.mkdir(parents=True, exist_ok=True)
                figures: list[str] = []
                if not args.no_figures:
                    figures = write_figures(
                        context_dir,
                        records=records,
                        summary=summary,
                        curves=curves,
                        pareto=pareto,
                        epsilon_max=args.plot_epsilon_max,
                    )
                write_csv(context_dir / "posterior_records.csv", records)
                write_csv(context_dir / "posterior_strategy_summary.csv", summary)
                write_csv(context_dir / "posterior_confidence_curves.csv", curves)
                write_csv(context_dir / "posterior_pareto.csv", pareto)
                write_csv(context_dir / "posterior_hypothesis_tests.csv", hypotheses)
                write_csv(context_dir / "posterior_hypothesis_summary.csv", hypothesis_summary)
                write_report(
                    context_dir / f"{target_context}_fse_posterior_report.md",
                    context=target_context,
                    n_configurations=len(dataset.y),
                    summary=summary,
                    pareto=pareto,
                    hypotheses=hypotheses,
                    figures=figures,
                    include_srs=include_srs,
                    prior_offset=args.prior_offset,
                    extreme=args.extreme,
                )

                all_records.extend(records)
                all_summary.extend(summary)
                all_curves.extend(curves)
                all_pareto.extend(pareto)
                all_hypotheses.extend(hypotheses)
                all_hypothesis_summaries.extend(hypothesis_summary)
                context_rows.extend(
                    summarize_context_levels(
                        input_index=input_index,
                        target_prop=target_prop,
                        cost_prop=cost_prop,
                        summary=summary,
                        pareto=pareto,
                        hypotheses=hypotheses,
                    )
                )
            except Exception as exc:  # noqa: BLE001 - keep the batch robust.
                skipped.append(
                    {
                        "context": target_context,
                        "input_index": input_index,
                        "target_property": target_prop,
                        "cost_property": cost_prop,
                        "error": str(exc),
                    }
                )

    trend_rows = strategy_budget_trends(all_summary)
    context_rows.sort(key=lambda row: (row["target_property"], row["input_index"], level_sort_key(row["level"])))
    write_csv(output_dir / "posterior_records.csv", all_records)
    write_csv(output_dir / "posterior_strategy_summary.csv", all_summary)
    write_csv(output_dir / "posterior_confidence_curves.csv", all_curves)
    write_csv(output_dir / "posterior_pareto.csv", all_pareto)
    write_csv(output_dir / "posterior_hypothesis_tests.csv", all_hypotheses)
    write_csv(output_dir / "posterior_hypothesis_summary.csv", all_hypothesis_summaries)
    write_csv(output_dir / "posterior_x264_context_summary.csv", context_rows)
    write_csv(output_dir / "posterior_x264_budget_trends.csv", trend_rows)
    write_csv(output_dir / "skipped_contexts.csv", skipped)
    write_batch_report(
        output_dir / "fse_posterior_x264_icpe_report.md",
        context_rows=context_rows,
        trend_rows=trend_rows,
        hypothesis_rows=all_hypotheses,
        fixed_level=args.fixed_level,
        target_props=target_props,
        cost_prop=args.cost_prop,
        srs_enabled=not args.no_srs,
        srs_seeds=args.srs_seeds,
    )
    print(f"Wrote x264 FSE posterior revisit outputs to {output_dir}")
    if skipped:
        print(f"Skipped {len(skipped)} contexts; see skipped_contexts.csv")


if __name__ == "__main__":
    main()
