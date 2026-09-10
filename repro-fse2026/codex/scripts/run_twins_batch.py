#!/usr/bin/env python3
"""Run generated-sampling protocol across TwinsOrFalseFriends systems."""

from __future__ import annotations

import argparse
import csv
from io import StringIO
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import zipfile
from typing import Any

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
from cost_sampling.metrics import LEARNER_CHOICES


DEFAULT_ZIP = "/private/tmp/TwinsOrFalseFriends-ICSE2023.zip"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", default=DEFAULT_ZIP, help="Path to TwinsOrFalseFriends ZIP.")
    parser.add_argument("--output-dir", default="artifacts/twins_generated_quick", help="Batch output directory.")
    parser.add_argument("--systems", default="ALL", help="Comma-separated systems or ALL.")
    parser.add_argument("--seeds", type=int, default=3, help="Stochastic seeds per budget for the broad pass.")
    parser.add_argument("--max-budget", type=int, default=32, help="Maximum sample size for the broad pass.")
    parser.add_argument(
        "--max-rows",
        type=int,
        default=5000,
        help="Cap rows after revision filtering for large systems; use 0 for no cap.",
    )
    parser.add_argument("--learner", default="ridge-log", choices=LEARNER_CHOICES)
    parser.add_argument("--keep-all-revisions", action="store_true", help="Do not filter revisioned systems to latest revision.")
    parser.add_argument("--continue-on-error", action="store_true", help="Continue if a system fails.")
    return parser.parse_args()


def _sniff_csv(text: str) -> csv.Dialect:
    return csv.Sniffer().sniff(text[:20000], delimiters=",;\t")


def _natural_key(value: str) -> tuple[Any, ...]:
    parts = re.split(r"(\d+)", value)
    out: list[Any] = []
    for part in parts:
        if part.isdigit():
            out.append(int(part))
        elif part:
            out.append(part)
    return tuple(out)


def _safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).replace(".", "_")


def _read_system_table(zip_path: str, system: str) -> tuple[list[str], list[dict[str, str]]]:
    with zipfile.ZipFile(zip_path) as archive:
        root = archive.namelist()[0].split("/")[0] + "/"
        member = f"{root}data/{system}/measurements.csv"
        text = archive.read(member).decode("utf-8", errors="replace")
    dialect = _sniff_csv(text)
    rows = list(csv.DictReader(StringIO(text), dialect=dialect))
    return list(rows[0].keys()), rows


def list_systems(zip_path: str) -> list[str]:
    with zipfile.ZipFile(zip_path) as archive:
        root = archive.namelist()[0].split("/")[0] + "/"
        systems = [
            name.split("/")[2]
            for name in archive.namelist()
            if name.startswith(root + "data/") and name.endswith("/measurements.csv")
        ]
    return sorted(systems, key=str.lower)


def _row_range(rows: list[dict[str, Any]], key: str) -> tuple[float, float]:
    values = [float(row[key]) for row in rows]
    return min(values), max(values)


def _build_report(
    output: Path,
    *,
    systems: list[dict[str, Any]],
    scenario_rows: list[dict[str, Any]],
    seeds: int,
    max_budget: int,
    max_rows: int,
) -> None:
    lines = [
        "# TwinsOrFalseFriends Generated-Sampling Batch",
        "",
        "## Scope",
        "",
        f"This is a broad generated-protocol pass with `{seeds}` seeds, max budget `{max_budget}`, "
        f"and row cap `{max_rows if max_rows else 'none'}`.",
        "",
        "Revisioned systems are filtered to the latest revision unless the batch is run with "
        "`--keep-all-revisions`. Large systems may be row-capped, so this folder is exploratory "
        "unless rerun without a cap and with `--seeds 100`.",
        "",
        "## System Coverage",
        "",
        "| System | Filter | Rows used | Row cap | Report |",
        "|---|---|---:|---:|---|",
    ]
    for row in systems:
        lines.append(
            f"| `{row['system']}` | `{row['filter'] or 'none'}` | {row['rows_used']} | "
            f"{row['row_cap'] or 'none'} | [{row['report']}]({row['report']}) |"
        )

    lines.extend(
        [
            "",
        "## Result Ranges",
        "",
        "![Cost CV range by system](fig_cost_cv_range_by_system.png)",
        "",
        "![Decision agreement by system](fig_decision_agreement_by_system.png)",
        "",
        "| System | Cost CV range | Top-1 agreement range | Pareto Jaccard range |",
            "|---|---:|---:|---:|",
        ]
    )
    for system in systems:
        rows = [row for row in scenario_rows if row["analysis_context"] == system["analysis_context"]]
        if not rows:
            continue
        cv_min, cv_max = _row_range(rows, "cost_cv")
        top_min, top_max = _row_range(rows, "rank_top1_agreement")
        jac_min, jac_max = _row_range(rows, "pareto_jaccard")
        lines.append(
            f"| `{system['analysis_context']}` | {cv_min:.4g}-{cv_max:.4g} | "
            f"{top_min:.4g}-{top_max:.4g} | {jac_min:.4g}-{jac_max:.4g} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This batch is designed to maximize dataset coverage quickly. Use it to identify systems "
            "where empirical cost clearly matters, then rerun the strongest and weakest systems with "
            "`--seeds 100`, a larger `--max-budget`, and no row cap if feasible.",
            "",
        ]
    )
    output.write_text("\n".join(lines), encoding="utf-8")


def _plot_batch_figures(output_dir: Path, systems: list[dict[str, Any]], scenario_rows: list[dict[str, Any]]) -> None:
    if not scenario_rows:
        return
    contexts = [row["analysis_context"] for row in systems]
    rows_by_context = {
        context: [row for row in scenario_rows if row["analysis_context"] == context]
        for context in contexts
    }

    cv_ranges = []
    top_ranges = []
    jac_ranges = []
    for context in contexts:
        rows = rows_by_context[context]
        cv_ranges.append(_row_range(rows, "cost_cv"))
        top_ranges.append(_row_range(rows, "rank_top1_agreement"))
        jac_ranges.append(_row_range(rows, "pareto_jaccard"))

    order = sorted(range(len(contexts)), key=lambda idx: cv_ranges[idx][1], reverse=True)
    labels = [contexts[idx] for idx in order]
    y = list(range(len(labels)))

    fig, ax = plt.subplots(figsize=(8.6, max(4.8, 0.35 * len(labels) + 1.2)))
    for pos, idx in enumerate(order):
        lo, hi = cv_ranges[idx]
        ax.plot([lo, hi], [pos, pos], color="#4C78A8", linewidth=5, solid_capstyle="round")
        ax.scatter([lo, hi], [pos, pos], color="#1f3b57", s=18, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel("Cost CV range across cost-target scenarios")
    ax.grid(axis="x", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(output_dir / "fig_cost_cv_range_by_system.png", dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8.6, max(4.8, 0.35 * len(labels) + 1.2)))
    height = 0.34
    for pos, idx in enumerate(order):
        top_lo, top_hi = top_ranges[idx]
        jac_lo, jac_hi = jac_ranges[idx]
        ax.plot([top_lo, top_hi], [pos - height / 2, pos - height / 2], color="#F58518", linewidth=4, solid_capstyle="round")
        ax.plot([jac_lo, jac_hi], [pos + height / 2, pos + height / 2], color="#54A24B", linewidth=4, solid_capstyle="round")
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlim(-0.02, 1.02)
    ax.set_xlabel("Agreement range across scenarios")
    ax.grid(axis="x", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    handles = [
        plt.Line2D([0], [0], color="#F58518", linewidth=4, label="Top-1 agreement"),
        plt.Line2D([0], [0], color="#54A24B", linewidth=4, label="Pareto Jaccard"),
    ]
    ax.legend(handles=handles, frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(output_dir / "fig_decision_agreement_by_system.png", dpi=200)
    plt.close(fig)


def _write_union_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    write_csv(path, rows, fieldnames=fieldnames)


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    available = list_systems(args.zip)
    systems = available if args.systems == "ALL" else [item.strip() for item in args.systems.split(",") if item.strip()]
    unknown = sorted(set(systems) - set(available))
    if unknown:
        raise SystemExit(f"Unknown systems: {', '.join(unknown)}; available: {', '.join(available)}")

    system_rows: list[dict[str, Any]] = []
    scenario_rows: list[dict[str, Any]] = []
    failed_rows: list[dict[str, Any]] = []

    for idx, system in enumerate(systems, start=1):
        header, rows = _read_system_table(args.zip, system)
        where_args: list[str] = []
        filter_label = ""
        if "revision" in header and not args.keep_all_revisions:
            revisions = sorted({row["revision"] for row in rows}, key=_natural_key)
            latest = revisions[-1]
            where_args = ["--where", f"revision={latest}"]
            filter_label = f"revision={latest}"
            rows_used_before_cap = sum(1 for row in rows if row["revision"] == latest)
        else:
            rows_used_before_cap = len(rows)

        analysis_context = system if not filter_label else f"{system}_{filter_label.split('=', 1)[1]}"
        context_dir = output_dir / _safe_name(analysis_context)
        row_cap = args.max_rows if args.max_rows and rows_used_before_cap > args.max_rows else 0
        cmd = [
            sys.executable,
            str(REPO_ROOT / "scripts" / "run_twins_generated.py"),
            "--zip",
            args.zip,
            "--system",
            system,
            "--seeds",
            str(args.seeds),
            "--max-budget",
            str(args.max_budget),
            "--learner",
            args.learner,
            "--output-dir",
            str(context_dir),
            "--progress-every",
            "0",
            *where_args,
        ]
        if row_cap:
            cmd.extend(["--max-rows", str(row_cap)])

        print(f"[{idx}/{len(systems)}] {analysis_context}: running {rows_used_before_cap} rows", flush=True)
        result = subprocess.run(cmd, cwd=REPO_ROOT)
        if result.returncode != 0:
            failed_rows.append({"system": system, "analysis_context": analysis_context, "returncode": result.returncode})
            if not args.continue_on_error:
                raise SystemExit(result.returncode)
            continue

        report = f"{_safe_name(analysis_context)}/{system}_generated_report.md"
        used_rows = min(rows_used_before_cap, row_cap) if row_cap else rows_used_before_cap
        system_rows.append(
            {
                "system": system,
                "analysis_context": analysis_context,
                "filter": filter_label,
                "rows_before_cap": rows_used_before_cap,
                "rows_used": used_rows,
                "row_cap": row_cap,
                "report": report,
            }
        )
        summary_path = context_dir / "scenario_summary.csv"
        with summary_path.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                item = dict(row)
                item["analysis_context"] = analysis_context
                item["row_cap"] = row_cap
                scenario_rows.append(item)

    _write_union_csv(output_dir / "system_summary.csv", system_rows)
    _write_union_csv(output_dir / "scenario_summary.csv", scenario_rows)
    _write_union_csv(output_dir / "failed_systems.csv", failed_rows)
    _plot_batch_figures(output_dir, system_rows, scenario_rows)
    _build_report(
        output_dir / "twins_generated_batch_report.md",
        systems=system_rows,
        scenario_rows=scenario_rows,
        seeds=args.seeds,
        max_budget=args.max_budget,
        max_rows=args.max_rows,
    )
    print(f"Done. Batch outputs: {output_dir}")


if __name__ == "__main__":
    main()
