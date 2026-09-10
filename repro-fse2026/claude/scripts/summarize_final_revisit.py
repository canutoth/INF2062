#!/usr/bin/env python3
"""Build a final paper-revisit bundle from completed experiment artifacts."""

from __future__ import annotations

import csv
from dataclasses import dataclass
import os
from pathlib import Path
import statistics
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


@dataclass(frozen=True)
class Artifact:
    family: str
    label: str
    learner: str
    role: str
    root: Path
    scope_note: str


ARTIFACTS = [
    Artifact(
        "REPLICATION-ICSE19",
        "Kaltenecker/NewRuns",
        "original/literature regression",
        "primary",
        Path("artifacts/newruns_systems"),
        "full 7-system published-trace revisit",
    ),
    Artifact(
        "REPLICATION-ICSE19",
        "Kaltenecker/NewRuns",
        "sk-rf-log",
        "sensitivity",
        Path("artifacts/strong_learner_overnight/replication/sk-rf-log/newruns"),
        "full 7-system sklearn random-forest sensitivity",
    ),
    Artifact(
        "REPLICATION-ICSE19",
        "Kaltenecker/NewRuns",
        "sk-hgbt-log",
        "sensitivity",
        Path("artifacts/strong_learner_overnight/replication/sk-hgbt-log/newruns"),
        "full 7-system sklearn HGBT sensitivity",
    ),
    Artifact(
        "REPLICATION-ICPE20",
        "x264 matrix",
        "original/literature regression",
        "primary",
        Path("artifacts/x264_matrix"),
        "full 17-input published-trace x264 revisit",
    ),
    Artifact(
        "REPLICATION-ICPE20",
        "x264 matrix",
        "sk-hgbt-log",
        "bounded sensitivity",
        Path("artifacts/strong_learner_overnight/replication/sk-hgbt-log/x264_matrix_slice"),
        "bounded 3-input HGBT slice; not a replacement for the full x264 result",
    ),
    Artifact(
        "ENERGY",
        "Twins/green configuration",
        "ridge-log",
        "primary",
        Path("artifacts/twins_generated_representative_100s"),
        "representative generated-sampling energy/performance batch",
    ),
    Artifact(
        "WORKLOAD",
        "ICSE 2023 workload-impact",
        "ridge-log",
        "baseline",
        Path("artifacts/workload_batch_overnight"),
        "full 9-system workload batch with lightweight learner",
    ),
    Artifact(
        "WORKLOAD",
        "ICSE 2023 workload-impact",
        "sk-hgbt-log",
        "primary",
        Path("artifacts/strong_learner_overnight/workload/sk-hgbt-log"),
        "full 9-system workload batch with sklearn HGBT",
    ),
    Artifact(
        "LCBENCH",
        "LCBench lightweight archive",
        "ridge-raw",
        "primary",
        Path("artifacts/lcbench_data_2k_lw"),
        "35-dataset external-validation batch",
    ),
    Artifact(
        "LCBENCH",
        "LCBench lightweight archive",
        "sk-hgbt-raw",
        "sensitivity",
        Path("artifacts/lcbench_data_2k_lw_skhgbt"),
        "35-dataset sklearn HGBT revisit",
    ),
    Artifact(
        "LINUX",
        "TuxKConfig cross-version",
        "sk-hgbt-log",
        "primary",
        Path("artifacts/linux_hgbt_full_strategy"),
        "full 7-release all-feature full-strategy sklearn HGBT batch",
    ),
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def f(value: Any, default: float = float("nan")) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def hypothesis_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for artifact in ARTIFACTS:
        for row in read_csv(artifact.root / "hypothesis_summary.csv"):
            scopes = f(row.get("scopes"), 0.0)
            supports = f(row.get("supports"), 0.0)
            rows.append(
                {
                    "family": artifact.family,
                    "label": artifact.label,
                    "learner": artifact.learner,
                    "role": artifact.role,
                    "hypothesis": row.get("hypothesis", ""),
                    "scopes": int(scopes),
                    "supports": int(supports),
                    "refutes": int(f(row.get("refutes"), 0.0)),
                    "inconclusive": int(f(row.get("inconclusive"), 0.0)),
                    "support_rate": supports / scopes if scopes else "",
                    "global_verdict": row.get("global_verdict", ""),
                    "source": str(artifact.root / "hypothesis_summary.csv"),
                }
            )
    return rows


def _median(rows: list[dict[str, str]], *names: str) -> float:
    for name in names:
        vals = [f(row.get(name)) for row in rows if row.get(name, "") != ""]
        vals = [value for value in vals if value == value]
        if vals:
            return float(statistics.median(vals))
    return float("nan")


def decision_rows() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for artifact in ARTIFACTS:
        candidates = [
            artifact.root / "release_summary.csv",
            artifact.root / "study_summary.csv",
            artifact.root / "scenario_summary.csv",
            artifact.root / "system_summary.csv",
        ]
        rows: list[dict[str, str]] = []
        source = ""
        best_score = -1
        for path in candidates:
            candidate_rows = read_csv(path)
            if not candidate_rows:
                continue
            keys = set(candidate_rows[0])
            score = len(
                keys
                & {
                    "best_simple_mre",
                    "best_mre",
                    "rank_top1_agreement",
                    "median_top1_agreement",
                    "rank_top1_flips",
                    "pareto_jaccard",
                    "median_pareto_jaccard",
                    "cost_cv",
                    "median_cost_cv",
                }
            )
            if score > best_score:
                rows = candidate_rows
                source = str(path)
                best_score = score
        if not rows:
            continue
        top1 = _median(rows, "median_top1_agreement", "rank_top1_agreement", "rank_top1_agreement_median")
        if top1 != top1:
            flips = [f(row.get("rank_top1_flips")) for row in rows if row.get("rank_top1_flips", "") != ""]
            flips = [value for value in flips if value == value]
            if flips:
                top1 = 1.0 - float(statistics.median(flips)) / 7.0
        out.append(
            {
                "family": artifact.family,
                "label": artifact.label,
                "learner": artifact.learner,
                "role": artifact.role,
                "units": len(rows),
                "median_mre": _median(rows, "best_simple_mre", "best_mre"),
                "median_cost_cv": _median(rows, "median_cost_cv", "cost_cv", "cost_cv_median"),
                "median_proxy_ratio": _median(rows, "median_proxy_ratio", "proxy_median_ratio", "proxy_median_ratio_median"),
                "median_top1_agreement": top1,
                "median_pareto_jaccard": _median(rows, "median_pareto_jaccard", "pareto_jaccard", "pareto_jaccard_median"),
                "source": source,
            }
        )
    return out


def manifest_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for artifact in ARTIFACTS:
        reports = sorted(artifact.root.glob("*report.md"))
        if not reports:
            reports = sorted(artifact.root.glob("*_report.md"))
        figs = sorted(artifact.root.glob("fig_*.png"))
        rows.append(
            {
                "family": artifact.family,
                "label": artifact.label,
                "learner": artifact.learner,
                "role": artifact.role,
                "scope_note": artifact.scope_note,
                "root": str(artifact.root),
                "hypothesis_summary": str(artifact.root / "hypothesis_summary.csv")
                if (artifact.root / "hypothesis_summary.csv").exists()
                else "",
                "main_report": str(reports[0]) if reports else "",
                "figures": "; ".join(str(path) for path in figs),
            }
        )
    return rows


def plot_hypotheses(rows: list[dict[str, Any]], output: Path) -> None:
    primary = [row for row in rows if row["role"] in {"primary", "baseline"} and row["hypothesis"] in {"H1a", "H1b", "H2a", "H2b", "H2c", "H3a", "H4a", "H4b"}]
    families = []
    for row in primary:
        key = f"{row['family']}\n{row['learner']}"
        if key not in families:
            families.append(key)
    hypotheses = ["H1a", "H1b", "H2a", "H2b", "H2c", "H3a", "H4a", "H4b"]
    values = [[float("nan") for _ in families] for _ in hypotheses]
    for row in primary:
        key = f"{row['family']}\n{row['learner']}"
        if key in families and row["hypothesis"] in hypotheses and row["support_rate"] != "":
            values[hypotheses.index(row["hypothesis"])][families.index(key)] = float(row["support_rate"])

    fig, ax = plt.subplots(figsize=(11.5, 4.8))
    image = ax.imshow(values, vmin=0, vmax=1, cmap="YlGnBu", aspect="auto")
    ax.set_xticks(range(len(families)))
    ax.set_xticklabels(families, rotation=35, ha="right", fontsize=8)
    ax.set_yticks(range(len(hypotheses)))
    ax.set_yticklabels(hypotheses)
    for i, row in enumerate(values):
        for j, value in enumerate(row):
            if value == value:
                ax.text(j, i, f"{value:.2f}", ha="center", va="center", fontsize=8)
            else:
                ax.text(j, i, "-", ha="center", va="center", fontsize=8, color="#777777")
    fig.colorbar(image, ax=ax, label="support rate")
    ax.set_title("Hypothesis support rates in final revisit artifacts")
    fig.tight_layout()
    fig.savefig(output, dpi=220)
    plt.close(fig)


def plot_decisions(rows: list[dict[str, Any]], output: Path) -> None:
    rows = [row for row in rows if row["median_top1_agreement"] == row["median_top1_agreement"]]
    labels = [f"{row['family']}\n{row['learner']}" for row in rows]
    x = range(len(rows))
    fig, ax = plt.subplots(figsize=(10.5, 4.5))
    ax.bar([i - 0.18 for i in x], [row["median_top1_agreement"] for row in rows], width=0.36, label="top-1 agreement")
    ax.bar([i + 0.18 for i in x], [row["median_pareto_jaccard"] for row in rows], width=0.36, label="Pareto Jaccard")
    ax.set_ylim(0, 1.05)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=8)
    ax.set_ylabel("median agreement")
    ax.legend(frameon=False)
    ax.set_title("Decision sensitivity under primary and robustness learners")
    ax.grid(axis="y", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(output, dpi=220)
    plt.close(fig)


def write_report(output: Path, manifest: list[dict[str, Any]], hypotheses: list[dict[str, Any]], decisions: list[dict[str, Any]]) -> None:
    primary = [row for row in manifest if row["role"] == "primary"]
    sensitivity = [
        row
        for row in manifest
        if row["role"] in {"sensitivity", "bounded sensitivity", "baseline", "pending sensitivity"}
    ]
    lines = [
        "# Final revisit learner-policy bundle",
        "",
        "## Methodological policy",
        "",
        "For `REPLICATION-ICSE19` and `REPLICATION-ICPE20`, the main paper should present the original/literature-aligned learner as the primary result because the scientific question is a revisit of published sampling assessments. Strong sklearn learners are robustness checks, not replacements for the replication baseline.",
        "",
        "For generated or newly framed families, the main paper should present the strongest validated learner available for the family. In the final completed artifacts this means sklearn HGBT for `WORKLOAD` and `LINUX`; `LCBENCH` and `ENERGY` remain reported with their completed generated-sampling artifacts unless stronger reruns are available. Random forests and boosted trees are treated as strong off-the-shelf sensitivity baselines, using sklearn implementations.",
        "",
        "RQ1 and RQ2 are learner-independent by construction. Learner sensitivity is therefore evaluated through RQ3/RQ4: prediction error, top-1 agreement, and Pareto-front overlap.",
        "",
        "## Primary artifacts",
        "",
        "| Family | Learner | Scope | Root |",
        "|---|---|---|---|",
    ]
    for row in primary:
        lines.append(f"| `{row['family']}` | `{row['learner']}` | {row['scope_note']} | `{row['root']}` |")

    lines.extend(["", "## Sensitivity artifacts", "", "| Family | Learner | Scope | Root |", "|---|---|---|---|"])
    for row in sensitivity:
        lines.append(f"| `{row['family']}` | `{row['learner']}` | {row['scope_note']} | `{row['root']}` |")

    lines.extend(
        [
            "",
            "## Headline learner-sensitivity reading",
            "",
            "- Stronger learners improve absolute prediction accuracy in the Linux all-feature setting, reaching best MRE around 6--11% across releases.",
            "- The main count-vs-empirical-cost conclusion survives: RQ3/RQ4 decision disagreements remain visible under sklearn HGBT/RF.",
            "- In `REPLICATION-ICSE19`, HGBT/RF leave H1/H2 verdicts unchanged and keep H3a refuted globally; H4 support strengthens from 5/7 to 6/7.",
            "- In `WORKLOAD`, HGBT leaves all system-level verdicts unchanged except H3b becomes supported rather than inconclusive.",
            "- In `LINUX`, full-strategy all-feature HGBT supports H1a, H1b, H2a, H2c, H3a, H4a, and H4b; H2b is refuted because aggregate calibration is close to 1 even though strategy-specific calibration differs.",
            "",
            "## Generated files",
            "",
            "- `manifest.csv`: source roots and report paths.",
            "- `hypothesis_by_family_learner.csv`: final hypothesis verdicts by learner/family.",
            "- `decision_by_family_learner.csv`: MRE and decision metrics where available.",
            "- `fig_hypothesis_support_by_family.png`: hypothesis support heatmap.",
            "- `fig_decision_sensitivity.png`: top-1/Pareto decision comparison.",
            "",
        ]
    )
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    output = Path("artifacts/final_revisit")
    output.mkdir(parents=True, exist_ok=True)
    manifest = manifest_rows()
    hypotheses = hypothesis_rows()
    decisions = decision_rows()
    write_csv(output / "manifest.csv", manifest)
    write_csv(output / "hypothesis_by_family_learner.csv", hypotheses)
    write_csv(output / "decision_by_family_learner.csv", decisions)
    plot_hypotheses(hypotheses, output / "fig_hypothesis_support_by_family.png")
    plot_decisions(decisions, output / "fig_decision_sensitivity.png")
    write_report(output / "final_revisit_report.md", manifest, hypotheses, decisions)
    print(f"Wrote final revisit bundle under {output}")


if __name__ == "__main__":
    main()
