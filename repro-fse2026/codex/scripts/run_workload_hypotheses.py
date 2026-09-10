#!/usr/bin/env python3
"""Compute cross-system hypothesis summaries for a workload-impact batch."""

from __future__ import annotations

import argparse
import csv
import math
import os
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
from cost_sampling.hypotheses import aggregate_verdicts, test_h3b_flip_correlation


VERDICT_ORDER = ["supports", "refutes", "inconclusive"]
VERDICT_COLORS = {
    "supports": "#54A24B",
    "refutes": "#E45756",
    "inconclusive": "#9D9DA1",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        default="artifacts/workload_batch_overnight",
        help="Batch root containing system_summary.csv and all_workload_summary.csv.",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Where to write hypothesis outputs. Defaults to --input-dir.",
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


def _row(
    *,
    hypothesis: str,
    scope: str,
    scope_value: str,
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
        "scope": scope,
        "scope_value": scope_value,
        "statistic": float(statistic_value) if statistic_value is not None else float("nan"),
        "statistic_name": statistic,
        "p_value": float(p_value) if p_value is not None else float("nan"),
        "effect": effect,
        "effect_value": float(effect_value) if effect_value is not None else float("nan"),
        "effect_label": effect_label,
        "verdict": verdict,
        "notes": notes,
    }


def _test_h1a(row: dict[str, Any]) -> dict[str, Any]:
    cv = _float(row, "cost_cv_max")
    if cv >= 1.0:
        label = "very large"
    elif cv >= 0.5:
        label = "large"
    elif cv >= 0.2:
        label = "moderate"
    elif cv >= 0.1:
        label = "small"
    else:
        label = "negligible"
    if cv >= 0.20:
        verdict = "supports"
    elif cv < 0.10:
        verdict = "refutes"
    else:
        verdict = "inconclusive"
    return _row(
        hypothesis="H1a",
        scope="system",
        scope_value=row["system"],
        statistic="cost_cv_max",
        statistic_value=cv,
        p_value=None,
        effect="cost_cv_range",
        effect_value=cv - _float(row, "cost_cv_min"),
        effect_label=label,
        verdict=verdict,
        notes=f"cost CV range {_fmt(_float(row, 'cost_cv_min'))}-{_fmt(cv)} across {row['n_workloads']} workloads",
    )


def _test_h2a(row: dict[str, Any]) -> dict[str, Any]:
    rho = _float(row, "proxy_spearman_min")
    if abs(rho) >= 0.7:
        label = "strong"
    elif abs(rho) >= 0.4:
        label = "moderate"
    elif abs(rho) >= 0.2:
        label = "weak"
    else:
        label = "negligible"
    if rho >= 0.50:
        verdict = "supports"
    elif rho <= 0.10:
        verdict = "refutes"
    else:
        verdict = "inconclusive"
    return _row(
        hypothesis="H2a",
        scope="system",
        scope_value=row["system"],
        statistic="proxy_spearman_min",
        statistic_value=rho,
        p_value=None,
        effect="rho_range",
        effect_value=_float(row, "proxy_spearman_max") - rho,
        effect_label=label,
        verdict=verdict,
        notes=f"Spearman rho range {_fmt(rho)}-{_fmt(_float(row, 'proxy_spearman_max'))} across workloads",
    )


def _test_h2b(row: dict[str, Any]) -> dict[str, Any]:
    lo = _float(row, "proxy_median_ratio_min")
    hi = _float(row, "proxy_median_ratio_max")
    deviation = max(abs(lo - 1.0), abs(hi - 1.0))
    if lo < 0.95 or hi > 1.05:
        verdict = "supports"
        label = "miscalibrated"
    elif lo >= 0.98 and hi <= 1.02:
        verdict = "refutes"
        label = "calibrated"
    else:
        verdict = "inconclusive"
        label = "borderline"
    return _row(
        hypothesis="H2b",
        scope="system",
        scope_value=row["system"],
        statistic="max_abs_ratio_deviation",
        statistic_value=deviation,
        p_value=None,
        effect="ratio_range",
        effect_value=hi - lo,
        effect_label=label,
        verdict=verdict,
        notes=f"median %cost/%n range {_fmt(lo)}-{_fmt(hi)} across workloads",
    )


def _test_h3a(row: dict[str, Any]) -> dict[str, Any]:
    agreement = _float(row, "rank_top1_agreement_min")
    flips = _int(row, "rank_top1_flips_max")
    frac = flips / 7.0
    if frac >= 0.5:
        label = "frequent flips"
    elif frac >= 0.15:
        label = "occasional flips"
    elif frac > 0:
        label = "rare flips"
    else:
        label = "no flips"
    verdict = "supports" if flips >= 1 or agreement < 0.999 else "refutes"
    return _row(
        hypothesis="H3a",
        scope="system",
        scope_value=row["system"],
        statistic="rank_top1_flips_max",
        statistic_value=flips,
        p_value=None,
        effect="flip_fraction_max",
        effect_value=frac,
        effect_label=label,
        verdict=verdict,
        notes=f"top-1 agreement range {_fmt(agreement)}-{_fmt(_float(row, 'rank_top1_agreement_max'))}; worst flips={flips}/7",
    )


def _test_h4a(row: dict[str, Any]) -> dict[str, Any]:
    j = _float(row, "pareto_jaccard_min")
    verdict = "supports" if j < 0.999 else "refutes"
    return _row(
        hypothesis="H4a",
        scope="system",
        scope_value=row["system"],
        statistic="pareto_jaccard_min",
        statistic_value=j,
        p_value=None,
        effect="exclusive_frontiers",
        effect_value=1.0 - j,
        effect_label="different" if j < 0.999 else "identical",
        verdict=verdict,
        notes=f"Pareto Jaccard range {_fmt(j)}-{_fmt(_float(row, 'pareto_jaccard_max'))} across workloads",
    )


def _test_h4b(row: dict[str, Any]) -> dict[str, Any]:
    j = _float(row, "pareto_jaccard_min")
    verdict = "supports" if j < 0.999 else "refutes"
    return _row(
        hypothesis="H4b",
        scope="system",
        scope_value=row["system"],
        statistic="pareto_jaccard_min",
        statistic_value=j,
        p_value=None,
        effect="frontier_overlap",
        effect_value=j,
        effect_label="frontiers differ" if j < 0.999 else "frontiers coincide",
        verdict=verdict,
        notes=f"minimum Pareto Jaccard={_fmt(j)}",
    )


def _test_h5a(row: dict[str, Any]) -> dict[str, Any]:
    verdict = row.get("h5a_verdict", "") or "inconclusive"
    label = verdict
    p = _float(row, "h5a_p_value")
    spread = _float(row, "h5a_ratio_spread")
    if not math.isfinite(p):
        verdict = "inconclusive"
        label = "nan"
    return _row(
        hypothesis="H5a",
        scope="system",
        scope_value=row["system"],
        statistic="h5a_p_value",
        statistic_value=p,
        p_value=p,
        effect="ratio_spread",
        effect_value=spread,
        effect_label=label,
        verdict=verdict,
        notes=f"workload ratio spread={_fmt(spread)}; stored H5a verdict={row.get('h5a_verdict', '')}",
    )


def _test_h5c(row: dict[str, Any]) -> dict[str, Any]:
    tau = _float(row, "rank_mean_kendall_tau_min")
    j = _float(row, "median_pareto_jaccard")
    if tau < 0.95 or j < 0.90:
        verdict = "supports"
    elif tau >= 0.99 and _float(row, "pareto_jaccard_min") >= 0.95:
        verdict = "refutes"
    else:
        verdict = "inconclusive"
    if tau < 0.7:
        label = "unstable"
    elif tau < 0.9:
        label = "moderately stable"
    else:
        label = "stable"
    return _row(
        hypothesis="H5c",
        scope="system",
        scope_value=row["system"],
        statistic="kendall_tau_min",
        statistic_value=tau,
        p_value=None,
        effect="median_pareto_jaccard",
        effect_value=j,
        effect_label=label,
        verdict=verdict,
        notes=f"mean Kendall tau range {_fmt(tau)}-{_fmt(_float(row, 'rank_mean_kendall_tau_max'))}; median Pareto Jaccard={_fmt(j)}",
    )


def _plot_hypothesis_verdicts(summary_rows: list[dict[str, Any]], output: Path) -> None:
    if not summary_rows:
        return
    labels = [row["hypothesis"] for row in summary_rows]
    x = np.arange(len(labels))
    bottom = np.zeros(len(labels))
    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    for verdict in VERDICT_ORDER:
        values = np.array([int(row.get(verdict, 0)) for row in summary_rows], dtype=float)
        ax.bar(x, values, bottom=bottom, label=verdict, color=VERDICT_COLORS[verdict])
        bottom += values
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Number of scopes")
    ax.set_title("Workload-batch hypothesis verdicts")
    ax.legend(frameon=False, ncols=3, loc="upper right")
    ax.grid(axis="y", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def _write_report(
    output: Path,
    *,
    input_dir: Path,
    hypothesis_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    system_rows: list[dict[str, Any]],
) -> None:
    by_h = {row["hypothesis"]: row for row in summary_rows}

    def verdict_text(hid: str) -> str:
        row = by_h.get(hid)
        if not row:
            return "--"
        return f"{row['global_verdict']} ({row['supports']} support, {row['refutes']} refute, {row['inconclusive']} inconclusive)"

    lines = [
        "# Workload-impact hypothesis report",
        "",
        f"Input batch: `{input_dir}`.",
        "",
        "## Global verdicts",
        "",
        f"- `H1a`: {verdict_text('H1a')}",
        f"- `H2a`: {verdict_text('H2a')}",
        f"- `H2b`: {verdict_text('H2b')}",
        f"- `H3a`: {verdict_text('H3a')}",
        f"- `H3b`: {verdict_text('H3b')}",
        f"- `H4a`: {verdict_text('H4a')}",
        f"- `H4b`: {verdict_text('H4b')}",
        f"- `H5a`: {verdict_text('H5a')}",
        f"- `H5c`: {verdict_text('H5c')}",
        "",
    ]

    strongest_h1a = max(system_rows, key=lambda row: _float(row, "cost_cv_max"))
    weakest_h2a = min(system_rows, key=lambda row: _float(row, "proxy_spearman_min"))
    weakest_h3a = min(system_rows, key=lambda row: _float(row, "rank_top1_agreement_min"))
    weakest_h4b = min(system_rows, key=lambda row: _float(row, "pareto_jaccard_min"))
    lines.extend(
        [
            "## Readout",
            "",
            f"- Strongest H1a case: `{strongest_h1a['system']}` with max CV `{_fmt(strongest_h1a['cost_cv_max'])}`.",
            f"- Weakest H2a case: `{weakest_h2a['system']}` with min Spearman rho `{_fmt(weakest_h2a['proxy_spearman_min'])}`.",
            f"- Least stable H3a case: `{weakest_h3a['system']}` with min top-1 agreement `{_fmt(weakest_h3a['rank_top1_agreement_min'])}`.",
            f"- Strongest H4b disagreement: `{weakest_h4b['system']}` with min Pareto Jaccard `{_fmt(weakest_h4b['pareto_jaccard_min'])}`.",
            "",
        ]
    )

    lines.extend(
        [
            "## Per-system workload hypotheses",
            "",
            "| System | H1a | H2a | H2b | H3a | H4b | H5a | H5c |",
            "|---|---|---|---|---|---|---|---|",
        ]
    )
    tests_by_system: dict[str, dict[str, str]] = {}
    for row in hypothesis_rows:
        if row["scope"] != "system":
            continue
        tests_by_system.setdefault(row["scope_value"], {})[row["hypothesis"]] = row["verdict"]
    for system in sorted(tests_by_system):
        row = tests_by_system[system]
        lines.append(
            f"| `{system}` | `{row.get('H1a','--')}` | `{row.get('H2a','--')}` | `{row.get('H2b','--')}` | "
            f"`{row.get('H3a','--')}` | `{row.get('H4b','--')}` | `{row.get('H5a','--')}` | `{row.get('H5c','--')}` |"
        )

    lines.extend(
        [
            "",
            "## Output Files",
            "",
            "- `hypothesis_tests.csv`: one row per system-level or global workload-batch hypothesis test.",
            "- `hypothesis_summary.csv`: support/refute/inconclusive counts per hypothesis.",
            "- `fig_workload_hypothesis_verdicts.png`: stacked verdict-count figure.",
            "",
        ]
    )
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    input_dir = REPO_ROOT / args.input_dir
    output_dir = Path(args.output_dir) if args.output_dir else input_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    system_rows = _read_csv(input_dir / "system_summary.csv")
    if not system_rows:
        raise SystemExit(f"Missing or empty {input_dir / 'system_summary.csv'}")

    hypothesis_rows: list[dict[str, Any]] = []
    for row in system_rows:
        hypothesis_rows.append(_test_h1a(row))
        hypothesis_rows.append(_test_h2a(row))
        hypothesis_rows.append(_test_h2b(row))
        hypothesis_rows.append(_test_h3a(row))
        hypothesis_rows.append(_test_h4a(row))
        hypothesis_rows.append(_test_h4b(row))
        hypothesis_rows.append(_test_h5a(row))
        hypothesis_rows.append(_test_h5c(row))

    h3b_rows = [
        {
            "cost_cv": _float(row, "median_cost_cv"),
            "rank_top1_flips": _int(row, "rank_top1_flips_max"),
        }
        for row in system_rows
    ]
    h3b = test_h3b_flip_correlation(h3b_rows)
    h3b["scope_value"] = "all_workload_batch_systems"
    h3b["notes"] = (
        f"Spearman(median cost CV, max top1 flips) rho={_fmt(h3b['statistic_value'])} "
        f"across n={len(system_rows)} systems"
    )
    hypothesis_rows.append(h3b)

    summary_rows = aggregate_verdicts(hypothesis_rows)
    write_csv(output_dir / "hypothesis_tests.csv", hypothesis_rows)
    write_csv(output_dir / "hypothesis_summary.csv", summary_rows)
    _plot_hypothesis_verdicts(summary_rows, output_dir / "fig_workload_hypothesis_verdicts.png")
    _write_report(
        output_dir / "workload_hypothesis_report.md",
        input_dir=input_dir,
        hypothesis_rows=hypothesis_rows,
        summary_rows=summary_rows,
        system_rows=system_rows,
    )
    print(f"Wrote workload hypothesis outputs to {output_dir}")


if __name__ == "__main__":
    main()
