#!/usr/bin/env python3
"""Build `results/hypotheses_table.tex` from the per-batch hypothesis summaries."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]


HYPOTHESIS_META = [
    ("H1a", "RQ1", "Per-config.\\ cost CV is non-negligible.",
     "$\\mathrm{CV}\\geq 0.20$ or $p_{90}/p_{10}\\geq 1.5$"),
    ("H1b", "RQ1", "Strategies differ in $\\TrainCost$ at fixed $n$.",
     "Kruskal--Wallis $p<0.05$ and $\\eta^2\\geq 0.01$"),
    ("H2a", "RQ2", "$n$ is positively rank-correlated with $\\TrainCost$.",
     "Spearman $\\rho>0$, $p<0.05$"),
    ("H2b", "RQ2", "Calibration ratio $\\Ratio$ is not centered at $1$.",
     "$95\\%$ bootstrap CI of median excludes $1$, $|\\widetilde{\\Ratio}-1|\\geq 0.05$"),
    ("H2c", "RQ2", "Calibration depends on sampling strategy.",
     "Kruskal--Wallis of $\\Ratio$ across strategies, $p<0.05$"),
    ("H3a", "RQ3", "Rankings under count vs.\\ measured cost diverge.",
     "$\\geq 1$ top-$1$ flip across $\\lambda$"),
    ("H3b", "RQ3", "Divergence is stronger when cost CV is high.",
     "Spearman(CV, flips/$7$) across systems"),
    ("H4a", "RQ4", "Some $(s,n)$ pairs are Pareto-efficient under one cost only.",
     "$\\geq 1$ pair only on count or only on measured-cost front"),
    ("H4b", "RQ4", "Measured-cost frontier differs from count frontier.",
     "Jaccard$<1$"),
    ("H5a", "RQ5", "Validity depends on input/workload within a fixed system.",
     "Kruskal--Wallis of $\\Ratio$ across inputs/workloads within a system"),
    ("H5b", "RQ5", "Size-as-cost gap differs by predicted property on x264.",
     "$|\\Delta\\text{flip-rate}|\\geq 0.05$"),
    ("H5c", "RQ5", "Measured-cost rankings less stable than count under context changes.",
     "mean Kendall $\\tau<0.95$ or median Jaccard$<0.9$"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--newruns", default="artifacts/newruns_systems")
    parser.add_argument("--matrix", default="artifacts/x264_matrix")
    parser.add_argument("--workload", default="artifacts/workload_batch_overnight")
    parser.add_argument("--lcbench", default="artifacts/lcbench_data_2k_lw")
    parser.add_argument(
        "--linux",
        default="artifacts/linux413_vmlinux,artifacts/linux415_vmlinux,artifacts/linux420_vmlinux,artifacts/linux500_vmlinux,artifacts/linux504_vmlinux,artifacts/linux507_vmlinux,artifacts/linux508_vmlinux",
        help="Comma-separated per-release hypothesis_tests.csv folders for Linux.",
    )
    parser.add_argument(
        "--output",
        default="607058f5f5131dcd1dbd783d/results/hypotheses_table.tex",
    )
    return parser.parse_args()


def load_summary(folder: Path) -> dict[str, dict[str, Any]]:
    path = folder / "hypothesis_summary.csv"
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as handle:
        return {row["hypothesis"]: row for row in csv.DictReader(handle)}


def load_linux_summary(folders: list[Path]) -> dict[str, dict[str, Any]]:
    """Aggregate per-release `hypothesis_tests.csv` files into a summary."""
    counts: dict[str, dict[str, int]] = {}
    for folder in folders:
        path = folder / "hypothesis_tests.csv"
        if not path.exists():
            continue
        with path.open(encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                h = row["hypothesis"]
                bucket = counts.setdefault(h, {"supports": 0, "refutes": 0, "inconclusive": 0, "scopes": 0})
                bucket["scopes"] += 1
                bucket[row["verdict"]] += 1
    out: dict[str, dict[str, Any]] = {}
    for h, c in counts.items():
        out[h] = {
            "hypothesis": h,
            "scopes": str(c["scopes"]),
            "supports": str(c["supports"]),
            "refutes": str(c["refutes"]),
            "inconclusive": str(c["inconclusive"]),
            "global_verdict": (
                f"supported ({c['supports']}/{c['scopes']})" if c["supports"] >= max(c["refutes"], c["inconclusive"])
                else f"refuted ({c['refutes']}/{c['scopes']})" if c["refutes"] >= max(c["supports"], c["inconclusive"])
                else f"mixed ({c['supports']}/{c['scopes']})"
            ),
        }
    return out


EXISTENTIAL = {"H3a", "H4a", "H4b"}  # "sometimes diverge" / "$\geq 1$" claims


def cell(summary: dict[str, dict[str, Any]], h: str) -> str:
    row = summary.get(h)
    if row is None:
        return "--"
    sup = int(row["supports"])
    n = int(row["scopes"])
    if h in EXISTENTIAL:
        marker = "$\\checkmark$" if sup >= 1 else "$\\times$"
    else:
        verdict = row["global_verdict"]
        if verdict.startswith("supported"):
            marker = "$\\checkmark$"
        elif verdict.startswith("refuted"):
            marker = "$\\times$"
        else:
            marker = "$\\circ$"
    return f"{marker}\\,{sup}/{n}"


def main() -> None:
    args = parse_args()
    nr_summary = load_summary(REPO_ROOT / args.newruns)
    mx_summary = load_summary(REPO_ROOT / args.matrix)
    wl_summary = load_summary(REPO_ROOT / args.workload)
    lc_summary = load_summary(REPO_ROOT / args.lcbench)
    linux_folders = [REPO_ROOT / part for part in args.linux.split(",") if part]
    lx_summary = load_linux_summary(linux_folders)

    lines = [
        "% Auto-generated by scripts/generate_hypotheses_table.py.",
        "% Do not edit by hand; rerun the generator after updating the artifacts.",
        "\\begin{table*}[t]",
        "\\centering",
        "\\caption{Hypothesis verdicts. Each verdict is `$\\checkmark$ supported',",
        "`$\\times$ refuted', or `$\\circ$ inconclusive', followed by the count of",
        "scopes (NewRuns systems for H1--H4, x264 inputs $\\times$ scenarios for the matrix",
        "column, workload-impact systems for the workload column, LCBench datasets",
        "for the LCBench column, and seven Linux releases for the Linux column)",
        "where the per-scope test agreed with the global label.",
        "Statistical tests and thresholds are in the third column. H3b and H5b are",
        "global tests (one scope each). The workload-impact column only contributes",
        "RQ5 evidence, since it was added specifically to test workload sensitivity",
        "across nine systems and $93$ workloads. The LCBench column contributes",
        "H1--H4 workload-level verdicts on $35$ dataset contexts and study-level",
        "RQ5 verdicts for the non-pure-software external-validation family. For the RQ5 rows specifically,",
        "the x264 column reports \\emph{scenario-level} verdicts on one system",
        "(four cost$\\times$target scenarios, each aggregating over $17$ input videos),",
        "whereas the workload-impact column reports \\emph{system-level} verdicts",
        "(nine systems, each aggregating over $6$--$13$ workloads), and the",
        "LCBench column reports a \\emph{study-level} verdict aggregating over",
        "$35$ dataset contexts.",
        "Linux is reported separately rather than aggregated because of its different",
        "protocol and strategy panel (\\Cref{sec:results}); H2b refutes on",
        "Linux at the aggregate median because the per-strategy ratios average to",
        "$\\sim\\!\\!1.00$, but the per-strategy decomposition shows two strategies",
        "(\\texttt{diversity}, \\texttt{uncertainty}) clearly miscalibrated. The",
        "size-as-cost effect (H5b) is borderline at the by-target average",
        "($\\Delta$ flip-rate $= 0.042$) but the asymmetric scenario alone",
        "(cost$=$time, target$=$size) shows a $13$-pp jump",
        "(\\Cref{tab:x264-matrix-summary}).}",
        "\\label{tab:hypothesis-verdicts}",
        "\\scriptsize",
        "\\setlength{\\tabcolsep}{3pt}",
        "\\begin{tabular}{l l p{4.2cm} p{3.2cm} c c c c c}",
        "\\toprule",
        "ID & RQ & Claim & Test / threshold & NewRuns & \\shortstack{x264 matrix \\\\ inputs} & \\shortstack{Workload-impact \\\\ workloads} & \\shortstack{LCBench \\\\ datasets} & Linux \\\\",
        "\\midrule",
    ]
    for hid, rq, claim, test in HYPOTHESIS_META:
        nr = cell(nr_summary, hid)
        mx = cell(mx_summary, hid)
        wl = cell(wl_summary, hid) if hid in {"H5a", "H5c"} else "--"
        lc = cell(lc_summary, hid)
        lx = cell(lx_summary, hid)
        lines.append(
            f"\\textbf{{{hid}}} & {rq} & {claim} & {test} & {nr} & {mx} & {wl} & {lc} & {lx} \\\\"
        )
    lines.extend(
        [
            "\\bottomrule",
            "\\end{tabular}",
            "\\end{table*}",
            "",
        ]
    )

    output = REPO_ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
