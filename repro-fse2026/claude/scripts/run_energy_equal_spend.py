#!/usr/bin/env python3
"""Equal-measured-spend comparison on the ENERGY (Twins) family.

The main posterior protocol compares strategies at equal sample size and
handles cost through a prior-based handicap. This experiment instead fixes a
measured budget B per scope (B = n_ref x mean pool cost, i.e. what uniform
random spends on average at n_ref) and lets every strategy buy as many
configurations as B affords, so cheap strategies like pilotCost realize
their full volume advantage. The outcome is the realized max-bound
posterior risk at equal spend.

The affordable size per (strategy, seed, budget) is found by binary search
on the strategy's own sample size, capped at the generated-protocol grid
maximum (30% of the pool / 256); hitting the cap is recorded as censoring.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any, Callable

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
for path in (REPO_ROOT, SCRIPT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from cost_sampling.analysis import write_csv
from cost_sampling.generated_sampling import (
    _balanced_sample,
    _diversity_sample,
    _pair_sets,
    _pairwise_sample,
    _pilot_cost_sample,
    _value_codes,
    budget_grid,
    load_twins_table,
    oriented_cost,
)
from cost_sampling.srs import srs_indices

ALL_SYSTEMS = [
    "7z", "Apache", "HSQLDB", "LLVM", "MongoDB", "PostgreSQL", "VP8",
    "brotli", "exastencils", "jump3r", "kanzi", "lrzip", "nginx", "x264",
]
REVISION_FILTERS = {"brotli": {"revision": "1.0.7"}, "PostgreSQL": {"revision": "11.2"}}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", required=True)
    parser.add_argument("--systems", nargs="+", default=["ALL"])
    parser.add_argument("--properties", default="energy,performance",
                        help="Comma-separated properties used as cost AND target (diagonal scenarios).")
    parser.add_argument("--ref-levels", default="8,16,32,64",
                        help="Reference sizes defining budgets B = n_ref x mean pool cost.")
    parser.add_argument("--seeds", type=int, default=30)
    parser.add_argument("--srs-seeds", type=int, default=30)
    parser.add_argument("--output-dir", default="artifacts/fse_posterior_energy_equal_spend")
    parser.add_argument("--quick", action="store_true", help="Two systems, two budgets, 10 seeds.")
    return parser.parse_args()


def posterior_risk(y: np.ndarray, idx: np.ndarray) -> float:
    return float(np.mean(y > np.max(y[idx])))


def affordable_sample(
    build: Callable[[int], np.ndarray],
    cost_values: np.ndarray,
    budget: float,
    n_cap: int,
) -> tuple[np.ndarray, int, float, bool]:
    """Largest-n sample of `build` whose measured cost fits in `budget`.

    Returns (indices, n, spent, cap_hit). Binary search on n; the final
    candidate is walked downward if sampling noise leaves it over budget.
    """

    def spent(idx: np.ndarray) -> float:
        return float(np.sum(cost_values[idx]))

    lo, hi = 0, n_cap
    best: np.ndarray | None = None
    while lo < hi:
        mid = (lo + hi + 1) // 2
        idx = build(mid)
        if spent(idx) <= budget:
            best, lo = idx, mid
        else:
            hi = mid - 1
    n = lo
    while n > 0:
        idx = build(n) if best is None or len(best) != n else best
        if spent(idx) <= budget:
            return idx, n, spent(idx), n == n_cap
        best = None
        n -= 1
    idx = np.asarray([int(np.argmin(cost_values))], dtype=int)
    return idx, 1, spent(idx), False


def main() -> None:
    args = parse_args()
    systems = ALL_SYSTEMS if [s.upper() for s in args.systems] == ["ALL"] else args.systems
    properties = [p.strip() for p in args.properties.split(",") if p.strip()]
    ref_levels = [int(x) for x in args.ref_levels.split(",")]
    seeds, srs_seeds = args.seeds, args.srs_seeds
    if args.quick:
        systems = systems[:2]
        ref_levels = ref_levels[:2]
        seeds = min(seeds, 10)
        srs_seeds = min(srs_seeds, 10)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    parts_dir = output_dir / "parts"
    parts_dir.mkdir(exist_ok=True)

    records: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []

    for system in systems:
        try:
            table = load_twins_table(args.zip, system, where=REVISION_FILTERS.get(system, {}))
        except Exception as exc:  # noqa: BLE001
            skipped.append({"scope": system, "error": str(exc)})
            print(f"[eqspend] skipped {system}: {exc}", flush=True)
            continue
        available = set(table.rows[0].keys())
        value_codes = _value_codes(table.raw_feature_values)
        pair_sets = _pair_sets(value_codes)
        n_configs = len(table.rows)
        n_cap = max(budget_grid(n_configs), default=0)
        if n_cap == 0:
            skipped.append({"scope": system, "error": "no valid budget grid"})
            continue

        for prop in properties:
            if prop not in available:
                skipped.append({"scope": f"{system}/{prop}", "error": "missing column"})
                continue
            y = np.asarray([float(row[prop]) for row in table.rows])
            cost_values = oriented_cost(y.copy(), "lower")
            mean_cost = float(np.mean(cost_values))
            scenario = f"{system}__prop_{prop}"
            part_path = parts_dir / f"{scenario}.csv"
            if part_path.exists():
                print(f"[eqspend] {scenario} already done (checkpoint), skipping", flush=True)
                continue
            scenario_records: list[dict[str, Any]] = []
            print(f"[eqspend] {scenario} (pool {n_configs}, cap {n_cap})", flush=True)

            builders: dict[str, tuple[bool, Callable[[int, int], np.ndarray]]] = {
                # strategy -> (stochastic, build(n, seed))
                "random": (True, lambda n, s: np.sort(
                    np.random.default_rng(s).choice(n_configs, size=n, replace=False))),
                "balanced": (True, lambda n, s: np.asarray(
                    _balanced_sample(value_codes, n, np.random.default_rng(s)), dtype=int)),
                "pilotCost": (True, lambda n, s: np.asarray(
                    _pilot_cost_sample(table.X, cost_values, n, np.random.default_rng(s)), dtype=int)),
                "diversity": (False, lambda n, s: np.asarray(
                    _diversity_sample(table.X, n, np.random.default_rng(0)), dtype=int)),
                "pairwise": (False, lambda n, s: np.asarray(
                    _pairwise_sample(pair_sets, n, np.random.default_rng(0)), dtype=int)),
                "SRSSampling": (True, lambda n, s: srs_indices(
                    table.X, y, n, rng=s + 1, extreme="max")),
            }

            for n_ref in ref_levels:
                if n_ref > n_cap:
                    skipped.append({"scope": f"{scenario}:n{n_ref}", "error": "ref level above protocol cap"})
                    continue
                budget = n_ref * mean_cost
                for strategy, (stochastic, build) in builders.items():
                    strat_seeds = (srs_seeds if strategy == "SRSSampling" else seeds) if stochastic else 1
                    for seed in range(strat_seeds):
                        idx, n_aff, spent, cap_hit = affordable_sample(
                            lambda n, _s=seed, _b=build: _b(n, _s), cost_values, budget, n_cap
                        )
                        scenario_records.append(
                            {
                                "system": system,
                                "property": prop,
                                "scenario": scenario,
                                "ref_level": f"n{n_ref}",
                                "budget": budget,
                                "strategy": strategy,
                                "seed": seed,
                                "afforded_n": n_aff,
                                "spent": spent,
                                "budget_utilization": spent / budget if budget else float("nan"),
                                "cap_hit": int(cap_hit),
                                "posterior_risk": posterior_risk(y, idx),
                                "n_configurations": n_configs,
                            }
                        )
                print(f"[eqspend]   n{n_ref} done", flush=True)
            write_csv(part_path, scenario_records)
            records.extend(scenario_records)

    # Aggregate from checkpoints so resumed runs include earlier parts.
    import pandas as pd

    part_frames = [pd.read_csv(p) for p in sorted(parts_dir.glob("*.csv"))]
    df = pd.concat(part_frames, ignore_index=True) if part_frames else pd.DataFrame(records)
    df.to_csv(output_dir / "equal_spend_records.csv", index=False)
    if df.empty:
        raise SystemExit("No records produced.")
    grouped = (
        df.groupby(["scenario", "ref_level", "strategy"])
        .agg(
            median_risk=("posterior_risk", "median"),
            mean_risk=("posterior_risk", "mean"),
            median_afforded_n=("afforded_n", "median"),
            cap_hits=("cap_hit", "sum"),
            runs=("seed", "count"),
            median_utilization=("budget_utilization", "median"),
        )
        .reset_index()
    )
    grouped["integrated_confidence"] = 1.0 - grouped["mean_risk"]
    grouped.to_csv(output_dir / "equal_spend_strategy_summary.csv", index=False)

    scope_rows = []
    for (scenario, level), sub in grouped.groupby(["scenario", "ref_level"]):
        sub = sub.set_index("strategy")
        winner = sub["median_risk"].idxmin()
        rnd = sub.loc["random"] if "random" in sub.index else None
        pc = sub.loc["pilotCost"] if "pilotCost" in sub.index else None
        srs = sub.loc["SRSSampling"] if "SRSSampling" in sub.index else None
        scope_rows.append(
            {
                "scenario": scenario,
                "ref_level": level,
                "equal_spend_winner": winner,
                "winner_median_risk": float(sub.loc[winner, "median_risk"]),
                "random_risk": float(rnd["median_risk"]) if rnd is not None else float("nan"),
                "pilotCost_risk": float(pc["median_risk"]) if pc is not None else float("nan"),
                "srs_risk": float(srs["median_risk"]) if srs is not None else float("nan"),
                "pilotCost_beats_random": int(pc is not None and rnd is not None and pc["median_risk"] < rnd["median_risk"]),
                "srs_beats_random": int(srs is not None and rnd is not None and srs["median_risk"] < rnd["median_risk"]),
                "pilotCost_n_multiplier": float(pc["median_afforded_n"] / rnd["median_afforded_n"]) if pc is not None and rnd is not None and rnd["median_afforded_n"] else float("nan"),
                "pilotCost_cap_hits": int(pc["cap_hits"]) if pc is not None else 0,
            }
        )
    scope_df = pd.DataFrame(scope_rows).sort_values(["scenario", "ref_level"])
    scope_df.to_csv(output_dir / "equal_spend_scope_summary.csv", index=False)
    write_csv(output_dir / "skipped_scopes.csv", skipped)

    n_scopes = len(scope_df)
    win_counts = scope_df["equal_spend_winner"].value_counts()
    pc_beats = int(scope_df["pilotCost_beats_random"].sum())
    srs_beats = int(scope_df["srs_beats_random"].sum())
    pc_mult = scope_df["pilotCost_n_multiplier"].median()
    pc_censored = int((scope_df["pilotCost_cap_hits"] > 0).sum())
    lines = [
        "# Equal-measured-spend comparison (ENERGY family)",
        "",
        "Budget per scope: B = n_ref x mean pool cost (uniform random's expected",
        "spend at n_ref). Every strategy buys as many configurations as B affords",
        "(binary search on its own sample size, capped at the protocol grid",
        "maximum; cap hits are censoring, counted below). Outcome: realized",
        "max-bound posterior risk at equal spend.",
        "",
        f"Systems: {', '.join(systems)}. Properties (cost=target): {', '.join(properties)}.",
        f"Reference levels: {', '.join('n'+str(n) for n in ref_levels)}. Stochastic seeds: {seeds} (SRS {srs_seeds}).",
        "",
        "## Headline",
        "",
        f"Scopes (scenario x budget level): {n_scopes}.",
        f"pilotCost beats random at equal spend in {pc_beats}/{n_scopes} scopes "
        f"(median affordable-n multiplier {pc_mult:.2f}x; capped in {pc_censored} scopes).",
        f"SRS beats random at equal spend in {srs_beats}/{n_scopes} scopes.",
        "",
        "Equal-spend winners:",
        "",
    ]
    for strategy, count in win_counts.items():
        lines.append(f"- `{strategy}`: {int(count)}/{n_scopes}")
    (output_dir / "equal_spend_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote equal-spend outputs to {output_dir}")


if __name__ == "__main__":
    main()
