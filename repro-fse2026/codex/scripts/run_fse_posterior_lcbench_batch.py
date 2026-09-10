#!/usr/bin/env python3
"""Run FSE-style posterior-bound analysis on LCBench measured pools."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import replace
from pathlib import Path
import re
import sys
from typing import Any

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
for path in (REPO_ROOT, SCRIPT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from cost_sampling.analysis import level_sort_key, strategy_sort_key, write_csv
from cost_sampling.generated_sampling import (
    build_generated_dataset,
    budget_grid,
    load_lcbench_table,
    parse_where,
    subset_measured_table,
)

from run_fse_posterior import (
    _fmt,
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


DEFAULT_FIGSHARE_URL = "https://ndownloader.figshare.com/files/21188598"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        default="/private/tmp/lcbench/data_2k_lw.json",
        help="Path to the full lightweight LCBench JSON.",
    )
    parser.add_argument(
        "--datasets",
        default="ALL",
        help="Comma-separated OpenML dataset names, or ALL.",
    )
    parser.add_argument("--dataset-limit", type=int, default=0, help="Optional first-N dataset limit.")
    parser.add_argument("--output-dir", default="artifacts/fse_posterior_lcbench")
    parser.add_argument("--target-column", default="final_val_accuracy")
    parser.add_argument("--cost-column", default="time_total")
    parser.add_argument("--cost-orientation", choices=("lower", "inverse"), default="lower")
    parser.add_argument("--runtime-mode", choices=("last", "sum"), default="last")
    parser.add_argument("--max-budget", type=int, default=64)
    parser.add_argument("--seeds", type=int, default=30)
    parser.add_argument("--no-oracles", action="store_true")
    parser.add_argument("--no-srs", action="store_true")
    parser.add_argument("--srs-seeds", type=int, default=30)
    parser.add_argument("--srs-step-size", type=int, default=25)
    parser.add_argument("--srs-p-threshold", type=float, default=0.05)
    parser.add_argument("--extreme", choices=("max", "min"), default="max")
    parser.add_argument("--prior-offset", type=int, default=1)
    parser.add_argument("--epsilon-points", type=int, default=151)
    parser.add_argument("--plot-epsilon-max", type=float, default=0.15)
    parser.add_argument("--no-figures", action="store_true")
    parser.add_argument(
        "--where",
        action="append",
        default=[],
        metavar="COLUMN=VALUE",
        help="Additional row filters before dataset slicing.",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Small smoke profile: six datasets, two budgets, fewer stochastic/SRS seeds.",
    )
    return parser.parse_args()


def _dataset_filter(raw: str) -> list[str] | None:
    if raw.strip().upper() == "ALL":
        return None
    return [part.strip() for part in raw.split(",") if part.strip()]


def _slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")
    return slug or "value"


def _pair(row: dict[str, Any]) -> str:
    return f"{row['strategy']}_{row['level']}"


def _add_metadata(rows: list[dict[str, Any]], *, workload: str, target: str, cost: str) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        item = dict(row)
        item["system"] = "lcbench"
        item["workload"] = workload
        item["target_property"] = target
        item["cost_property"] = cost
        out.append(item)
    return out


def summarize_workload_levels(
    *,
    workload: str,
    summary: list[dict[str, Any]],
    hypotheses: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = []
    for level in sorted({row["level"] for row in summary}, key=level_sort_key):
        level_summary = [row for row in summary if row["level"] == level]
        best_risk = min(level_summary, key=lambda row: row["median_posterior_risk"])
        best_size = max(level_summary, key=lambda row: row["omega_size_baseline"])
        best_cost = max(level_summary, key=lambda row: row["omega_cost_baseline"])
        srs = next((row for row in level_summary if row["strategy"] == "SRSSampling"), None)
        random = next((row for row in level_summary if row["strategy"] == "random"), None)
        count_front, empirical_front = level_confidence_frontiers(level_summary)
        union = count_front | empirical_front
        fse_by_id = {
            row["hypothesis"]: row
            for row in hypotheses
            if str(row["scope"]).endswith(f":{level}")
        }
        rows.append(
            {
                "workload": workload,
                "context": best_cost["context"],
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


def strategy_budget_trends(summary_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in summary_rows:
        grouped[(str(row["workload"]), str(row["strategy"]))].append(row)
    out = []
    for (workload, strategy), rows in grouped.items():
        rows.sort(key=lambda row: level_sort_key(row["level"]))
        risks = [float(row["median_posterior_risk"]) for row in rows]
        areas = [float(row["posterior_confidence_area"]) for row in rows]
        omega_size = [float(row["omega_size_baseline"]) for row in rows]
        omega_cost = [float(row["omega_cost_baseline"]) for row in rows]
        out.append(
            {
                "workload": workload,
                "strategy": strategy,
                "levels": ",".join(str(row["level"]) for row in rows),
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
    out.sort(key=lambda row: (row["workload"], strategy_sort_key(row["strategy"])))
    return out


def _verdict_counts(rows: list[dict[str, Any]], hypothesis: str) -> Counter[str]:
    counter: Counter[str] = Counter()
    for row in rows:
        if row["hypothesis"] == hypothesis:
            counter[str(row["verdict"])] += 1
    return counter


def write_batch_report(
    output: Path,
    *,
    workload_rows: list[dict[str, Any]],
    trend_rows: list[dict[str, Any]],
    hypothesis_rows: list[dict[str, Any]],
    workloads: list[str],
    target_column: str,
    cost_column: str,
    source_json: str,
    srs_enabled: bool,
    srs_seeds: int,
    include_oracles: bool,
) -> None:
    n_scopes = len(workload_rows)
    fse1 = _verdict_counts(hypothesis_rows, "FSE1")
    fse5 = _verdict_counts(hypothesis_rows, "FSE5")
    fse6 = _verdict_counts(hypothesis_rows, "FSE6")
    srs_best = sum(int(row["srs_best_cost"]) for row in workload_rows)
    srs_front = sum(int(row["srs_on_empirical_confidence_front"]) for row in workload_rows)
    changed_top = sum(int(row["top_changed_by_cost"]) for row in workload_rows)
    changed_front = sum(1 for row in workload_rows if float(row["pareto_jaccard"]) < 1.0)
    srs_trends = [row for row in trend_rows if row["strategy"] == "SRSSampling"]
    best_counts = Counter(row["best_cost_pair"] for row in workload_rows)

    lines = [
        "# FSE 2026 posterior-risk revisit on LCBench",
        "",
        "## Scope",
        "",
        "This applies the FSE posterior-risk/posterior-confidence framework to LCBench measured pools.",
        "Each OpenML dataset is a distinct reference universe, and each hyperparameter configuration is a sampled object.",
        "The result is reference-relative posterior risk over the measured LCBench pool, not a configurable-software claim.",
        "",
        f"Source JSON: `{source_json}`.",
        f"Target column: `{target_column}`. Cost column: `{cost_column}`.",
        f"Datasets analyzed: `{', '.join(workloads)}`.",
        f"SRS generated: `{srs_enabled}` with `{srs_seeds}` seeds per dataset/level.",
        f"Diagnostic oracles included: `{include_oracles}`.",
        "",
        "## Headline",
        "",
        f"Strategy posterior-risk distributions differ in {fse1.get('supports', 0)}/{n_scopes} dataset-level scopes.",
        f"SRS is the best empirical-cost-normalized recommendation in {srs_best}/{n_scopes} scopes and "
        f"appears on the empirical cost/confidence Pareto frontier in {srs_front}/{n_scopes} scopes.",
        f"Cost-normalization changes the top recommendation in {changed_top}/{n_scopes} scopes and "
        f"changes the confidence Pareto frontier in {changed_front}/{n_scopes} scopes.",
        f"SRS has lower posterior risk than random in {fse5.get('supports', 0)}/{n_scopes} scopes; "
        f"its empirical acquisition cost differs from random in {fse6.get('supports', 0)}/{n_scopes} scopes.",
        "",
        "Best empirical-cost-normalized pairs:",
        "",
    ]
    for pair, count in best_counts.most_common():
        lines.append(f"- `{pair}`: {count}/{n_scopes}")

    lines.extend(
        [
            "",
            "## Dataset-Level Summary",
            "",
            "| Dataset | Level | n | Best cost pair | SRS best? | SRS on front? | Jaccard |",
            "|---|---|---:|---|---:|---:|---:|",
        ]
    )
    for row in workload_rows:
        lines.append(
            f"| `{row['workload']}` | `{row['level']}` | {int(row['n'])} | `{row['best_cost_pair']}` | "
            f"{row['srs_best_cost']} | {row['srs_on_empirical_confidence_front']} | "
            f"{_fmt(row['pareto_jaccard'])} |"
        )

    lines.extend(
        [
            "",
            "## Budget Scaling",
            "",
            "| Strategy | Risk non-increasing | Posterior area non-decreasing | Omega(size) >= 0 all datasets | Omega(cost) >= 0 all datasets |",
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
    if srs_trends:
        lines.extend(
            [
                "",
                f"For SRS, posterior risk is non-increasing in "
                f"{sum(int(row['risk_nonincreasing']) for row in srs_trends)}/{len(srs_trends)} datasets "
                f"and posterior area is non-decreasing in "
                f"{sum(int(row['posterior_area_nondecreasing']) for row in srs_trends)}/{len(srs_trends)} datasets.",
            ]
        )

    lines.extend(
        [
            "",
            "## Applicability",
            "",
            "LCBench is applicable as an external-validation dataset for reference-relative posterior risk. "
            "It should not be merged directly with configurable-software systems: the sampled objects are "
            "ML hyperparameter configurations, and the contexts are OpenML datasets.",
            "",
            "## Output Files",
            "",
            "- `posterior_lcbench_dataset_summary.csv`: dataset-level posterior/cost decisions.",
            "- `posterior_lcbench_budget_trends.csv`: budget-scaling trends per strategy.",
            "- `posterior_hypothesis_tests.csv`: per-dataset/level FSE-style tests.",
            "- per-dataset folders with CSVs, reports, and figures.",
        ]
    )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    source_json = Path(args.json)
    if not source_json.exists():
        raise SystemExit(
            f"LCBench JSON not found at {source_json}. Expected the lightweight archive's "
            f"`data_2k_lw.json`; source archive: {DEFAULT_FIGSHARE_URL}"
        )

    dataset_names = _dataset_filter(args.datasets)
    max_budget = args.max_budget
    seeds = args.seeds
    srs_seeds = args.srs_seeds
    dataset_limit = args.dataset_limit
    if args.quick:
        max_budget = min(max_budget, 16)
        seeds = min(seeds, 10)
        srs_seeds = min(srs_seeds, 10)
        if dataset_names is None and dataset_limit == 0:
            dataset_limit = 6

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    table = load_lcbench_table(
        source_json,
        datasets=dataset_names,
        where=parse_where(args.where),
        runtime_mode=args.runtime_mode,
    )
    workloads = sorted({row["workload"] for row in table.rows})
    if dataset_limit > 0:
        workloads = workloads[:dataset_limit]

    all_records: list[dict[str, Any]] = []
    all_summary: list[dict[str, Any]] = []
    all_curves: list[dict[str, Any]] = []
    all_pareto: list[dict[str, Any]] = []
    all_hypotheses: list[dict[str, Any]] = []
    all_hypothesis_summaries: list[dict[str, Any]] = []
    workload_rows: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    successful_workloads: list[str] = []

    for workload in workloads:
        slug = _slug(workload)
        try:
            print(f"[lcbench] loading {workload}", flush=True)
            indices = np.asarray(
                [idx for idx, row in enumerate(table.rows) if row["workload"] == workload],
                dtype=int,
            )
            subset = subset_measured_table(table, indices, analysis_name=f"lcbench__workload_{slug}")
            budgets = [n for n in budget_grid(len(subset.rows)) if n <= max_budget]
            if args.quick:
                budgets = budgets[:2]
            if not budgets:
                raise ValueError(f"No valid budget grid for {workload!r}.")
            dataset = build_generated_dataset(
                subset,
                target_property=args.target_column,
                cost_property=args.cost_column,
                cost_orientation=args.cost_orientation,
                budgets=budgets,
                seeds=seeds,
                include_oracles=not args.no_oracles,
            )
            samples = dataset.samples
            include_srs = not args.no_srs
            if include_srs:
                print(f"[lcbench] generating SRS for {workload}", flush=True)
                samples = _with_srs_samples(
                    dataset,
                    samples,
                    context=dataset.context,
                    seeds=srs_seeds,
                    step_size=args.srs_step_size,
                    p_threshold=args.srs_p_threshold,
                    extreme=args.extreme,
                )
            dataset = replace(dataset, samples=samples)

            records = posterior_records(dataset, dataset.samples, extreme=args.extreme)
            records = _add_metadata(records, workload=workload, target=args.target_column, cost=args.cost_column)
            summary = posterior_summary(records, n_configurations=len(dataset.y), prior_offset=args.prior_offset)
            summary = _add_metadata(summary, workload=workload, target=args.target_column, cost=args.cost_column)
            curves = confidence_curves(records, epsilon_points=args.epsilon_points, prior_offset=args.prior_offset)
            curves = _add_metadata(curves, workload=workload, target=args.target_column, cost=args.cost_column)
            pareto = posterior_pareto(summary)
            pareto = _add_metadata(pareto, workload=workload, target=args.target_column, cost=args.cost_column)
            hypotheses = posterior_hypothesis_tests(records, summary, pareto, context=dataset.context)
            hypotheses = _add_metadata(hypotheses, workload=workload, target=args.target_column, cost=args.cost_column)
            hypothesis_summary = posterior_hypothesis_summary(hypotheses)
            hypothesis_summary = _add_metadata(
                hypothesis_summary,
                workload=workload,
                target=args.target_column,
                cost=args.cost_column,
            )

            workload_dir = output_dir / f"lcbench_{slug}"
            workload_dir.mkdir(parents=True, exist_ok=True)
            figures: list[str] = []
            if not args.no_figures:
                figures = write_figures(
                    workload_dir,
                    records=records,
                    summary=summary,
                    curves=curves,
                    pareto=pareto,
                    epsilon_max=args.plot_epsilon_max,
                )
            write_csv(workload_dir / "posterior_records.csv", records)
            write_csv(workload_dir / "posterior_strategy_summary.csv", summary)
            write_csv(workload_dir / "posterior_confidence_curves.csv", curves)
            write_csv(workload_dir / "posterior_pareto.csv", pareto)
            write_csv(workload_dir / "posterior_hypothesis_tests.csv", hypotheses)
            write_csv(workload_dir / "posterior_hypothesis_summary.csv", hypothesis_summary)
            write_report(
                workload_dir / f"lcbench_{slug}_fse_posterior_report.md",
                context=dataset.context,
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
            workload_rows.extend(
                summarize_workload_levels(
                    workload=workload,
                    summary=summary,
                    hypotheses=hypotheses,
                )
            )
            successful_workloads.append(workload)
            print(f"[lcbench] finished {workload}", flush=True)
        except Exception as exc:  # noqa: BLE001
            skipped.append({"workload": workload, "error": str(exc)})
            print(f"[lcbench] skipped {workload}: {exc}", flush=True)

    trend_rows = strategy_budget_trends(all_summary)
    workload_rows.sort(key=lambda row: (row["workload"], level_sort_key(row["level"])))
    write_csv(output_dir / "posterior_records.csv", all_records)
    write_csv(output_dir / "posterior_strategy_summary.csv", all_summary)
    write_csv(output_dir / "posterior_confidence_curves.csv", all_curves)
    write_csv(output_dir / "posterior_pareto.csv", all_pareto)
    write_csv(output_dir / "posterior_hypothesis_tests.csv", all_hypotheses)
    write_csv(output_dir / "posterior_hypothesis_summary.csv", all_hypothesis_summaries)
    write_csv(output_dir / "posterior_lcbench_dataset_summary.csv", workload_rows)
    write_csv(output_dir / "posterior_lcbench_budget_trends.csv", trend_rows)
    write_csv(output_dir / "skipped_contexts.csv", skipped)
    write_batch_report(
        output_dir / "fse_posterior_lcbench_report.md",
        workload_rows=workload_rows,
        trend_rows=trend_rows,
        hypothesis_rows=all_hypotheses,
        workloads=successful_workloads,
        target_column=args.target_column,
        cost_column=args.cost_column,
        source_json=str(source_json),
        srs_enabled=not args.no_srs,
        srs_seeds=srs_seeds,
        include_oracles=not args.no_oracles,
    )
    print(f"Wrote LCBench FSE posterior outputs to {output_dir}")
    if skipped:
        print(f"Skipped {len(skipped)} datasets; see skipped_contexts.csv")


if __name__ == "__main__":
    main()
