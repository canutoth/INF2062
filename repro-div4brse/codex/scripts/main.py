import argparse
import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Upstream main.py has a missing comma between 'RQ3/sintonia.py' and
# 'RQ3/stats_tests.py' (their implicit concatenation yields a bogus path and
# stats_tests.py never runs through the orchestrator). Fixed here.
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

MODULE_FLAGS = {
    "characterization": ("--characterization", "participant characterization"),
    "rq1": ("--rq1", "discrimination-definition coding (mislabeled upstream)"),
    "rq2": ("--rq2", "prejudice-definition coding"),
    "rq3": ("--rq3", "perceived discrimination by demographic profile"),
    "rq4": ("--rq4", "perceived discrimination by organizational setting"),
    "rq5": ("--rq5", "recognize / narrate / silence discourse strategies"),
    "rq6": ("--rq6", "representation in teams vs leadership roles"),
    "rq7": ("--rq7", "unconscious-bias coding"),
}


def build_arg_parser():
    parser = argparse.ArgumentParser(
        description="Run the Diversity4BRSE analysis scripts from their own directories."
    )
    parser.add_argument(
        "--all", action="store_true", help="run every module, in order"
    )
    for module, (flag, help_text) in MODULE_FLAGS.items():
        parser.add_argument(flag, action="store_true", help=help_text)
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="suppress script output"
    )
    return parser


def requested_modules(args):
    if args.all:
        return ORDER
    return [module for module in ORDER if getattr(args, module, False)]


def run_module(module, quiet):
    for rel_path in SCRIPTS[module]:
        full_path = os.path.join(SCRIPT_DIR, rel_path)
        if not os.path.exists(full_path):
            print(f"Error: script not found: {full_path}", file=sys.stderr)
            sys.exit(1)
        kwargs = {"cwd": os.path.dirname(full_path)}
        if quiet:
            result = subprocess.run(
                [sys.executable, os.path.basename(full_path)],
                capture_output=True,
                text=True,
                **kwargs,
            )
        else:
            result = subprocess.run(
                [sys.executable, os.path.basename(full_path)], **kwargs
            )
        if result.returncode != 0:
            print(f"Script failed: {rel_path}", file=sys.stderr)
            if quiet:
                if result.stdout:
                    print(result.stdout, file=sys.stderr)
                if result.stderr:
                    print(result.stderr, file=sys.stderr)
            sys.exit(result.returncode)


def main():
    args = build_arg_parser().parse_args()
    modules = requested_modules(args)
    if not modules:
        build_arg_parser().print_help()
        sys.exit(0)
    for module in modules:
        run_module(module, args.quiet)


if __name__ == "__main__":
    main()