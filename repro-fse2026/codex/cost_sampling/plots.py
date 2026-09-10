"""Matplotlib figures for the x264 proof of concept."""

from __future__ import annotations

import os
from pathlib import Path
import tempfile
from typing import Any

_cache_root = Path(tempfile.gettempdir()) / "cost_sampling_cache"
(_cache_root / "matplotlib").mkdir(parents=True, exist_ok=True)
(_cache_root / "fontconfig").mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_cache_root / "matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(_cache_root / "fontconfig"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .analysis import level_sort_key, strategy_sort_key
from .metrics import pareto_mask


PALETTE = {
    "random": "#4C78A8",
    "solverBased": "#F58518",
    "henard": "#54A24B",
    "distBased": "#E45756",
    "divDistBased": "#72B7B2",
    "twise": "#B279A2",
    "balanced": "#59A14F",
    "diversity": "#E15759",
    "uncertainty": "#EDC948",
    "coverage": "#AF7AA1",
    "SRSSampling": "#D55E00",
    "pairwise": "#B07AA1",
    "pilotCost": "#9C755F",
    "cheapOracle": "#76B7B2",
    "expensiveOracle": "#FF9DA7",
}

MARKERS = {"t1": "o", "t2": "s", "t3": "^"}


def _strategies(records: list[dict[str, Any]]) -> list[str]:
    return sorted({row["strategy"] for row in records}, key=strategy_sort_key)


def _levels(records: list[dict[str, Any]]) -> list[str]:
    return sorted({row["level"] for row in records}, key=level_sort_key)


def plot_cost_distribution(records: list[dict[str, Any]], output: str | Path) -> None:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    strategies = _strategies(records)
    levels = _levels(records)
    fig, axes = plt.subplots(1, len(levels), figsize=(4.7 * len(levels), 4.2), sharey=True)
    if len(levels) == 1:
        axes = [axes]

    for ax, level in zip(axes, levels):
        data = [
            [100 * row["pct_cost"] for row in records if row["level"] == level and row["strategy"] == strategy]
            for strategy in strategies
        ]
        boxes = ax.boxplot(data, patch_artist=True, showfliers=False)
        for patch, strategy in zip(boxes["boxes"], strategies):
            patch.set_facecolor(PALETTE.get(strategy, "#999999"))
            patch.set_alpha(0.75)
        ax.set_title(f"{level} training sets")
        ax.set_xticks(range(1, len(strategies) + 1))
        ax.set_xticklabels(strategies, rotation=35, ha="right")
        ax.grid(axis="y", color="#dddddd", linewidth=0.8)
        ax.set_axisbelow(True)

    axes[0].set_ylabel("Measured training cost (% of full cost)")
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def plot_calibration(records: list[dict[str, Any]], output: str | Path) -> None:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    strategies = _strategies(records)
    levels = _levels(records)
    offsets = {
        strategy: (idx - (len(strategies) - 1) / 2) * 0.08
        for idx, strategy in enumerate(strategies)
    }
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    for strategy in strategies:
        for level in levels:
            xs = [
                100 * row["pct_n"] + offsets[strategy]
                for row in records
                if row["strategy"] == strategy and row["level"] == level
            ]
            ys = [
                100 * row["pct_cost"]
                for row in records
                if row["strategy"] == strategy and row["level"] == level
            ]
            if not xs:
                continue
            ax.scatter(
                xs,
                ys,
                s=14,
                alpha=0.35,
                marker=MARKERS.get(level, "o"),
                color=PALETTE.get(strategy, "#999999"),
                edgecolors="none",
            )
    max_axis = max(max(100 * row["pct_n"] for row in records), max(100 * row["pct_cost"] for row in records)) * 1.08
    ax.plot([0, max_axis], [0, max_axis], color="#222222", linewidth=1.2, linestyle="--", label="size = cost")
    ax.set_xlim(0, max_axis)
    ax.set_ylim(0, max_axis)
    ax.set_xlabel("Training size (% of configurations)")
    ax.set_ylabel("Measured training cost (% of full cost)")
    ax.grid(color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    handles = [
        plt.Line2D([0], [0], marker="o", linestyle="", color=PALETTE.get(strategy, "#999999"), label=strategy)
        for strategy in strategies
    ]
    ax.legend(handles=handles, frameon=False, ncols=2, loc="upper left")
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def plot_accuracy_cost(pareto_rows: list[dict[str, Any]], output: str | Path) -> None:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    strategies = sorted({row["strategy"] for row in pareto_rows}, key=strategy_sort_key)
    levels = sorted({row["level"] for row in pareto_rows}, key=level_sort_key)
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    for row in pareto_rows:
        strategy = row["strategy"]
        level = row["level"]
        ax.scatter(
            100 * row["median_pct_cost"],
            row["median_mre"],
            s=90 if row["pareto_empirical"] else 58,
            marker=MARKERS.get(level, "o"),
            color=PALETTE.get(strategy, "#999999"),
            edgecolors="#111111" if row["pareto_empirical"] else "white",
            linewidths=1.4 if row["pareto_empirical"] else 0.6,
            alpha=0.92,
        )
    ax.set_xlabel("Median measured training cost (% of full cost)")
    ax.set_ylabel("Median MRE")
    ax.grid(color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    strategy_handles = [
        plt.Line2D([0], [0], marker="o", linestyle="", color=PALETTE.get(strategy, "#999999"), label=strategy)
        for strategy in strategies
    ]
    level_handles = [
        plt.Line2D([0], [0], marker=MARKERS.get(level, "o"), linestyle="", color="#555555", label=level)
        for level in levels
    ]
    pareto_handle = plt.Line2D(
        [0],
        [0],
        marker="o",
        linestyle="",
        markerfacecolor="white",
        markeredgecolor="#111111",
        markeredgewidth=1.4,
        color="#111111",
        label="measured-cost Pareto",
    )
    legend1 = ax.legend(handles=strategy_handles, frameon=False, loc="upper left", ncols=2)
    ax.add_artist(legend1)
    ax.legend(handles=[*level_handles, pareto_handle], frameon=False, loc="lower left", ncols=2)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def plot_posterior_risk_distribution(records: list[dict[str, Any]], output: str | Path) -> None:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    pairs = sorted(
        {(row["strategy"], row["level"]) for row in records},
        key=lambda item: (level_sort_key(item[1]), strategy_sort_key(item[0])),
    )
    data = [
        [
            float(row["posterior_risk"])
            for row in records
            if row["strategy"] == strategy and row["level"] == level
        ]
        for strategy, level in pairs
    ]
    labels = [f"{strategy}_{level}" for strategy, level in pairs]
    fig_width = max(7.2, 0.72 * len(labels) + 2.2)
    fig, ax = plt.subplots(figsize=(fig_width, 4.8))
    boxes = ax.boxplot(data, patch_artist=True, showfliers=False)
    for patch, (strategy, _) in zip(boxes["boxes"], pairs):
        patch.set_facecolor(PALETTE.get(strategy, "#999999"))
        patch.set_alpha(0.72)
    rng = np.random.default_rng(0)
    for pos, values in enumerate(data, start=1):
        if not values:
            continue
        jitter = rng.uniform(-0.14, 0.14, size=len(values))
        strategy = pairs[pos - 1][0]
        ax.scatter(
            np.full(len(values), pos) + jitter,
            values,
            s=13,
            alpha=0.35,
            color=PALETTE.get(strategy, "#999999"),
            edgecolors="none",
        )
    ax.set_xticks(range(1, len(labels) + 1))
    ax.set_xticklabels(labels, rotation=35, ha="right")
    ax.set_ylabel("Posterior risk")
    ax.grid(axis="y", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def plot_posterior_confidence_discrepancy(
    curve_rows: list[dict[str, Any]],
    output: str | Path,
    *,
    epsilon_max: float = 0.15,
) -> None:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = [row for row in curve_rows if float(row["epsilon"]) <= epsilon_max]
    if not rows:
        rows = curve_rows
    pairs = sorted(
        {(row["strategy"], row["level"]) for row in rows},
        key=lambda item: (level_sort_key(item[1]), strategy_sort_key(item[0])),
    )
    fig, ax = plt.subplots(figsize=(7.8, 4.8))
    for strategy, level in pairs:
        pair_rows = sorted(
            [row for row in rows if row["strategy"] == strategy and row["level"] == level],
            key=lambda row: float(row["epsilon"]),
        )
        if not pair_rows:
            continue
        ax.plot(
            [float(row["epsilon"]) for row in pair_rows],
            [float(row["confidence_discrepancy"]) for row in pair_rows],
            color=PALETTE.get(strategy, "#999999"),
            linewidth=2.0,
            marker=MARKERS.get(level, "o"),
            markevery=max(1, len(pair_rows) // 6),
            markersize=4.5,
            label=f"{strategy}_{level}",
        )
    ax.axhline(0.0, color="#222222", linewidth=1.0, linestyle="--")
    ax.set_xlabel("Accepted risk epsilon")
    ax.set_ylabel("Posterior - prior confidence")
    ax.grid(color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, ncols=2, fontsize=8)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def plot_posterior_cost_frontier(pareto_rows: list[dict[str, Any]], output: str | Path) -> None:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = sorted(pareto_rows, key=lambda row: (level_sort_key(row["level"]), strategy_sort_key(row["strategy"])))
    fig, ax = plt.subplots(figsize=(7.6, 5.0))
    for row in rows:
        is_frontier = bool(row["pareto_empirical_cost_confidence"])
        x = 100.0 * float(row["median_pct_cost"])
        y = float(row["posterior_confidence_area"])
        ax.scatter(
            x,
            y,
            s=105 if is_frontier else 58,
            marker=MARKERS.get(row["level"], "o"),
            color=PALETTE.get(row["strategy"], "#999999"),
            edgecolors="#111111" if is_frontier else "white",
            linewidths=1.4 if is_frontier else 0.6,
            alpha=0.95 if is_frontier else 0.68,
        )
        ax.annotate(
            f"{row['strategy']}_{row['level']}",
            (x, y),
            xytext=(4, 3),
            textcoords="offset points",
            fontsize=8,
        )
    ax.set_xlabel("Median measured acquisition cost (% of full cost)")
    ax.set_ylabel("Integrated posterior confidence")
    ax.grid(color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    pareto_handle = plt.Line2D(
        [0],
        [0],
        marker="o",
        linestyle="",
        markerfacecolor="white",
        markeredgecolor="#111111",
        markeredgewidth=1.4,
        color="#111111",
        label="measured-cost/confidence Pareto",
    )
    ax.legend(handles=[pareto_handle], frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def plot_posterior_omega(summary_rows: list[dict[str, Any]], output: str | Path) -> None:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = sorted(summary_rows, key=lambda row: (level_sort_key(row["level"]), strategy_sort_key(row["strategy"])))
    labels = [f"{row['strategy']}_{row['level']}" for row in rows]
    x = np.arange(len(rows))
    width = 0.36
    fig_width = max(7.2, 0.72 * len(labels) + 2.2)
    fig, ax = plt.subplots(figsize=(fig_width, 4.8))
    ax.bar(
        x - width / 2,
        [float(row["omega_size_baseline"]) for row in rows],
        width=width,
        color="#4C78A8",
        label="sample-size baseline",
    )
    ax.bar(
        x + width / 2,
        [float(row["omega_cost_baseline"]) for row in rows],
        width=width,
        color="#F58518",
        label="measured-cost baseline",
    )
    ax.axhline(0.0, color="#222222", linewidth=1.0)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=35, ha="right")
    ax.set_ylabel("Integrated confidence discrepancy (omega)")
    ax.grid(axis="y", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def plot_rank_stability(rank_rows: list[dict[str, Any]], output: str | Path) -> None:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    lambdas = [row["lambda"] for row in rank_rows]
    tau = [row["kendall_tau"] for row in rank_rows]
    top3 = [row["top3_overlap"] for row in rank_rows]
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(lambdas, tau, marker="o", color="#4C78A8", label="Kendall tau")
    ax.plot(lambdas, top3, marker="s", color="#F58518", label="Top-3 overlap")
    ax.set_xscale("log")
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel("Cost weight")
    ax.set_ylabel("Agreement")
    ax.grid(color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def plot_strategy_cost_bias(summary_rows: list[dict[str, Any]], output: str | Path) -> None:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    strategies = _strategies(summary_rows)
    data = [
        [row["cost_over_random"] for row in summary_rows if row["strategy"] == strategy]
        for strategy in strategies
    ]
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    boxes = ax.boxplot(data, patch_artist=True, showfliers=False)
    for patch, strategy in zip(boxes["boxes"], strategies):
        patch.set_facecolor(PALETTE.get(strategy, "#999999"))
        patch.set_alpha(0.75)
    ax.axhline(1.0, color="#222222", linestyle="--", linewidth=1.1)
    ax.set_xticks(range(1, len(strategies) + 1))
    ax.set_xticklabels(strategies, rotation=30, ha="right")
    ax.set_ylabel("Median measured cost / random cost")
    ax.grid(axis="y", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def plot_aggregate_rank_agreement(
    rank_rows: list[dict[str, Any]],
    output: str | Path,
    *,
    context_label: str = "contexts",
) -> None:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    lambdas = sorted({row["lambda"] for row in rank_rows})
    top1 = []
    top3 = []
    tau = []
    for lam in lambdas:
        rows = [row for row in rank_rows if row["lambda"] == lam]
        top1.append(sum(row["top1_agreement"] for row in rows) / len(rows))
        top3.append(sum(row["top3_overlap"] for row in rows) / len(rows))
        tau.append(sum(row["kendall_tau"] for row in rows) / len(rows))

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(lambdas, top1, marker="o", color="#4C78A8", label="Top-1 agreement")
    ax.plot(lambdas, top3, marker="s", color="#F58518", label="Mean top-3 overlap")
    ax.plot(lambdas, tau, marker="^", color="#54A24B", label="Mean Kendall tau")
    ax.set_xscale("log")
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel("Cost weight")
    ax.set_ylabel(f"Agreement across {context_label}")
    ax.grid(color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def plot_context_sensitivity(
    context_rows: list[dict[str, Any]],
    output: str | Path,
    *,
    context_prefix: str = "x264_size_",
) -> None:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = sorted(context_rows, key=lambda row: int(str(row["target_context"]).rsplit("_", 1)[1]))
    x = list(range(len(rows)))
    labels = [str(row["target_context"]).replace(context_prefix, "") for row in rows]

    fig, axes = plt.subplots(2, 1, figsize=(8.4, 6.2), sharex=True)
    axes[0].plot(x, [row["cost_cv"] for row in rows], marker="o", color="#4C78A8")
    axes[0].set_ylabel("Cost CV")
    axes[0].grid(color="#dddddd", linewidth=0.8)
    axes[0].set_axisbelow(True)

    axes[1].plot(x, [row["proxy_median_ratio"] for row in rows], marker="s", color="#F58518", label="median ratio")
    axes[1].fill_between(
        x,
        [row["proxy_q1_ratio"] for row in rows],
        [row["proxy_q3_ratio"] for row in rows],
        color="#F58518",
        alpha=0.2,
        linewidth=0,
        label="IQR",
    )
    axes[1].axhline(1.0, color="#222222", linestyle="--", linewidth=1.1)
    axes[1].set_ylabel("%cost / %n")
    axes[1].set_xlabel("x264 input index")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels)
    axes[1].grid(color="#dddddd", linewidth=0.8)
    axes[1].set_axisbelow(True)
    axes[1].legend(frameon=False)

    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def plot_calibration_by_strategy(proxy_rows: list[dict[str, Any]], output: str | Path, *, title: str = "") -> None:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = [row for row in proxy_rows if row["strategy"] != "ALL"]
    strategies = _strategies(rows)
    data = [
        [float(row["median_calibration_ratio"]) for row in rows if row["strategy"] == strategy]
        for strategy in strategies
    ]
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    boxes = ax.boxplot(data, patch_artist=True, showfliers=False)
    for patch, strategy in zip(boxes["boxes"], strategies):
        patch.set_facecolor(PALETTE.get(strategy, "#999999"))
        patch.set_alpha(0.75)
    ax.axhline(1.0, color="#222222", linestyle="--", linewidth=1.1)
    ax.set_xticks(range(1, len(strategies) + 1))
    ax.set_xticklabels(strategies, rotation=30, ha="right")
    ax.set_ylabel("Median calibration ratio (%cost / %n)")
    if title:
        ax.set_title(title)
    ax.grid(axis="y", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def plot_rank_agreement_by_scenario(
    rank_rows: list[dict[str, Any]],
    output: str | Path,
    *,
    scenario_order: list[str],
    scenario_labels: dict[str, str],
) -> None:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(2, 2, figsize=(10.4, 7.2), sharex=True, sharey=True)
    axes_list = list(axes.flat)
    for ax, scenario in zip(axes_list, scenario_order):
        rows = [row for row in rank_rows if row["scenario"] == scenario]
        lambdas = sorted({float(row["lambda"]) for row in rows})
        top1 = []
        top3 = []
        tau = []
        for lam in lambdas:
            lam_rows = [row for row in rows if float(row["lambda"]) == lam]
            top1.append(sum(float(row["top1_agreement"]) for row in lam_rows) / len(lam_rows))
            top3.append(sum(float(row["top3_overlap"]) for row in lam_rows) / len(lam_rows))
            tau.append(sum(float(row["kendall_tau"]) for row in lam_rows) / len(lam_rows))
        ax.plot(lambdas, top1, marker="o", color="#4C78A8", label="Top-1")
        ax.plot(lambdas, top3, marker="s", color="#F58518", label="Top-3")
        ax.plot(lambdas, tau, marker="^", color="#54A24B", label="Kendall tau")
        ax.set_xscale("log")
        ax.set_title(scenario_labels.get(scenario, scenario))
        ax.grid(color="#dddddd", linewidth=0.8)
        ax.set_axisbelow(True)
    for ax in axes[:, 0]:
        ax.set_ylabel("Agreement")
    for ax in axes[-1, :]:
        ax.set_xlabel("Cost weight")
    axes_list[0].legend(frameon=False, loc="lower left")
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def plot_pareto_jaccard_by_scenario(
    context_rows: list[dict[str, Any]],
    output: str | Path,
    *,
    scenario_order: list[str],
    scenario_labels: dict[str, str],
) -> None:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    data = []
    labels = []
    for scenario in scenario_order:
        values = [float(row["pareto_jaccard"]) for row in context_rows if row["scenario"] == scenario]
        data.append(values)
        labels.append(scenario_labels.get(scenario, scenario).replace(", ", "\n"))
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    boxes = ax.boxplot(data, patch_artist=True, showfliers=False)
    colors = ["#4C78A8", "#F58518", "#54A24B", "#B279A2"]
    for patch, color in zip(boxes["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.72)
    ax.set_xticks(range(1, len(labels) + 1))
    ax.set_xticklabels(labels)
    ax.set_ylim(-0.02, 1.02)
    ax.set_ylabel("Count-vs-measured Pareto Jaccard")
    ax.grid(axis="y", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def plot_pareto_pair_frequencies(
    context_rows: list[dict[str, Any]],
    output: str | Path,
    *,
    title: str,
) -> None:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    count_freq: dict[str, int] = {}
    empirical_freq: dict[str, int] = {}
    for row in context_rows:
        for pair in str(row["pareto_count_pairs"]).split(","):
            pair = pair.strip()
            if pair:
                count_freq[pair] = count_freq.get(pair, 0) + 1
        for pair in str(row["pareto_empirical_pairs"]).split(","):
            pair = pair.strip()
            if pair:
                empirical_freq[pair] = empirical_freq.get(pair, 0) + 1
    pairs = sorted(set(count_freq) | set(empirical_freq), key=lambda pair: (-empirical_freq.get(pair, 0), pair))
    y = list(range(len(pairs)))
    height = 0.38
    fig_height = max(4.4, 0.32 * len(pairs) + 1.4)
    fig, ax = plt.subplots(figsize=(8.6, fig_height))
    ax.barh([pos - height / 2 for pos in y], [count_freq.get(pair, 0) for pair in pairs], height=height, color="#4C78A8", label="count")
    ax.barh([pos + height / 2 for pos in y], [empirical_freq.get(pair, 0) for pair in pairs], height=height, color="#F58518", label="measured")
    ax.set_yticks(y)
    ax.set_yticklabels(pairs)
    ax.invert_yaxis()
    ax.set_xlabel("Inputs where pair is Pareto-efficient")
    ax.set_title(title)
    ax.grid(axis="x", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def _median(values: list[float]) -> float:
    values = sorted(values)
    n = len(values)
    mid = n // 2
    if n % 2:
        return values[mid]
    return (values[mid - 1] + values[mid]) / 2.0


def _pair_label(row: dict[str, Any]) -> str:
    return f"{row['strategy']}_{row['level']}"


def plot_pareto_frontier_comparison(
    summary_rows: list[dict[str, Any]],
    output: str | Path,
    *,
    scenario: str,
    scenario_label: str,
) -> None:
    """Plot count-cost and measured-cost Pareto planes for one scenario.

    Points are median strategy-size pairs across contexts for readability. The
    report's Jaccard statistics are still computed per context.
    """

    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = [row for row in summary_rows if row["scenario"] == scenario]
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault((row["strategy"], row["level"]), []).append(row)

    points: list[dict[str, Any]] = []
    for (strategy, level), items in grouped.items():
        points.append(
            {
                "strategy": strategy,
                "level": level,
                "label": f"{strategy}_{level}",
                "pct_n": _median([float(item["pct_n"]) for item in items]),
                "pct_cost": _median([float(item["median_pct_cost"]) for item in items]),
                "mre": _median([float(item["median_mre"]) for item in items]),
            }
        )
    points.sort(key=lambda row: (level_sort_key(row["level"]), strategy_sort_key(row["strategy"])))

    count_cost = [point["pct_n"] for point in points]
    empirical_cost = [point["pct_cost"] for point in points]
    error = [point["mre"] for point in points]
    count_frontier = pareto_mask(np.array(count_cost, dtype=float), np.array(error, dtype=float))
    empirical_frontier = pareto_mask(np.array(empirical_cost, dtype=float), np.array(error, dtype=float))
    membership: list[str] = []
    for on_count, on_measured in zip(count_frontier, empirical_frontier):
        if on_count and on_measured:
            membership.append("shared")
        elif on_measured:
            membership.append("measured_only")
        elif on_count:
            membership.append("count_only")
        else:
            membership.append("neither")

    membership_styles = {
        "shared": {"edge": "#111111", "label": "shared frontier", "width": 1.7},
        "measured_only": {"edge": "#E45756", "label": "measured-only frontier", "width": 2.0},
        "count_only": {"edge": "#4C78A8", "label": "count-only frontier", "width": 2.0},
        "neither": {"edge": "white", "label": "", "width": 0.6},
    }
    count_n = int(sum(bool(value) for value in count_frontier))
    measured_n = int(sum(bool(value) for value in empirical_frontier))
    measured_only_n = sum(value == "measured_only" for value in membership)
    count_only_n = sum(value == "count_only" for value in membership)
    measured_delta = ""
    if measured_only_n or count_only_n:
        pieces = []
        if measured_only_n:
            pieces.append(f"+{measured_only_n}")
        if count_only_n:
            pieces.append(f"-{count_only_n}")
        measured_delta = f"; {'/'.join(pieces)}"

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.2), sharey=True)
    panels = [
        (axes[0], f"Count-cost frontier ({count_n} pairs)", count_cost, count_frontier, "Training size (% of configurations)"),
        (
            axes[1],
            f"Measured-cost frontier ({measured_n} pairs{measured_delta})",
            empirical_cost,
            empirical_frontier,
            "Measured cost (% of full cost)",
        ),
    ]
    for ax, title, x_values, frontier, xlabel in panels:
        for idx, point in enumerate(points):
            is_frontier = bool(frontier[idx])
            style = membership_styles[membership[idx]]
            highlighted = membership[idx] != "neither"
            ax.scatter(
                100 * x_values[idx],
                point["mre"],
                s=104 if highlighted else 50,
                marker=MARKERS.get(point["level"], "o"),
                color=PALETTE.get(point["strategy"], "#999999"),
                edgecolors=style["edge"],
                linewidths=style["width"],
                alpha=0.95 if highlighted or is_frontier else 0.56,
            )
        frontier_points = [
            (100 * x_values[idx], error[idx], points[idx]["label"], idx)
            for idx, is_frontier in enumerate(frontier)
            if is_frontier
        ]
        frontier_points.sort(key=lambda item: (item[0], item[1]))
        if frontier_points:
            ax.plot(
                [item[0] for item in frontier_points],
                [item[1] for item in frontier_points],
                color="#222222",
                linewidth=1.2,
                alpha=0.75,
            )
            for x, y, label, idx in frontier_points:
                ax.annotate(
                    label,
                    (x, y),
                    xytext=(4, 4),
                    textcoords="offset points",
                    fontsize=7,
                    color=membership_styles[membership[idx]]["edge"],
                )
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.grid(color="#dddddd", linewidth=0.8)
        ax.set_axisbelow(True)

    axes[0].set_ylabel("Median MRE")
    fig.suptitle(scenario_label, y=1.02)
    strategy_handles = [
        plt.Line2D([0], [0], marker="o", linestyle="", color=PALETTE.get(strategy, "#999999"), label=strategy)
        for strategy in sorted({point["strategy"] for point in points}, key=strategy_sort_key)
    ]
    level_handles = [
        plt.Line2D([0], [0], marker=MARKERS.get(level, "o"), linestyle="", color="#555555", label=level)
        for level in sorted({point["level"] for point in points}, key=level_sort_key)
    ]
    membership_handles = []
    for name in ["shared", "measured_only", "count_only"]:
        if name not in membership:
            continue
        style = membership_styles[name]
        membership_handles.append(
            plt.Line2D(
                [0],
                [0],
                marker="o",
                linestyle="",
                markerfacecolor="white",
                markeredgecolor=style["edge"],
                markeredgewidth=style["width"],
                color=style["edge"],
                label=style["label"],
            )
        )
    axes[0].legend(handles=membership_handles, frameon=False, fontsize=8, loc="upper right")
    axes[1].legend(
        handles=[*strategy_handles, *level_handles],
        frameon=False,
        fontsize=8,
        loc="upper right",
    )
    fig.tight_layout()
    fig.savefig(output, dpi=200, bbox_inches="tight")
    plt.close(fig)
