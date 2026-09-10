#!/usr/bin/env python3
"""Create explanatory bias plots for Twins generated-sampling outputs.

These plots are meant to explain *why* empirical cost changes the conclusions:
heavy-tailed per-configuration cost distributions, strategy-specific
calibration bias, and samples that are costly without improving prediction
error. The script keeps the run-level diagnostic scatter and also writes two
aggregated alternatives: one median point per strategy/budget trajectory, and
one fixed-budget strategy comparison for selected `n` levels.
"""

from __future__ import annotations

import argparse
import csv
import math
import os
from pathlib import Path
import re
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

from cost_sampling.generated_sampling import load_twins_table, parse_where


DEFAULT_ZIP = "/private/tmp/TwinsOrFalseFriends-ICSE2023.zip"
STRATEGY_ORDER = [
    "random",
    "balanced",
    "diversity",
    "pairwise",
    "pilotCost",
    "cheapOracle",
    "expensiveOracle",
]
STRATEGY_COLORS = {
    "random": "#4C78A8",
    "balanced": "#F58518",
    "diversity": "#54A24B",
    "pairwise": "#B279A2",
    "pilotCost": "#E45756",
    "cheapOracle": "#72B7B2",
    "expensiveOracle": "#9D755D",
}
SCENARIO_ORDER = [
    ("performance", "performance"),
    ("performance", "energy"),
    ("energy", "performance"),
    ("energy", "energy"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default="artifacts/twins_generated_representative_100s")
    parser.add_argument("--zip", default=DEFAULT_ZIP)
    parser.add_argument(
        "--systems",
        default="ALL",
        help="Comma-separated analysis contexts from system_summary.csv, or ALL.",
    )
    parser.add_argument(
        "--scenarios",
        default="ALL",
        help="Comma-separated cost:target pairs, e.g. performance:energy, or ALL.",
    )
    parser.add_argument(
        "--exclude-oracles",
        action="store_true",
        help="Hide cheap/expensive diagnostic oracles from per-scenario scatter plots.",
    )
    parser.add_argument(
        "--fixed-levels",
        default="n8",
        help="Comma-separated sample-size levels for fixed-budget summary plots, e.g. n8,n16.",
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


def _safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).replace(".", "_")


def _scenario_name(cost: str, target: str) -> str:
    return f"cost_{cost}__target_{target}"


def _level_n(level: str) -> int:
    return int(level[1:]) if level.startswith("n") and level[1:].isdigit() else 0


def _format_ratio(value: float) -> str:
    if not math.isfinite(value):
        return ""
    if value >= 10:
        return f"{value:.0f}"
    if value >= 1:
        return f"{value:.2f}"
    return f"{value:.2f}"


def _selected_systems(system_rows: list[dict[str, Any]], requested: str) -> list[dict[str, Any]]:
    if requested == "ALL":
        return system_rows
    wanted = {item.strip() for item in requested.split(",") if item.strip()}
    return [row for row in system_rows if row.get("analysis_context") in wanted or row.get("system") in wanted]


def _selected_scenarios(requested: str) -> list[tuple[str, str]]:
    if requested == "ALL":
        return SCENARIO_ORDER
    out = []
    for item in requested.split(","):
        item = item.strip()
        if not item:
            continue
        if ":" not in item:
            raise ValueError(f"Expected cost:target scenario, got {item!r}")
        cost, target = item.split(":", 1)
        out.append((cost, target))
    return out


def _selected_levels(requested: str) -> list[str]:
    return [item.strip() for item in requested.split(",") if item.strip()]


def _folder_for(input_dir: Path, row: dict[str, Any]) -> Path:
    report = row.get("report", "")
    if "/" in report:
        return input_dir / report.split("/", 1)[0]
    return input_dir / _safe_name(row["analysis_context"])


def _load_cost_values(zip_path: str, row: dict[str, Any], cost_property: str) -> np.ndarray:
    where = parse_where([row["filter"]]) if row.get("filter") else {}
    max_rows = int(float(row.get("row_cap", 0) or 0)) or None
    table = load_twins_table(zip_path, row["system"], where=where, max_rows=max_rows)
    return np.asarray([float(item[cost_property]) for item in table.rows], dtype=float)


def _finite_percentile(values: list[float], pct: float) -> float:
    arr = np.asarray([value for value in values if math.isfinite(value)], dtype=float)
    return float(np.percentile(arr, pct)) if arr.size else float("nan")


def _set_mre_scale(ax: plt.Axes, values: list[float]) -> None:
    finite = [value for value in values if math.isfinite(value)]
    if finite and max(finite) > 5 * max(1e-9, float(np.percentile(finite, 75))):
        ax.set_yscale("symlog", linthresh=1.0)


def plot_calibration_heatmap(input_dir: Path, system_rows: list[dict[str, Any]]) -> None:
    rows: list[str] = []
    matrix: list[list[float]] = []
    for system in system_rows:
        folder = _folder_for(input_dir, system)
        records = _read_csv(folder / "records.csv")
        for cost in ("performance", "energy"):
            label = f"{system['analysis_context']} / {cost}"
            values = []
            for strategy in STRATEGY_ORDER:
                ratios = [
                    _float(row, "calibration_ratio")
                    for row in records
                    if row.get("cost_property") == cost
                    and row.get("target_property") == cost
                    and row.get("strategy") == strategy
                    and math.isfinite(_float(row, "calibration_ratio"))
                ]
                values.append(float(np.median(ratios)) if ratios else float("nan"))
            rows.append(label)
            matrix.append(values)
    if not matrix:
        return
    arr = np.asarray(matrix, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        log_arr = np.log2(arr)
    finite = log_arr[np.isfinite(log_arr)]
    limit = max(1.0, float(np.nanpercentile(np.abs(finite), 95))) if finite.size else 1.0

    fig, ax = plt.subplots(figsize=(10.5, max(5.2, 0.34 * len(rows) + 1.4)))
    image = ax.imshow(log_arr, aspect="auto", cmap="coolwarm", vmin=-limit, vmax=limit)
    ax.set_yticks(np.arange(len(rows)))
    ax.set_yticklabels(rows)
    ax.set_xticks(np.arange(len(STRATEGY_ORDER)))
    ax.set_xticklabels(STRATEGY_ORDER, rotation=25, ha="right")
    ax.set_title("Strategy calibration bias: median %TrainCost/%n")
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            value = arr[i, j]
            if math.isfinite(value):
                ax.text(j, i, _format_ratio(value), ha="center", va="center", fontsize=7)
    cbar = fig.colorbar(image, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_label("log2 calibration ratio")
    fig.tight_layout()
    fig.savefig(input_dir / "fig_explain_strategy_calibration_heatmap.png", dpi=200)
    plt.close(fig)


def _plot_scenario_cost_error(
    *,
    input_dir: Path,
    zip_path: str,
    system: dict[str, Any],
    cost: str,
    target: str,
    exclude_oracles: bool,
) -> None:
    folder = _folder_for(input_dir, system)
    records = [
        row
        for row in _read_csv(folder / "records.csv")
        if row.get("cost_property") == cost and row.get("target_property") == target
    ]
    if exclude_oracles:
        records = [row for row in records if row.get("strategy") not in {"cheapOracle", "expensiveOracle"}]
    suffix = "_deployable" if exclude_oracles else ""
    if not records:
        return
    cost_values = _load_cost_values(zip_path, system, cost)
    positive_costs = cost_values[cost_values > 0]
    if positive_costs.size == 0:
        return
    scenario = _scenario_name(cost, target)
    summary_rows = [
        row
        for row in _read_csv(folder / "strategy_summary.csv")
        if row.get("cost_property") == cost and row.get("target_property") == target
    ]
    by_pair = {(row["strategy"], row["level"]): row for row in summary_rows}

    fig = plt.figure(figsize=(10.8, 7.2))
    grid = fig.add_gridspec(2, 1, height_ratios=[1.0, 3.2], hspace=0.08)
    ax_hist = fig.add_subplot(grid[0])
    ax = fig.add_subplot(grid[1], sharex=ax_hist)

    bins = np.geomspace(float(np.min(positive_costs)), float(np.max(positive_costs)), 42)
    ax_hist.hist(positive_costs, bins=bins, color="#c8c8c8", edgecolor="#ffffff")
    ax_hist.set_xscale("log")
    ax_hist.set_ylabel("configs")
    ax_hist.set_title(
        f"{system['analysis_context']}: sampled cost regions vs prediction error "
        f"(cost={cost}, target={target})"
    )
    plt.setp(ax_hist.get_xticklabels(), visible=False)

    median_cost = float(np.median(positive_costs))
    q90_cost = float(np.percentile(positive_costs, 90))
    for axis in (ax_hist, ax):
        axis.axvline(median_cost, color="#333333", linestyle="-", linewidth=1.0, alpha=0.75)
        axis.axvline(q90_cost, color="#333333", linestyle="--", linewidth=1.0, alpha=0.75)

    for strategy in STRATEGY_ORDER:
        xs = []
        ys = []
        sizes = []
        for row in records:
            if row.get("strategy") != strategy:
                continue
            n = _float(row, "n")
            train_cost = _float(row, "train_cost")
            mre = _float(row, "mre")
            if n <= 0 or train_cost <= 0 or not math.isfinite(mre):
                continue
            xs.append(train_cost / n)
            ys.append(mre)
            sizes.append(14 + 36 * min(1.0, n / 256.0))
        if xs:
            ax.scatter(
                xs,
                ys,
                s=sizes,
                color=STRATEGY_COLORS.get(strategy, "#666666"),
                alpha=0.28 if len(xs) > 50 else 0.65,
                edgecolors="none",
                label=strategy,
            )

    # Annotate the largest-budget strategy summaries. This links cost bias to
    # actual prediction quality without overwhelming the run-level points.
    levels = sorted({row["level"] for row in summary_rows}, key=lambda value: int(value[1:]) if value.startswith("n") else 0)
    if levels:
        largest = levels[-1]
        for strategy in STRATEGY_ORDER:
            row = by_pair.get((strategy, largest))
            if not row:
                continue
            x = _float(row, "median_train_cost") / max(_float(row, "n"), 1.0)
            y = _float(row, "median_mre")
            if not (math.isfinite(x) and math.isfinite(y)):
                continue
            ax.scatter(
                [x],
                [y],
                s=95,
                marker="D",
                color=STRATEGY_COLORS.get(strategy, "#666666"),
                edgecolors="#111111",
                linewidths=0.7,
                zorder=5,
            )

    ax.set_xscale("log")
    _set_mre_scale(ax, [_float(row, "mre") for row in records])
    ax.set_xlabel(f"Mean sampled {cost} cost per selected configuration")
    ax.set_ylabel(f"MRE predicting {target}")
    ax.grid(color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, ncols=4, fontsize=8, loc="upper left")
    ax.text(
        0.99,
        0.98,
        "solid line: full median cost\n dashed line: full p90 cost\n diamonds: largest budget medians",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=8,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "alpha": 0.9},
    )
    fig.tight_layout()
    fig.savefig(folder / f"fig_explain_cost_error_{scenario}{suffix}.png", dpi=200)
    plt.close(fig)


def _scenario_records(
    *,
    input_dir: Path,
    system: dict[str, Any],
    cost: str,
    target: str,
    exclude_oracles: bool,
) -> list[dict[str, Any]]:
    folder = _folder_for(input_dir, system)
    records = [
        row
        for row in _read_csv(folder / "records.csv")
        if row.get("cost_property") == cost and row.get("target_property") == target
    ]
    if exclude_oracles:
        records = [row for row in records if row.get("strategy") not in {"cheapOracle", "expensiveOracle"}]
    return records


def _aggregate_strategy_level(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in records:
        grouped.setdefault((row["strategy"], row["level"]), []).append(row)
    out: list[dict[str, Any]] = []
    for (strategy, level), rows in grouped.items():
        pct_cost = [_float(row, "pct_cost") for row in rows]
        mre = [_float(row, "mre") for row in rows]
        ratios = [_float(row, "calibration_ratio") for row in rows]
        out.append(
            {
                "strategy": strategy,
                "level": level,
                "n": _level_n(level),
                "median_pct_cost": _finite_percentile(pct_cost, 50),
                "q1_pct_cost": _finite_percentile(pct_cost, 25),
                "q3_pct_cost": _finite_percentile(pct_cost, 75),
                "median_mre": _finite_percentile(mre, 50),
                "q1_mre": _finite_percentile(mre, 25),
                "q3_mre": _finite_percentile(mre, 75),
                "median_ratio": _finite_percentile(ratios, 50),
                "runs": len(rows),
            }
        )
    return sorted(out, key=lambda row: (STRATEGY_ORDER.index(row["strategy"]) if row["strategy"] in STRATEGY_ORDER else 99, row["n"]))


def _plot_strategy_budget_path(
    *,
    input_dir: Path,
    system: dict[str, Any],
    cost: str,
    target: str,
    exclude_oracles: bool,
) -> None:
    folder = _folder_for(input_dir, system)
    suffix = "_deployable" if exclude_oracles else ""
    records = _scenario_records(input_dir=input_dir, system=system, cost=cost, target=target, exclude_oracles=exclude_oracles)
    rows = _aggregate_strategy_level(records)
    if not rows:
        return
    scenario = _scenario_name(cost, target)
    fig, ax = plt.subplots(figsize=(9.2, 6.2))
    y_values = []
    for strategy in STRATEGY_ORDER:
        items = [row for row in rows if row["strategy"] == strategy and math.isfinite(row["median_pct_cost"]) and math.isfinite(row["median_mre"])]
        if not items:
            continue
        xs = [row["median_pct_cost"] for row in items]
        ys = [row["median_mre"] for row in items]
        y_values.extend(ys)
        sizes = [32 + 90 * min(1.0, row["n"] / 256.0) for row in items]
        ax.plot(xs, ys, color=STRATEGY_COLORS.get(strategy, "#666666"), alpha=0.65, linewidth=1.6)
        ax.scatter(
            xs,
            ys,
            s=sizes,
            color=STRATEGY_COLORS.get(strategy, "#666666"),
            edgecolors="#111111",
            linewidths=0.4,
            alpha=0.9,
            label=strategy,
        )
        # Label the smallest and largest budget to make the trajectory readable.
        for row in (items[0], items[-1]):
            ax.annotate(
                row["level"],
                (row["median_pct_cost"], row["median_mre"]),
                xytext=(4, 4),
                textcoords="offset points",
                fontsize=7,
                color=STRATEGY_COLORS.get(strategy, "#333333"),
            )
    _set_mre_scale(ax, y_values)
    ax.margins(x=0.12, y=0.22)
    ax.set_xlabel(f"Median fraction of full {cost} cost")
    ax.set_ylabel(f"Median MRE predicting {target}")
    ax.set_title(f"{system['analysis_context']}: strategy-budget trajectories (cost={cost}, target={target})")
    ax.grid(color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, ncols=4, fontsize=8)
    fig.tight_layout()
    fig.savefig(folder / f"fig_explain_strategy_budget_path_{scenario}{suffix}.png", dpi=200)
    plt.close(fig)


def _plot_fixed_level(
    *,
    input_dir: Path,
    system: dict[str, Any],
    cost: str,
    target: str,
    level: str,
    exclude_oracles: bool,
) -> None:
    folder = _folder_for(input_dir, system)
    suffix = "_deployable" if exclude_oracles else ""
    records = [
        row
        for row in _scenario_records(input_dir=input_dir, system=system, cost=cost, target=target, exclude_oracles=exclude_oracles)
        if row.get("level") == level
    ]
    rows = _aggregate_strategy_level(records)
    rows = [row for row in rows if row["level"] == level and math.isfinite(row["median_pct_cost"]) and math.isfinite(row["median_mre"])]
    if not rows:
        return
    scenario = _scenario_name(cost, target)
    fig, ax = plt.subplots(figsize=(8.8, 5.8))
    y_values = [row["median_mre"] for row in rows]
    for row in rows:
        x = row["median_pct_cost"]
        y = row["median_mre"]
        xerr = [[max(0.0, x - row["q1_pct_cost"])], [max(0.0, row["q3_pct_cost"] - x)]]
        yerr = [[max(0.0, y - row["q1_mre"])], [max(0.0, row["q3_mre"] - y)]]
        color = STRATEGY_COLORS.get(row["strategy"], "#666666")
        show_error = row["runs"] > 1 and all(math.isfinite(v[0]) for v in xerr + yerr)
        if show_error:
            ax.errorbar(
                [x],
                [y],
                xerr=xerr,
                yerr=yerr,
                fmt="o",
                color=color,
                ecolor=color,
                elinewidth=1.1,
                capsize=3,
                markersize=8,
                markeredgecolor="#111111",
                markeredgewidth=0.4,
            )
        else:
            ax.scatter([x], [y], s=95, color=color, edgecolors="#111111", linewidths=0.5)
        ax.annotate(
            row["strategy"],
            (x, y),
            xytext=(6, 5),
            textcoords="offset points",
            fontsize=8,
            color=color,
        )
    _set_mre_scale(ax, y_values)
    ax.margins(x=0.12, y=0.22)
    ax.set_xlabel(f"Median fraction of full {cost} cost at {level}")
    ax.set_ylabel(f"Median MRE predicting {target}")
    ax.set_title(f"{system['analysis_context']}: fixed sample size {level} (cost={cost}, target={target})")
    ax.grid(color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.text(
        0.99,
        0.98,
        "error bars: IQR over seeds\nsingle markers: deterministic strategy",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=8,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "alpha": 0.9},
    )
    fig.tight_layout()
    fig.savefig(folder / f"fig_explain_fixed_{level}_{scenario}{suffix}.png", dpi=200)
    plt.close(fig)


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir)
    system_rows = _selected_systems(_read_csv(input_dir / "system_summary.csv"), args.systems)
    scenarios = _selected_scenarios(args.scenarios)
    fixed_levels = _selected_levels(args.fixed_levels)
    if not system_rows:
        raise SystemExit(f"No systems selected from {input_dir / 'system_summary.csv'}")

    plot_calibration_heatmap(input_dir, system_rows)
    for system in system_rows:
        for cost, target in scenarios:
            _plot_scenario_cost_error(
                input_dir=input_dir,
                zip_path=args.zip,
                system=system,
                cost=cost,
                target=target,
                exclude_oracles=args.exclude_oracles,
            )
            _plot_strategy_budget_path(
                input_dir=input_dir,
                system=system,
                cost=cost,
                target=target,
                exclude_oracles=args.exclude_oracles,
            )
            for level in fixed_levels:
                _plot_fixed_level(
                    input_dir=input_dir,
                    system=system,
                    cost=cost,
                    target=target,
                    level=level,
                    exclude_oracles=args.exclude_oracles,
                )
    print(f"Wrote explanatory bias plots under {input_dir}")


if __name__ == "__main__":
    main()
