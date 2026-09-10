#!/usr/bin/env python3
"""Run the full lightweight LCBench study and summarize it."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from cost_sampling.metrics import LEARNER_CHOICES


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        default="/private/tmp/lcbench/data_2k_lw.json",
        help="Path to the full lightweight LCBench JSON.",
    )
    parser.add_argument("--target-column", default="final_val_accuracy", help="Prediction target column.")
    parser.add_argument("--cost-column", default="time_total", help="Empirical cost column.")
    parser.add_argument(
        "--cost-orientation",
        choices=["lower", "inverse"],
        default="lower",
        help="Use inverse only for benefit-like cost columns.",
    )
    parser.add_argument(
        "--runtime-mode",
        choices=["last", "sum"],
        default="last",
        help="How to flatten the runtime learning curve into scalar acquisition cost.",
    )
    parser.add_argument("--output-dir", default="artifacts/lcbench_data_2k_lw", help="Study output directory.")
    parser.add_argument("--seeds", type=int, default=30, help="Stochastic seeds per budget.")
    parser.add_argument("--max-budget", type=int, default=64, help="Maximum generated sample size.")
    parser.add_argument("--alpha", type=float, default=1.0, help="Ridge regularization strength.")
    parser.add_argument(
        "--learner",
        choices=LEARNER_CHOICES,
        default="ridge-raw",
        help="Learner used to estimate the prediction target.",
    )
    parser.add_argument("--no-oracles", action="store_true", help="Skip cheap/expensive diagnostic oracles.")
    parser.add_argument(
        "--progress-every",
        type=int,
        default=500,
        help="Print progress every N sample evaluations.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = REPO_ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    run_generated = REPO_ROOT / "scripts" / "run_lcbench_generated.py"
    summarize = REPO_ROOT / "scripts" / "summarize_lcbench_study.py"

    generated_cmd = [
        sys.executable,
        str(run_generated),
        "--json",
        args.json,
        "--target-column",
        args.target_column,
        "--cost-column",
        args.cost_column,
        "--cost-orientation",
        args.cost_orientation,
        "--runtime-mode",
        args.runtime_mode,
        "--output-dir",
        str(output_dir),
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
    ]
    if args.no_oracles:
        generated_cmd.append("--no-oracles")

    subprocess.run(generated_cmd, cwd=str(REPO_ROOT), check=True)
    subprocess.run(
        [
            sys.executable,
            str(summarize),
            "--input-dir",
            str(output_dir.relative_to(REPO_ROOT)),
        ],
        cwd=str(REPO_ROOT),
        check=True,
    )
    print(f"Wrote full LCBench study to {output_dir}")


if __name__ == "__main__":
    main()
