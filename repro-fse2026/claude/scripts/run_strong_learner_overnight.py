#!/usr/bin/env python3
"""Launch the overnight strong-learner robustness batch.

The batch is intentionally explicit: it runs the literature/original learner
where that is the paper baseline, and runs sklearn HGBT as the strong default
candidate where we control the generated-sampling protocol.
"""

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


LINUX_RELEASES = {
    "413": "ICPE-rawdata/linux/tuxkconfig_413.parquet",
    "415": "ICPE-rawdata/linux/tuxkconfig_415.parquet",
    "420": "ICPE-rawdata/linux/tuxkconfig_420.parquet",
    "500": "ICPE-rawdata/linux/tuxkconfig_500.parquet",
    "504": "ICPE-rawdata/linux/tuxkconfig_504.parquet",
    "507": "ICPE-rawdata/linux/tuxkconfig_507.parquet",
    "508": "ICPE-rawdata/linux/tuxkconfig_508.parquet",
}


@dataclass(frozen=True)
class Job:
    family: str
    label: str
    learner: str
    output_dir: Path
    cmd: list[str]
    expected_file: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="artifacts/strong_learner_overnight")
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    parser.add_argument("--workload-seeds", type=int, default=30)
    parser.add_argument("--workload-max-budget", type=int, default=64)
    parser.add_argument("--x264-max-runs", type=int, default=100)
    parser.add_argument("--x264-contexts", default="0-16")
    parser.add_argument(
        "--linux-levels",
        default="0.0108,0.0540,0.1080",
        help="Approximately 1k, 5k, 10k training configs on Linux 4.13.",
    )
    parser.add_argument("--linux-stochastic-runs", type=int, default=3)
    parser.add_argument("--include-rf-targeted", action="store_true")
    return parser.parse_args()


def append_manifest(path: Path, row: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists() and path.stat().st_size > 0
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def job_done(job: Job) -> bool:
    return (job.output_dir / job.expected_file).exists()


def build_jobs(args: argparse.Namespace, root: Path) -> list[Job]:
    py = sys.executable
    jobs: list[Job] = []

    jobs.append(
        Job(
            "REPLICATION",
            "x264_matrix",
            "sk-hgbt-log",
            root / "replication" / "sk-hgbt-log" / "x264_matrix",
            [
                py,
                "scripts/run_x264_matrix.py",
                "--max-runs",
                str(args.x264_max_runs),
                "--contexts",
                args.x264_contexts,
                "--learner",
                "sk-hgbt-log",
                "--output-dir",
                str(root / "replication" / "sk-hgbt-log" / "x264_matrix"),
            ],
            "hypothesis_summary.csv",
        )
    )
    jobs.append(
        Job(
            "REPLICATION",
            "newruns",
            "sk-hgbt-log",
            root / "replication" / "sk-hgbt-log" / "newruns",
            [
                py,
                "scripts/run_newruns_batch.py",
                "--max-runs",
                str(args.x264_max_runs),
                "--learner",
                "sk-hgbt-log",
                "--output-dir",
                str(root / "replication" / "sk-hgbt-log" / "newruns"),
            ],
            "hypothesis_summary.csv",
        )
    )

    jobs.append(
        Job(
            "WORKLOAD",
            "all_systems",
            "sk-hgbt-log",
            root / "workload" / "sk-hgbt-log",
            [
                py,
                "scripts/run_workload_batch.py",
                "--seeds",
                str(args.workload_seeds),
                "--max-budget",
                str(args.workload_max_budget),
                "--learner",
                "sk-hgbt-log",
                "--continue-on-error",
                "--output-dir",
                str((root / "workload" / "sk-hgbt-log").relative_to(REPO_ROOT)),
            ],
            "system_summary.csv",
        )
    )

    for release, parquet in LINUX_RELEASES.items():
        out = root / "linux" / "sk-hgbt-log-allfeatures" / f"linux{release}_vmlinux"
        jobs.append(
            Job(
                "LINUX",
                release,
                "sk-hgbt-log-allfeatures",
                out,
                [
                    py,
                    "scripts/run_linux_kernel.py",
                    "--parquet",
                    parquet,
                    "--release",
                    release,
                    "--output-dir",
                    str(out),
                    "--learner",
                    "sk-hgbt-log",
                    "--top-k-features",
                    "0",
                    "--levels",
                    args.linux_levels,
                    "--stochastic-runs",
                    str(args.linux_stochastic_runs),
                    "--diversity-runs",
                    "0",
                    "--uncertainty-runs",
                    "0",
                    "--coverage-runs",
                    "0",
                    "--predict-chunk",
                    "8192",
                ],
                "strategy_summary.csv",
            )
        )

    twins_zip = Path("/private/tmp/TwinsOrFalseFriends-ICSE2023.zip")
    if twins_zip.exists():
        for learner in ("ridge-log", "sk-hgbt-log"):
            out = root / "energy" / learner
            jobs.append(
                Job(
                    "ENERGY",
                    "twins",
                    learner,
                    out,
                    [
                        py,
                        "scripts/run_twins_batch.py",
                        "--zip",
                        str(twins_zip),
                        "--seeds",
                        "30",
                        "--max-budget",
                        "64",
                        "--max-rows",
                        "5000",
                        "--learner",
                        learner,
                        "--continue-on-error",
                        "--output-dir",
                        str(out),
                    ],
                    "system_summary.csv",
                )
            )

    lcbench_json = Path("/private/tmp/lcbench/data_2k_lw.json")
    if lcbench_json.exists():
        for learner in ("ridge-raw", "sk-hgbt-raw"):
            out = root / "lcbench" / learner
            jobs.append(
                Job(
                    "LCBENCH",
                    "data_2k_lw",
                    learner,
                    out,
                    [
                        py,
                        "scripts/run_lcbench_systematic.py",
                        "--json",
                        str(lcbench_json),
                        "--seeds",
                        "30",
                        "--max-budget",
                        "64",
                        "--learner",
                        learner,
                        "--output-dir",
                        str(out.relative_to(REPO_ROOT)),
                    ],
                    "hypothesis_summary.csv",
                )
            )

    if args.include_rf_targeted:
        out = root / "replication" / "sk-rf-log" / "newruns"
        jobs.append(
            Job(
                "REPLICATION",
                "newruns",
                "sk-rf-log",
                out,
                [
                    py,
                    "scripts/run_newruns_batch.py",
                    "--max-runs",
                    "50",
                    "--learner",
                    "sk-rf-log",
                    "--output-dir",
                    str(out),
                ],
                "hypothesis_summary.csv",
            )
        )

    return jobs


def write_readme(root: Path, jobs: list[Job], args: argparse.Namespace) -> None:
    lines = [
        "# Strong Learner Overnight Batch",
        "",
        "## Purpose",
        "",
        "Collect evidence for the learner policy:",
        "",
        "- keep original/literature learners for reproducibility-sensitive families;",
        "- use sklearn HGBT as the strong default where we choose the learner;",
        "- report learner sensitivity at the decision level, not only MRE.",
        "",
        "## Planned Jobs",
        "",
        "| Family | Label | Learner | Output |",
        "|---|---|---|---|",
    ]
    for job in jobs:
        lines.append(f"| `{job.family}` | `{job.label}` | `{job.learner}` | `{job.output_dir}` |")
    lines.extend(
        [
            "",
            "## Inputs",
            "",
            f"- Workload seeds: `{args.workload_seeds}`",
            f"- Workload max budget: `{args.workload_max_budget}`",
            f"- x264/NewRuns max runs: `{args.x264_max_runs}`",
            f"- x264 contexts: `{args.x264_contexts}`",
            f"- Linux levels: `{args.linux_levels}`",
            f"- Linux stochastic runs: `{args.linux_stochastic_runs}`",
            "",
            "ENERGY and LCBENCH jobs are included only if their source files exist at the expected `/private/tmp` paths.",
        ]
    )
    root.mkdir(parents=True, exist_ok=True)
    (root / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    root = REPO_ROOT / args.output_dir
    jobs = build_jobs(args, root)
    write_readme(root, jobs, args)
    manifest = root / "manifest.csv"

    for index, job in enumerate(jobs, start=1):
        job.output_dir.mkdir(parents=True, exist_ok=True)
        log_path = job.output_dir / "run.log"
        if args.skip_existing and job_done(job):
            print(f"[{index}/{len(jobs)}] skip existing {job.family} {job.label} {job.learner}", flush=True)
            append_manifest(
                manifest,
                {
                    "index": index,
                    "family": job.family,
                    "label": job.label,
                    "learner": job.learner,
                    "status": "skipped_existing",
                    "returncode": 0,
                    "elapsed_seconds": 0,
                    "output_dir": str(job.output_dir),
                    "log_path": str(log_path),
                },
            )
            continue

        print(f"[{index}/{len(jobs)}] start {job.family} {job.label} {job.learner}", flush=True)
        start = time.time()
        with log_path.open("w", encoding="utf-8") as handle:
            handle.write("COMMAND: " + " ".join(job.cmd) + "\n\n")
            handle.flush()
            result = subprocess.run(job.cmd, cwd=REPO_ROOT, stdout=handle, stderr=subprocess.STDOUT, text=True)
        elapsed = time.time() - start
        print(
            f"[{index}/{len(jobs)}] done {job.family} {job.label} {job.learner} "
            f"rc={result.returncode} elapsed={elapsed:.1f}s",
            flush=True,
        )
        append_manifest(
            manifest,
            {
                "index": index,
                "family": job.family,
                "label": job.label,
                "learner": job.learner,
                "status": "done" if result.returncode == 0 else "failed",
                "returncode": result.returncode,
                "elapsed_seconds": round(elapsed, 3),
                "output_dir": str(job.output_dir),
                "log_path": str(log_path),
            },
        )
        if result.returncode != 0 and not args.continue_on_error:
            raise SystemExit(result.returncode)

    print(f"Wrote overnight batch under {root}")


if __name__ == "__main__":
    main()
