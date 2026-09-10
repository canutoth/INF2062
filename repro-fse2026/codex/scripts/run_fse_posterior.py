#!/usr/bin/env python3
"""Compute FSE-style posterior guarantee/cost tradeoffs for sampled runs."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import replace
import math
from pathlib import Path
import statistics
import sys
from typing import Any

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from cost_sampling.analysis import level_sort_key, strategy_sort_key, write_csv
from cost_sampling.archive_runs import RunDataset, Sample, SampleRef, load_runs_dataset
from cost_sampling.fse_artifact import load_fse_directory_dataset
from cost_sampling.hypotheses import kruskal_wallis, mann_whitney_u, vd_magnitude
from cost_sampling.metrics import pareto_mask
from cost_sampling.posterior import (
    confidence_curve_rows,
    integrated_confidence,
    sample_risk_bound,
)
from cost_sampling.srs import srs_indices


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--context", default="LLVM", help="System/context name inside NewRuns.zip.")
    parser.add_argument("--runs-zip", default="ICPE-rawdata/NewRuns.zip", help="Path to NewRuns.zip.")
    parser.add_argument(
        "--fse-root",
        default=None,
        help="Optional extracted FSE 2026 artifact root, data/, or data/sampling/ directory.",
    )
    parser.add_argument("--output-dir", default=None, help="Output directory.")
    parser.add_argument("--max-runs", type=int, default=100, help="Maximum run id to load.")
    parser.add_argument("--performance-name", default="Performance", help="Performance column in sampled CSVs.")
    parser.add_argument(
        "--strategies",
        default="random,solverBased,divDistBased",
        help=(
            "Comma-separated sampled strategies to analyze. The default mirrors the FSE artifact's "
            "main curve strategies available in NewRuns; use ALL for every strategy in the archive."
        ),
    )
    parser.add_argument(
        "--levels",
        default="t2",
        help="Comma-separated levels to analyze, e.g. t2 or t1,t2,t3. Use ALL for every level.",
    )
    parser.add_argument("--extreme", choices=("max", "min"), default="max", help="Performance-bound direction.")
    parser.add_argument(
        "--prior-offset",
        type=int,
        default=1,
        help="Prior-confidence exponent offset. Default 1 matches the FSE artifact notebook.",
    )
    parser.add_argument("--epsilon-points", type=int, default=151, help="Number of epsilon grid points for curves.")
    parser.add_argument("--include-srs", action="store_true", help="Generate SRS samples at the analyzed levels.")
    parser.add_argument("--srs-seeds", type=int, default=100, help="Number of generated SRS repetitions.")
    parser.add_argument("--srs-step-size", type=int, default=25, help="SRS recursive batch size.")
    parser.add_argument("--srs-p-threshold", type=float, default=0.05, help="SRS Welch-test p-value threshold.")
    parser.add_argument(
        "--plot-epsilon-max",
        type=float,
        default=0.15,
        help="Maximum epsilon shown in the posterior/prior discrepancy figure.",
    )
    return parser.parse_args()


def _parse_set(raw: str) -> set[str] | None:
    if raw.strip().upper() == "ALL":
        return None
    return {part.strip() for part in raw.split(",") if part.strip()}


def _unique_preserve_order(indices: np.ndarray) -> np.ndarray:
    seen: set[int] = set()
    out: list[int] = []
    for idx in indices:
        value = int(idx)
        if value not in seen:
            seen.add(value)
            out.append(value)
    return np.array(out, dtype=int)


def _fmt(value: float) -> str:
    return f"{value:.4g}"


def _fmt_p(value: float) -> str:
    if value is None or not math.isfinite(value):
        return ""
    if value < 0.001:
        return f"{value:.2e}"
    return f"{value:.3g}"


def _median(values: list[float]) -> float:
    return float(statistics.median(values))


def _iqr(values: list[float]) -> tuple[float, float]:
    array = np.asarray(values, dtype=float)
    return float(np.percentile(array, 25)), float(np.percentile(array, 75))


def _filtered_samples(dataset: RunDataset, strategies: set[str] | None, levels: set[str] | None) -> list[Sample]:
    out = []
    for sample in dataset.samples:
        if strategies is not None and sample.ref.strategy not in strategies:
            continue
        if levels is not None and sample.ref.level not in levels:
            continue
        out.append(sample)
    return out


def _sample_sizes_by_level(samples: list[Sample]) -> dict[str, int]:
    grouped: dict[str, list[int]] = defaultdict(list)
    for sample in samples:
        grouped[sample.ref.level].append(len(_unique_preserve_order(sample.indices)))
    return {level: int(round(_median(sizes))) for level, sizes in grouped.items()}


def _with_srs_samples(
    dataset: RunDataset,
    samples: list[Sample],
    *,
    context: str,
    seeds: int,
    step_size: int,
    p_threshold: float,
    extreme: str,
) -> list[Sample]:
    by_level = _sample_sizes_by_level(samples)
    generated = list(samples)
    for level, size in sorted(by_level.items()):
        for seed in range(1, seeds + 1):
            indices = srs_indices(
                dataset.X,
                dataset.y,
                size,
                rng=seed,
                step_sample_size=step_size,
                p_threshold=p_threshold,
                extreme=extreme,  # type: ignore[arg-type]
            )
            generated.append(
                Sample(
                    ref=SampleRef(
                        context=context,
                        run_id=seed,
                        strategy="SRSSampling",
                        level=level,
                        zip_member=f"generated:SRS:{context}:{level}:seed{seed}",
                    ),
                    indices=indices,
                )
            )
    return generated


def posterior_records(dataset: RunDataset, samples: list[Sample], *, extreme: str) -> list[dict[str, Any]]:
    rows = []
    n_configs = len(dataset.y)
    full_cost = dataset.full_cost
    for sample in samples:
        indices = _unique_preserve_order(sample.indices)
        bound = sample_risk_bound(dataset.y, indices, extreme=extreme)  # type: ignore[arg-type]
        train_cost = float(np.sum(dataset.cost_values[indices]))
        pct_n = len(indices) / n_configs
        pct_cost = train_cost / full_cost
        rows.append(
            {
                "context": dataset.context,
                "run": sample.ref.run_id,
                "strategy": sample.ref.strategy,
                "level": sample.ref.level,
                "n": len(indices),
                "pct_n": pct_n,
                "train_cost": train_cost,
                "pct_cost": pct_cost,
                "effective_n_by_cost": pct_cost * n_configs,
                "calibration_ratio": pct_cost / pct_n if pct_n else float("nan"),
                "posterior_risk": bound.risk,
                "n_violations": bound.n_violations,
                "sample_bound": bound.bound,
                "extreme": extreme,
                "zip_member": sample.ref.zip_member,
            }
        )
    rows.sort(key=lambda row: (row["strategy"], row["level"], row["run"]))
    return rows


def posterior_summary(
    records: list[dict[str, Any]],
    *,
    n_configurations: int,
    prior_offset: int,
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in records:
        grouped[(row["strategy"], row["level"])].append(row)

    out = []
    for (strategy, level), rows in grouped.items():
        risks = np.array([row["posterior_risk"] for row in rows], dtype=float)
        sample_size = _median([row["n"] for row in rows])
        effective_n = _median([row["effective_n_by_cost"] for row in rows])
        size_conf = integrated_confidence(risks, sample_size, exponent_offset=prior_offset)
        cost_conf = integrated_confidence(risks, effective_n, exponent_offset=prior_offset)
        q1_risk, q3_risk = _iqr([float(row["posterior_risk"]) for row in rows])
        q1_ratio, q3_ratio = _iqr([float(row["calibration_ratio"]) for row in rows])
        out.append(
            {
                "context": rows[0]["context"],
                "strategy": strategy,
                "level": level,
                "runs": len(rows),
                "n": sample_size,
                "pct_n": sample_size / n_configurations,
                "median_train_cost": _median([float(row["train_cost"]) for row in rows]),
                "median_pct_cost": _median([float(row["pct_cost"]) for row in rows]),
                "median_effective_n_by_cost": effective_n,
                "median_calibration_ratio": _median([float(row["calibration_ratio"]) for row in rows]),
                "q1_calibration_ratio": q1_ratio,
                "q3_calibration_ratio": q3_ratio,
                "median_posterior_risk": _median([float(row["posterior_risk"]) for row in rows]),
                "q1_posterior_risk": q1_risk,
                "q3_posterior_risk": q3_risk,
                "min_posterior_risk": float(np.min(risks)),
                "max_posterior_risk": float(np.max(risks)),
                "posterior_confidence_area": size_conf.posterior_area,
                "prior_confidence_area_size": size_conf.prior_area,
                "omega_size_baseline": size_conf.omega,
                "omega_size_over_max": size_conf.omega_over_max,
                "prior_confidence_area_cost": cost_conf.prior_area,
                "omega_cost_baseline": cost_conf.omega,
                "omega_cost_over_max": cost_conf.omega_over_max,
                "posterior_area_per_pct_cost": (
                    size_conf.posterior_area / _median([float(row["pct_cost"]) for row in rows])
                    if _median([float(row["pct_cost"]) for row in rows]) > 0
                    else float("nan")
                ),
            }
        )
    out.sort(key=lambda row: (level_sort_key(row["level"]), strategy_sort_key(row["strategy"])))
    return out


def confidence_curves(
    records: list[dict[str, Any]],
    *,
    epsilon_points: int,
    prior_offset: int,
) -> list[dict[str, object]]:
    grid = np.linspace(0.0, 1.0, epsilon_points)
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in records:
        grouped[(row["context"], row["strategy"], row["level"])].append(row)

    out = []
    for (context, strategy, level), rows in grouped.items():
        risks = np.array([row["posterior_risk"] for row in rows], dtype=float)
        sample_size = _median([float(row["n"]) for row in rows])
        out.extend(
            confidence_curve_rows(
                context=context,
                strategy=strategy,
                level=level,
                risks=risks,
                sample_size=sample_size,
                epsilon_grid=grid,
                exponent_offset=prior_offset,
            )
        )
    return out


def posterior_pareto(summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not summary:
        return []
    count_cost = np.array([row["pct_n"] for row in summary], dtype=float)
    empirical_cost = np.array([row["median_pct_cost"] for row in summary], dtype=float)
    risk = np.array([row["median_posterior_risk"] for row in summary], dtype=float)
    confidence_loss = -np.array([row["posterior_confidence_area"] for row in summary], dtype=float)

    count_risk = pareto_mask(count_cost, risk)
    empirical_risk = pareto_mask(empirical_cost, risk)
    count_conf = pareto_mask(count_cost, confidence_loss)
    empirical_conf = pareto_mask(empirical_cost, confidence_loss)

    rows = []
    for idx, row in enumerate(summary):
        item = dict(row)
        item["pareto_count_cost_risk"] = int(count_risk[idx])
        item["pareto_empirical_cost_risk"] = int(empirical_risk[idx])
        item["pareto_count_cost_confidence"] = int(count_conf[idx])
        item["pareto_empirical_cost_confidence"] = int(empirical_conf[idx])
        rows.append(item)
    return rows


def level_confidence_frontiers(level_summary: list[dict[str, Any]]) -> tuple[set[str], set[str]]:
    """Return count-cost and empirical-cost confidence Pareto labels within one level."""

    if not level_summary:
        return set(), set()
    count_cost = np.array([row["pct_n"] for row in level_summary], dtype=float)
    empirical_cost = np.array([row["median_pct_cost"] for row in level_summary], dtype=float)
    confidence_loss = -np.array([row["posterior_confidence_area"] for row in level_summary], dtype=float)
    count_front = pareto_mask(count_cost, confidence_loss)
    empirical_front = pareto_mask(empirical_cost, confidence_loss)
    count_labels = {
        _strategy_level_label(row)
        for row, is_frontier in zip(level_summary, count_front)
        if is_frontier
    }
    empirical_labels = {
        _strategy_level_label(row)
        for row, is_frontier in zip(level_summary, empirical_front)
        if is_frontier
    }
    return count_labels, empirical_labels


def _strategy_level_label(row: dict[str, Any]) -> str:
    return f"{row['strategy']}_{row['level']}"


def _hypothesis_row(
    *,
    hypothesis: str,
    question: str,
    scope: str,
    statistic: str,
    statistic_value: float,
    p_value: float | None,
    effect: str,
    effect_value: float,
    effect_label: str,
    verdict: str,
    notes: str,
) -> dict[str, Any]:
    return {
        "hypothesis": hypothesis,
        "question": question,
        "scope": scope,
        "statistic": statistic,
        "statistic_value": statistic_value,
        "p_value": float(p_value) if p_value is not None else float("nan"),
        "effect": effect,
        "effect_value": effect_value,
        "effect_label": effect_label,
        "verdict": verdict,
        "notes": notes,
    }


def _omega_gap_label(gap: float) -> str:
    gap = abs(gap)
    if gap >= 0.01:
        return "large"
    if gap >= 0.001:
        return "moderate"
    if gap >= 0.0001:
        return "small"
    return "negligible"


def _risk_spread_label(spread: float) -> str:
    if spread >= 0.05:
        return "large"
    if spread >= 0.01:
        return "moderate"
    if spread >= 0.001:
        return "small"
    return "negligible"


def posterior_hypothesis_tests(
    records: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    pareto: list[dict[str, Any]],
    *,
    context: str,
) -> list[dict[str, Any]]:
    tests: list[dict[str, Any]] = []
    levels = sorted({row["level"] for row in records}, key=level_sort_key)

    for level in levels:
        level_records = [row for row in records if row["level"] == level]
        strategies = sorted({row["strategy"] for row in level_records}, key=strategy_sort_key)
        risk_groups = [
            [float(row["posterior_risk"]) for row in level_records if row["strategy"] == strategy]
            for strategy in strategies
        ]
        if len([group for group in risk_groups if group]) >= 2:
            result = kruskal_wallis(risk_groups)
            medians = {
                strategy: _median([float(row["posterior_risk"]) for row in level_records if row["strategy"] == strategy])
                for strategy in strategies
            }
            spread = max(medians.values()) - min(medians.values())
            p_value = result["p_value"]
            eta = result["eta_squared"]
            if math.isfinite(p_value) and p_value < 0.05 and eta >= 0.01:
                verdict = "supports"
            elif math.isfinite(p_value) and p_value >= 0.05 and eta < 0.01:
                verdict = "refutes"
            else:
                verdict = "inconclusive"
            median_text = ", ".join(f"{strategy}={_fmt(value)}" for strategy, value in medians.items())
            tests.append(
                _hypothesis_row(
                    hypothesis="FSE1",
                    question="Posterior risk differs across sampling strategies at the same nominal budget.",
                    scope=f"{context}:{level}",
                    statistic="kruskal_wallis_H",
                    statistic_value=float(result["H"]),
                    p_value=p_value,
                    effect="eta_squared",
                    effect_value=float(eta),
                    effect_label=_risk_spread_label(spread),
                    verdict=verdict,
                    notes=f"median risks: {median_text}; spread={_fmt(spread)}",
                )
            )

    for level in sorted({row["level"] for row in summary}, key=level_sort_key):
        level_records = [row for row in records if row["level"] == level]
        level_summary = [
            row for row in summary if row["level"] == level
        ]
        level_summary.sort(key=lambda row: strategy_sort_key(row["strategy"]))
        best_size = max(level_summary, key=lambda row: row["omega_size_baseline"])
        best_cost = max(level_summary, key=lambda row: row["omega_cost_baseline"])
        count_front, empirical_front = level_confidence_frontiers(level_summary)
        changed = _strategy_level_label(best_size) != _strategy_level_label(best_cost)
        tests.append(
            _hypothesis_row(
                hypothesis="FSE2",
                question="Cost-normalized integrated confidence changes the top recommendation.",
                scope=f"{context}:{level}",
                statistic="top_recommendation_changed",
                statistic_value=1.0 if changed else 0.0,
                p_value=None,
                effect="omega_cost_gap_against_size_best",
                effect_value=float(best_cost["omega_cost_baseline"] - best_size["omega_cost_baseline"]),
                effect_label="changed" if changed else "unchanged",
                verdict="supports" if changed else "refutes",
                notes=(
                    f"best size-normalized={_strategy_level_label(best_size)}; "
                    f"best cost-normalized={_strategy_level_label(best_cost)}"
                ),
            )
        )

        srs = next((row for row in level_summary if row["strategy"] == "SRSSampling"), None)
        if srs is None:
            tests.append(
                _hypothesis_row(
                    hypothesis="FSE3",
                    question="SRS remains the best recommendation after empirical-cost normalization.",
                    scope=f"{context}:{level}",
                    statistic="srs_best_cost_normalized",
                    statistic_value=float("nan"),
                    p_value=None,
                    effect="best_minus_srs_omega_cost",
                    effect_value=float("nan"),
                    effect_label="missing",
                    verdict="inconclusive",
                    notes="No SRSSampling rows in the selected sample set.",
                )
            )
        else:
            gap = float(best_cost["omega_cost_baseline"] - srs["omega_cost_baseline"])
            tied_best = abs(gap) <= 1e-12
            srs_frontier = _strategy_level_label(srs) in empirical_front
            tests.append(
                _hypothesis_row(
                    hypothesis="FSE3",
                    question="SRS remains the best recommendation after empirical-cost normalization.",
                    scope=f"{context}:{level}",
                    statistic="srs_best_cost_normalized",
                    statistic_value=1.0 if tied_best else 0.0,
                    p_value=None,
                    effect="best_minus_srs_omega_cost",
                    effect_value=gap,
                    effect_label="best" if tied_best else _omega_gap_label(gap),
                    verdict="supports" if tied_best else "refutes",
                    notes=(
                        f"best cost-normalized={_strategy_level_label(best_cost)}; "
                        f"SRS on empirical cost/confidence Pareto={srs_frontier}"
                    ),
                )
            )

        union = count_front | empirical_front
        jaccard = len(count_front & empirical_front) / len(union) if union else 1.0
        if jaccard < 0.5:
            label = "large frontier change"
        elif jaccard < 1.0:
            label = "frontier change"
        else:
            label = "same frontier"
        tests.append(
            _hypothesis_row(
                hypothesis="FSE4",
                question="Empirical-cost normalization changes the confidence Pareto frontier.",
                scope=f"{context}:{level}",
                statistic="pareto_jaccard",
                statistic_value=jaccard,
                p_value=None,
                effect="frontier_symmetric_difference",
                effect_value=float(len(count_front ^ empirical_front)),
                effect_label=label,
                verdict="supports" if jaccard < 1.0 else "refutes",
                notes=(
                    f"count front={','.join(sorted(count_front)) or 'empty'}; "
                    f"empirical front={','.join(sorted(empirical_front)) or 'empty'}"
                ),
            )
        )

        srs_risk = [
            float(row["posterior_risk"])
            for row in level_records
            if row["strategy"] == "SRSSampling"
        ]
        random_risk = [
            float(row["posterior_risk"])
            for row in level_records
            if row["strategy"] == "random"
        ]
        if srs_risk and random_risk:
            result = mann_whitney_u(srs_risk, random_risk)
            a12 = result["A12"]
            p_value = result["p_value"]
            if math.isfinite(p_value) and p_value < 0.05 and a12 < 0.44:
                verdict = "supports"
            elif math.isfinite(p_value) and p_value < 0.05 and a12 > 0.56:
                verdict = "refutes"
            elif abs(a12 - 0.5) < 0.06:
                verdict = "refutes"
            else:
                verdict = "inconclusive"
            tests.append(
                _hypothesis_row(
                    hypothesis="FSE5",
                    question="SRS has lower posterior risk than random sampling.",
                    scope=f"{context}:{level}",
                    statistic="mann_whitney_U",
                    statistic_value=float(result["U"]),
                    p_value=p_value,
                    effect="A12_SRS_greater_risk_than_random",
                    effect_value=float(a12),
                    effect_label=vd_magnitude(a12),
                    verdict=verdict,
                    notes=(
                        "A12<0.5 means SRS risks tend to be lower; "
                        f"median SRS={_fmt(_median(srs_risk))}, median random={_fmt(_median(random_risk))}"
                    ),
                )
            )

        srs_cost = [
            float(row["pct_cost"])
            for row in level_records
            if row["strategy"] == "SRSSampling"
        ]
        random_cost = [
            float(row["pct_cost"])
            for row in level_records
            if row["strategy"] == "random"
        ]
        if srs_cost and random_cost:
            result = mann_whitney_u(srs_cost, random_cost)
            a12 = result["A12"]
            p_value = result["p_value"]
            non_negligible = abs(a12 - 0.5) >= 0.06
            if math.isfinite(p_value) and p_value < 0.05 and non_negligible:
                verdict = "supports"
            elif (not math.isfinite(p_value) or p_value >= 0.05) and not non_negligible:
                verdict = "refutes"
            else:
                verdict = "inconclusive"
            tests.append(
                _hypothesis_row(
                    hypothesis="FSE6",
                    question="SRS and random sampling have different empirical acquisition costs.",
                    scope=f"{context}:{level}",
                    statistic="mann_whitney_U",
                    statistic_value=float(result["U"]),
                    p_value=p_value,
                    effect="A12_SRS_greater_cost_than_random",
                    effect_value=float(a12),
                    effect_label=vd_magnitude(a12),
                    verdict=verdict,
                    notes=(
                        "A12>0.5 means SRS costs tend to be higher; "
                        f"median SRS={_fmt(_median(srs_cost))}, median random={_fmt(_median(random_cost))}"
                    ),
                )
            )

    return tests


def posterior_hypothesis_summary(tests: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_hypothesis: dict[str, Counter[str]] = defaultdict(Counter)
    question_by_hypothesis: dict[str, str] = {}
    for row in tests:
        by_hypothesis[row["hypothesis"]][row["verdict"]] += 1
        question_by_hypothesis[row["hypothesis"]] = row["question"]
    out = []
    for hypothesis in sorted(by_hypothesis):
        counts = by_hypothesis[hypothesis]
        out.append(
            {
                "hypothesis": hypothesis,
                "question": question_by_hypothesis[hypothesis],
                "supports": counts.get("supports", 0),
                "refutes": counts.get("refutes", 0),
                "inconclusive": counts.get("inconclusive", 0),
                "total": sum(counts.values()),
            }
        )
    return out


def write_figures(
    output_dir: Path,
    *,
    records: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    curves: list[dict[str, Any]],
    pareto: list[dict[str, Any]],
    epsilon_max: float,
) -> list[str]:
    from cost_sampling.plots import (
        plot_posterior_confidence_discrepancy,
        plot_posterior_cost_frontier,
        plot_posterior_omega,
        plot_posterior_risk_distribution,
    )

    figures = [
        ("fig_posterior_risk_by_strategy.png", plot_posterior_risk_distribution, records),
        ("fig_confidence_discrepancy.png", plot_posterior_confidence_discrepancy, curves),
        ("fig_guarantee_cost_frontier.png", plot_posterior_cost_frontier, pareto),
        ("fig_integrated_confidence_discrepancy.png", plot_posterior_omega, summary),
    ]
    written: list[str] = []
    for filename, plotter, rows in figures:
        if not rows:
            continue
        output = output_dir / filename
        if filename == "fig_confidence_discrepancy.png":
            plotter(rows, output, epsilon_max=epsilon_max)
        else:
            plotter(rows, output)
        written.append(filename)
    return written


def write_report(
    output: Path,
    *,
    context: str,
    n_configurations: int,
    summary: list[dict[str, Any]],
    pareto: list[dict[str, Any]],
    hypotheses: list[dict[str, Any]],
    figures: list[str],
    include_srs: bool,
    prior_offset: int,
    extreme: str,
) -> None:
    best_risk = min(summary, key=lambda row: row["median_posterior_risk"])
    best_cost_norm = max(summary, key=lambda row: row["omega_cost_baseline"])
    empirical_conf_front = [
        row for row in pareto if row["pareto_empirical_cost_confidence"]
    ]
    lines = [
        f"# {context} FSE-style posterior guarantee report",
        "",
        "## Scope",
        "",
        f"This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. "
        f"The bound direction is `{extreme}` over {n_configurations} reconstructed configurations.",
        "",
        "The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with "
        f"`offset={prior_offset}`. The default offset of 1 matches the FSE 2026 artifact notebook.",
        "",
        f"SRS generated in this run: `{include_srs}`. When enabled, the implementation uses the FSE artifact defaults: "
        "`step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.",
        "",
        "## Headline",
        "",
        f"Lowest median posterior risk: `{best_risk['strategy']}_{best_risk['level']}` "
        f"(risk {_fmt(best_risk['median_posterior_risk'])}, %cost {_fmt(best_risk['median_pct_cost'])}).",
        "",
        f"Best integrated confidence after normalizing the prior baseline by empirical cost: "
        f"`{best_cost_norm['strategy']}_{best_cost_norm['level']}` "
        f"(omega_cost {_fmt(best_cost_norm['omega_cost_baseline'])}, %cost {_fmt(best_cost_norm['median_pct_cost'])}).",
        "",
        "Empirical cost/confidence Pareto front:",
        "",
    ]
    lines.extend(
        [
            f"- `{row['strategy']}_{row['level']}`: posterior area {_fmt(row['posterior_confidence_area'])}, "
            f"risk {_fmt(row['median_posterior_risk'])}, %cost {_fmt(row['median_pct_cost'])}, "
            f"omega_cost {_fmt(row['omega_cost_baseline'])}"
            for row in empirical_conf_front
        ]
    )
    lines.extend(
        [
            "",
            "## Figures",
            "",
        ]
    )
    if figures:
        lines.extend(
            [
                f"- `{name}`"
                for name in figures
            ]
        )
    else:
        lines.append("No figures were generated.")
    lines.extend(
        [
            "",
            "## Hypothesis Tests",
            "",
            "| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |",
            "|---|---|---|---:|---:|---|---|",
        ]
    )
    for row in hypotheses:
        lines.append(
            f"| `{row['hypothesis']}` | `{row['scope']}` | `{row['verdict']}` | "
            f"{_fmt(float(row['statistic_value']))} | {_fmt_p(float(row['p_value']))} | "
            f"{row['effect_label']} ({_fmt(float(row['effect_value']))}) | {row['notes']} |"
        )
    lines.extend(
        [
            "",
            "## Strategy Summary",
            "",
            "| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in summary:
        lines.append(
            f"| `{row['strategy']}_{row['level']}` | {_fmt(row['n'])} | {_fmt(row['pct_n'])} | "
            f"{_fmt(row['median_pct_cost'])} | {_fmt(row['median_posterior_risk'])} | "
            f"{_fmt(row['posterior_confidence_area'])} | {_fmt(row['omega_size_baseline'])} | "
            f"{_fmt(row['omega_cost_baseline'])} |"
        )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir or f"artifacts/fse_posterior_{args.context}")
    output_dir.mkdir(parents=True, exist_ok=True)

    strategies = _parse_set(args.strategies)
    levels = _parse_set(args.levels)
    if args.fse_root:
        dataset = load_fse_directory_dataset(
            args.fse_root,
            args.context,
            max_runs=args.max_runs,
            strategies=strategies,
            levels=levels,
            performance_name=args.performance_name,
        )
        samples = list(dataset.samples)
    else:
        dataset = load_runs_dataset(
            args.runs_zip,
            args.context,
            max_runs=args.max_runs,
            performance_name=args.performance_name,
        )
        samples = _filtered_samples(dataset, strategies, levels)
    if not samples:
        raise SystemExit("No samples matched the requested strategies/levels")
    if args.include_srs and not any(sample.ref.strategy == "SRSSampling" for sample in samples):
        samples = _with_srs_samples(
            dataset,
            samples,
            context=args.context,
            seeds=args.srs_seeds,
            step_size=args.srs_step_size,
            p_threshold=args.srs_p_threshold,
            extreme=args.extreme,
        )
    elif args.include_srs:
        print("SRS samples already present in the selected sample set; not generating duplicates.")
    dataset = replace(dataset, samples=samples)

    records = posterior_records(dataset, dataset.samples, extreme=args.extreme)
    summary = posterior_summary(
        records,
        n_configurations=len(dataset.y),
        prior_offset=args.prior_offset,
    )
    curves = confidence_curves(
        records,
        epsilon_points=args.epsilon_points,
        prior_offset=args.prior_offset,
    )
    pareto = posterior_pareto(summary)
    hypotheses = posterior_hypothesis_tests(records, summary, pareto, context=args.context)
    hypothesis_summary = posterior_hypothesis_summary(hypotheses)
    figures = write_figures(
        output_dir,
        records=records,
        summary=summary,
        curves=curves,
        pareto=pareto,
        epsilon_max=args.plot_epsilon_max,
    )

    write_csv(output_dir / "posterior_records.csv", records)
    write_csv(output_dir / "posterior_strategy_summary.csv", summary)
    write_csv(output_dir / "posterior_confidence_curves.csv", curves)
    write_csv(output_dir / "posterior_pareto.csv", pareto)
    write_csv(output_dir / "posterior_hypothesis_tests.csv", hypotheses)
    write_csv(output_dir / "posterior_hypothesis_summary.csv", hypothesis_summary)
    write_report(
        output_dir / f"{args.context}_fse_posterior_report.md",
        context=args.context,
        n_configurations=len(dataset.y),
        summary=summary,
        pareto=pareto,
        hypotheses=hypotheses,
        figures=figures,
        include_srs=args.include_srs,
        prior_offset=args.prior_offset,
        extreme=args.extreme,
    )
    print(f"Wrote FSE-style posterior guarantee outputs to {output_dir}")


if __name__ == "__main__":
    main()
