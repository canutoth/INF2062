"""Shared batch plumbing for FSE-posterior runs on generated-sampling families.

Factored from `run_fse_posterior_lcbench_batch.py` so the ENERGY (twins) and
WORKLOAD wrappers share one implementation of scope summaries, budget trends,
the per-scenario posterior pipeline, and the aggregate report. The LCBench
batch script predates this module and keeps its own copy of the same logic.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import replace
from pathlib import Path
import re
from typing import Any

from cost_sampling.analysis import level_sort_key, strategy_sort_key, write_csv
from cost_sampling.generated_sampling import (
    GeneratedDataset,
    MeasuredTable,
    build_generated_dataset,
    budget_grid,
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


def slug(value: str) -> str:
    out = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")
    return out or "value"


def pair_label(row: dict[str, Any]) -> str:
    return f"{row['strategy']}_{row['level']}"


def parse_levels(raw: str) -> list[int]:
    """Parse `n8,n16,n32` (or `8,16,32`) into sample sizes."""

    budgets: list[int] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        budgets.append(int(part[1:] if part.lower().startswith("n") else part))
    if not budgets:
        raise ValueError(f"No budgets parsed from {raw!r}")
    return sorted(set(budgets))


def clamp_budgets(budgets: list[int], n_configurations: int, *, scope: str) -> list[int]:
    """Apply the generated-protocol cap; report anything dropped."""

    grid_max = max(budget_grid(n_configurations), default=0)
    kept = [n for n in budgets if n <= grid_max]
    dropped = sorted(set(budgets) - set(kept))
    if dropped:
        print(
            f"[{scope}] dropped budgets {dropped} (universe {n_configurations}, "
            f"protocol max {grid_max})",
            flush=True,
        )
    return kept


def add_metadata(rows: list[dict[str, Any]], **extra: Any) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        item = dict(row)
        item.update(extra)
        out.append(item)
    return out


def summarize_scope_levels(
    *,
    scope: str,
    summary: list[dict[str, Any]],
    hypotheses: list[dict[str, Any]],
    scope_key: str = "scope",
) -> list[dict[str, Any]]:
    """One decision row per (scope, level): best pairs, SRS status, frontier change."""

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
                scope_key: scope,
                "context": best_cost["context"],
                "level": level,
                "n": best_cost["n"],
                "n_configurations": round(best_cost["n"] / best_cost["pct_n"]),
                "best_risk_pair": pair_label(best_risk),
                "best_risk": best_risk["median_posterior_risk"],
                "best_size_pair": pair_label(best_size),
                "best_cost_pair": pair_label(best_cost),
                "top_changed_by_cost": int(pair_label(best_size) != pair_label(best_cost)),
                "best_cost_omega": best_cost["omega_cost_baseline"],
                "srs_best_cost": int(srs is not None and pair_label(srs) == pair_label(best_cost)),
                "srs_on_empirical_confidence_front": int(
                    srs is not None and pair_label(srs) in empirical_front
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


def strategy_budget_trends(
    summary_rows: list[dict[str, Any]],
    *,
    scope_key: str = "scope",
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in summary_rows:
        grouped[(str(row[scope_key]), str(row["strategy"]))].append(row)
    out = []
    for (scope, strategy), rows in grouped.items():
        rows.sort(key=lambda row: level_sort_key(row["level"]))
        risks = [float(row["median_posterior_risk"]) for row in rows]
        areas = [float(row["posterior_confidence_area"]) for row in rows]
        omega_size = [float(row["omega_size_baseline"]) for row in rows]
        omega_cost = [float(row["omega_cost_baseline"]) for row in rows]
        out.append(
            {
                scope_key: scope,
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
    out.sort(key=lambda row: (row[scope_key], strategy_sort_key(row["strategy"])))
    return out


def verdict_counts(rows: list[dict[str, Any]], hypothesis: str) -> Counter[str]:
    counter: Counter[str] = Counter()
    for row in rows:
        if row["hypothesis"] == hypothesis:
            counter[str(row["verdict"])] += 1
    return counter


def run_posterior_scenario(
    table: MeasuredTable,
    *,
    scope_dir: Path,
    report_name: str,
    target_property: str,
    cost_property: str,
    cost_orientation: str,
    budgets: list[int],
    seeds: int,
    include_oracles: bool,
    include_srs: bool,
    srs_seeds: int,
    srs_step_size: int,
    srs_p_threshold: float,
    extreme: str,
    prior_offset: int,
    epsilon_points: int,
    plot_epsilon_max: float,
    figures_enabled: bool,
    metadata: dict[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    """Run the FSE-posterior pipeline for one measured scenario.

    Returns the aggregate row lists (records/summary/curves/pareto/hypotheses/
    hypothesis_summary) with `metadata` columns attached to each row.
    """

    dataset: GeneratedDataset = build_generated_dataset(
        table,
        target_property=target_property,
        cost_property=cost_property,
        cost_orientation=cost_orientation,
        budgets=budgets,
        seeds=seeds,
        include_oracles=include_oracles,
    )
    samples = dataset.samples
    if include_srs:
        print(f"[{metadata.get('family', 'generated')}] generating SRS for {dataset.context}", flush=True)
        samples = _with_srs_samples(
            dataset,
            samples,
            context=dataset.context,
            seeds=srs_seeds,
            step_size=srs_step_size,
            p_threshold=srs_p_threshold,
            extreme=extreme,
        )
    dataset = replace(dataset, samples=samples)

    records = add_metadata(posterior_records(dataset, dataset.samples, extreme=extreme), **metadata)
    summary = add_metadata(
        posterior_summary(records, n_configurations=len(dataset.y), prior_offset=prior_offset), **metadata
    )
    curves = add_metadata(
        confidence_curves(records, epsilon_points=epsilon_points, prior_offset=prior_offset), **metadata
    )
    pareto = add_metadata(posterior_pareto(summary), **metadata)
    hypotheses = add_metadata(
        posterior_hypothesis_tests(records, summary, pareto, context=dataset.context), **metadata
    )
    hypothesis_summary = add_metadata(posterior_hypothesis_summary(hypotheses), **metadata)

    scope_dir.mkdir(parents=True, exist_ok=True)
    figures: list[str] = []
    if figures_enabled:
        figures = write_figures(
            scope_dir,
            records=records,
            summary=summary,
            curves=curves,
            pareto=pareto,
            epsilon_max=plot_epsilon_max,
        )
    write_csv(scope_dir / "posterior_records.csv", records)
    write_csv(scope_dir / "posterior_strategy_summary.csv", summary)
    write_csv(scope_dir / "posterior_confidence_curves.csv", curves)
    write_csv(scope_dir / "posterior_pareto.csv", pareto)
    write_csv(scope_dir / "posterior_hypothesis_tests.csv", hypotheses)
    write_csv(scope_dir / "posterior_hypothesis_summary.csv", hypothesis_summary)
    write_report(
        scope_dir / report_name,
        context=dataset.context,
        n_configurations=len(dataset.y),
        summary=summary,
        pareto=pareto,
        hypotheses=hypotheses,
        figures=figures,
        include_srs=include_srs,
        prior_offset=prior_offset,
        extreme=extreme,
    )
    return {
        "records": records,
        "summary": summary,
        "curves": curves,
        "pareto": pareto,
        "hypotheses": hypotheses,
        "hypothesis_summary": hypothesis_summary,
    }


def write_family_report(
    output: Path,
    *,
    title: str,
    scope_noun: str,
    scope_rows: list[dict[str, Any]],
    trend_rows: list[dict[str, Any]],
    hypothesis_rows: list[dict[str, Any]],
    scope_key: str,
    intro_lines: list[str],
    srs_enabled: bool,
    srs_seeds: int,
    include_oracles: bool,
) -> None:
    n_scopes = len(scope_rows)
    fse1 = verdict_counts(hypothesis_rows, "FSE1")
    fse5 = verdict_counts(hypothesis_rows, "FSE5")
    fse6 = verdict_counts(hypothesis_rows, "FSE6")
    srs_best = sum(int(row["srs_best_cost"]) for row in scope_rows)
    srs_front = sum(int(row["srs_on_empirical_confidence_front"]) for row in scope_rows)
    changed_top = sum(int(row["top_changed_by_cost"]) for row in scope_rows)
    changed_front = sum(1 for row in scope_rows if float(row["pareto_jaccard"]) < 1.0)
    srs_trends = [row for row in trend_rows if row["strategy"] == "SRSSampling"]
    best_counts = Counter(row["best_cost_pair"] for row in scope_rows)

    lines = [
        f"# {title}",
        "",
        "## Scope",
        "",
        *intro_lines,
        f"SRS generated: `{srs_enabled}` with `{srs_seeds}` seeds per {scope_noun}/level.",
        f"Diagnostic oracles included: `{include_oracles}`.",
        "",
        "## Headline",
        "",
        f"Strategy posterior-risk distributions differ in {fse1.get('supports', 0)}/{n_scopes} {scope_noun}-level scopes.",
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
            f"## {scope_noun.capitalize()}-Level Summary",
            "",
            f"| {scope_noun.capitalize()} | Level | n | Best cost pair | SRS best? | SRS on front? | Jaccard |",
            "|---|---|---:|---|---:|---:|---:|",
        ]
    )
    for row in scope_rows:
        lines.append(
            f"| `{row[scope_key]}` | `{row['level']}` | {int(row['n'])} | `{row['best_cost_pair']}` | "
            f"{row['srs_best_cost']} | {row['srs_on_empirical_confidence_front']} | "
            f"{_fmt(row['pareto_jaccard'])} |"
        )

    lines.extend(
        [
            "",
            "## Budget Scaling",
            "",
            f"| Strategy | Risk non-increasing | Posterior area non-decreasing | Omega(size) >= 0 all {scope_noun}s | Omega(cost) >= 0 all {scope_noun}s |",
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
                f"{sum(int(row['risk_nonincreasing']) for row in srs_trends)}/{len(srs_trends)} {scope_noun}s "
                f"and posterior area is non-decreasing in "
                f"{sum(int(row['posterior_area_nondecreasing']) for row in srs_trends)}/{len(srs_trends)} {scope_noun}s.",
            ]
        )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
