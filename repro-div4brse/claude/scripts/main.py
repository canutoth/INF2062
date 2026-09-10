"""CLI orchestrator — Specification 00 §5.

Runs each analysis script as a subprocess from its own directory, so the
`../../data/` and `../../results/` relative paths used by the scripts resolve.

    python main.py --all
    python main.py --rq3 --rq4
    python main.py --characterization -q

NOTE (Spec 00 §5.1): the upstream `main.py` is missing a comma between
`'RQ3/sintonia.py'` and `'RQ3/stats_tests.py'`, so Python concatenates them into
one bogus path and `stats_tests.py` never runs through the orchestrator. That
bug is FIXED here — `--rq3` runs all three RQ3 scripts. The upstream argparse
help strings are also mislabeled; the help below follows the authoritative
`SCRIPTS` table instead.
"""

import argparse
import os
import subprocess
import sys

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

SCRIPTS = {
    "characterization": ["participant_characterization/characterization.py"],
    "rq1": ["RQ1/coding_inclusion_diversity.py", "RQ1/diversitycloud.py"],
    "rq2": ["RQ2/coding_discrimination_prejudice.py", "RQ2/discriminationcloud.py"],
    "rq3": ["RQ3/profile.py", "RQ3/sintonia.py", "RQ3/stats_tests.py"],
    "rq4": ["RQ4/company.py", "RQ4/logistic_regression.py"],
    "rq5": ["RQ5/intersection.py"],
    "rq6": ["RQ6/teams.py", "RQ6/leaders.py"],
    "rq7": ["RQ7/coding_bias.py"],
}

ORDER = ["characterization", "rq1", "rq2", "rq3", "rq4", "rq5", "rq6", "rq7"]

HELP = {
    "characterization": "Demographic and professional profile of the sample",
    "rq1": "RQ1 — how practitioners define diversity and inclusion",
    "rq2": "RQ2 — how practitioners define prejudice and discrimination",
    "rq3": "RQ3 — perceived recurrence of discrimination by demographic profile",
    "rq4": "RQ4 — perceived recurrence of discrimination by organizational setting",
    "rq5": "RQ5 — workplace discrimination: recognize, narrate, silence",
    "rq6": "RQ6 — representation in development teams vs. leadership roles",
    "rq7": "RQ7 — self-awareness of unconscious bias",
}


def run_script(relative_path, quiet):
    full_path = os.path.join(SCRIPTS_DIR, relative_path)
    if not os.path.exists(full_path):
        print(f"[SKIP] {relative_path} — file not found", file=sys.stderr)
        return False

    workdir = os.path.dirname(full_path)
    filename = os.path.basename(full_path)

    if not quiet:
        print(f"\n{'=' * 72}\n[RUN] {relative_path}\n{'=' * 72}")

    completed = subprocess.run(
        [sys.executable, filename],
        cwd=workdir,
        capture_output=quiet,
        text=True,
    )

    if completed.returncode != 0:
        print(f"[FAIL] {relative_path} (exit {completed.returncode})", file=sys.stderr)
        if quiet and completed.stderr:
            print(completed.stderr, file=sys.stderr)
        return False

    if quiet:
        print(f"[OK] {relative_path}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Reproduce the analyses of 'Diversity, Equity, and Inclusion in "
        "Software Engineering: Perceptions from Professionals in Brazil'.",
    )
    parser.add_argument("--all", action="store_true", help="Run every module, in order")
    for module in ORDER:
        parser.add_argument(f"--{module}", action="store_true", help=HELP[module])
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress script output")

    args = parser.parse_args()
    selected = [m for m in ORDER if getattr(args, m.replace("-", "_"))]
    if args.all or not selected:
        selected = ORDER

    failures = []
    for module in selected:
        for relative_path in SCRIPTS[module]:
            if not run_script(relative_path, args.quiet):
                failures.append(relative_path)

    print()
    if failures:
        print(f"Finished with {len(failures)} failure(s): {', '.join(failures)}")
        return 1
    print(f"Finished: {sum(len(SCRIPTS[m]) for m in selected)} script(s) ran successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
