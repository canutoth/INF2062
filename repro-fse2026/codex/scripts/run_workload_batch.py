#!/usr/bin/env python3
"""Run the workload-impact generated-sampling pilot across all systems."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys
import time


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from cost_sampling.metrics import LEARNER_CHOICES


@dataclass(frozen=True)
class SystemSpec:
    system: str
    target_column: str
    cost_column: str
    cost_orientation: str
    note: str


SYSTEM_SPECS = {
    "batik": SystemSpec("batik", "time", "time", "lower", "runtime"),
    "dconvert": SystemSpec("dconvert", "time", "time", "lower", "runtime"),
    "h2": SystemSpec("h2", "throughput", "throughput", "inverse", "throughput oriented to cost=1/throughput"),
    "jump3r": SystemSpec("jump3r", "time", "time", "lower", "runtime"),
    "kanzi": SystemSpec("kanzi", "time", "time", "lower", "runtime"),
    "lrzip": SystemSpec("lrzip", "time", "time", "lower", "runtime"),
    "x264": SystemSpec("x264", "time", "time", "lower", "runtime"),
    "xz": SystemSpec("xz", "time", "time", "lower", "runtime"),
    "z3": SystemSpec("z3", "time", "time", "lower", "runtime"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--zip",
        default="/Users/mathieuacher/SANDBOX/cost-sampling-matters/workload-impact-ICSE2023/artifact_excluding_raw_coverage.zip",
        help="Path to artifact_excluding_raw_coverage.zip.",
    )
    parser.add_argument(
        "--systems",
        default="all",
        help="Comma-separated systems to run, or 'all'.",
    )
    parser.add_argument("--seeds", type=int, default=30, help="Stochastic seeds per budget.")
    parser.add_argument("--max-budget", type=int, default=64, help="Maximum generated sample size.")
    parser.add_argument("--max-rows", type=int, default=None, help="Optional deterministic row cap.")
    parser.add_argument("--row-seed", type=int, default=0, help="Seed for --max-rows.")
    parser.add_argument("--alpha", type=float, default=1.0, help="Ridge regularization strength.")
    parser.add_argument(
        "--learner",
        choices=LEARNER_CHOICES,
        default="ridge-log",
        help="Learner passed through to run_workload_generated.py.",
    )
    parser.add_argument("--no-oracles", action="store_true", help="Skip cheap/expensive diagnostic oracles.")
    parser.add_argument(
        "--progress-every",
        type=int,
        default=200,
        help="Print progress every N sample evaluations per system.",
    )
    parser.add_argument(
        "--output-dir",
        default="artifacts/workload_batch_all_systems",
        help="Batch output directory.",
    )
    parser.add_argument("--continue-on-error", action="store_true", help="Continue if one system fails.")
    return parser.parse_args()


def _selected_systems(raw: str) -> list[str]:
    if raw == "all":
        return sorted(SYSTEM_SPECS)
    systems = [part.strip() for part in raw.split(",") if part.strip()]
    unknown = [system for system in systems if system not in SYSTEM_SPECS]
    if unknown:
        raise SystemExit(f"Unknown systems: {', '.join(unknown)}")
    return systems


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    systems = _selected_systems(args.systems)
    batch_dir = REPO_ROOT / args.output_dir
    batch_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = batch_dir / "batch_manifest.csv"
    summary_path = batch_dir / "batch_summary.md"

    rows: list[dict[str, object]] = []
    run_script = REPO_ROOT / "scripts" / "run_workload_generated.py"

    for system in systems:
        spec = SYSTEM_SPECS[system]
        system_dir = batch_dir / system
        system_dir.mkdir(parents=True, exist_ok=True)
        log_path = system_dir / "run.log"
        cmd = [
            sys.executable,
            str(run_script),
            "--zip",
            args.zip,
            "--system",
            spec.system,
            "--target-column",
            spec.target_column,
            "--cost-column",
            spec.cost_column,
            "--cost-orientation",
            spec.cost_orientation,
            "--seeds",
            str(args.seeds),
            "--max-budget",
            str(args.max_budget),
            "--alpha",
            str(args.alpha),
            "--learner",
            args.learner,
            "--progress-every",
            str(args.progress_every),
            "--output-dir",
            str(system_dir),
        ]
        if args.max_rows is not None:
            cmd.extend(["--max-rows", str(args.max_rows), "--row-seed", str(args.row_seed)])
        if args.no_oracles:
            cmd.append("--no-oracles")

        start = time.time()
        with log_path.open("w", encoding="utf-8") as log_handle:
            log_handle.write("COMMAND: " + " ".join(cmd) + "\n\n")
            log_handle.flush()
            proc = subprocess.run(
                cmd,
                cwd=str(REPO_ROOT),
                stdout=log_handle,
                stderr=subprocess.STDOUT,
                text=True,
            )
        elapsed = time.time() - start
        row = {
            "system": spec.system,
            "target_column": spec.target_column,
            "cost_column": spec.cost_column,
            "cost_orientation": spec.cost_orientation,
            "note": spec.note,
            "returncode": proc.returncode,
            "elapsed_seconds": round(elapsed, 3),
            "output_dir": str(system_dir),
            "log_path": str(log_path),
        }
        rows.append(row)
        _write_csv(manifest_path, rows)

        if proc.returncode != 0 and not args.continue_on_error:
            break

    lines = [
        "# Workload-impact batch run",
        "",
        f"Archive: `{args.zip}`",
        "",
        f"Systems requested: `{', '.join(systems)}`",
        "",
        f"Seeds per budget: `{args.seeds}`. Max budget: `{args.max_budget}`. Learner: `{args.learner}`.",
        "",
        "| System | Target | Cost | Orientation | Return code | Elapsed (s) | Output |",
        "|---|---|---|---|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['system']}` | `{row['target_column']}` | `{row['cost_column']}` | "
            f"`{row['cost_orientation']}` | {row['returncode']} | {row['elapsed_seconds']} | "
            f"`{Path(str(row['output_dir'])).name}` |"
        )
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if rows and rows[-1]["returncode"] != 0 and not args.continue_on_error:
        raise SystemExit(int(rows[-1]["returncode"]))


if __name__ == "__main__":
    main()
