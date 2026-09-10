#!/usr/bin/env python3
"""Merge per-release Linux full-pass parts into one aggregate directory.

The resumable sweep (`run_linux_full_parts.sh`) writes one output directory
per release under `artifacts/fse_posterior_linux_full_parts/r<rel>/`. Each
part carries the same CSV schemas as a monolithic
`run_fse_posterior_linux_batch.py` run restricted to that release, so the
aggregate tables are plain concatenations. The merged directory can then be
passed to `build_fse_posterior_synthesis.py --linux-dir`.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

CSVS = [
    "posterior_linux_release_summary.csv",
    "posterior_linux_budget_trends.csv",
    "posterior_strategy_summary.csv",
    "posterior_hypothesis_summary.csv",
    "posterior_hypothesis_tests.csv",
    "posterior_pareto.csv",
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parts-dir", default="artifacts/fse_posterior_linux_full_parts")
    parser.add_argument("--output-dir", default="artifacts/fse_posterior_linux_all_full")
    parser.add_argument(
        "--require",
        type=int,
        default=7,
        help="Expected number of release parts; fail if fewer are complete.",
    )
    args = parser.parse_args()

    parts_dir = Path(args.parts_dir)
    parts = sorted(
        p for p in parts_dir.glob("r*") if (p / "posterior_linux_release_summary.csv").exists()
    )
    print(f"[merge] complete parts: {[p.name for p in parts]}")
    if len(parts) < args.require:
        raise SystemExit(f"Only {len(parts)}/{args.require} parts complete; not merging.")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for name in CSVS:
        frames = [pd.read_csv(p / name) for p in parts if (p / name).exists()]
        if not frames:
            print(f"[merge] WARNING: {name} missing in all parts")
            continue
        merged = pd.concat(frames, ignore_index=True)
        merged.to_csv(output_dir / name, index=False)
        print(f"[merge] {name}: {len(merged)} rows from {len(frames)} parts")

    summary = pd.read_csv(output_dir / "posterior_linux_release_summary.csv")
    n = len(summary)
    lines = [
        "# Full Linux pass (merged from per-release parts)",
        "",
        "Protocol: levels 0.01/0.02/0.05, 100 stochastic runs, 20 runs per",
        "deterministic family, 100 SRS seeds, top-k 512 features, extreme max,",
        "prior offset 1. Run release-by-release for jetsam resilience",
        "(`scripts/run_linux_full_parts.sh`), merged by this script.",
        "",
        f"Scopes (release x level): {n}",
        f"- risk distributions differ: {(summary['fse1_verdict'] == 'supports').sum()}/{n}",
        f"- SRS best cost-normalized: {int(summary['srs_best_cost'].sum())}/{n}",
        f"- SRS on empirical frontier: {int(summary['srs_on_empirical_confidence_front'].sum())}/{n}",
        f"- top changed by cost: {int(summary['top_changed_by_cost'].sum())}/{n}",
        f"- frontier changed by cost: {int((summary['pareto_jaccard'] < 1.0).sum())}/{n}",
        f"- SRS lower risk than random: {(summary['fse5_verdict'] == 'supports').sum()}/{n}",
        f"- SRS cost differs from random: {(summary['fse6_verdict'] == 'supports').sum()}/{n}",
        "",
        "Per-release reports live in the part directories",
        f"(`{parts_dir}/r<release>/`).",
    ]
    (output_dir / "fse_posterior_linux_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[merge] wrote {output_dir}/fse_posterior_linux_report.md")


if __name__ == "__main__":
    main()
