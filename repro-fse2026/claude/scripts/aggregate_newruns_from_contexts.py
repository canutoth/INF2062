#!/usr/bin/env python3
"""Aggregate NewRuns per-context outputs without rerunning learners."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from cost_sampling.analysis import write_csv
from cost_sampling.hypotheses import aggregate_verdicts, test_h3b_flip_correlation
from run_newruns_batch import (
    DEFAULT_CONTEXTS,
    plot_calibration_by_system,
    plot_cost_heterogeneity_by_system,
    plot_decision_change_by_system,
    plot_strategy_bias_heatmap,
    write_batch_report,
)


PER_CONTEXT_FILES = {
    "records": "records.csv",
    "heterogeneity": "rq1_cost_heterogeneity.csv",
    "strategy": "strategy_summary.csv",
    "proxy": "rq2_proxy_summary.csv",
    "ranks": "rq3_rank_stability.csv",
    "pareto": "rq4_pareto.csv",
    "context": "context_summary.csv",
    "hypotheses": "hypothesis_tests.csv",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        default="artifacts/strong_learner_overnight/replication/sk-hgbt-log/newruns",
        help="Directory containing one subdirectory per NewRuns context.",
    )
    parser.add_argument(
        "--contexts",
        default=",".join(DEFAULT_CONTEXTS),
        help="Comma-separated contexts to aggregate.",
    )
    return parser.parse_args()


def _coerce(value: str) -> Any:
    if value == "":
        return None
    if value == "True":
        return True
    if value == "False":
        return False
    try:
        if any(char in value for char in ".eE"):
            return float(value)
        return int(value)
    except ValueError:
        return value


def read_rows(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [{key: _coerce(value) for key, value in row.items()} for row in csv.DictReader(handle)]


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    contexts = [part.strip() for part in args.contexts.split(",") if part.strip()]

    combined: dict[str, list[dict[str, Any]]] = {key: [] for key in PER_CONTEXT_FILES}
    skipped: dict[str, str] = {}
    for context in contexts:
        context_dir = output_dir / context
        try:
            for key, filename in PER_CONTEXT_FILES.items():
                combined[key].extend(read_rows(context_dir / filename))
        except FileNotFoundError as exc:
            skipped[context] = f"missing {exc.filename}"

    write_csv(output_dir / "records.csv", combined["records"])
    write_csv(output_dir / "rq1_cost_heterogeneity.csv", combined["heterogeneity"])
    write_csv(output_dir / "strategy_summary.csv", combined["strategy"])
    write_csv(output_dir / "rq2_proxy_summary.csv", combined["proxy"])
    write_csv(output_dir / "rq3_rank_stability.csv", combined["ranks"])
    write_csv(output_dir / "rq4_pareto.csv", combined["pareto"])
    write_csv(output_dir / "system_summary.csv", combined["context"])
    write_csv(
        output_dir / "skipped_contexts.csv",
        [{"context": context, "reason": reason} for context, reason in sorted(skipped.items())],
    )

    hypotheses = list(combined["hypotheses"])
    if combined["context"]:
        h3b = test_h3b_flip_correlation(combined["context"])
        h3b["system"] = "ALL"
        h3b["cost_property"] = "performance"
        h3b["target_property"] = "performance"
        h3b["scenario"] = "global"
        hypotheses.append(h3b)
    write_csv(output_dir / "hypothesis_tests.csv", hypotheses)
    write_csv(output_dir / "hypothesis_summary.csv", aggregate_verdicts(hypotheses))

    if combined["context"]:
        plot_cost_heterogeneity_by_system(combined["context"], output_dir / "fig_rq1_cost_heterogeneity_by_system.png")
        plot_strategy_bias_heatmap(combined["strategy"], output_dir / "fig_rq1_strategy_bias_heatmap.png")
        plot_calibration_by_system(combined["context"], output_dir / "fig_rq2_calibration_by_system.png")
        plot_decision_change_by_system(combined["context"], output_dir / "fig_rq3_rq4_decision_change_by_system.png")
        write_batch_report(
            output_dir / "newruns_systems_report.md",
            context_rows=combined["context"],
            strategy_rows=combined["strategy"],
            skipped=skipped,
        )

    print(
        f"Aggregated {len(combined['context'])}/{len(contexts)} NewRuns contexts under {output_dir}. "
        f"Skipped: {len(skipped)}."
    )


if __name__ == "__main__":
    main()
