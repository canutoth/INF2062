#!/usr/bin/env python3
"""Run learner-sensitivity experiments across the study families.

This is deliberately separate from the paper-generation scripts: it creates a
robustness artifact that varies only the prediction learner while keeping the
sampling/cost protocol for each family fixed.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import subprocess
import sys
import time


REPO_ROOT = Path(__file__).resolve().parents[1]


LINUX_RELEASES = {
    "413": "ICPE-rawdata/linux/tuxkconfig_413.parquet",
    "415": "ICPE-rawdata/linux/tuxkconfig_415.parquet",
    "420": "ICPE-rawdata/linux/tuxkconfig_420.parquet",
    "500": "ICPE-rawdata/linux/tuxkconfig_500.parquet",
    "504": "ICPE-rawdata/linux/tuxkconfig_504.parquet",
    "507": "ICPE-rawdata/linux/tuxkconfig_507.parquet",
    "508": "ICPE-rawdata/linux/tuxkconfig_508.parquet",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="artifacts/learner_sensitivity")
    parser.add_argument(
        "--families",
        default="replication,energy,workload,lcbench,linux",
        help="Comma-separated subset of replication,energy,workload,lcbench,linux.",
    )
    parser.add_argument("--trace-learners", default="ridge-log,rf-log,gbt-log")
    parser.add_argument("--generated-learners", default="ridge-log,rf-log,gbt-log")
    parser.add_argument("--lcbench-learners", default="ridge-raw,rf-raw,gbt-raw")
    parser.add_argument("--max-runs", type=int, default=20, help="Published-trace runs for REPLICATION.")
    parser.add_argument("--replication-contexts", default="0-16", help="x264 input indices for REPLICATION matrix.")
    parser.add_argument(
        "--newruns-contexts",
        default="7z,BerkeleyDBC,Dune,Hipacc,LLVM,Polly,lrzip",
        help="Comma-separated NewRuns contexts for REPLICATION.",
    )
    parser.add_argument("--seeds", type=int, default=10, help="Generated-family stochastic seeds.")
    parser.add_argument("--max-budget", type=int, default=64, help="Generated-family maximum sample size.")
    parser.add_argument("--twins-max-rows", type=int, default=5000)
    parser.add_argument("--linux-levels", default="0.01,0.02,0.05")
    parser.add_argument("--linux-stochastic-runs", type=int, default=10)
    parser.add_argument("--linux-diversity-runs", type=int, default=2)
    parser.add_argument("--linux-uncertainty-runs", type=int, default=2)
    parser.add_argument("--linux-coverage-runs", type=int, default=2)
    parser.add_argument(
        "--linux-top-k-features",
        type=int,
        default=512,
        help="Linux feature cap passed to run_linux_kernel.py. Use 0 to keep all post-pruning features.",
    )
    parser.add_argument("--continue-on-error", action="store_true")
    return parser.parse_args()


def _split(raw: str) -> list[str]:
    return [item.strip() for item in raw.split(",") if item.strip()]


def _append_manifest(path: Path, row: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists() and path.stat().st_size > 0
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def _run(
    *,
    manifest: Path,
    family: str,
    learner: str,
    label: str,
    output_dir: Path,
    cmd: list[str],
    continue_on_error: bool,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    log_path = output_dir / "run.log"
    start = time.time()
    with log_path.open("w", encoding="utf-8") as log:
        log.write("COMMAND: " + " ".join(cmd) + "\n\n")
        log.flush()
        result = subprocess.run(cmd, cwd=REPO_ROOT, stdout=log, stderr=subprocess.STDOUT, text=True)
    elapsed = time.time() - start
    row = {
        "family": family,
        "learner": learner,
        "label": label,
        "returncode": result.returncode,
        "elapsed_seconds": round(elapsed, 3),
        "output_dir": str(output_dir),
        "log_path": str(log_path),
    }
    _append_manifest(manifest, row)
    if result.returncode != 0 and not continue_on_error:
        raise SystemExit(result.returncode)


def main() -> None:
    args = parse_args()
    root = REPO_ROOT / args.output_dir
    root.mkdir(parents=True, exist_ok=True)
    manifest = root / "manifest.csv"
    families = set(_split(args.families))

    if "replication" in families:
        for learner in _split(args.trace_learners):
            out = root / "replication" / learner / "x264_matrix"
            _run(
                manifest=manifest,
                family="REPLICATION",
                learner=learner,
                label="x264_matrix",
                output_dir=out,
                cmd=[
                    sys.executable,
                    "scripts/run_x264_matrix.py",
                    "--max-runs",
                    str(args.max_runs),
                    "--contexts",
                    args.replication_contexts,
                    "--learner",
                    learner,
                    "--output-dir",
                    str(out),
                ],
                continue_on_error=args.continue_on_error,
            )
            out = root / "replication" / learner / "newruns"
            _run(
                manifest=manifest,
                family="REPLICATION",
                learner=learner,
                label="newruns",
                output_dir=out,
                cmd=[
                    sys.executable,
                    "scripts/run_newruns_batch.py",
                    "--max-runs",
                    str(args.max_runs),
                    "--contexts",
                    args.newruns_contexts,
                    "--learner",
                    learner,
                    "--output-dir",
                    str(out),
                ],
                continue_on_error=args.continue_on_error,
            )

    if "energy" in families:
        for learner in _split(args.generated_learners):
            out = root / "energy" / learner
            _run(
                manifest=manifest,
                family="ENERGY",
                learner=learner,
                label="twins",
                output_dir=out,
                cmd=[
                    sys.executable,
                    "scripts/run_twins_batch.py",
                    "--seeds",
                    str(args.seeds),
                    "--max-budget",
                    str(args.max_budget),
                    "--max-rows",
                    str(args.twins_max_rows),
                    "--learner",
                    learner,
                    "--continue-on-error",
                    "--output-dir",
                    str(out),
                ],
                continue_on_error=args.continue_on_error,
            )

    if "workload" in families:
        for learner in _split(args.generated_learners):
            out = root / "workload" / learner
            _run(
                manifest=manifest,
                family="WORKLOAD",
                learner=learner,
                label="workload-impact",
                output_dir=out,
                cmd=[
                    sys.executable,
                    "scripts/run_workload_batch.py",
                    "--seeds",
                    str(args.seeds),
                    "--max-budget",
                    str(args.max_budget),
                    "--learner",
                    learner,
                    "--continue-on-error",
                    "--output-dir",
                    str(out.relative_to(REPO_ROOT)),
                ],
                continue_on_error=args.continue_on_error,
            )
            subprocess.run(
                [
                    sys.executable,
                    "scripts/summarize_workload_batch.py",
                    "--input-dir",
                    str(out.relative_to(REPO_ROOT)),
                ],
                cwd=REPO_ROOT,
                check=False,
            )

    if "lcbench" in families:
        for learner in _split(args.lcbench_learners):
            out = root / "lcbench" / learner
            _run(
                manifest=manifest,
                family="LCBENCH",
                learner=learner,
                label="data_2k_lw",
                output_dir=out,
                cmd=[
                    sys.executable,
                    "scripts/run_lcbench_systematic.py",
                    "--seeds",
                    str(args.seeds),
                    "--max-budget",
                    str(args.max_budget),
                    "--learner",
                    learner,
                    "--output-dir",
                    str(out.relative_to(REPO_ROOT)),
                ],
                continue_on_error=args.continue_on_error,
            )

    if "linux" in families:
        for learner in _split(args.generated_learners):
            for release, parquet in LINUX_RELEASES.items():
                out = root / "linux" / learner / f"linux{release}_vmlinux"
                if not (REPO_ROOT / parquet).exists():
                    _append_manifest(
                        manifest,
                        {
                            "family": "LINUX",
                            "learner": learner,
                            "label": release,
                            "returncode": 127,
                            "elapsed_seconds": 0,
                            "output_dir": str(out),
                            "log_path": "",
                        },
                    )
                    continue
                _run(
                    manifest=manifest,
                    family="LINUX",
                    learner=learner,
                    label=release,
                    output_dir=out,
                    cmd=[
                        sys.executable,
                        "scripts/run_linux_kernel.py",
                        "--parquet",
                        parquet,
                        "--release",
                        release,
                        "--levels",
                        args.linux_levels,
                        "--stochastic-runs",
                        str(args.linux_stochastic_runs),
                        "--diversity-runs",
                        str(args.linux_diversity_runs),
                        "--uncertainty-runs",
                        str(args.linux_uncertainty_runs),
                        "--coverage-runs",
                        str(args.linux_coverage_runs),
                        "--top-k-features",
                        str(args.linux_top_k_features),
                        "--learner",
                        learner,
                        "--output-dir",
                        str(out),
                    ],
                    continue_on_error=args.continue_on_error,
                )

    print(f"Wrote learner-sensitivity runs under {root}")


if __name__ == "__main__":
    main()
