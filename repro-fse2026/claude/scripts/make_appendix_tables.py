#!/usr/bin/env python3
"""Generate the paper's appendix tables from committed result CSVs.

Emits LaTeX (booktabs) tables into paper-emse/tables/:
- appendix_linux.tex: per-release x per-level breakdown of the full
  Linux protocol (21 scopes).
- appendix_energy.tex: per-system rollup of the ENERGY family (14
  systems x up to 16 scopes each).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

OUT = Path("paper-emse/tables")
CHECK = r"\checkmark"


def esc(s: str) -> str:
    return s.replace("_", r"\_")


def strategy_of(pair: str) -> str:
    return pair.rsplit("_", 1)[0]


def linux_table() -> str:
    df = pd.read_csv("artifacts/fse_posterior_linux_all_full/posterior_linux_release_summary.csv")
    df = df.sort_values(["release", "n"])
    lines = [
        r"\begin{table}[t]",
        r"  \centering\small",
        r"  \caption{Per-release breakdown of the full Linux protocol (pool-relative;",
        r"  levels 1\%/2\%/5\% of each release's measured pool). $n$: sample size at",
        r"  the level; H1: posterior-risk distributions differ (Kruskal--Wallis,",
        r"  $\alpha{=}.05$); winner: best cost-normalized strategy",
        r"  ($\omega_{\mathrm{cost}}$); \srs{} front.: \srs{} on the empirical",
        r"  cost/confidence Pareto frontier; top chg.: top recommendation changes",
        r"  under the cost axis; $J$: Jaccard overlap of the two frontiers.}",
        r"  \label{tab:appendix-linux}",
        r"  \setlength{\tabcolsep}{4.5pt}",
        r"  \begin{tabular}{@{}llrlcccr@{}}",
        r"    \toprule",
        r"    Release & Level & $n$ & Winner & H1 & \srs{} front. & Top chg. & $J$ \\",
        r"    \midrule",
    ]
    for _, r in df.iterrows():
        lines.append(
            f"    {r.release} & {int(round(r.n / r.n_configurations * 100))}\\% & {int(r.n):,} & "
            f"\\textsf{{{esc(strategy_of(r.best_cost_pair))}}} & "
            f"{CHECK if r.fse1_verdict == 'supports' else '--'} & "
            f"{CHECK if r.srs_on_empirical_confidence_front == 1 else '--'} & "
            f"{CHECK if r.top_changed_by_cost == 1 else '--'} & "
            f"{r.pareto_jaccard:.2f} \\\\"
        )
    lines += [r"    \bottomrule", r"  \end{tabular}", r"\end{table}"]
    return "\n".join(lines) + "\n"


def energy_table() -> str:
    df = pd.read_csv("artifacts/fse_posterior_energy_final/posterior_energy_scenario_summary.csv")
    df["system"] = df.scenario.str.split("__").str[0]
    df["winner"] = df.best_cost_pair.map(strategy_of)
    rows = []
    for system, g in df.groupby("system"):
        winner_counts = g.winner.value_counts()
        top = f"\\textsf{{{esc(winner_counts.index[0])}}} ({winner_counts.iloc[0]})"
        rows.append(
            {
                "system": esc(system),
                "nconf": f"{int(g.n_configurations.iloc[0]):,}",
                "scopes": len(g),
                "h1": int((g.fse1_verdict == "supports").sum()),
                "srs_best": int(g.srs_best_cost.sum()),
                "srs_front": int(g.srs_on_empirical_confidence_front.sum()),
                "topchg": int(g.top_changed_by_cost.sum()),
                "frontchg": int((g.pareto_jaccard < 1.0).sum()),
                "winner": top,
            }
        )
    rows.sort(key=lambda r: r["system"].lower())
    lines = [
        r"\begin{table}[t]",
        r"  \centering\small",
        r"  \caption{Per-system rollup of the ENERGY family (each system contributes",
        r"  up to 16 scopes: \{energy, runtime\} cost $\times$ \{energy, runtime\}",
        r"  target $\times$ budgets $n8$--$n64$, protocol-capped). H1 / \srs{} best /",
        r"  \srs{} front.\ / top chg.\ / frontier chg.: scopes where the outcome",
        r"  holds; winner: most frequent best cost-normalized strategy (scopes won).}",
        r"  \label{tab:appendix-energy}",
        r"  \setlength{\tabcolsep}{4pt}",
        r"  \begin{tabular}{@{}lrrrrrrrl@{}}",
        r"    \toprule",
        r"    System & $|\mathcal{V}|$ & Scopes & H1 & \srs{} best & \srs{} front. & Top chg. & Front.\ chg. & Winner \\",
        r"    \midrule",
    ]
    for r in rows:
        lines.append(
            f"    {r['system']} & {r['nconf']} & {r['scopes']} & {r['h1']} & "
            f"{r['srs_best']} & {r['srs_front']} & {r['topchg']} & {r['frontchg']} & {r['winner']} \\\\"
        )
    lines += [r"    \bottomrule", r"  \end{tabular}", r"\end{table}"]
    return "\n".join(lines) + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "appendix_linux.tex").write_text(linux_table(), encoding="utf-8")
    (OUT / "appendix_energy.tex").write_text(energy_table(), encoding="utf-8")
    print("Wrote", OUT / "appendix_linux.tex", "and", OUT / "appendix_energy.tex")


if __name__ == "__main__":
    main()
