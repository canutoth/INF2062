#!/usr/bin/env python3
"""Summarize a completed LCBench generated-sampling study."""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from cost_sampling.analysis import write_csv
from cost_sampling.hypotheses import aggregate_verdicts, evaluate_per_context_hypotheses


VERDICT_ORDER = ("supports", "refutes", "inconclusive")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        default="artifacts/lcbench_data_2k_lw",
        help="LCBench study directory produced by run_lcbench_generated.py.",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Where to write summary outputs. Defaults to --input-dir.",
    )
    return parser.parse_args()


def _read_csv(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _float(row: dict[str, Any], key: str, default: float = float("nan")) -> float:
    try:
        return float(row.get(key, default))
    except (TypeError, ValueError):
        return default


def _int(row: dict[str, Any], key: str, default: int = 0) -> int:
    try:
        return int(float(row.get(key, default)))
    except (TypeError, ValueError):
        return default


def _fmt(value: Any, digits: int = 4) -> str:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not math.isfinite(x):
        return "--"
    return f"{x:.{digits}g}"


def _coerce_records(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["run"] = _int(item, "run")
        item["n"] = _int(item, "n")
        for key in ("pct_n", "train_cost", "pct_cost", "calibration_ratio", "mre"):
            item[key] = _float(item, key)
        out.append(item)
    return out


def _coerce_heterogeneity(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["n_configurations"] = _int(item, "n_configurations")
        for key in (
            "full_cost",
            "min_cost",
            "q1_cost",
            "median_cost",
            "mean_cost",
            "q3_cost",
            "max_cost",
            "std_cost",
            "cv_cost",
            "p90_over_p10",
        ):
            item[key] = _float(item, key)
        out.append(item)
    return out


def _coerce_ranks(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["lambda"] = _float(item, "lambda")
        item["top1_agreement"] = _int(item, "top1_agreement")
        item["top3_overlap"] = _float(item, "top3_overlap")
        item["kendall_tau"] = _float(item, "kendall_tau")
        item["mean_abs_rank_difference"] = _float(item, "mean_abs_rank_difference")
        out.append(item)
    return out


def _coerce_pareto(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["n"] = _int(item, "n")
        item["pareto_count"] = _int(item, "pareto_count")
        item["pareto_empirical"] = _int(item, "pareto_empirical")
        for key in ("pct_n", "median_pct_cost", "median_train_cost", "median_mre"):
            item[key] = _float(item, key)
        out.append(item)
    return out


def _coerce_workload_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["n_configurations"] = _int(item, "n_configurations")
        item["seeds"] = _int(item, "seeds")
        item["rank_top1_flips"] = _int(item, "rank_top1_flips")
        item["pareto_count_n"] = _int(item, "pareto_count_n")
        item["pareto_empirical_n"] = _int(item, "pareto_empirical_n")
        item["pareto_overlap_n"] = _int(item, "pareto_overlap_n")
        for key in (
            "full_cost",
            "cost_cv",
            "cost_p90_over_p10",
            "proxy_spearman",
            "proxy_median_ratio",
            "proxy_q1_ratio",
            "proxy_q3_ratio",
            "cost_over_random_min",
            "cost_over_random_max",
            "rank_top1_agreement",
            "rank_mean_kendall_tau",
            "rank_mean_top3_overlap",
            "pareto_jaccard",
            "best_simple_mre",
            "best_simple_pct_cost",
        ):
            item[key] = _float(item, key)
        out.append(item)
    return out


def _coerce_h5(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["statistic_value"] = _float(item, "statistic_value")
        item["p_value"] = _float(item, "p_value")
        item["effect_value"] = _float(item, "effect_value")
        out.append(item)
    return out


def _median(values: list[float]) -> float:
    finite = [value for value in values if math.isfinite(value)]
    if not finite:
        return float("nan")
    ordered = sorted(finite)
    n = len(ordered)
    mid = n // 2
    if n % 2:
        return float(ordered[mid])
    return float((ordered[mid - 1] + ordered[mid]) / 2.0)


def _study_summary_row(workload_rows: list[dict[str, Any]], h5_row: dict[str, Any] | None) -> dict[str, Any]:
    def values(key: str) -> list[float]:
        return [_float(row, key) for row in workload_rows]

    return {
        "system": "lcbench",
        "n_workloads": len(workload_rows),
        "n_configurations": _int(workload_rows[0], "n_configurations") if workload_rows else 0,
        "seeds": _int(workload_rows[0], "seeds") if workload_rows else 0,
        "target_column": workload_rows[0].get("target_property", "") if workload_rows else "",
        "cost_column": workload_rows[0].get("cost_property", "") if workload_rows else "",
        "cost_cv_min": min(values("cost_cv")) if workload_rows else float("nan"),
        "cost_cv_max": max(values("cost_cv")) if workload_rows else float("nan"),
        "cost_cv_median": _median(values("cost_cv")),
        "proxy_spearman_min": min(values("proxy_spearman")) if workload_rows else float("nan"),
        "proxy_spearman_max": max(values("proxy_spearman")) if workload_rows else float("nan"),
        "proxy_spearman_median": _median(values("proxy_spearman")),
        "proxy_median_ratio_min": min(values("proxy_median_ratio")) if workload_rows else float("nan"),
        "proxy_median_ratio_max": max(values("proxy_median_ratio")) if workload_rows else float("nan"),
        "proxy_median_ratio_median": _median(values("proxy_median_ratio")),
        "rank_top1_agreement_min": min(values("rank_top1_agreement")) if workload_rows else float("nan"),
        "rank_top1_agreement_max": max(values("rank_top1_agreement")) if workload_rows else float("nan"),
        "rank_top1_agreement_median": _median(values("rank_top1_agreement")),
        "rank_top1_flips_max": max(_int(row, "rank_top1_flips") for row in workload_rows) if workload_rows else 0,
        "rank_mean_kendall_tau_min": min(values("rank_mean_kendall_tau")) if workload_rows else float("nan"),
        "rank_mean_kendall_tau_max": max(values("rank_mean_kendall_tau")) if workload_rows else float("nan"),
        "rank_mean_kendall_tau_median": _median(values("rank_mean_kendall_tau")),
        "pareto_jaccard_min": min(values("pareto_jaccard")) if workload_rows else float("nan"),
        "pareto_jaccard_max": max(values("pareto_jaccard")) if workload_rows else float("nan"),
        "pareto_jaccard_median": _median(values("pareto_jaccard")),
        "h5a_p_value": _float(h5_row, "p_value") if h5_row else float("nan"),
        "h5a_ratio_spread": _float(h5_row, "effect_value") if h5_row else float("nan"),
        "h5a_verdict": h5_row.get("verdict", "") if h5_row else "",
    }


def _workload_level_hypotheses(
    records: list[dict[str, Any]],
    heterogeneity: list[dict[str, Any]],
    ranks: list[dict[str, Any]],
    pareto: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    workloads = sorted({row["workload"] for row in records})
    for workload in workloads:
        rows = evaluate_per_context_hypotheses(
            scope_value=f"lcbench/{workload}",
            records=[row for row in records if row["workload"] == workload],
            heterogeneity=[row for row in heterogeneity if row["workload"] == workload],
            rank_rows=[row for row in ranks if row["workload"] == workload],
            pareto_rows=[row for row in pareto if row["workload"] == workload],
        )
        for row in rows:
            row["system"] = "lcbench"
            row["workload"] = workload
            row["analysis_scope"] = f"lcbench/{workload}"
        out.extend(rows)
    return out


def _robustness_rows(hypothesis_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in hypothesis_rows:
        grouped[row["hypothesis"]].append(row)

    out: list[dict[str, Any]] = []
    for hypothesis, rows in sorted(grouped.items()):
        counts = {verdict: sum(1 for row in rows if row["verdict"] == verdict) for verdict in VERDICT_ORDER}
        scopes = len(rows)
        support_rate = counts["supports"] / scopes if scopes else float("nan")
        verdict_types = [verdict for verdict in VERDICT_ORDER if counts[verdict] > 0]
        unanimous = len(verdict_types) == 1
        majority_verdict = max(VERDICT_ORDER, key=lambda verdict: (counts[verdict], -VERDICT_ORDER.index(verdict)))
        if counts["supports"] == scopes:
            robustness = "fully robust"
        elif counts["supports"] >= max(1, math.ceil(0.8 * scopes)):
            robustness = "mostly robust"
        elif counts["supports"] == 0:
            robustness = "never supports"
        else:
            robustness = "workload-sensitive"
        out.append(
            {
                "system": "lcbench",
                "hypothesis": hypothesis,
                "n_workloads": scopes,
                "supports": counts["supports"],
                "refutes": counts["refutes"],
                "inconclusive": counts["inconclusive"],
                "support_rate": support_rate,
                "majority_verdict": majority_verdict,
                "unanimous": "yes" if unanimous else "no",
                "workload_changes_verdict": "yes" if len(verdict_types) > 1 else "no",
                "robustness": robustness,
            }
        )
    return out


def _study_level_rows(summary_row: dict[str, Any]) -> list[dict[str, Any]]:
    h5a_verdict = summary_row.get("h5a_verdict", "") or "inconclusive"
    h5a = {
        "hypothesis": "H5a",
        "scope": "system",
        "scope_value": "lcbench",
        "statistic": "h5a_p_value",
        "statistic_value": _float(summary_row, "h5a_p_value"),
        "p_value": _float(summary_row, "h5a_p_value"),
        "effect": "ratio_spread",
        "effect_value": _float(summary_row, "h5a_ratio_spread"),
        "effect_label": h5a_verdict,
        "verdict": h5a_verdict,
        "notes": (
            f"dataset-level ratio spread={_fmt(_float(summary_row, 'h5a_ratio_spread'))}; "
            f"stored H5a verdict={h5a_verdict}"
        ),
    }

    tau = _float(summary_row, "rank_mean_kendall_tau_min")
    j = _float(summary_row, "pareto_jaccard_median")
    if tau < 0.95 or j < 0.90:
        h5c_verdict = "supports"
    elif tau >= 0.99 and _float(summary_row, "pareto_jaccard_min") >= 0.95:
        h5c_verdict = "refutes"
    else:
        h5c_verdict = "inconclusive"
    if tau < 0.7:
        label = "unstable"
    elif tau < 0.9:
        label = "moderately stable"
    else:
        label = "stable"
    h5c = {
        "hypothesis": "H5c",
        "scope": "system",
        "scope_value": "lcbench",
        "statistic": "kendall_tau_min",
        "statistic_value": tau,
        "p_value": float("nan"),
        "effect": "median_pareto_jaccard",
        "effect_value": j,
        "effect_label": label,
        "verdict": h5c_verdict,
        "notes": (
            f"mean Kendall tau range {_fmt(tau)}-{_fmt(_float(summary_row, 'rank_mean_kendall_tau_max'))}; "
            f"median Pareto Jaccard={_fmt(j)}"
        ),
    }
    return [h5a, h5c]


def _write_report(
    path: Path,
    *,
    summary_row: dict[str, Any],
    robustness_rows: list[dict[str, Any]],
    study_rows: list[dict[str, Any]],
    aggregate_rows: list[dict[str, Any]],
) -> None:
    support_lookup = {row["hypothesis"]: row for row in robustness_rows}
    study_lookup = {row["hypothesis"]: row for row in study_rows}

    def verdict_text(hypothesis: str) -> str:
        if hypothesis in support_lookup:
            row = support_lookup[hypothesis]
            return (
                f"{row['supports']}/{row['n_workloads']} support, "
                f"{row['refutes']} refute, {row['inconclusive']} inconclusive "
                f"({row['robustness']})"
            )
        row = study_lookup.get(hypothesis)
        if row is not None:
            return f"{row['verdict']} ({row['notes']})"
        return "--"

    weakest_proxy = min(
        robustness_rows,
        key=lambda row: row["support_rate"] if math.isfinite(float(row["support_rate"])) else 1.0,
    ) if robustness_rows else None

    lines = [
        "# LCBench systematic study",
        "",
        "## Scope",
        "",
        f"Workloads analyzed: `{summary_row['n_workloads']}` OpenML datasets.",
        "",
        f"Configurations per dataset: `{summary_row['n_configurations']}`. Seeds per budget: `{summary_row['seeds']}`.",
        "",
        f"Target: `{summary_row['target_column']}`. Cost: `{summary_row['cost_column']}`.",
        "",
        "## Aggregate signal",
        "",
        f"- Cost heterogeneity spans CV `{_fmt(summary_row['cost_cv_min'])}` to `{_fmt(summary_row['cost_cv_max'])}`.",
        f"- Count-cost Spearman spans `{_fmt(summary_row['proxy_spearman_min'])}` to `{_fmt(summary_row['proxy_spearman_max'])}`.",
        f"- Median `%cost/%n` spans `{_fmt(summary_row['proxy_median_ratio_min'])}` to `{_fmt(summary_row['proxy_median_ratio_max'])}`.",
        f"- Top-1 agreement spans `{_fmt(summary_row['rank_top1_agreement_min'])}` to `{_fmt(summary_row['rank_top1_agreement_max'])}`.",
        f"- Pareto Jaccard spans `{_fmt(summary_row['pareto_jaccard_min'])}` to `{_fmt(summary_row['pareto_jaccard_max'])}`.",
        "",
        "## Hypothesis robustness across datasets",
        "",
        f"- `H1a`: {verdict_text('H1a')}",
        f"- `H1b`: {verdict_text('H1b')}",
        f"- `H2a`: {verdict_text('H2a')}",
        f"- `H2b`: {verdict_text('H2b')}",
        f"- `H2c`: {verdict_text('H2c')}",
        f"- `H3a`: {verdict_text('H3a')}",
        f"- `H3b`: {verdict_text('H3b')}",
        f"- `H4a`: {verdict_text('H4a')}",
        f"- `H4b`: {verdict_text('H4b')}",
        f"- `H5a`: {verdict_text('H5a')}",
        f"- `H5c`: {verdict_text('H5c')}",
    ]
    if weakest_proxy is not None:
        lines.extend(
            [
                "",
                "## Readout",
                "",
                f"- Weakest workload-level hypothesis by support rate: `{weakest_proxy['hypothesis']}` with `{_fmt(weakest_proxy['support_rate'])}` support rate.",
                (
                    f"- H5a stored verdict: `{summary_row.get('h5a_verdict', '')}` "
                    f"(p=`{_fmt(summary_row.get('h5a_p_value'))}`, spread=`{_fmt(summary_row.get('h5a_ratio_spread'))}`)."
                ),
            ]
        )
    if aggregate_rows:
        lines.extend(
            [
                "",
                "## Aggregate verdict table",
                "",
                "| Hypothesis | Supports | Refutes | Inconclusive | Global verdict |",
                "|---|---:|---:|---:|---|",
            ]
        )
        for row in aggregate_rows:
            lines.append(
                f"| `{row['hypothesis']}` | {row['supports']} | {row['refutes']} | {row['inconclusive']} | `{row['global_verdict']}` |"
            )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    input_dir = REPO_ROOT / args.input_dir
    output_dir = REPO_ROOT / args.output_dir if args.output_dir else input_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    records = _coerce_records(_read_csv(input_dir / "records.csv"))
    heterogeneity = _coerce_heterogeneity(_read_csv(input_dir / "rq1_cost_heterogeneity.csv"))
    ranks = _coerce_ranks(_read_csv(input_dir / "rq3_rank_stability.csv"))
    pareto = _coerce_pareto(_read_csv(input_dir / "rq4_pareto.csv"))
    workload_summary = _coerce_workload_summary(_read_csv(input_dir / "workload_summary.csv"))
    h5_rows = _coerce_h5(_read_csv(input_dir / "h5_workload_sensitivity.csv"))
    if not records or not workload_summary:
        raise SystemExit(f"No completed LCBench study found in {input_dir}")

    summary_row = _study_summary_row(workload_summary, h5_rows[0] if h5_rows else None)
    workload_hypotheses = _workload_level_hypotheses(records, heterogeneity, ranks, pareto)
    robustness_rows = _robustness_rows(workload_hypotheses)
    study_rows = _study_level_rows(summary_row)
    aggregate_rows = aggregate_verdicts([*workload_hypotheses, *study_rows])

    write_csv(output_dir / "study_summary.csv", [summary_row])
    write_csv(output_dir / "workload_level_hypothesis_tests.csv", workload_hypotheses)
    write_csv(output_dir / "workload_hypothesis_robustness.csv", robustness_rows)
    write_csv(output_dir / "study_level_hypothesis_tests.csv", study_rows)
    write_csv(output_dir / "hypothesis_summary.csv", aggregate_rows)
    _write_report(
        output_dir / "systematic_report.md",
        summary_row=summary_row,
        robustness_rows=robustness_rows,
        study_rows=study_rows,
        aggregate_rows=aggregate_rows,
    )
    print(f"Wrote LCBench systematic summary to {output_dir}")


if __name__ == "__main__":
    main()
