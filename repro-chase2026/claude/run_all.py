#!/usr/bin/env python3
"""Run the reproducible core (modules 03 -> 04 -> 05) and write a run manifest.

Modules 01-02 (Ollama inference) are deliberately **not** run: Spec 00 §1.1 /
§3 state that modules 03-04 consume the *delivered* prediction bundles and that
a re-run of inference will not bit-match them.  Run them explicitly if you have
a populated Ollama server:

    python claude/01_inference_nocontext.py
    python claude/02_inference_context.py

Spec 00 §3 — the run manifest records the resolved dependency versions.

Run from the repository root:  python claude/run_all.py
"""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from repro_common import ensure_dir, resolve_output_root  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

MODULES = [
    ("03", "03_evaluation_metrics.py"),
    ("04", "04_per_emotion_analysis.py"),
    ("05", "05_latex_tables.py"),
]


def resolved_versions() -> dict:
    versions = {"python": sys.version.split()[0], "platform": platform.platform()}
    dist_names = {"sklearn": "scikit-learn"}
    for name in ("pandas", "numpy", "sklearn", "ollama", "tqdm"):
        try:
            module = __import__(name)
        except ImportError:
            versions[name] = "not installed"
            continue
        version = getattr(module, "__version__", None)
        if not version:
            # Packages without a __version__ attribute (e.g. ollama).
            try:
                version = importlib.metadata.version(dist_names.get(name, name))
            except importlib.metadata.PackageNotFoundError:
                version = "unknown"
        versions[name] = version
    return versions


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", default=None)
    args = parser.parse_args()

    out_root = ensure_dir(resolve_output_root(args.output_root))
    passthrough = ["--output-root", out_root]

    statuses = {}
    failures = 0
    for label, script in MODULES:
        print(f"\n########## module {label}: {script} ##########")
        proc = subprocess.run(
            [sys.executable, os.path.join(HERE, script), *passthrough],
            check=False,
        )
        statuses[label] = proc.returncode
        if proc.returncode != 0:
            failures += 1

    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "study": "Emotion Recognition in Agile Software Meetings (CHASE 2026) — "
                 "text-based LLM track",
        "modules_run": [label for label, _ in MODULES],
        "modules_skipped": {
            "01": "Ollama inference (no-context) — delivered bundles are used instead",
            "02": "Ollama inference (with context) — delivered bundles are used instead",
        },
        "module_exit_codes": statuses,
        "randomness": "none — the evaluation path is deterministic pandas/sklearn "
                      "scoring; no seed is set because no stochastic operation exists "
                      "(Spec 00 §3)",
        "output_root": out_root,
        "resolved_versions": resolved_versions(),
    }
    manifest_path = os.path.join(out_root, "run_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"\nSaved: {manifest_path}")

    if failures:
        print(f"\n{failures} module(s) reported a validation failure.")
        return 1
    print("\nAll modules validated against the committed reference artefacts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
