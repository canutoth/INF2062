#!/usr/bin/env python3
"""Summarize the Linux HGBT all-feature strategy-complete one-budget pilot."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
import statistics
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        default="artifacts/linux_hgbt_strategy_complete_pilot_all",
        help="Directory containing linux*_vmlinux pilot outputs.",
    )
    return parser.parse_args()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def fnum(row: dict[str, str], key: str) -> float:
    return float(row[key])


def median(values: list[float]) -> float:
    return float(statistics.median(values))


def fmt(value: float) -> str:
    return f"{value:.3g}"


def release_from_dir(path: Path) -> str:
    return path.name.split("_")[0].replace("linux", "")


def strategy_rows(input_dir: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(input_dir.glob("linux*_vmlinux/strategy_summary.csv")):
        release = release_from_dir(path.parent)
        for row in read_rows(path):
            rows.append(
                {
                    "release": release,
                    "strategy": row["strategy"],
                    "level": row["level"],
                    "n": int(float(row["n"])),
                    "pct_n": fnum(row, "pct_n"),
                    "cost_over_random": fnum(row, "cost_over_random"),
                    "calibration_ratio": fnum(row, "median_calibration_ratio"),
                    "mre": fnum(row, "median_mre"),
                    "pct_cost": fnum(row, "median_pct_cost"),
                }
            )
    return rows


def decision_rows(input_dir: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for run_dir in sorted(input_dir.glob("linux*_vmlinux")):
        release = release_from_dir(run_dir)
        ranks = read_rows(run_dir / "rq3_rank_stability.csv")
        pareto = read_rows(run_dir / "rq4_pareto.csv")
        top1_size = Counter(row["top1_size"] for row in ranks)
        top1_time = Counter(row["top1_time"] for row in ranks)
        count_pairs = sorted(
            f"{row['strategy']}_{row['level']}"
            for row in pareto
            if int(float(row["pareto_count"])) == 1
        )
        empirical_pairs = sorted(
            f"{row['strategy']}_{row['level']}"
            for row in pareto
            if int(float(row["pareto_empirical"])) == 1
        )
        overlap = sorted(set(count_pairs) & set(empirical_pairs))
        rows.append(
            {
                "release": release,
                "rank_top1_flips": sum(1 for row in ranks if int(float(row["top1_agreement"])) == 0),
                "rank_lambdas": len(ranks),
                "mean_kendall_tau": median([fnum(row, "kendall_tau") for row in ranks]),
                "mean_top3_overlap": median([fnum(row, "top3_overlap") for row in ranks]),
                "top1_count_mode": top1_size.most_common(1)[0][0] if top1_size else "",
                "top1_empirical_mode": top1_time.most_common(1)[0][0] if top1_time else "",
                "pareto_count_n": len(count_pairs),
                "pareto_empirical_n": len(empirical_pairs),
                "pareto_overlap_n": len(overlap),
                "pareto_jaccard": len(overlap) / len(set(count_pairs) | set(empirical_pairs))
                if set(count_pairs) | set(empirical_pairs)
                else 1.0,
                "pareto_count_pairs": ", ".join(count_pairs),
                "pareto_empirical_pairs": ", ".join(empirical_pairs),
            }
        )
    return rows


def aggregate_strategy(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["strategy"]].append(row)
    out: list[dict[str, Any]] = []
    for strategy, values in sorted(grouped.items()):
        cost = [row["cost_over_random"] for row in values]
        mre = [row["mre"] for row in values]
        calibration = [row["calibration_ratio"] for row in values]
        out.append(
            {
                "strategy": strategy,
                "releases": len(values),
                "median_cost_over_random": median(cost),
                "min_cost_over_random": min(cost),
                "max_cost_over_random": max(cost),
                "median_mre": median(mre),
                "min_mre": min(mre),
                "max_mre": max(mre),
                "median_calibration_ratio": median(calibration),
            }
        )
    return out


def write_report(
    output: Path,
    *,
    strategy: list[dict[str, Any]],
    aggregate: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> None:
    best_mre = min(strategy, key=lambda row: row["mre"])
    cheapest = min(strategy, key=lambda row: row["cost_over_random"])
    flips = sum(row["rank_top1_flips"] for row in decisions)
    lambdas = sum(row["rank_lambdas"] for row in decisions)
    pareto_changed = sum(1 for row in decisions if row["pareto_jaccard"] < 1.0)

    lines = [
        "# Linux HGBT strategy-complete pilot",
        "",
        "## Scope",
        "",
        "This is a one-budget, one-seed pilot over all seven Linux releases. It restores `coverage`, "
        "`diversity`, and `uncertainty` for the all-feature `sk-hgbt-log` Linux setting. It is useful "
        "for checking whether the narrow HGBT Linux panel missed important decision behavior, but it "
        "is not a replacement for the full multi-budget, multi-seed Linux experiment.",
        "",
        "## Strategy-level summary",
        "",
        "| Strategy | Median cost/random | Cost range | Median MRE | MRE range | Median %cost/%n |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in aggregate:
        lines.append(
            f"| `{row['strategy']}` | {fmt(row['median_cost_over_random'])} | "
            f"{fmt(row['min_cost_over_random'])}-{fmt(row['max_cost_over_random'])} | "
            f"{fmt(row['median_mre'])} | {fmt(row['min_mre'])}-{fmt(row['max_mre'])} | "
            f"{fmt(row['median_calibration_ratio'])} |"
        )

    lines.extend(
        [
            "",
            "## Decision-level summary",
            "",
            f"Across releases and lambdas, top-1 recommendations change in {flips}/{lambdas} "
            "count-cost versus empirical-cost comparisons. The Pareto set changes in "
            f"{pareto_changed}/{len(decisions)} releases.",
            "",
            "| Release | Top-1 flips | Count top-1 mode | Empirical top-1 mode | Pareto Jaccard | Empirical Pareto |",
            "|---|---:|---|---|---:|---|",
        ]
    )
    for row in decisions:
        lines.append(
            f"| `{row['release']}` | {row['rank_top1_flips']}/{row['rank_lambdas']} | "
            f"`{row['top1_count_mode']}` | `{row['top1_empirical_mode']}` | "
            f"{fmt(row['pareto_jaccard'])} | `{row['pareto_empirical_pairs']}` |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            f"The best single observed MRE is `{best_mre['strategy']}` on Linux {best_mre['release']} "
            f"with MRE {fmt(best_mre['mre'])}. The cheapest observed strategy is "
            f"`{cheapest['strategy']}` on Linux {cheapest['release']} at "
            f"{fmt(cheapest['cost_over_random'])}x random cost, but its MRE is {fmt(cheapest['mre'])}.",
            "",
            "`coverage` is competitive with `random` and `balanced` on MRE at this budget, and it is "
            "often the count-cost winner. `uncertainty` often buys lower empirical cost, but with worse "
            "MRE in this pilot. `diversity` is consistently costly and inaccurate here. The immediate "
            "paper implication is that the previous all-feature HGBT Linux run should not be presented "
            "as a complete strategy-panel result: restoring the omitted strategies changes RQ3/RQ4 "
            "decision evidence even at one budget.",
            "",
        ]
    )
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir)
    strategy = strategy_rows(input_dir)
    decisions = decision_rows(input_dir)
    aggregate = aggregate_strategy(strategy)
    write_csv(input_dir / "combined_strategy_summary.csv", strategy)
    write_csv(input_dir / "strategy_aggregate_summary.csv", aggregate)
    write_csv(input_dir / "decision_summary.csv", decisions)
    write_report(
        input_dir / "linux_hgbt_strategy_complete_pilot_report.md",
        strategy=strategy,
        aggregate=aggregate,
        decisions=decisions,
    )
    print(f"Wrote Linux strategy-complete pilot summary under {input_dir}")


if __name__ == "__main__":
    main()
