#!/usr/bin/env python3
"""Run the LinuxData (TuxKConfig) empirical sampling-cost experiment.

This mirrors `scripts/run_poc.py` but operates on a pool-based subsampling
view of the OpenML 46759 parquet (Linux 4.13).  The five strategies
implemented in `cost_sampling.pool_samplers` are evaluated at five sample
sizes, with the existing analysis pipeline reused for RQ1-RQ4.

The runner is memory-conscious: the option matrix is kept as int8 in the
LinuxDataset, training rows are upcast to float64 only during the ridge fit,
and test-set predictions are chunked.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import sys
import time

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from cost_sampling.analysis import (
    cost_heterogeneity_summary,
    pareto_summary,
    proxy_summary,
    rank_stability,
    strategy_summary,
    write_csv,
    strategy_sort_key,
    level_sort_key,
)
from cost_sampling.linux_data import load_linux_dataset
from cost_sampling.metrics import LEARNER_CHOICES, fit_learner, fit_ridge, mean_relative_error, predict
from cost_sampling.plots import (
    plot_accuracy_cost,
    plot_calibration,
    plot_cost_distribution,
    plot_rank_stability,
    plot_strategy_cost_bias,
)
from cost_sampling.pool_samplers import (
    STRATEGY_BALANCED,
    STRATEGY_CHEAP,
    STRATEGY_COVERAGE,
    STRATEGY_DIVERSITY,
    STRATEGY_EXPENSIVE,
    STRATEGY_RANDOM,
    STRATEGY_UNCERTAINTY,
    balanced_sample,
    cheap_oracle_sample,
    coverage_sample,
    diversity_sample,
    expensive_oracle_sample,
    random_sample,
    uncertainty_sample,
)


DEFAULT_LAMBDAS = [0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 10.0]


@dataclass(frozen=True)
class SampleRef:
    context: str
    run_id: int
    strategy: str
    level: str
    zip_member: str = ""


@dataclass(frozen=True)
class Sample:
    ref: SampleRef
    indices: np.ndarray


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--parquet",
        default="ICPE-rawdata/linux/tuxkconfig_413.parquet",
        help="Path to the TuxKConfig parquet file.",
    )
    parser.add_argument("--release", default="413", help="Kernel release label, e.g. 413.")
    parser.add_argument("--target-column", default="vmlinux")
    parser.add_argument(
        "--cost-column",
        default=None,
        help="Cost column; defaults to target column.",
    )
    parser.add_argument("--output-dir", default=None)
    parser.add_argument(
        "--levels",
        default="0.01,0.02,0.05,0.10,0.20",
        help="Comma-separated training fractions.",
    )
    parser.add_argument("--stochastic-runs", type=int, default=100,
                        help="Runs per level for `random` and `balanced`.")
    parser.add_argument("--diversity-runs", type=int, default=20,
                        help="Diversity (farthest-first) runs per level. 0 disables. "
                        "The sampler is O(n × candidates × features) and gets expensive fast.")
    parser.add_argument("--diversity-max-n", type=int, default=1851,
                        help="Skip diversity sampling at levels where n exceeds this cap.")
    parser.add_argument("--diversity-candidate-size", type=int, default=512)
    parser.add_argument("--uncertainty-runs", type=int, default=20,
                        help="Active-learning runs per level. 0 disables.")
    parser.add_argument("--uncertainty-seed-fraction", type=float, default=0.25)
    parser.add_argument("--coverage-runs", type=int, default=20,
                        help="Coverage / option-frequency-matching runs per level. 0 disables.")
    parser.add_argument("--coverage-candidate-size", type=int, default=512)
    parser.add_argument("--top-k-features", type=int, default=512,
                        help="Keep only the top-K kernel-option columns by marginal "
                        "effect on the target. Set to 0 to keep all features.")
    parser.add_argument("--alpha", type=float, default=1.0)
    parser.add_argument("--learner", default="ridge-log", choices=LEARNER_CHOICES)
    parser.add_argument("--no-log-target", action="store_true")
    parser.add_argument("--predict-chunk", type=int, default=4096)
    parser.add_argument("--seed", type=int, default=20260506)
    parser.add_argument("--quick", action="store_true",
                        help="Smoke-test mode: 5 stochastic runs, 2 diversity runs, smaller candidate set.")
    return parser.parse_args()


def fmt_secs(t: float) -> str:
    return f"{t:6.1f}s" if t < 60 else f"{t / 60:5.1f}m"


def evaluate_sample_chunked(
    *,
    dataset_X: np.ndarray,
    y: np.ndarray,
    cost_values: np.ndarray,
    full_cost: float,
    n_configs: int,
    train_indices: np.ndarray,
    alpha: float,
    learner: str,
    log_target: bool,
    predict_chunk: int,
) -> tuple[float, float, int]:
    indices = np.array(sorted(set(int(idx) for idx in train_indices)), dtype=int)
    n = len(indices)
    test_mask = np.ones(n_configs, dtype=bool)
    test_mask[indices] = False

    X_train = dataset_X[indices].astype(np.float64, copy=False)
    effective_learner = learner
    if not log_target and learner == "ridge-log":
        effective_learner = "ridge-raw"
    elif not log_target and learner == "cart-log":
        effective_learner = "cart-raw"
    elif not log_target and learner == "rf-log":
        effective_learner = "rf-raw"
    elif not log_target and learner == "gbt-log":
        effective_learner = "gbt-raw"
    model = fit_learner(X_train, y[indices], alpha=alpha, learner=effective_learner)
    del X_train

    test_idx = np.flatnonzero(test_mask)
    abs_err_sum = 0.0
    count = 0
    for start in range(0, len(test_idx), predict_chunk):
        chunk = test_idx[start : start + predict_chunk]
        X_chunk = dataset_X[chunk].astype(np.float64, copy=False)
        y_pred = predict(model, X_chunk)
        y_true = y[chunk]
        denom = np.maximum(np.abs(y_true), 1e-12)
        abs_err_sum += float(np.sum(np.abs(y_true - y_pred) / denom))
        count += len(chunk)
    mre = abs_err_sum / max(count, 1)

    train_cost = float(np.sum(cost_values[indices]))
    return mre, train_cost, n


def build_samples(
    *,
    dataset,
    levels: list[float],
    stochastic_runs: int,
    diversity_runs: int,
    diversity_candidate_size: int,
    diversity_max_n: int,
    uncertainty_runs: int,
    uncertainty_seed_fraction: float,
    coverage_runs: int,
    coverage_candidate_size: int,
    alpha: float,
    log_target: bool,
    seed: int,
) -> list[Sample]:
    pool_size = dataset.X.shape[0]
    rng_master = np.random.default_rng(seed)

    def level_label(fraction: float, n: int) -> str:
        return f"n{n:05d}"

    samples: list[Sample] = []
    for fraction in levels:
        n = int(round(fraction * pool_size))
        level = level_label(fraction, n)

        # random
        for run_id in range(1, stochastic_runs + 1):
            rng = np.random.default_rng(rng_master.integers(0, 2**63 - 1))
            indices = random_sample(n, pool_size=pool_size, rng=rng)
            samples.append(Sample(SampleRef(dataset.context, run_id, STRATEGY_RANDOM, level), indices))

        # balanced (stratified by active_options decile)
        for run_id in range(1, stochastic_runs + 1):
            rng = np.random.default_rng(rng_master.integers(0, 2**63 - 1))
            indices = balanced_sample(n, active_options=dataset.active_options, rng=rng)
            samples.append(Sample(SampleRef(dataset.context, run_id, STRATEGY_BALANCED, level), indices))

        # diversity (farthest-first with candidate batches) — capped to small n
        if diversity_runs > 0 and n <= diversity_max_n:
            for run_id in range(1, diversity_runs + 1):
                rng = np.random.default_rng(rng_master.integers(0, 2**63 - 1))
                indices = diversity_sample(
                    n,
                    X=dataset.X,
                    rng=rng,
                    candidate_size=diversity_candidate_size,
                )
                samples.append(Sample(SampleRef(dataset.context, run_id, STRATEGY_DIVERSITY, level), indices))

        # uncertainty (residual-driven active learning)
        if uncertainty_runs > 0:
            for run_id in range(1, uncertainty_runs + 1):
                rng = np.random.default_rng(rng_master.integers(0, 2**63 - 1))
                indices = uncertainty_sample(
                    n,
                    X=dataset.X,
                    y=dataset.y,
                    rng=rng,
                    seed_fraction=uncertainty_seed_fraction,
                    alpha=alpha,
                    log_target=log_target,
                )
                samples.append(Sample(SampleRef(dataset.context, run_id, STRATEGY_UNCERTAINTY, level), indices))

        # coverage (greedy option-frequency matching)
        if coverage_runs > 0:
            for run_id in range(1, coverage_runs + 1):
                rng = np.random.default_rng(rng_master.integers(0, 2**63 - 1))
                indices = coverage_sample(
                    n,
                    X=dataset.X,
                    rng=rng,
                    candidate_size=coverage_candidate_size,
                )
                samples.append(Sample(SampleRef(dataset.context, run_id, STRATEGY_COVERAGE, level), indices))

        # cheap oracle (deterministic, single run)
        indices = cheap_oracle_sample(n, cost_values=dataset.cost_values)
        samples.append(Sample(SampleRef(dataset.context, 1, STRATEGY_CHEAP, level), indices))

        # expensive oracle (deterministic, single run)
        indices = expensive_oracle_sample(n, cost_values=dataset.cost_values)
        samples.append(Sample(SampleRef(dataset.context, 1, STRATEGY_EXPENSIVE, level), indices))

    return samples


def evaluate_all(
    *,
    dataset,
    samples: list[Sample],
    alpha: float,
    learner: str,
    log_target: bool,
    predict_chunk: int,
) -> list[dict]:
    records: list[dict] = []
    cost_values = dataset.cost_values
    full_cost = dataset.full_cost
    n_configs = dataset.X.shape[0]

    # Cache MRE keyed by sorted indices so deterministic strategies and
    # repeated random draws are not recomputed.
    mre_cache: dict[bytes, tuple[float, float, int]] = {}

    t0 = time.time()
    for k, sample in enumerate(samples, 1):
        sorted_idx = np.array(sorted(set(int(i) for i in sample.indices)), dtype=int)
        key = sorted_idx.tobytes()
        if key in mre_cache:
            mre, train_cost, n = mre_cache[key]
        else:
            mre, train_cost, n = evaluate_sample_chunked(
                dataset_X=dataset.X,
                y=dataset.y,
                cost_values=cost_values,
                full_cost=full_cost,
                n_configs=n_configs,
                train_indices=sorted_idx,
                alpha=alpha,
                learner=learner,
                log_target=log_target,
                predict_chunk=predict_chunk,
            )
            mre_cache[key] = (mre, train_cost, n)

        pct_n = n / n_configs
        pct_cost = train_cost / full_cost
        records.append(
            {
                "context": sample.ref.context,
                "target_context": dataset.context,
                "cost_context": dataset.effective_cost_context,
                "run": sample.ref.run_id,
                "strategy": sample.ref.strategy,
                "level": sample.ref.level,
                "n": n,
                "pct_n": pct_n,
                "train_cost": train_cost,
                "pct_cost": pct_cost,
                "calibration_ratio": pct_cost / pct_n if pct_n else float("nan"),
                "mre": mre,
                "learner": learner,
                "zip_member": "",
            }
        )

        if k % 25 == 0 or k == len(samples):
            elapsed = time.time() - t0
            rate = k / max(elapsed, 1e-9)
            eta = (len(samples) - k) / max(rate, 1e-9)
            print(f"  evaluated {k:5d}/{len(samples)} "
                  f"({elapsed:6.1f}s elapsed, ETA {fmt_secs(eta)})")

    records.sort(key=lambda row: (
        strategy_sort_key(row["strategy"]),
        level_sort_key(row["level"]),
        row["run"],
    ))
    return records


def write_markdown_summary(
    output: Path,
    *,
    context: str,
    cost_context: str,
    feature_count: int,
    pool_size: int,
    heterogeneity: list[dict],
    proxy: list[dict],
    summary: list[dict],
    ranks: list[dict],
    pareto: list[dict],
    levels: list[float],
    learner: str,
) -> None:
    h = heterogeneity[0]
    overall = next(row for row in proxy if row["strategy"] == "ALL")
    empirical_frontier = [f"{row['strategy']}_{row['level']}" for row in pareto if row["pareto_empirical"]]
    count_frontier = [f"{row['strategy']}_{row['level']}" for row in pareto if row["pareto_count"]]
    rank_flips = [row for row in ranks if row["top1_agreement"] == 0]

    def fmt(v):
        return f"{v:.4g}"

    lines = [
        f"# LinuxData report: {context}",
        "",
        "## Pool",
        "",
        f"- Configurations: {pool_size}",
        f"- Active option columns after pruning: {feature_count}",
        f"- Cost signal: `{cost_context}`",
        f"- Learner: `{learner}`",
        f"- Cost p90/p10 ratio: {fmt(h['p90_over_p10'])}",
        f"- Cost CV: {fmt(h['cv_cost'])}",
        f"- Min / median / max cost: {fmt(h['min_cost'])} / {fmt(h['median_cost'])} / {fmt(h['max_cost'])}",
        "",
        "## RQ snapshots",
        "",
        f"- RQ1 — fixed-n strategy cost overhead vs random ranges from "
        f"{fmt(min(row['cost_over_random'] for row in summary))} to "
        f"{fmt(max(row['cost_over_random'] for row in summary))}.",
        f"- RQ2 — Spearman ρ(n, train_cost) = {fmt(overall['spearman_n_train_cost'])}; "
        f"median calibration ratio = {fmt(overall['median_calibration_ratio'])}.",
        f"- RQ3 — top-1 strategy/size pair changes for {len(rank_flips)} / {len(ranks)} λ values.",
        f"- RQ4 — empirical-Pareto pairs: {', '.join(empirical_frontier)}.",
        f"  count-Pareto pairs: {', '.join(count_frontier)}.",
        "",
        "## Calibration by strategy",
        "",
        "| strategy | median ratio | bias |",
        "|---|---|---|",
    ]
    for row in proxy:
        if row["strategy"] == "ALL":
            continue
        lines.append(
            f"| {row['strategy']} | {fmt(row['median_calibration_ratio'])} | {fmt(row['median_bias'])} |"
        )

    lines += [
        "",
        "## Notes",
        "",
        "- Pool-based subsampling only.  Synthesis strategies (true uniform-",
        "  over-feasible, t-wise) are not evaluable on the published TuxKConfig",
        "  artifact and are flagged in `LINUX_KERNEL_PLAN.md` as out of scope.",
        "- `cheapOracle` and `expensiveOracle` are diagnostic references, not",
        "  deployable strategies — they assume access to the cost they help",
        "  bound.",
        "- All MRE values are computed against the complement of the training",
        "  sample within the same 92,562-row pool; cost = sum of `vmlinux`",
        "  binary size over selected configurations.",
        "",
    ]
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    levels = [float(x) for x in args.levels.split(",")]

    stochastic_runs = args.stochastic_runs
    diversity_runs = args.diversity_runs
    candidate_size = args.diversity_candidate_size
    uncertainty_runs = args.uncertainty_runs
    coverage_runs = args.coverage_runs
    if args.quick:
        stochastic_runs = 5
        diversity_runs = min(diversity_runs, 1)
        candidate_size = 128
        uncertainty_runs = min(uncertainty_runs, 2)
        coverage_runs = min(coverage_runs, 2)

    cost_column = args.cost_column or args.target_column
    context = f"linux{args.release}_{args.target_column.replace('-', '_')}"
    output_dir = Path(args.output_dir or f"artifacts/{context}")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading {args.parquet}")
    t0 = time.time()
    top_k = args.top_k_features if args.top_k_features and args.top_k_features > 0 else None
    dataset = load_linux_dataset(
        args.parquet,
        context=context,
        target_column=args.target_column,
        cost_column=cost_column,
        top_k_features=top_k,
    )
    from cost_sampling.linux_data import NON_OPTION_COLUMNS
    feature_set = set(dataset.feature_names)
    leaked = feature_set & set(NON_OPTION_COLUMNS)
    assert not leaked, f"Forbidden columns leaked into features: {leaked}"
    print(
        f"  pool={dataset.X.shape[0]} configs, "
        f"features={dataset.X.shape[1]} (after pruning), "
        f"loaded in {fmt_secs(time.time() - t0)}"
    )
    print(
        f"  forbidden columns excluded from features: {len(NON_OPTION_COLUMNS)} "
        f"(target {args.target_column!r}, all {len(NON_OPTION_COLUMNS) - 2} size variants, "
        f"active_options, cid)"
    )

    # Persist the pruned feature list so reviewers can inspect what columns
    # the learner actually sees.
    feat_rows = [{"index": i, "name": name} for i, name in enumerate(dataset.feature_names)]
    write_csv(output_dir / "linux_feature_columns.csv", feat_rows, ["index", "name"])

    print(
        f"Building samples: random={stochastic_runs}r, balanced={stochastic_runs}r, "
        f"diversity={diversity_runs}r@n<={args.diversity_max_n} (cand={candidate_size}), "
        f"uncertainty={uncertainty_runs}r (seed_frac={args.uncertainty_seed_fraction}), "
        f"coverage={coverage_runs}r (cand={args.coverage_candidate_size}), "
        f"cheap/expensiveOracle=1r each, levels={levels}"
    )
    t0 = time.time()
    samples = build_samples(
        dataset=dataset,
        levels=levels,
        stochastic_runs=stochastic_runs,
        diversity_runs=diversity_runs,
        diversity_candidate_size=candidate_size,
        diversity_max_n=args.diversity_max_n,
        uncertainty_runs=uncertainty_runs,
        uncertainty_seed_fraction=args.uncertainty_seed_fraction,
        coverage_runs=coverage_runs,
        coverage_candidate_size=args.coverage_candidate_size,
        alpha=args.alpha,
        log_target=not args.no_log_target,
        seed=args.seed,
    )
    dataset.samples.extend(samples)
    print(f"  {len(samples)} samples built in {fmt_secs(time.time() - t0)}")

    print("Evaluating samples")
    records = evaluate_all(
        dataset=dataset,
        samples=samples,
        alpha=args.alpha,
        learner=args.learner,
        log_target=not args.no_log_target,
        predict_chunk=args.predict_chunk,
    )

    print("Aggregating analyses")
    heterogeneity = cost_heterogeneity_summary(dataset)
    summary = strategy_summary(records)
    proxy = proxy_summary(records)
    ranks = rank_stability(summary, DEFAULT_LAMBDAS)
    pareto = pareto_summary(summary)

    write_csv(output_dir / "records.csv", records)
    write_csv(output_dir / "rq1_cost_heterogeneity.csv", heterogeneity)
    write_csv(output_dir / "strategy_summary.csv", summary)
    write_csv(output_dir / "rq2_proxy_summary.csv", proxy)
    write_csv(output_dir / "rq3_rank_stability.csv", ranks)
    write_csv(output_dir / "rq4_pareto.csv", pareto)

    print("Writing figures")
    plot_cost_distribution(records, output_dir / "fig_rq1_cost_distribution.png")
    plot_calibration(records, output_dir / "fig_rq2_size_cost_calibration.png")
    plot_accuracy_cost(pareto, output_dir / "fig_rq4_accuracy_cost_frontier.png")
    plot_rank_stability(ranks, output_dir / "fig_rq3_rank_stability.png")
    plot_strategy_cost_bias(summary, output_dir / "fig_rq1_strategy_cost_bias.png")

    write_markdown_summary(
        output_dir / f"{context}_report.md",
        context=context,
        cost_context=dataset.effective_cost_context if dataset.cost is not None else dataset.target_name,
        feature_count=dataset.X.shape[1],
        pool_size=dataset.X.shape[0],
        heterogeneity=heterogeneity,
        proxy=proxy,
        summary=summary,
        ranks=ranks,
        pareto=pareto,
        levels=levels,
        learner=args.learner,
    )

    print(f"Done. Outputs: {output_dir}")


if __name__ == "__main__":
    main()
