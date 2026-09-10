#!/usr/bin/env python3
"""Multiple-comparison sensitivity for the FSE-posterior hypothesis tests.

Applies Benjamini-Hochberg FDR control (alpha = 0.05) within each
(corpus, hypothesis) family over all conducted tests, for the three
p-value-based hypotheses (FSE1 Kruskal-Wallis; FSE5/FSE6 Mann-Whitney).
FSE2/3/4 are decision rules without significance tests and are unaffected.
A scope counts as corrected-supported when its uncorrected verdict is
`supports` and its BH-adjusted q-value is <= alpha (BH is never more
liberal than the per-test threshold, so corrected counts can only shrink).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ALPHA = 0.05
CORPORA = {
    "fse_artifact": "artifacts/fse_posterior_fse_artifact_final_t2",
    "x264": "artifacts/fse_posterior_x264_icpe_final",
    "energy": "artifacts/fse_posterior_energy_final",
    "workload": "artifacts/fse_posterior_workload_final",
    "linux_full": "artifacts/fse_posterior_linux_all_full",
    "lcbench": "artifacts/fse_posterior_lcbench_no_oracles_final",
}
P_HYPOTHESES = ["FSE1", "FSE5", "FSE6"]
OUT_DIR = Path("artifacts/fse_posterior_synthesis")


def bh_qvalues(p: np.ndarray) -> np.ndarray:
    m = len(p)
    order = np.argsort(p)
    ranked = p[order] * m / (np.arange(m) + 1)
    q = np.minimum.accumulate(ranked[::-1])[::-1]
    out = np.empty(m)
    out[order] = np.minimum(q, 1.0)
    return out


def main() -> None:
    rows = []
    for corpus, directory in CORPORA.items():
        path = Path(directory) / "posterior_hypothesis_tests.csv"
        tests = pd.read_csv(path)
        for hyp in P_HYPOTHESES:
            fam = tests[(tests.hypothesis == hyp) & tests.p_value.notna()].copy()
            if fam.empty:
                continue
            fam["q_value"] = bh_qvalues(fam.p_value.to_numpy())
            raw = int((fam.verdict == "supports").sum())
            corrected = int(((fam.verdict == "supports") & (fam.q_value <= ALPHA)).sum())
            rows.append(
                {
                    "corpus": corpus,
                    "hypothesis": hyp,
                    "tests": len(fam),
                    "supports_raw": raw,
                    "supports_bh": corrected,
                    "lost_to_correction": raw - corrected,
                    "max_q_of_raw_supports": float(fam.loc[fam.verdict == "supports", "q_value"].max())
                    if raw
                    else float("nan"),
                }
            )
    df = pd.DataFrame(rows)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_DIR / "multiple_comparison_sensitivity.csv", index=False)

    lines = [
        "# Multiple-comparison sensitivity (Benjamini-Hochberg, FDR 0.05)",
        "",
        "BH applied within each (corpus, hypothesis) family over all conducted",
        "tests; a scope stays supported only if its uncorrected verdict was",
        "`supports` and its BH q-value is <= 0.05. FSE2/3/4 are decision rules",
        "without p-values and are unaffected by correction.",
        "",
        "| Corpus | Hypothesis | Tests | Supports (raw) | Supports (BH) | Lost |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for _, r in df.iterrows():
        lines.append(
            f"| {r.corpus} | {r.hypothesis} | {r.tests} | {r.supports_raw} | "
            f"{r.supports_bh} | {r.lost_to_correction} |"
        )
    total_raw = int(df.supports_raw.sum())
    total_bh = int(df.supports_bh.sum())
    lines += [
        "",
        f"Across all families: {total_raw} raw supports, {total_bh} after BH "
        f"({total_raw - total_bh} lost, {(total_raw - total_bh) / max(total_raw, 1):.1%}).",
    ]
    (OUT_DIR / "multiple_comparison_sensitivity.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(df.to_string(index=False))
    print(f"\nWrote {OUT_DIR}/multiple_comparison_sensitivity.{{csv,md}}")


if __name__ == "__main__":
    main()
