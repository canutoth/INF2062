#!/usr/bin/env python3
"""Quantify how much count-cost recommendations lose under measured cost.

The script consumes the final primary artifact roots listed in
artifacts/final_revisit/manifest.csv. For each rank-stability decision, it
compares the count-cost top-1 recommendation with the measured-cost top-1
recommendation using the same min-max normalized objective as
cost_sampling.analysis.rank_stability:

    J_n = norm(MRE) + lambda * norm(sample-size share)
    J_c = norm(MRE) + lambda * norm(measured-cost share)

The headline metric is measured-cost regret:

    J_c(count-cost winner) - J_c(measured-cost winner)

It is zero when the recommendations agree and positive when the count-based
recommendation is less effective once measured acquisition cost is charged.
"""

from __future__ import annotations

import argparse
import csv
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


REQUIRED = ("strategy_summary.csv", "rq3_rank_stability.csv", "rq4_pareto.csv")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def fnum(value: Any, default: float = math.nan) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def median(values: list[float]) -> float:
    values = [value for value in values if math.isfinite(value)]
    return statistics.median(values) if values else math.nan


def quantile(values: list[float], q: float) -> float:
    values = sorted(value for value in values if math.isfinite(value))
    if not values:
        return math.nan
    if len(values) == 1:
        return values[0]
    pos = q * (len(values) - 1)
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return values[lo]
    return values[lo] * (hi - pos) + values[hi] * (pos - lo)


def minmax(values: list[float]) -> list[float]:
    finite = [value for value in values if math.isfinite(value)]
    if not finite:
        return [0.0 for _ in values]
    lo = min(finite)
    hi = max(finite)
    if abs(hi - lo) < 1e-12:
        return [0.0 for _ in values]
    return [(value - lo) / (hi - lo) if math.isfinite(value) else 0.0 for value in values]


def label(row: dict[str, Any]) -> str:
    return f"{row['strategy']}_{row['level']}"


def context_key(row: dict[str, Any]) -> tuple[str, str]:
    target = row.get("target_context", "")
    cost = row.get("cost_context", target)
    return str(target), str(cost)


def analysis_dirs(root: Path) -> list[Path]:
    if all((root / name).is_file() for name in REQUIRED):
        return [root]
    dirs = []
    for path in root.rglob("strategy_summary.csv"):
        directory = path.parent
        if all((directory / name).is_file() for name in REQUIRED):
            dirs.append(directory)
    return sorted(set(dirs))


def load_manifest(path: Path) -> list[dict[str, str]]:
    rows = read_csv(path)
    return [row for row in rows if row.get("role") == "primary"]


def pareto_metrics(
    family: str,
    label_name: str,
    learner: str,
    unit: str,
    pareto_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in pareto_rows:
        grouped[context_key(row)].append(row)

    out = []
    for key, rows in grouped.items():
        count_front = {label(row) for row in rows if int(fnum(row.get("pareto_count"), 0)) == 1}
        empirical_front = {label(row) for row in rows if int(fnum(row.get("pareto_empirical"), 0)) == 1}
        union = count_front | empirical_front
        out.append(
            {
                "family": family,
                "label": label_name,
                "learner": learner,
                "analysis_unit": unit,
                "target_context": key[0],
                "cost_context": key[1],
                "count_front_n": len(count_front),
                "empirical_front_n": len(empirical_front),
                "count_only_n": len(count_front - empirical_front),
                "empirical_only_n": len(empirical_front - count_front),
                "pareto_jaccard": len(count_front & empirical_front) / len(union) if union else 1.0,
            }
        )
    return out


def decision_regret_rows(manifest_row: dict[str, str], unit_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    family = manifest_row["family"]
    label_name = manifest_row["label"]
    learner = manifest_row["learner"]
    unit = str(unit_dir)
    summary_rows = read_csv(unit_dir / "strategy_summary.csv")
    rank_rows = read_csv(unit_dir / "rq3_rank_stability.csv")
    pareto_rows = read_csv(unit_dir / "rq4_pareto.csv")

    summary_by_context: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in summary_rows:
        summary_by_context[context_key(row)].append(row)

    pareto_by_context: dict[tuple[str, str], dict[str, dict[str, str]]] = defaultdict(dict)
    for row in pareto_rows:
        pareto_by_context[context_key(row)][label(row)] = row

    out = []
    skipped = 0
    for rank in rank_rows:
        key = context_key(rank)
        summary = summary_by_context.get(key, [])
        if not summary:
            skipped += 1
            continue

        labels = [label(row) for row in summary]
        index = {item: idx for idx, item in enumerate(labels)}
        count_label = rank.get("top1_size", "")
        empirical_label = rank.get("top1_time", "")
        if count_label not in index or empirical_label not in index:
            skipped += 1
            continue

        mre = [fnum(row.get("median_mre")) for row in summary]
        pct_n = [fnum(row.get("pct_n")) for row in summary]
        pct_cost = [fnum(row.get("median_pct_cost")) for row in summary]
        mre_norm = minmax(mre)
        n_norm = minmax(pct_n)
        cost_norm = minmax(pct_cost)
        lam = fnum(rank.get("lambda"), 0.0)
        j_size = [m + lam * n for m, n in zip(mre_norm, n_norm)]
        j_emp = [m + lam * c for m, c in zip(mre_norm, cost_norm)]

        c_idx = index[count_label]
        e_idx = index[empirical_label]
        c_row = summary[c_idx]
        e_row = summary[e_idx]
        c_pareto = pareto_by_context.get(key, {}).get(count_label, {})

        c_cost = fnum(c_row.get("median_pct_cost"))
        e_cost = fnum(e_row.get("median_pct_cost"))
        c_n = fnum(c_row.get("pct_n"))
        e_n = fnum(e_row.get("pct_n"))
        c_mre = fnum(c_row.get("median_mre"))
        e_mre = fnum(e_row.get("median_mre"))
        changed = int(count_label != empirical_label)

        out.append(
            {
                "family": family,
                "label": label_name,
                "learner": learner,
                "analysis_unit": unit,
                "target_context": key[0],
                "cost_context": key[1],
                "lambda": lam,
                "count_winner": count_label,
                "empirical_winner": empirical_label,
                "changed": changed,
                "count_winner_empirical_regret": j_emp[c_idx] - j_emp[e_idx],
                "count_winner_count_advantage": j_size[e_idx] - j_size[c_idx],
                "count_winner_cost_ratio_vs_empirical_winner": c_cost / e_cost if e_cost > 0 else math.nan,
                "count_winner_sample_ratio_vs_empirical_winner": c_n / e_n if e_n > 0 else math.nan,
                "count_winner_mre_delta_vs_empirical_winner": c_mre - e_mre,
                "count_winner_more_accurate_but_costlier": int(changed and c_mre < e_mre and c_cost > e_cost),
                "count_winner_less_accurate_and_costlier": int(changed and c_mre > e_mre and c_cost > e_cost),
                "count_winner_not_empirical_pareto": int(
                    changed and int(fnum(c_pareto.get("pareto_empirical"), 0)) == 0
                ),
                "count_winner_pct_n": c_n,
                "count_winner_pct_cost": c_cost,
                "count_winner_mre": c_mre,
                "empirical_winner_pct_n": e_n,
                "empirical_winner_pct_cost": e_cost,
                "empirical_winner_mre": e_mre,
            }
        )

    if skipped:
        print(f"Skipped {skipped} rank rows in {unit_dir}", flush=True)
    return out, pareto_metrics(family, label_name, learner, unit, pareto_rows)


def summarize_decisions(rows: list[dict[str, Any]], pareto_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[row["family"]].append(row)
    groups["ALL_PRIMARY"] = rows

    pareto_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in pareto_rows:
        pareto_groups[row["family"]].append(row)
    pareto_groups["ALL_PRIMARY"] = pareto_rows

    out = []
    for family in sorted(groups.keys(), key=lambda item: (item != "ALL_PRIMARY", item)):
        items = groups[family]
        changed = [row for row in items if int(row["changed"]) == 1]
        changed_costlier = [
            row for row in changed if fnum(row["count_winner_cost_ratio_vs_empirical_winner"]) > 1.0
        ]
        pareto = pareto_groups.get(family, [])
        count_front_total = sum(int(row["count_front_n"]) for row in pareto)
        empirical_front_total = sum(int(row["empirical_front_n"]) for row in pareto)
        count_only_total = sum(int(row["count_only_n"]) for row in pareto)
        empirical_only_total = sum(int(row["empirical_only_n"]) for row in pareto)
        out.append(
            {
                "family": family,
                "decision_cases": len(items),
                "changed_cases": len(changed),
                "changed_rate": len(changed) / len(items) if items else math.nan,
                "median_empirical_regret_changed": median(
                    [fnum(row["count_winner_empirical_regret"]) for row in changed]
                ),
                "q75_empirical_regret_changed": quantile(
                    [fnum(row["count_winner_empirical_regret"]) for row in changed], 0.75
                ),
                "max_empirical_regret_changed": max(
                    [fnum(row["count_winner_empirical_regret"]) for row in changed] or [math.nan]
                ),
                "median_cost_ratio_changed": median(
                    [fnum(row["count_winner_cost_ratio_vs_empirical_winner"]) for row in changed]
                ),
                "q75_cost_ratio_changed": quantile(
                    [fnum(row["count_winner_cost_ratio_vs_empirical_winner"]) for row in changed], 0.75
                ),
                "max_cost_ratio_changed": max(
                    [fnum(row["count_winner_cost_ratio_vs_empirical_winner"]) for row in changed] or [math.nan]
                ),
                "changed_costlier_rate": len(changed_costlier) / len(changed) if changed else math.nan,
                "more_accurate_but_costlier_rate": sum(
                    int(row["count_winner_more_accurate_but_costlier"]) for row in changed
                )
                / len(changed)
                if changed
                else math.nan,
                "less_accurate_and_costlier_rate": sum(
                    int(row["count_winner_less_accurate_and_costlier"]) for row in changed
                )
                / len(changed)
                if changed
                else math.nan,
                "not_empirical_pareto_rate_changed": sum(
                    int(row["count_winner_not_empirical_pareto"]) for row in changed
                )
                / len(changed)
                if changed
                else math.nan,
                "pareto_contexts": len(pareto),
                "count_front_false_positive_rate": count_only_total / count_front_total
                if count_front_total
                else math.nan,
                "empirical_front_hidden_choice_rate": empirical_only_total / empirical_front_total
                if empirical_front_total
                else math.nan,
                "median_pareto_jaccard": median([fnum(row["pareto_jaccard"]) for row in pareto]),
            }
        )
    return out


def fmt(value: Any, digits: int = 3) -> str:
    number = fnum(value)
    if not math.isfinite(number):
        return "NA"
    return f"{number:.{digits}f}"


def write_report(path: Path, summary: list[dict[str, Any]], decision_rows: list[dict[str, Any]]) -> None:
    top_strategies = Counter()
    changed = [row for row in decision_rows if int(row["changed"]) == 1]
    for row in changed:
        top_strategies[str(row["count_winner"]).split("_", 1)[0]] += 1

    lines = [
        "# Count-Cost Recommendation Regret",
        "",
        "This report quantifies how often a sampling recommendation that looks best under sample-size cost loses once measured acquisition cost is charged.",
        "",
        "Definitions:",
        "",
        "- `changed_rate`: fraction of `(context, lambda)` decisions whose top strategy--budget pair changes when measured cost replaces sample-size cost.",
        "- measured-cost regret (CSV field `empirical_regret`): `J_meas(count winner) - J_meas(measured-cost winner)`, using the same min-max-normalized MRE and measured-cost objective as the RQ3 rank-stability analysis.",
        "- `cost_ratio`: measured training cost of the count-cost winner divided by the measured-cost winner.",
        "- `more_accurate_but_costlier`: the count-cost winner has lower MRE but higher measured cost; this is a trade-off pattern, not a strict same-budget dominance claim.",
        "- `not_empirical_pareto`: the count-cost winner is not on the measured-cost Pareto frontier, so another strategy--budget pair is no less accurate and no more expensive under measured cost.",
        "",
        "## Summary",
        "",
        "| Family | Decisions | Changed | Median regret | Median cost ratio | Accurate but costlier | Not measured-cost Pareto | Count-front false positives | Hidden measured-cost pairs |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary:
        lines.append(
            f"| `{row['family']}` | {row['decision_cases']} | "
            f"{row['changed_cases']} ({fmt(row['changed_rate'])}) | "
            f"{fmt(row['median_empirical_regret_changed'])} | "
            f"{fmt(row['median_cost_ratio_changed'])} | "
            f"{fmt(row['more_accurate_but_costlier_rate'])} | "
            f"{fmt(row['not_empirical_pareto_rate_changed'])} | "
            f"{fmt(row['count_front_false_positive_rate'])} | "
            f"{fmt(row['empirical_front_hidden_choice_rate'])} |"
        )

    overall = next(row for row in summary if row["family"] == "ALL_PRIMARY")
    lines.extend(
        [
            "",
            "## Headline Reading",
            "",
            f"Across primary artifacts, `{overall['changed_cases']}/{overall['decision_cases']}` count-cost top strategy--budget pairs change under measured cost.",
            f"Among changed decisions, the median measured-cost ratio of the count winner is `{fmt(overall['median_cost_ratio_changed'])}`.",
            "The CSV and summary table retain normalized objective regret for auditability, but it is not a reader-facing effect size.",
            f"In `{fmt(overall['more_accurate_but_costlier_rate'])}` of changed decisions, the count-cost winner buys more accuracy at higher measured cost; this explains why the measured-cost objective can choose differently, but it is a trade-off.",
            f"In `{fmt(overall['not_empirical_pareto_rate_changed'])}` of changed decisions, the stronger same-budget failure appears: the count-cost winner is not on the measured-cost Pareto frontier.",
            f"Pareto analysis also shows a count-front false-positive rate of `{fmt(overall['count_front_false_positive_rate'])}` and a hidden measured-cost pair rate of `{fmt(overall['empirical_front_hidden_choice_rate'])}`.",
            "",
            "Most frequent count-cost winner strategies in changed decisions:",
            "",
        ]
    )
    for strategy, count in top_strategies.most_common(10):
        lines.append(f"- `{strategy}`: {count}")
    lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="artifacts/final_revisit/manifest.csv")
    parser.add_argument("--output-dir", default="artifacts/final_revisit")
    args = parser.parse_args()

    manifest = load_manifest(Path(args.manifest))
    all_decisions: list[dict[str, Any]] = []
    all_pareto: list[dict[str, Any]] = []
    for row in manifest:
        root = Path(row["root"])
        dirs = analysis_dirs(root)
        if not dirs:
            print(f"No analysis dirs found for {row['family']} at {root}", flush=True)
            continue
        for directory in dirs:
            decisions, pareto = decision_regret_rows(row, directory)
            all_decisions.extend(decisions)
            all_pareto.extend(pareto)

    summary = summarize_decisions(all_decisions, all_pareto)
    output = Path(args.output_dir)
    write_csv(output / "count_cost_regret.csv", all_decisions)
    write_csv(output / "count_cost_pareto_overlap.csv", all_pareto)
    write_csv(output / "count_cost_regret_summary.csv", summary)
    write_report(output / "count_cost_regret_report.md", summary, all_decisions)
    print(f"Wrote {len(all_decisions)} decision rows and {len(all_pareto)} Pareto-context rows to {output}")


if __name__ == "__main__":
    main()
