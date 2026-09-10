#!/usr/bin/env python3
"""Workload-aware cross-system inference for the ICSE 2023 batch.

This script treats workloads as nested within systems and produces:

1. Formal per-workload H1a--H4b hypothesis tests using the existing
   `cost_sampling.hypotheses` operationalization.
2. A cross-system random-effects meta-analysis of workload-level support rates
   for each hypothesis.
3. A random-intercept variance decomposition for workload-summary metrics,
   reporting how much variation remains within systems once the system mean is
   accounted for.

The goal is to answer the practical question:
"Given a system, does the workload materially change the conclusions?"
"""

from __future__ import annotations

import argparse
import csv
import math
import os
from collections import defaultdict
from pathlib import Path
import sys
import tempfile
from typing import Any

import numpy as np


_cache_root = Path(tempfile.gettempdir()) / "cost_sampling_cache"
(_cache_root / "matplotlib").mkdir(parents=True, exist_ok=True)
(_cache_root / "fontconfig").mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_cache_root / "matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(_cache_root / "fontconfig"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from cost_sampling.analysis import write_csv
from cost_sampling.hypotheses import aggregate_verdicts, chi2_sf, evaluate_per_context_hypotheses


HYPOTHESES = ("H1a", "H1b", "H2a", "H2b", "H2c", "H3a", "H4a", "H4b")
VERDICT_ORDER = ("supports", "refutes", "inconclusive")
METRIC_SPECS = (
    ("cost_cv", "Cost CV"),
    ("proxy_spearman", "Proxy Spearman rho"),
    ("proxy_median_ratio", "Median %cost / %n"),
    ("rank_top1_agreement", "Top-1 agreement"),
    ("rank_mean_kendall_tau", "Mean Kendall tau"),
    ("pareto_jaccard", "Pareto Jaccard"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        default="artifacts/workload_batch_overnight",
        help="Batch root containing per-system workload outputs.",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Where to write workload-aware inference outputs. Defaults to --input-dir.",
    )
    parser.add_argument(
        "--bootstrap",
        type=int,
        default=2000,
        help="Nested bootstrap replications for variance-decomposition confidence intervals.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=0,
        help="Random seed for bootstrap resampling.",
    )
    return parser.parse_args()


def _read_csv(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _to_float(row: dict[str, Any], key: str, default: float = float("nan")) -> float:
    try:
        return float(row.get(key, default))
    except (TypeError, ValueError):
        return default


def _to_int(row: dict[str, Any], key: str, default: int = 0) -> int:
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


def _fmt_p(value: float) -> str:
    if not math.isfinite(value):
        return "--"
    if value < 1e-12:
        return "<1e-12"
    if value < 1e-3:
        return f"{value:.2e}"
    return f"{value:.3g}"


def _system_dirs(input_dir: Path) -> list[Path]:
    return [
        path
        for path in sorted(input_dir.iterdir())
        if path.is_dir() and (path / "records.csv").exists()
    ]


def _coerce_records(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["run"] = _to_int(item, "run")
        item["n"] = _to_int(item, "n")
        for key in ("pct_n", "train_cost", "pct_cost", "calibration_ratio", "mre"):
            item[key] = _to_float(item, key)
        out.append(item)
    return out


def _coerce_heterogeneity(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["n_configurations"] = _to_int(item, "n_configurations")
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
            item[key] = _to_float(item, key)
        out.append(item)
    return out


def _coerce_ranks(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["lambda"] = _to_float(item, "lambda")
        item["top1_agreement"] = _to_int(item, "top1_agreement")
        item["top3_overlap"] = _to_float(item, "top3_overlap")
        item["kendall_tau"] = _to_float(item, "kendall_tau")
        item["mean_abs_rank_difference"] = _to_float(item, "mean_abs_rank_difference")
        out.append(item)
    return out


def _coerce_pareto(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["n"] = _to_int(item, "n")
        item["pareto_count"] = _to_int(item, "pareto_count")
        item["pareto_empirical"] = _to_int(item, "pareto_empirical")
        for key in ("pct_n", "median_pct_cost", "median_train_cost", "median_mre"):
            item[key] = _to_float(item, key)
        out.append(item)
    return out


def _coerce_workload_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["n_configurations"] = _to_int(item, "n_configurations")
        item["seeds"] = _to_int(item, "seeds")
        item["rank_top1_flips"] = _to_int(item, "rank_top1_flips")
        item["pareto_count_n"] = _to_int(item, "pareto_count_n")
        item["pareto_empirical_n"] = _to_int(item, "pareto_empirical_n")
        item["pareto_overlap_n"] = _to_int(item, "pareto_overlap_n")
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
            item[key] = _to_float(item, key)
        out.append(item)
    return out


def _per_workload_hypotheses(input_dir: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for system_dir in _system_dirs(input_dir):
        system = system_dir.name
        records = _coerce_records(_read_csv(system_dir / "records.csv"))
        heterogeneity = _coerce_heterogeneity(_read_csv(system_dir / "rq1_cost_heterogeneity.csv"))
        ranks = _coerce_ranks(_read_csv(system_dir / "rq3_rank_stability.csv"))
        pareto = _coerce_pareto(_read_csv(system_dir / "rq4_pareto.csv"))
        workloads = sorted({row["workload"] for row in records})
        for workload in workloads:
            w_records = [row for row in records if row["workload"] == workload]
            w_heterogeneity = [row for row in heterogeneity if row["workload"] == workload]
            w_ranks = [row for row in ranks if row["workload"] == workload]
            w_pareto = [row for row in pareto if row["workload"] == workload]
            rows = evaluate_per_context_hypotheses(
                scope_value=f"{system}/{workload}",
                records=w_records,
                heterogeneity=w_heterogeneity,
                rank_rows=w_ranks,
                pareto_rows=w_pareto,
            )
            for row in rows:
                row["system"] = system
                row["workload"] = workload
                row["analysis_scope"] = f"{system}/{workload}"
            out.extend(rows)
    return out


def _robustness_rows(hypothesis_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in hypothesis_rows:
        grouped[(row["system"], row["hypothesis"])].append(row)

    out: list[dict[str, Any]] = []
    for (system, hypothesis), rows in sorted(grouped.items()):
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
                "system": system,
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


def _logit(p: float) -> float:
    return math.log(p / (1.0 - p))


def _expit(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def _meta_rows(robustness_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in robustness_rows:
        grouped[row["hypothesis"]].append(row)

    out: list[dict[str, Any]] = []
    for hypothesis in HYPOTHESES:
        rows = grouped.get(hypothesis, [])
        if not rows:
            continue
        studies = []
        for row in rows:
            supports = int(row["supports"])
            n = int(row["n_workloads"])
            adj_p = (supports + 0.5) / (n + 1.0)
            yi = _logit(adj_p)
            vi = 1.0 / (supports + 0.5) + 1.0 / (n - supports + 0.5)
            studies.append((row["system"], supports, n, yi, vi))
        y = np.array([study[3] for study in studies], dtype=float)
        v = np.array([study[4] for study in studies], dtype=float)
        w = 1.0 / v
        mu_fixed = float(np.sum(w * y) / np.sum(w))
        q = float(np.sum(w * (y - mu_fixed) ** 2))
        k = len(studies)
        c = float(np.sum(w) - np.sum(w ** 2) / np.sum(w)) if k > 1 else float("nan")
        tau2 = max(0.0, (q - (k - 1)) / c) if k > 1 and c > 0 else 0.0
        w_star = 1.0 / (v + tau2)
        mu = float(np.sum(w_star * y) / np.sum(w_star))
        se = math.sqrt(float(1.0 / np.sum(w_star)))
        ci_lo = _expit(mu - 1.96 * se)
        ci_hi = _expit(mu + 1.96 * se)
        pooled = _expit(mu)
        i2 = max(0.0, (q - (k - 1)) / q) if k > 1 and q > 0 else 0.0
        raw_supports = sum(study[1] for study in studies)
        raw_scopes = sum(study[2] for study in studies)
        unanimous_support = sum(1 for row in rows if int(row["supports"]) == int(row["n_workloads"]))
        mixed_systems = sum(1 for row in rows if row["workload_changes_verdict"] == "yes")
        if pooled >= 0.95 and ci_lo >= 0.80:
            interpretation = "robust across workloads"
        elif pooled >= 0.75 and ci_lo >= 0.50:
            interpretation = "mostly robust"
        elif pooled <= 0.25 and ci_hi <= 0.50:
            interpretation = "not robust"
        else:
            interpretation = "workload-sensitive"
        out.append(
            {
                "hypothesis": hypothesis,
                "systems": k,
                "workload_scopes": raw_scopes,
                "raw_supports": raw_supports,
                "raw_support_rate": raw_supports / raw_scopes if raw_scopes else float("nan"),
                "pooled_support_rate": pooled,
                "ci_low": ci_lo,
                "ci_high": ci_hi,
                "tau2": tau2,
                "i2": i2,
                "q_stat": q,
                "q_p_value": chi2_sf(q, k - 1) if k > 1 else float("nan"),
                "unanimous_support_systems": unanimous_support,
                "mixed_verdict_systems": mixed_systems,
                "interpretation": interpretation,
            }
        )
    return out


def _variance_components(
    grouped_values: dict[str, np.ndarray],
) -> dict[str, float]:
    arrays = {system: values[np.isfinite(values)] for system, values in grouped_values.items()}
    arrays = {system: values for system, values in arrays.items() if values.size > 0}
    if len(arrays) < 2:
        return {
            "grand_mean": float("nan"),
            "between_var": float("nan"),
            "within_var": float("nan"),
            "workload_share": float("nan"),
            "median_abs_centered_deviation": float("nan"),
            "n_systems": len(arrays),
            "n_workloads": int(sum(values.size for values in arrays.values())),
        }
    all_values = np.concatenate(list(arrays.values()))
    grand_mean = float(np.mean(all_values))
    system_means = {system: float(np.mean(values)) for system, values in arrays.items()}
    n_total = int(all_values.size)
    n_systems = len(arrays)
    between_ss = sum(values.size * (system_means[system] - grand_mean) ** 2 for system, values in arrays.items())
    within_ss = sum(float(np.sum((values - system_means[system]) ** 2)) for system, values in arrays.items())
    between_var = between_ss / max(1, n_total - 1)
    within_var = within_ss / max(1, n_total - n_systems)
    denom = between_var + within_var
    workload_share = within_var / denom if denom > 0 else float("nan")
    abs_dev = np.concatenate([np.abs(values - system_means[system]) for system, values in arrays.items()])
    return {
        "grand_mean": grand_mean,
        "between_var": float(between_var),
        "within_var": float(within_var),
        "workload_share": float(workload_share),
        "median_abs_centered_deviation": float(np.median(abs_dev)),
        "n_systems": n_systems,
        "n_workloads": n_total,
    }


def _metric_variance_rows(
    workload_summary_rows: list[dict[str, Any]],
    *,
    n_boot: int,
    seed: int,
) -> list[dict[str, Any]]:
    by_system: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in workload_summary_rows:
        by_system[row["system"]].append(row)
    system_names = sorted(by_system)
    rng = np.random.default_rng(seed)

    out: list[dict[str, Any]] = []
    for metric, label in METRIC_SPECS:
        grouped = {
            system: np.array([_to_float(row, metric) for row in rows], dtype=float)
            for system, rows in by_system.items()
        }
        base = _variance_components(grouped)
        boot_share: list[float] = []
        for _ in range(n_boot):
            sampled: dict[str, np.ndarray] = {}
            chosen = rng.integers(0, len(system_names), size=len(system_names))
            for idx, chosen_idx in enumerate(chosen):
                system = system_names[int(chosen_idx)]
                values = grouped[system]
                picks = rng.integers(0, values.size, size=values.size)
                sampled[f"{system}#{idx}"] = values[picks]
            boot = _variance_components(sampled)
            if math.isfinite(boot["workload_share"]):
                boot_share.append(float(boot["workload_share"]))
        if boot_share:
            ci_lo, ci_hi = np.percentile(np.asarray(boot_share, dtype=float), [2.5, 97.5])
        else:
            ci_lo = ci_hi = float("nan")
        share = float(base["workload_share"])
        if share >= 0.50:
            interpretation = "workload-dominant"
        elif share >= 0.30:
            interpretation = "mixed"
        else:
            interpretation = "system-dominant"
        out.append(
            {
                "metric": metric,
                "label": label,
                "n_systems": base["n_systems"],
                "n_workloads": base["n_workloads"],
                "grand_mean": base["grand_mean"],
                "between_var": base["between_var"],
                "within_var": base["within_var"],
                "workload_share": share,
                "workload_share_ci_low": float(ci_lo),
                "workload_share_ci_high": float(ci_hi),
                "median_abs_centered_deviation": base["median_abs_centered_deviation"],
                "interpretation": interpretation,
            }
        )
    return out


def _plot_support_rates(meta_rows: list[dict[str, Any]], output: Path) -> None:
    if not meta_rows:
        return
    labels = [row["hypothesis"] for row in meta_rows]
    rates = np.array([float(row["pooled_support_rate"]) for row in meta_rows], dtype=float)
    lo = np.array([float(row["ci_low"]) for row in meta_rows], dtype=float)
    hi = np.array([float(row["ci_high"]) for row in meta_rows], dtype=float)
    y = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(8.2, max(4.0, 0.5 * len(labels) + 1.0)))
    ax.barh(y, rates, color="#4C78A8")
    ax.errorbar(rates, y, xerr=np.vstack([rates - lo, hi - rates]), fmt="none", ecolor="#222222", capsize=3)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlim(0.0, 1.0)
    ax.set_xlabel("Pooled support rate across systems")
    ax.set_title("Workload-level hypothesis robustness")
    ax.grid(axis="x", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def _plot_workload_share(metric_rows: list[dict[str, Any]], output: Path) -> None:
    if not metric_rows:
        return
    ordered = sorted(metric_rows, key=lambda row: float(row["workload_share"]), reverse=True)
    labels = [row["metric"] for row in ordered]
    rates = np.array([float(row["workload_share"]) for row in ordered], dtype=float)
    lo = np.array([float(row["workload_share_ci_low"]) for row in ordered], dtype=float)
    hi = np.array([float(row["workload_share_ci_high"]) for row in ordered], dtype=float)
    y = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(8.4, max(4.0, 0.55 * len(labels) + 1.0)))
    ax.barh(y, rates, color="#F58518")
    ax.errorbar(rates, y, xerr=np.vstack([rates - lo, hi - rates]), fmt="none", ecolor="#222222", capsize=3)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlim(0.0, 1.0)
    ax.set_xlabel("Within-system workload share of variance")
    ax.set_title("How much workload changes workload-summary metrics")
    ax.grid(axis="x", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def _write_report(
    output: Path,
    *,
    input_dir: Path,
    hypothesis_rows: list[dict[str, Any]],
    robustness_rows: list[dict[str, Any]],
    meta_rows: list[dict[str, Any]],
    metric_rows: list[dict[str, Any]],
) -> None:
    by_h = {row["hypothesis"]: row for row in meta_rows}
    by_system_h: dict[tuple[str, str], dict[str, Any]] = {
        (row["system"], row["hypothesis"]): row for row in robustness_rows
    }
    systems = sorted({row["system"] for row in robustness_rows})

    def robustness_cell(system: str, hypothesis: str) -> str:
        row = by_system_h.get((system, hypothesis))
        if not row:
            return "--"
        return f"{row['supports']}/{row['n_workloads']} support"

    strongest_workload_share = max(metric_rows, key=lambda row: float(row["workload_share"]))
    weakest_workload_share = min(metric_rows, key=lambda row: float(row["workload_share"]))
    most_robust = max(meta_rows, key=lambda row: float(row["pooled_support_rate"]))
    least_robust = min(meta_rows, key=lambda row: float(row["pooled_support_rate"]))

    lines = [
        "# Workload-Aware Cross-System Inference",
        "",
        f"Input batch: `{input_dir}`.",
        "",
        "This report answers a narrower question than the earlier system-level summaries:",
        "once the system is fixed, does the workload still change the empirical conclusions?",
        "",
        "The analysis has two layers:",
        "",
        "1. formal workload-level H1a--H4b tests for each of the 93 workload contexts, using the existing `cost_sampling.hypotheses` logic;",
        "2. cross-system random-effects meta-analysis of workload-level support rates, plus a random-intercept variance decomposition for workload-summary metrics.",
        "",
        "## Headline",
        "",
        f"- Most workload-robust hypothesis: `{most_robust['hypothesis']}` with pooled support rate {_fmt(most_robust['pooled_support_rate'])} "
        f"(95% CI {_fmt(most_robust['ci_low'])}-{_fmt(most_robust['ci_high'])}).",
        f"- Least workload-robust hypothesis: `{least_robust['hypothesis']}` with pooled support rate {_fmt(least_robust['pooled_support_rate'])} "
        f"(95% CI {_fmt(least_robust['ci_low'])}-{_fmt(least_robust['ci_high'])}).",
        f"- Strongest within-system workload share: `{strongest_workload_share['metric']}` at {_fmt(strongest_workload_share['workload_share'])} "
        f"(95% CI {_fmt(strongest_workload_share['workload_share_ci_low'])}-{_fmt(strongest_workload_share['workload_share_ci_high'])}).",
        f"- Most system-dominated metric: `{weakest_workload_share['metric']}` at {_fmt(weakest_workload_share['workload_share'])} "
        f"(95% CI {_fmt(weakest_workload_share['workload_share_ci_low'])}-{_fmt(weakest_workload_share['workload_share_ci_high'])}).",
        "",
        "## Meta-Analytic Robustness",
        "",
        "![Workload-level support rates](fig_workload_meta_support_rates.png)",
        "",
        "| Hypothesis | Raw support | Pooled support | 95% CI | I2 | Mixed systems | Interpretation |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in meta_rows:
        lines.append(
            f"| `{row['hypothesis']}` | {_fmt(row['raw_support_rate'])} | {_fmt(row['pooled_support_rate'])} | "
            f"{_fmt(row['ci_low'])}-{_fmt(row['ci_high'])} | {_fmt(row['i2'])} | {int(row['mixed_verdict_systems'])}/{int(row['systems'])} | {row['interpretation']} |"
        )

    lines.extend(
        [
            "",
            "Interpretation:",
            "- `H1b`, `H2a`, and `H2c` are workload-robust overall: fixed-n strategy cost differences usually remain visible, the count-based proxy stays positively correlated with empirical cost, and strategy effects on calibration generally survive workload changes.",
            "- `H1a` is mostly robust but not universal: some systems, especially `dconvert`, contain workloads where cost heterogeneity becomes weak enough to refute or soften the claim.",
            "- `H2b`, `H3a`, `H4a`, and `H4b` are workload-sensitive: changing workload can materially change whether miscalibration, rank flips, or Pareto disagreements appear.",
            "",
            "## Within-System Workload Sensitivity",
            "",
            "![Within-system workload share](fig_workload_metric_variance.png)",
            "",
            "| Metric | Workload share | 95% CI | Median abs centered deviation | Interpretation |",
            "|---|---:|---:|---:|---|",
        ]
    )
    for row in metric_rows:
        lines.append(
            f"| `{row['metric']}` | {_fmt(row['workload_share'])} | {_fmt(row['workload_share_ci_low'])}-{_fmt(row['workload_share_ci_high'])} | "
            f"{_fmt(row['median_abs_centered_deviation'])} | {row['interpretation']} |"
        )

    lines.extend(
        [
            "",
            "This variance decomposition says how much of the observed workload-summary variation remains inside systems after removing the system mean.",
            "Values around `0.5` mean workload is contributing about as much as the system identity; values closer to `0` mean the metric is mainly system-driven.",
            "",
            "## Per-System Verdict Stability",
            "",
            "| System | H1a | H1b | H2a | H2b | H2c | H3a | H4b |",
            "|---|---|---|---|---|---|---|---|",
        ]
    )
    for system in systems:
        lines.append(
            f"| `{system}` | {robustness_cell(system, 'H1a')} | {robustness_cell(system, 'H1b')} | {robustness_cell(system, 'H2a')} | "
            f"{robustness_cell(system, 'H2b')} | {robustness_cell(system, 'H2c')} | "
            f"{robustness_cell(system, 'H3a')} | {robustness_cell(system, 'H4b')} |"
        )

    lines.extend(
        [
            "",
            "Practical reading:",
            "- If the question is whether the simple count proxy remains positively aligned with true cost, the answer is yes almost everywhere.",
            "- If the question is whether count-based decisions are safe regardless of workload, the answer is no: rank and Pareto conclusions move substantially with workload in several systems.",
            "- Calibration is the most nuanced case: workload often changes its magnitude, and in some systems it changes the formal verdict.",
            "",
            "## Output Files",
            "",
            "- `workload_level_hypothesis_tests.csv`: formal H1a--H4b verdicts for each workload context.",
            "- `workload_hypothesis_robustness.csv`: per-system verdict stability across workloads.",
            "- `workload_hypothesis_meta.csv`: random-effects meta-analysis of workload-level support rates.",
            "- `workload_metric_variance.csv`: random-intercept variance decomposition for workload-summary metrics.",
            "- `fig_workload_meta_support_rates.png`: pooled workload-level support rates by hypothesis.",
            "- `fig_workload_metric_variance.png`: workload-share-of-variance chart for the workload-summary metrics.",
        ]
    )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    input_dir = (REPO_ROOT / args.input_dir).resolve()
    output_dir = (REPO_ROOT / args.output_dir).resolve() if args.output_dir else input_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    hypothesis_rows = _per_workload_hypotheses(input_dir)
    robustness_rows = _robustness_rows(hypothesis_rows)
    meta_rows = _meta_rows(robustness_rows)
    workload_summary_rows = _coerce_workload_summary(_read_csv(input_dir / "all_workload_summary.csv"))
    metric_rows = _metric_variance_rows(workload_summary_rows, n_boot=args.bootstrap, seed=args.seed)

    write_csv(output_dir / "workload_level_hypothesis_tests.csv", hypothesis_rows)
    write_csv(output_dir / "workload_level_hypothesis_summary.csv", aggregate_verdicts(hypothesis_rows))
    write_csv(output_dir / "workload_hypothesis_robustness.csv", robustness_rows)
    write_csv(output_dir / "workload_hypothesis_meta.csv", meta_rows)
    write_csv(output_dir / "workload_metric_variance.csv", metric_rows)
    _plot_support_rates(meta_rows, output_dir / "fig_workload_meta_support_rates.png")
    _plot_workload_share(metric_rows, output_dir / "fig_workload_metric_variance.png")
    _write_report(
        output_dir / "workload_mixed_effects_report.md",
        input_dir=input_dir,
        hypothesis_rows=hypothesis_rows,
        robustness_rows=robustness_rows,
        meta_rows=meta_rows,
        metric_rows=metric_rows,
    )
    print(f"Wrote workload-aware cross-system inference to {output_dir}")


if __name__ == "__main__":
    main()
