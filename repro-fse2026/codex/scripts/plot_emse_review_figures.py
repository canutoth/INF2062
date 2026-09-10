#!/usr/bin/env python3
"""Generate paper-facing EMSE review figures from committed synthesis tables."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper" / "emse-svjour3" / "figures"


def read_csv(path: str | Path) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="") as handle:
        return list(csv.DictReader(handle))


def parse_ratio(text: str) -> tuple[int, int]:
    left, right = text.split("/", 1)
    return int(left), int(right)


def save(fig: plt.Figure, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def read_cropped_image(path: Path, threshold: float = 0.985, pad: int = 16) -> np.ndarray:
    image = plt.imread(path)
    rgb = image[..., :3]
    mask = np.any(rgb < threshold, axis=2)
    ys, xs = np.where(mask)
    if len(xs) == 0 or len(ys) == 0:
        return image
    y0 = max(int(ys.min()) - pad, 0)
    y1 = min(int(ys.max()) + pad + 1, image.shape[0])
    x0 = max(int(xs.min()) - pad, 0)
    x1 = min(int(xs.max()) + pad + 1, image.shape[1])
    return image[y0:y1, x0:x1]


def result_rates() -> None:
    rows = read_csv("artifacts/fse_posterior_paper_protocol_synthesis/fse_posterior_paper_protocol_synthesis.csv")
    corpora = [row["corpus"].replace("Original FSE artifact", "FSE artifact") for row in rows]
    metrics = [
        ("risk_distributions_differ", "Risk differs"),
        ("srs_best_cost_normalized", "SRS best"),
        ("srs_on_empirical_pareto", "SRS Pareto"),
        ("frontier_changed_by_cost", "Frontier changes"),
    ]
    y = np.arange(len(corpora))
    height = 0.18
    offsets = np.linspace(-1.5 * height, 1.5 * height, len(metrics))
    colors = ["#4C78A8", "#54A24B", "#F58518", "#E45756"]

    fig, ax = plt.subplots(figsize=(9.2, 4.8))
    for offset, (key, label), color in zip(offsets, metrics, colors):
        values = []
        labels = []
        for row in rows:
            n, d = parse_ratio(row[key])
            values.append(100.0 * n / d)
            labels.append(f"{n}/{d}")
        bars = ax.barh(y + offset, values, height=height, color=color, label=label)
        for bar, text in zip(bars, labels):
            ax.text(
                min(bar.get_width() + 1.2, 102),
                bar.get_y() + bar.get_height() / 2,
                text,
                va="center",
                fontsize=7,
            )

    ax.set_yticks(y)
    ax.set_yticklabels(corpora)
    ax.invert_yaxis()
    ax.set_xlim(0, 108)
    ax.set_xlabel("Scopes supporting indicator (%)")
    ax.set_title("Posterior guarantee and empirical-cost outcomes by corpus")
    ax.grid(axis="x", color="#dddddd", linewidth=0.7)
    ax.legend(loc="lower right", frameon=False, ncols=2)
    save(fig, "fig_result_rates.png")


def verdict_heatmap() -> None:
    rows = [
        row
        for row in read_csv("artifacts/fse_posterior_statistical_tests/fse_posterior_blocked_statistical_summary.csv")
        if row["corpus_role"] == "primary"
    ]
    corpora = ["Original FSE artifact", "x264", "ENERGY", "WORKLOAD", "Linux full", "LCBench"]
    hyps = ["FSE1", "FSE2", "FSE3", "FSE4", "FSE5", "FSE6"]
    label = {
        "supports": 1,
        "refutes": -1,
        "inconclusive": 0,
        "no_decisive_blocks": 0.5,
    }
    colors = {
        1: "#4C78A8",
        -1: "#E45756",
        0: "#C7C7C7",
        0.5: "#F2CF5B",
    }
    text = {
        1: "supports",
        -1: "refutes",
        0: "inconcl.",
        0.5: "mixed",
    }
    lookup = {(row["corpus"], row["hypothesis"]): label[row["block_sign_verdict"]] for row in rows}

    fig, ax = plt.subplots(figsize=(8.5, 4.1))
    for i, corpus in enumerate(corpora):
        for j, hyp in enumerate(hyps):
            value = lookup.get((corpus, hyp), 0)
            ax.add_patch(plt.Rectangle((j, i), 1, 1, color=colors[value], ec="white", lw=1.5))
            ax.text(j + 0.5, i + 0.5, text[value], ha="center", va="center", fontsize=7)

    ax.set_xlim(0, len(hyps))
    ax.set_ylim(0, len(corpora))
    ax.set_xticks(np.arange(len(hyps)) + 0.5)
    ax.set_xticklabels(hyps)
    ax.set_yticks(np.arange(len(corpora)) + 0.5)
    ax.set_yticklabels([c.replace("Original FSE artifact", "FSE artifact") for c in corpora])
    ax.invert_yaxis()
    ax.tick_params(length=0)
    ax.set_title("Block-level verdicts for the FSE1-FSE6 hypothesis family")
    for spine in ax.spines.values():
        spine.set_visible(False)
    save(fig, "fig_block_verdict_heatmap.png")


def fse_system_summary() -> None:
    rows = read_csv("artifacts/fse_posterior_fse_artifact_clean_paper_protocol/posterior_system_summary.csv")
    rows.sort(key=lambda row: float(row["best_cost_omega"]) - float(row["srs_omega_cost"]), reverse=True)
    systems = [row["context"] for row in rows]
    gaps = [float(row["best_cost_omega"]) - float(row["srs_omega_cost"]) for row in rows]
    pareto = [row["srs_on_empirical_confidence_frontier"] == "1" for row in rows]
    best = [row["srs_best_cost_normalized"] == "1" for row in rows]
    changed = [row["cost_normalization_changed_top"] == "1" for row in rows]

    fig, ax = plt.subplots(figsize=(8.4, 4.4))
    y = np.arange(len(rows))
    colors = ["#54A24B" if is_best else "#F58518" if is_pareto else "#B9B9B9" for is_best, is_pareto in zip(best, pareto)]
    bars = ax.barh(y, gaps, color=colors)
    for idx, (bar, is_changed, row) in enumerate(zip(bars, changed, rows)):
        marker = "*" if is_changed else ""
        ax.text(
            max(bar.get_width(), 0) + 0.00008,
            bar.get_y() + bar.get_height() / 2,
            f"{row['best_cost_pair']}{marker}",
            va="center",
            fontsize=7,
        )

    ax.set_yticks(y)
    ax.set_yticklabels(systems)
    ax.invert_yaxis()
    ax.set_xlabel("Best cost-normalized omega minus SRS omega")
    ax.set_title("Direct FSE artifact systems: where empirical cost moves SRS")
    ax.axvline(0, color="#333333", linewidth=0.8)
    ax.grid(axis="x", color="#dddddd", linewidth=0.7)
    ax.text(
        0.98,
        0.08,
        "Green: SRS best; orange: SRS Pareto but not best; * top recommendation changes",
        transform=ax.transAxes,
        ha="right",
        fontsize=7,
    )
    save(fig, "fig_fse_system_srs_gap.png")


def fse_key_posteriors() -> None:
    panels = [
        ("7z", ROOT / "artifacts/fse_posterior_fse_artifact_clean_paper_protocol/7z/fig_posterior_risk_by_strategy.png"),
        ("Dune", ROOT / "artifacts/fse_posterior_fse_artifact_clean_paper_protocol/Dune/fig_posterior_risk_by_strategy.png"),
        ("LLVM", ROOT / "artifacts/fse_posterior_fse_artifact_clean_paper_protocol/LLVM/fig_posterior_risk_by_strategy.png"),
    ]
    fig, axes = plt.subplots(1, len(panels), figsize=(11.0, 4.3))
    for ax, (title, path) in zip(axes, panels):
        image = read_cropped_image(path)
        ax.imshow(image)
        ax.set_title(title, fontsize=11)
        ax.axis("off")
    save(fig, "fig_fse_key_posteriors.png")


def curated_gap_examples() -> None:
    rows = read_csv("artifacts/fse_posterior_curated_frontiers/curated_frontier_examples.csv")
    labels = [row["corpus"].replace("Original FSE artifact", "FSE") for row in rows]
    values = [float(row["best_minus_srs_omega_cost"]) for row in rows]
    best = [row["srs_best_cost"] == "1" for row in rows]
    frontier = [row["srs_on_empirical_confidence_front"] == "1" for row in rows]
    colors = ["#54A24B" if b else "#F58518" if f else "#E45756" for b, f in zip(best, frontier)]

    fig, ax = plt.subplots(figsize=(8.4, 3.7))
    x = np.arange(len(rows))
    bars = ax.bar(x, values, color=colors)
    for bar, row in zip(bars, rows):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(values) * 0.03,
            row["level"],
            ha="center",
            fontsize=7,
        )
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=18, ha="right")
    ax.set_ylabel("Best minus SRS omega-cost gap")
    ax.set_title("Curated frontier examples: SRS strength and stress cases")
    ax.grid(axis="y", color="#dddddd", linewidth=0.7)
    ax.text(
        0.02,
        0.92,
        "Green: SRS best; orange: SRS Pareto; red: SRS not frontier",
        transform=ax.transAxes,
        fontsize=7,
    )
    save(fig, "fig_curated_srs_gap.png")


def main() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )
    result_rates()
    verdict_heatmap()
    fse_system_summary()
    fse_key_posteriors()
    curated_gap_examples()


if __name__ == "__main__":
    main()
