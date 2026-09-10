#!/usr/bin/env python3
"""Cross-corpus synthesis of the FSE-posterior-under-empirical-cost study.

Reads the per-corpus scope summaries produced by the run_fse_posterior_*
batch scripts, normalizes them into one scope table, and emits the roadmap's
synthesis table, CSV, and figures (corpus-outcome heatmap, SRS status matrix,
cost-normalization impact, representative guarantee-cost frontiers,
calibration plot).
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Entity-stable strategy hues (validated categorical palette; strategies that
# share a hue never co-occur in one corpus/figure).
STRATEGY_COLORS = {
    "SRSSampling": "#2a78d6",
    "random": "#1baf7a",
    "solverBased": "#eda100",
    "balanced": "#eda100",
    "divDistBased": "#008300",
    "twise": "#4a3aa7",
    "pilotCost": "#4a3aa7",
    "distBased": "#e34948",
    "coverage": "#e34948",
    "henard": "#e87ba4",
    "pairwise": "#e87ba4",
    "uncertainty": "#e87ba4",
    "diversity": "#eb6834",
}
NEUTRAL = "#6b6a63"
SEQ_CMAP = "Blues"

OUTCOME_COLUMNS = [
    ("risk_differs", "Risk distributions differ (H1)"),
    ("top_changed", "Top changed by cost (H2)"),
    ("srs_best", "SRS best cost-normalized (H3)"),
    ("frontier_changed", "Pareto frontier changed (H4)"),
    ("srs_lt_random", "SRS lower risk than random (H5)"),
    ("srs_cost_diff", "SRS cost differs from random (H6)"),
    ("srs_on_front", "SRS on empirical frontier"),
]
OUTCOME_SHORT = {
    "risk_differs": "H1\nrisk\ndiffers",
    "top_changed": "H2\ntop\nchanges",
    "srs_best": "H3\nSRS\nbest",
    "frontier_changed": "H4\nfrontier\nchanges",
    "srs_lt_random": "H5\nSRS <\nrandom",
    "srs_cost_diff": "H6\ncost\ndiffers",
    "srs_on_front": "SRS on\nfrontier",
}

CORPORA = [
    # key, label, taxonomy status
    ("fse", "FSE artifact (REPLICATION-FSE26)", "direct replication"),
    ("x264", "x264 (REPLICATION-ICPE20)", "published-study replication"),
    ("energy", "ENERGY (Twins)", "generated protocol, energy cost"),
    ("workload", "WORKLOAD (ICSE'23)", "generated protocol, workload contexts"),
    ("linux", "Linux (TuxKConfig pools)", "external validity, pool-relative"),
    ("lcbench", "LCBench (HPO pools)", "external validity, pool-relative"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fse-dir", default="artifacts/fse_posterior_fse_artifact_final_t2")
    parser.add_argument("--x264-dir", default="artifacts/fse_posterior_x264_icpe_final")
    parser.add_argument("--x264-level", default="t2")
    parser.add_argument("--energy-dir", default="artifacts/fse_posterior_energy_final")
    parser.add_argument("--workload-dir", default="artifacts/fse_posterior_workload_final")
    parser.add_argument("--linux-dir", default="artifacts/fse_posterior_linux_all_quick_final")
    parser.add_argument("--lcbench-dir", default="artifacts/fse_posterior_lcbench_no_oracles_final")
    parser.add_argument("--output-dir", default="artifacts/fse_posterior_synthesis")
    return parser.parse_args()


def _supports(series: pd.Series) -> pd.Series:
    return (series.astype(str) == "supports").astype(int)


def load_fse(directory: Path) -> pd.DataFrame:
    summary = pd.read_csv(directory / "posterior_system_summary.csv")
    tests = pd.read_csv(directory / "posterior_hypothesis_tests.csv")
    fse1 = {
        str(row["scope"]).split(":")[0]: int(row["verdict"] == "supports")
        for _, row in tests[tests.hypothesis == "FSE1"].iterrows()
    }
    return pd.DataFrame(
        {
            "scope": summary["context"],
            "risk_differs": summary["context"].map(fse1).fillna(0).astype(int),
            "srs_best": summary["srs_best_cost_normalized"].astype(int),
            "srs_on_front": summary["srs_on_empirical_confidence_frontier"].astype(int),
            "top_changed": summary["cost_normalization_changed_top"].astype(int),
            "frontier_changed": summary["confidence_pareto_changed"].astype(int),
            "srs_lt_random": _supports(summary["srs_vs_random_risk_verdict"]),
            "srs_cost_diff": _supports(summary["srs_vs_random_cost_verdict"]),
        }
    )


def load_generated(path: Path, scope_cols: list[str], *, level_filter: str | None = None) -> pd.DataFrame:
    df = pd.read_csv(path)
    if level_filter is not None:
        df = df[df["level"] == level_filter]
    return pd.DataFrame(
        {
            "scope": df[scope_cols].astype(str).agg(":".join, axis=1),
            "risk_differs": _supports(df["fse1_verdict"]),
            "srs_best": df["srs_best_cost"].astype(int),
            "srs_on_front": df["srs_on_empirical_confidence_front"].astype(int),
            "top_changed": df["top_changed_by_cost"].astype(int),
            "frontier_changed": (df["pareto_jaccard"].astype(float) < 1.0).astype(int),
            "srs_lt_random": _supports(df["fse5_verdict"]),
            "srs_cost_diff": _supports(df["fse6_verdict"]),
        }
    )


def load_all(args: argparse.Namespace) -> dict[str, pd.DataFrame]:
    loaders = {
        "fse": lambda: load_fse(Path(args.fse_dir)),
        "x264": lambda: load_generated(
            Path(args.x264_dir) / "posterior_x264_context_summary.csv",
            ["context"],
            level_filter=args.x264_level,
        ),
        "energy": lambda: load_generated(
            Path(args.energy_dir) / "posterior_energy_scenario_summary.csv", ["scenario", "level"]
        ),
        "workload": lambda: load_generated(
            Path(args.workload_dir) / "posterior_workload_context_summary.csv", ["context_pair", "level"]
        ),
        "linux": lambda: load_generated(
            Path(args.linux_dir) / "posterior_linux_release_summary.csv", ["release", "level"]
        ),
        "lcbench": lambda: load_generated(
            Path(args.lcbench_dir) / "posterior_lcbench_dataset_summary.csv", ["workload", "level"]
        ),
    }
    out: dict[str, pd.DataFrame] = {}
    for key, label, _ in CORPORA:
        try:
            out[key] = loaders[key]()
            print(f"[synthesis] {key}: {len(out[key])} scopes")
        except Exception as exc:  # noqa: BLE001
            print(f"[synthesis] SKIPPED {key}: {exc}")
    return out


def corpus_table(scopes: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for key, label, status in CORPORA:
        if key not in scopes:
            continue
        df = scopes[key]
        row: dict[str, object] = {
            "corpus": label,
            "corpus_key": key,
            "status": status,
            "scopes": len(df),
        }
        for col, _ in OUTCOME_COLUMNS:
            row[f"{col}_count"] = int(df[col].sum())
            row[f"{col}_rate"] = float(df[col].mean())
        rows.append(row)
    return pd.DataFrame(rows)


def write_markdown(table: pd.DataFrame, output: Path, *, x264_level: str) -> None:
    lines = [
        "# Cross-corpus synthesis: posterior guarantees per empirical acquisition cost",
        "",
        "Scope = one (context, budget-level) decision cell of the corpus "
        f"(x264 restricted to the fixed `{x264_level}` level; FSE artifact is per system at `t2`).",
        "Counts are scopes where the outcome holds.",
        "",
        "| Corpus | Scopes | Risk differs | SRS best (cost) | SRS on front | Top changes | Frontier changes | SRS < random risk | SRS cost != random | Status |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for _, row in table.iterrows():
        def cell(col: str) -> str:
            return f"{row[f'{col}_count']}/{row['scopes']}"

        lines.append(
            f"| {row['corpus']} | {row['scopes']} | {cell('risk_differs')} | {cell('srs_best')} | "
            f"{cell('srs_on_front')} | {cell('top_changed')} | {cell('frontier_changed')} | "
            f"{cell('srs_lt_random')} | {cell('srs_cost_diff')} | {row['status']} |"
        )
    lines.extend(
        [
            "",
            "Reading guide:",
            "",
            "- `Risk differs`: Kruskal-Wallis on posterior-risk distributions across strategies (H1).",
            "- `SRS best (cost)`: SRS is the top integrated-confidence pick against the empirical-cost prior baseline (H3).",
            "- `Top changes` / `Frontier changes`: switching the cost axis from sample count to measured cost changes the top pick (H2) / the confidence Pareto frontier (H4).",
            "- Linux and LCBench statements are pool-relative (measured reference universes, not exhaustive spaces).",
        ]
    )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def fig_heatmap(table: pd.DataFrame, output: Path) -> None:
    cols = [col for col, _ in OUTCOME_COLUMNS]
    labels = [OUTCOME_SHORT[col] for col in cols]
    data = table[[f"{c}_rate" for c in cols]].to_numpy()
    fig, ax = plt.subplots(figsize=(10.5, 0.62 * len(table) + 2.4))
    im = ax.imshow(data, cmap=SEQ_CMAP, vmin=0.0, vmax=1.0, aspect="auto")
    ax.set_xticks(range(len(labels)), labels, fontsize=8)
    ax.set_yticks(range(len(table)), table["corpus"], fontsize=9)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            value = data[i, j]
            ax.text(
                j,
                i,
                f"{value:.0%}",
                ha="center",
                va="center",
                fontsize=8,
                color="#ffffff" if value > 0.55 else "#1a1a19",
            )
    ax.set_title("Outcome support rate by corpus", fontsize=11, loc="left")
    fig.colorbar(im, ax=ax, shrink=0.8, label="share of scopes")
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def fig_srs_status(table: pd.DataFrame, output: Path) -> None:
    cols = ["srs_best", "srs_on_front", "srs_lt_random", "srs_cost_diff"]
    labels = ["Best\ncost-normalized", "On empirical\nfrontier", "Lower risk\nthan random", "Cost differs\nfrom random"]
    data = table[[f"{c}_rate" for c in cols]].to_numpy()
    fig, ax = plt.subplots(figsize=(8.0, 0.62 * len(table) + 2.2))
    im = ax.imshow(data, cmap=SEQ_CMAP, vmin=0.0, vmax=1.0, aspect="auto")
    ax.set_xticks(range(len(labels)), labels, fontsize=8)
    ax.set_yticks(range(len(table)), table["corpus"], fontsize=9)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            value = data[i, j]
            ax.text(
                j,
                i,
                f"{value:.0%}",
                ha="center",
                va="center",
                fontsize=8,
                color="#ffffff" if value > 0.55 else "#1a1a19",
            )
    ax.set_title("SRS status by corpus (share of scopes)", fontsize=11, loc="left")
    fig.colorbar(im, ax=ax, shrink=0.8, label="share of scopes")
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def fig_impact(table: pd.DataFrame, output: Path) -> None:
    x = np.arange(len(table))
    width = 0.36
    fig, ax = plt.subplots(figsize=(9.0, 4.2))
    bars1 = ax.bar(x - width / 2, table["top_changed_rate"], width, color="#2a78d6", label="Top recommendation changed")
    bars2 = ax.bar(x + width / 2, table["frontier_changed_rate"], width, color="#1baf7a", label="Pareto frontier changed")
    for bars in (bars1, bars2):
        for bar in bars:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.015,
                f"{bar.get_height():.0%}",
                ha="center",
                fontsize=8,
                color="#44433c",
            )
    ax.set_xticks(x, [c.split(" (")[0] for c in table["corpus"]], fontsize=9)
    ax.set_ylim(0, 1.12)
    ax.set_ylabel("share of scopes", fontsize=9)
    ax.set_title("What empirical-cost normalization changes", fontsize=11, loc="left")
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0%}")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#e5e4dc", linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def _frontier_panel(ax: plt.Axes, pareto: pd.DataFrame, *, level: str, title: str) -> None:
    rows = pareto[pareto["level"] == level].copy()
    rows["median_pct_cost"] = rows["median_pct_cost"].astype(float)
    rows["posterior_confidence_area"] = rows["posterior_confidence_area"].astype(float)
    front = rows[rows["pareto_empirical_cost_confidence"].astype(int) == 1].sort_values("median_pct_cost")
    ax.plot(
        front["median_pct_cost"],
        front["posterior_confidence_area"],
        color=NEUTRAL,
        linewidth=1.4,
        zorder=1,
        drawstyle="steps-post",
    )
    for _, row in rows.iterrows():
        color = STRATEGY_COLORS.get(str(row["strategy"]), NEUTRAL)
        is_srs = row["strategy"] == "SRSSampling"
        ax.scatter(
            row["median_pct_cost"],
            row["posterior_confidence_area"],
            s=64 if is_srs else 36,
            color=color,
            edgecolor="#ffffff",
            linewidth=1.2,
            zorder=3 if is_srs else 2,
        )
        if is_srs:
            ax.annotate(
                "SRS",
                (row["median_pct_cost"], row["posterior_confidence_area"]),
                textcoords="offset points",
                xytext=(6, 6),
                fontsize=9,
                color="#2a78d6",
                fontweight="bold",
            )
    ax.set_title(title, fontsize=9.5, loc="left")
    ax.set_xlabel("median % of full acquisition cost", fontsize=8)
    ax.tick_params(labelsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(color="#e5e4dc", linewidth=0.7)
    ax.set_axisbelow(True)


def fig_frontiers(panels: list[tuple[Path, str, str]], output: Path) -> None:
    """panels: (pareto_csv_path, level, title)."""

    available = [(p, level, title) for p, level, title in panels if p.exists()]
    if not available:
        print("[synthesis] no frontier panels available; skipping figure")
        return
    fig, axes = plt.subplots(1, len(available), figsize=(4.2 * len(available), 4.0))
    if len(available) == 1:
        axes = [axes]
    for ax, (path, level, title) in zip(axes, available):
        pareto = pd.read_csv(path)
        _frontier_panel(ax, pareto, level=level, title=title)
        # Per-panel legend: strategy sets differ per corpus and some hues are
        # shared across corpora, so one merged legend would be ambiguous.
        strategies = sorted(pareto[pareto["level"] == level]["strategy"].unique())
        handles = [
            plt.Line2D([], [], marker="o", linestyle="", color=STRATEGY_COLORS.get(s, NEUTRAL), label=s, markersize=6)
            for s in strategies
        ]
        ax.legend(
            handles=handles,
            frameon=False,
            fontsize=7,
            loc="upper center",
            bbox_to_anchor=(0.5, -0.22),
            ncol=2,
        )
    axes[0].set_ylabel("integrated posterior confidence", fontsize=8)
    fig.suptitle("Guarantee-cost frontiers: SRS best / on frontier / off frontier", fontsize=11, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0.02, 1, 0.94))
    fig.savefig(output, dpi=200, bbox_inches="tight")
    plt.close(fig)


def fig_calibration(summaries: list[tuple[str, Path]], output: Path) -> None:
    available = [(label, path) for label, path in summaries if path.exists()]
    if not available:
        print("[synthesis] no calibration inputs; skipping figure")
        return
    ncols = 3
    nrows = int(np.ceil(len(available) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(3.9 * ncols, 4.1 * nrows))
    axes = np.atleast_1d(axes).ravel()
    for ax, (label, path) in zip(axes, available):
        df = pd.read_csv(path)
        df = df[~df["strategy"].astype(str).str.contains("Oracle")]
        lim = 0.0
        panel_strategies: list[str] = []
        for strategy, grp in df.groupby("strategy"):
            color = STRATEGY_COLORS.get(str(strategy), NEUTRAL)
            x = grp["pct_n"].astype(float)
            y = grp["median_pct_cost"].astype(float)
            ax.scatter(x, y, s=14, color=color, alpha=0.75, linewidth=0)
            lim = max(lim, x.max(), y.max())
            panel_strategies.append(str(strategy))
        lim *= 1.06
        ax.plot([0, lim], [0, lim], color=NEUTRAL, linewidth=1.0, linestyle="--", zorder=1)
        ax.set_xlim(0, lim)
        ax.set_ylim(0, lim)
        ax.set_title(label, fontsize=9.5, loc="left")
        ax.tick_params(labelsize=7)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(color="#e5e4dc", linewidth=0.7)
        ax.set_axisbelow(True)
        ax.set_xlabel("% of configurations sampled", fontsize=8)
        ax.set_ylabel("median % of full cost", fontsize=8)
        # Per-panel legend: strategy sets differ per corpus and hues are only
        # unique within a corpus, so one merged legend would be ambiguous.
        handles = [
            plt.Line2D([], [], marker="o", linestyle="", color=STRATEGY_COLORS.get(s, NEUTRAL), label=s, markersize=5)
            for s in sorted(panel_strategies)
        ]
        ax.legend(
            handles=handles,
            frameon=False,
            fontsize=6.5,
            loc="upper center",
            bbox_to_anchor=(0.5, -0.18),
            ncol=3,
        )
    for ax in axes[len(available):]:
        ax.set_visible(False)
    fig.suptitle("Sample-size share vs measured-cost share (y = x: count is a perfect cost proxy)", fontsize=11, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0.01, 1, 0.96))
    fig.savefig(output, dpi=200, bbox_inches="tight")
    plt.close(fig)


def pick_frontier_panels(args: argparse.Namespace, scopes: dict[str, pd.DataFrame]) -> list[tuple[Path, str, str]]:
    panels: list[tuple[Path, str, str]] = []
    # (a) SRS best: first x264 t2 context with srs_best.
    x264 = pd.read_csv(Path(args.x264_dir) / "posterior_x264_context_summary.csv")
    x264 = x264[(x264["level"] == args.x264_level) & (x264["srs_best_cost"] == 1)]
    if len(x264):
        ctx = str(x264.iloc[0]["context"])
        panels.append(
            (Path(args.x264_dir) / ctx / "posterior_pareto.csv", args.x264_level, f"SRS best - x264 `{ctx}` ({args.x264_level})")
        )
    # (b) SRS on frontier but not best: FSE artifact system.
    fse = pd.read_csv(Path(args.fse_dir) / "posterior_system_summary.csv")
    fse_row = fse[(fse["srs_on_empirical_confidence_frontier"] == 1) & (fse["srs_best_cost_normalized"] == 0)]
    if len(fse_row):
        system = str(fse_row.iloc[0]["context"])
        panels.append((Path(args.fse_dir) / system / "posterior_pareto.csv", "t2", f"SRS on frontier, not best - {system} (t2)"))
    # (c) SRS off the frontier: LCBench dataset at its largest level.
    lc = pd.read_csv(Path(args.lcbench_dir) / "posterior_lcbench_dataset_summary.csv")
    lc = lc[(lc["srs_on_empirical_confidence_front"] == 0) & (lc["level"] == "n64")]
    if len(lc):
        workload = str(lc.iloc[0]["workload"])
        slug = "".join(ch if ch.isalnum() else "_" for ch in workload).strip("_")
        panels.append(
            (Path(args.lcbench_dir) / f"lcbench_{slug}" / "posterior_pareto.csv", "n64", f"SRS off frontier - LCBench `{workload}` (n64)")
        )
    return panels


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    scopes = load_all(args)
    if not scopes:
        raise SystemExit("No corpus inputs found.")

    normalized = pd.concat(
        [df.assign(corpus_key=key) for key, df in scopes.items()], ignore_index=True
    )
    normalized.to_csv(output_dir / "fse_posterior_synthesis_scopes.csv", index=False)

    table = corpus_table(scopes)
    table.to_csv(output_dir / "fse_posterior_synthesis.csv", index=False)
    write_markdown(table, output_dir / "fse_posterior_synthesis.md", x264_level=args.x264_level)

    fig_heatmap(table, output_dir / "fig_synthesis_heatmap.png")
    fig_srs_status(table, output_dir / "fig_srs_status_matrix.png")
    fig_impact(table, output_dir / "fig_cost_normalization_impact.png")
    fig_frontiers(pick_frontier_panels(args, scopes), output_dir / "fig_frontiers_representative.png")
    fig_calibration(
        [
            ("FSE artifact", Path(args.fse_dir) / "posterior_strategy_summary.csv"),
            ("x264", Path(args.x264_dir) / "posterior_strategy_summary.csv"),
            ("ENERGY", Path(args.energy_dir) / "posterior_strategy_summary.csv"),
            ("WORKLOAD", Path(args.workload_dir) / "posterior_strategy_summary.csv"),
            ("Linux", Path(args.linux_dir) / "posterior_strategy_summary.csv"),
            ("LCBench", Path(args.lcbench_dir) / "posterior_strategy_summary.csv"),
        ],
        output_dir / "fig_calibration_pct_n_vs_pct_cost.png",
    )
    print(f"Wrote synthesis outputs to {output_dir}")


if __name__ == "__main__":
    main()
