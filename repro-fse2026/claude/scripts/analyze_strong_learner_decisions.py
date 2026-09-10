#!/usr/bin/env python3
"""Summarize decision-level effects of stronger learner experiments."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import statistics


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def median(rows: list[dict[str, str]], column: str) -> float:
    return float(statistics.median(float(row[column]) for row in rows))


def strategy(pair: str) -> str:
    return pair.split("_n", 1)[0]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def workload_rows(root: Path) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    systems = sorted(
        {
            path.name
            for path in (root / "sk-hgbt-log").iterdir()
            if (path / "workload_summary.csv").exists()
            and (root / "ridge-log" / path.name / "workload_summary.csv").exists()
        }
    )
    for system in systems:
        ridge = read_csv(root / "ridge-log" / system / "workload_summary.csv")
        hgbt = read_csv(root / "sk-hgbt-log" / system / "workload_summary.csv")
        if not ridge or not hgbt:
            continue
        paired = list(zip(ridge, hgbt))
        out.append(
            {
                "family": "WORKLOAD",
                "system": system,
                "contexts": len(paired),
                "ridge_median_mre": median(ridge, "best_simple_mre"),
                "hgbt_median_mre": median(hgbt, "best_simple_mre"),
                "ridge_median_top1_agreement": median(ridge, "rank_top1_agreement"),
                "hgbt_median_top1_agreement": median(hgbt, "rank_top1_agreement"),
                "ridge_median_pareto_jaccard": median(ridge, "pareto_jaccard"),
                "hgbt_median_pareto_jaccard": median(hgbt, "pareto_jaccard"),
                "hgbt_better_mre_contexts": sum(
                    float(h["best_simple_mre"]) < float(r["best_simple_mre"]) for r, h in paired
                ),
                "best_pair_changed_contexts": sum(r["best_simple_pair"] != h["best_simple_pair"] for r, h in paired),
                "best_strategy_changed_contexts": sum(
                    strategy(r["best_simple_pair"]) != strategy(h["best_simple_pair"]) for r, h in paired
                ),
                "hgbt_lower_top1_contexts": sum(
                    float(h["rank_top1_agreement"]) < float(r["rank_top1_agreement"]) for r, h in paired
                ),
                "hgbt_lower_pareto_contexts": sum(
                    float(h["pareto_jaccard"]) < float(r["pareto_jaccard"]) for r, h in paired
                ),
            }
        )
    return out


def linux_baseline_rows(root: Path) -> list[dict[str, object]]:
    rows = read_csv(root / "linux_sklearn_baseline_summary.csv")
    out: list[dict[str, object]] = []
    by_release: dict[str, dict[str, dict[str, str]]] = {}
    for row in rows:
        if row["learner"] != "hgbt-log" or row["budget"] != "10000":
            continue
        by_release.setdefault(row["release"], {})[row["feature_set"]] = row
    for release, values in sorted(by_release.items()):
        if "all" not in values or "topk512" not in values:
            continue
        all_mape = float(values["all"]["median_mape"])
        topk_mape = float(values["topk512"]["median_mape"])
        out.append(
            {
                "family": "LINUX",
                "release": release,
                "all_features_hgbt_mape_10k": all_mape,
                "topk512_hgbt_mape_10k": topk_mape,
                "topk_over_all_ratio": topk_mape / all_mape if all_mape else float("nan"),
            }
        )
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workload-root", default="artifacts/learner_sensitivity_sklearn_generated/workload")
    parser.add_argument("--linux-root", default="artifacts/linux_sklearn_baseline")
    parser.add_argument("--output-dir", default="artifacts/strong_learner_decision_robustness")
    args = parser.parse_args()

    output = Path(args.output_dir)
    workload = workload_rows(Path(args.workload_root))
    linux = linux_baseline_rows(Path(args.linux_root))
    write_csv(output / "workload_hgbt_vs_ridge_decisions.csv", workload)
    write_csv(output / "linux_hgbt_feature_effect.csv", linux)

    lines = [
        "# Strong learner decision robustness",
        "",
        "This diagnostic separates prediction accuracy from decision-level conclusions.",
        "",
        "## Workload slices",
        "",
        "| System | Contexts | Ridge MRE | HGBT MRE | Ridge top-1 | HGBT top-1 | Ridge Pareto | HGBT Pareto | Best pair changed | Best strategy changed |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in workload:
        lines.append(
            f"| `{row['system']}` | {row['contexts']} | {row['ridge_median_mre']:.4f} | "
            f"{row['hgbt_median_mre']:.4f} | {row['ridge_median_top1_agreement']:.4f} | "
            f"{row['hgbt_median_top1_agreement']:.4f} | {row['ridge_median_pareto_jaccard']:.4f} | "
            f"{row['hgbt_median_pareto_jaccard']:.4f} | {row['best_pair_changed_contexts']} | "
            f"{row['best_strategy_changed_contexts']} |"
        )
    lines.extend(
        [
            "",
            "## Linux feature effect",
            "",
            "| Release | HGBT all features, 10k | HGBT top-k 512, 10k | Top-k / all ratio |",
            "|---|---:|---:|---:|",
        ]
    )
    for row in linux:
        lines.append(
            f"| `{row['release']}` | {row['all_features_hgbt_mape_10k']:.4f} | "
            f"{row['topk512_hgbt_mape_10k']:.4f} | {row['topk_over_all_ratio']:.2f} |"
        )
    lines.extend(
        [
            "",
            "## Reading",
            "",
            "- RQ1/RQ2 remain learner-independent because they use sampled configurations and empirical costs.",
            "- Strong learners can substantially change MRE and the selected best pair.",
            "- The count-cost versus empirical-cost disagreement does not disappear in the completed workload slices.",
            "- For Linux, feature representation dominates: HGBT with all features is paper-like, while HGBT with top-k 512 remains poor.",
        ]
    )
    output.mkdir(parents=True, exist_ok=True)
    (output / "decision_robustness_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
