#!/usr/bin/env python3
"""Run FSE-style posterior-bound analysis on Linux/TuxKConfig releases."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import replace
from pathlib import Path
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
for path in (REPO_ROOT, SCRIPT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from cost_sampling.analysis import level_sort_key, strategy_sort_key, write_csv
from cost_sampling.linux_data import load_linux_dataset

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
from run_linux_kernel import build_samples


RELEASES = {
    "413": "ICPE-rawdata/linux/tuxkconfig_413.parquet",
    "415": "ICPE-rawdata/linux/tuxkconfig_415.parquet",
    "420": "ICPE-rawdata/linux/tuxkconfig_420.parquet",
    "500": "ICPE-rawdata/linux/tuxkconfig_500.parquet",
    "504": "ICPE-rawdata/linux/tuxkconfig_504.parquet",
    "507": "ICPE-rawdata/linux/tuxkconfig_507.parquet",
    "508": "ICPE-rawdata/linux/tuxkconfig_508.parquet",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--releases", default="508", help="Comma-separated releases or ALL.")
    parser.add_argument("--output-dir", default="artifacts/fse_posterior_linux")
    parser.add_argument("--target-column", default="vmlinux")
    parser.add_argument("--cost-column", default=None)
    parser.add_argument("--levels", default="0.01,0.02,0.05")
    parser.add_argument("--stochastic-runs", type=int, default=30)
    parser.add_argument("--diversity-runs", type=int, default=5)
    parser.add_argument("--diversity-max-n", type=int, default=1851)
    parser.add_argument("--diversity-candidate-size", type=int, default=512)
    parser.add_argument("--uncertainty-runs", type=int, default=5)
    parser.add_argument("--uncertainty-seed-fraction", type=float, default=0.25)
    parser.add_argument("--coverage-runs", type=int, default=5)
    parser.add_argument("--coverage-candidate-size", type=int, default=512)
    parser.add_argument("--top-k-features", type=int, default=512)
    parser.add_argument("--alpha", type=float, default=1.0)
    parser.add_argument("--no-log-target", action="store_true")
    parser.add_argument("--srs-seeds", type=int, default=30)
    parser.add_argument("--srs-step-size", type=int, default=25)
    parser.add_argument("--srs-p-threshold", type=float, default=0.05)
    parser.add_argument("--no-srs", action="store_true")
    parser.add_argument("--extreme", choices=("max", "min"), default="max")
    parser.add_argument("--prior-offset", type=int, default=1)
    parser.add_argument("--epsilon-points", type=int, default=151)
    parser.add_argument("--plot-epsilon-max", type=float, default=0.15)
    parser.add_argument("--no-figures", action="store_true")
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Small smoke profile: fewer runs and two levels.",
    )
    return parser.parse_args()


def _release_keys(raw: str) -> list[str]:
    if raw.strip().upper() == "ALL":
        return list(RELEASES)
    return [part.strip() for part in raw.split(",") if part.strip()]


def _levels(raw: str) -> list[float]:
    return [float(part.strip()) for part in raw.split(",") if part.strip()]


def _pair(row: dict[str, Any]) -> str:
    return f"{row['strategy']}_{row['level']}"


def summarize_release_levels(
    *,
    release: str,
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
        fse_by_id = {
            row["hypothesis"]: row
            for row in hypotheses
            if str(row["scope"]).endswith(f":{level}")
        }
        union = count_front | empirical_front
        rows.append(
            {
                "release": release,
                "context": f"linux{release}_vmlinux",
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
        grouped[(str(row["release"]), str(row["strategy"]))].append(row)
    out = []
    for (release, strategy), rows in grouped.items():
        rows.sort(key=lambda row: level_sort_key(row["level"]))
        risks = [float(row["median_posterior_risk"]) for row in rows]
        areas = [float(row["posterior_confidence_area"]) for row in rows]
        omega_size = [float(row["omega_size_baseline"]) for row in rows]
        omega_cost = [float(row["omega_cost_baseline"]) for row in rows]
        out.append(
            {
                "release": release,
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
    out.sort(key=lambda row: (row["release"], strategy_sort_key(row["strategy"])))
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
    release_rows: list[dict[str, Any]],
    trend_rows: list[dict[str, Any]],
    hypothesis_rows: list[dict[str, Any]],
    releases: list[str],
    levels: list[float],
    srs_enabled: bool,
    srs_seeds: int,
) -> None:
    n_scopes = len(release_rows)
    fse1 = _verdict_counts(hypothesis_rows, "FSE1")
    fse5 = _verdict_counts(hypothesis_rows, "FSE5")
    fse6 = _verdict_counts(hypothesis_rows, "FSE6")
    srs_best = sum(int(row["srs_best_cost"]) for row in release_rows)
    srs_front = sum(int(row["srs_on_empirical_confidence_front"]) for row in release_rows)
    changed_top = sum(int(row["top_changed_by_cost"]) for row in release_rows)
    changed_front = sum(1 for row in release_rows if float(row["pareto_jaccard"]) < 1.0)
    srs_trends = [row for row in trend_rows if row["strategy"] == "SRSSampling"]
    best_counts = Counter(row["best_cost_pair"] for row in release_rows)

    lines = [
        "# FSE 2026 posterior-risk revisit on Linux/TuxKConfig",
        "",
        "## Scope",
        "",
        "This applies the FSE posterior-risk/posterior-confidence framework to Linux/TuxKConfig releases.",
        "Important caveat: Linux is a large measured pool, not the full Linux configuration space. "
        "Posterior risk is therefore interpreted relative to the measured TuxKConfig pool.",
        "",
        f"Releases: `{','.join(releases)}`. Levels/fractions: `{','.join(str(v) for v in levels)}`.",
        f"SRS generated: `{srs_enabled}` with `{srs_seeds}` seeds per release/level.",
        "",
        "## Headline",
        "",
        f"Strategy posterior-risk distributions differ in {fse1.get('supports', 0)}/{n_scopes} release-level scopes.",
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
            "## Release-Level Summary",
            "",
            "| Release | Level | n | Best cost pair | SRS best? | SRS on front? | Jaccard |",
            "|---|---|---:|---|---:|---:|---:|",
        ]
    )
    for row in release_rows:
        lines.append(
            f"| `{row['release']}` | `{row['level']}` | {int(row['n'])} | `{row['best_cost_pair']}` | "
            f"{row['srs_best_cost']} | {row['srs_on_empirical_confidence_front']} | "
            f"{_fmt(row['pareto_jaccard'])} |"
        )

    lines.extend(
        [
            "",
            "## Budget Scaling",
            "",
            "| Strategy | Risk non-increasing | Posterior area non-decreasing | Omega(size) >= 0 all levels | Omega(cost) >= 0 all levels |",
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
                f"{sum(int(row['risk_nonincreasing']) for row in srs_trends)}/{len(srs_trends)} releases "
                f"and posterior area is non-decreasing in "
                f"{sum(int(row['posterior_area_nondecreasing']) for row in srs_trends)}/{len(srs_trends)} releases.",
            ]
        )

    lines.extend(
        [
            "",
            "## Applicability",
            "",
            "Linux is applicable as a replication-plus-extension dataset if the claim is scoped to the measured pool. "
            "It is not a direct full-space replication like the FSE systems or x264 because the full valid Linux "
            "configuration space is not exhaustively measured.",
            "",
            "## Output Files",
            "",
            "- `posterior_linux_release_summary.csv`: release-level posterior/cost decisions.",
            "- `posterior_linux_budget_trends.csv`: budget-scaling trends per strategy.",
            "- `posterior_hypothesis_tests.csv`: per-release/level FSE-style tests.",
            "- per-release folders with CSVs, reports, and figures.",
        ]
    )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    release_keys = _release_keys(args.releases)
    levels = _levels(args.levels)
    stochastic_runs = args.stochastic_runs
    diversity_runs = args.diversity_runs
    uncertainty_runs = args.uncertainty_runs
    coverage_runs = args.coverage_runs
    srs_seeds = args.srs_seeds
    if args.quick:
        levels = levels[:2]
        stochastic_runs = min(stochastic_runs, 10)
        diversity_runs = min(diversity_runs, 2)
        uncertainty_runs = min(uncertainty_runs, 2)
        coverage_runs = min(coverage_runs, 2)
        srs_seeds = min(srs_seeds, 5)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    all_records: list[dict[str, Any]] = []
    all_summary: list[dict[str, Any]] = []
    all_curves: list[dict[str, Any]] = []
    all_pareto: list[dict[str, Any]] = []
    all_hypotheses: list[dict[str, Any]] = []
    all_hypothesis_summaries: list[dict[str, Any]] = []
    release_rows: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    successful_releases: list[str] = []

    for release in release_keys:
        context = f"linux{release}_vmlinux"
        try:
            print(f"[linux] loading {context}", flush=True)
            dataset = load_linux_dataset(
                RELEASES[release],
                context=context,
                target_column=args.target_column,
                cost_column=args.cost_column,
                top_k_features=None if args.top_k_features == 0 else args.top_k_features,
            )
            samples = build_samples(
                dataset=dataset,
                levels=levels,
                stochastic_runs=stochastic_runs,
                diversity_runs=diversity_runs,
                diversity_candidate_size=args.diversity_candidate_size,
                diversity_max_n=args.diversity_max_n,
                uncertainty_runs=uncertainty_runs,
                uncertainty_seed_fraction=args.uncertainty_seed_fraction,
                coverage_runs=coverage_runs,
                coverage_candidate_size=args.coverage_candidate_size,
                alpha=args.alpha,
                log_target=not args.no_log_target,
                seed=20260513 + int(release),
            )
            include_srs = not args.no_srs
            if include_srs:
                print(f"[linux] generating SRS for {context}", flush=True)
                samples = _with_srs_samples(
                    dataset,
                    samples,
                    context=context,
                    seeds=srs_seeds,
                    step_size=args.srs_step_size,
                    p_threshold=args.srs_p_threshold,
                    extreme=args.extreme,
                )
            dataset = replace(dataset, samples=samples)
            records = posterior_records(dataset, dataset.samples, extreme=args.extreme)
            for row in records:
                row["release"] = release
            summary = posterior_summary(records, n_configurations=len(dataset.y), prior_offset=args.prior_offset)
            for row in summary:
                row["release"] = release
            curves = confidence_curves(records, epsilon_points=args.epsilon_points, prior_offset=args.prior_offset)
            for row in curves:
                row["release"] = release
            pareto = posterior_pareto(summary)
            for row in pareto:
                row["release"] = release
            hypotheses = posterior_hypothesis_tests(records, summary, pareto, context=context)
            for row in hypotheses:
                row["release"] = release
            hypothesis_summary = posterior_hypothesis_summary(hypotheses)
            for row in hypothesis_summary:
                row["release"] = release

            release_dir = output_dir / context
            release_dir.mkdir(parents=True, exist_ok=True)
            figures: list[str] = []
            if not args.no_figures:
                figures = write_figures(
                    release_dir,
                    records=records,
                    summary=summary,
                    curves=curves,
                    pareto=pareto,
                    epsilon_max=args.plot_epsilon_max,
                )
            write_csv(release_dir / "posterior_records.csv", records)
            write_csv(release_dir / "posterior_strategy_summary.csv", summary)
            write_csv(release_dir / "posterior_confidence_curves.csv", curves)
            write_csv(release_dir / "posterior_pareto.csv", pareto)
            write_csv(release_dir / "posterior_hypothesis_tests.csv", hypotheses)
            write_csv(release_dir / "posterior_hypothesis_summary.csv", hypothesis_summary)
            write_report(
                release_dir / f"{context}_fse_posterior_report.md",
                context=context,
                n_configurations=len(dataset.y),
                summary=summary,
                pareto=pareto,
                hypotheses=hypotheses,
                figures=figures,
                include_srs=include_srs,
                    prior_offset=args.prior_offset,
                    extreme=args.extreme,
                )
            successful_releases.append(release)
            print(f"[linux] finished {context}", flush=True)

            all_records.extend(records)
            all_summary.extend(summary)
            all_curves.extend(curves)
            all_pareto.extend(pareto)
            all_hypotheses.extend(hypotheses)
            all_hypothesis_summaries.extend(hypothesis_summary)
            release_rows.extend(
                summarize_release_levels(
                    release=release,
                    summary=summary,
                    hypotheses=hypotheses,
                )
            )
        except Exception as exc:  # noqa: BLE001
            skipped.append({"release": release, "context": context, "error": str(exc)})
            print(f"[linux] skipped {context}: {exc}", flush=True)

    trend_rows = strategy_budget_trends(all_summary)
    release_rows.sort(key=lambda row: (row["release"], level_sort_key(row["level"])))
    write_csv(output_dir / "posterior_records.csv", all_records)
    write_csv(output_dir / "posterior_strategy_summary.csv", all_summary)
    write_csv(output_dir / "posterior_confidence_curves.csv", all_curves)
    write_csv(output_dir / "posterior_pareto.csv", all_pareto)
    write_csv(output_dir / "posterior_hypothesis_tests.csv", all_hypotheses)
    write_csv(output_dir / "posterior_hypothesis_summary.csv", all_hypothesis_summaries)
    write_csv(output_dir / "posterior_linux_release_summary.csv", release_rows)
    write_csv(output_dir / "posterior_linux_budget_trends.csv", trend_rows)
    write_csv(output_dir / "skipped_contexts.csv", skipped)
    write_batch_report(
        output_dir / "fse_posterior_linux_report.md",
        release_rows=release_rows,
        trend_rows=trend_rows,
        hypothesis_rows=all_hypotheses,
        releases=successful_releases,
        levels=levels,
        srs_enabled=not args.no_srs,
        srs_seeds=srs_seeds,
    )
    print(f"Wrote Linux FSE posterior outputs to {output_dir}")
    if skipped:
        print(f"Skipped {len(skipped)} releases; see skipped_contexts.csv")


if __name__ == "__main__":
    main()
