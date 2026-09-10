"""RQ-oriented analyses for empirical sampling-cost experiments."""

from __future__ import annotations

from collections import defaultdict
import csv
from pathlib import Path
from typing import Any

import numpy as np

from .archive_runs import RunDataset
from .metrics import (
    fit_learner,
    iqr,
    kendall_tau_from_scores,
    mean_relative_error,
    minmax,
    pareto_mask,
    predict,
    spearman,
)


def level_sort_key(level: str) -> tuple[int, str]:
    if level.startswith("t") and level[1:].isdigit():
        return int(level[1:]), level
    if level.startswith("n") and level[1:].isdigit():
        return int(level[1:]), level
    return 999, level


def strategy_sort_key(strategy: str) -> tuple[int, str]:
    order = {
        "random": 0,
        "solverBased": 1,
        "henard": 2,
        "distBased": 3,
        "divDistBased": 4,
        "twise": 5,
        "balanced": 6,
        "diversity": 7,
        "uncertainty": 8,
        "coverage": 9,
        "SRSSampling": 10,
        "pairwise": 12,
        "pilotCost": 13,
        "cheapOracle": 20,
        "expensiveOracle": 21,
    }
    return order.get(strategy, 99), strategy


def evaluate_samples(
    dataset: RunDataset,
    *,
    alpha: float = 1.0,
    log_target: bool = True,
    learner: str = "ridge-log",
    mre_cache: dict[tuple[Any, ...], float] | None = None,
    mre_cache_prefix: tuple[Any, ...] = (),
    progress_label: str = "",
    progress_every: int = 0,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    full_cost = dataset.full_cost
    cost_values = dataset.cost_values
    n_configs = len(dataset.y)
    cache = mre_cache if mre_cache is not None else {}
    effective_learner = learner
    if not log_target and learner == "ridge-log":
        effective_learner = "ridge-raw"
    elif not log_target and learner == "cart-log":
        effective_learner = "cart-raw"

    for sample_idx, sample in enumerate(dataset.samples, start=1):
        indices = np.array(sorted(set(int(idx) for idx in sample.indices)), dtype=int)
        cache_key = (*mre_cache_prefix, effective_learner, tuple(indices.tolist()))
        if cache_key in cache:
            mre = cache[cache_key]
        else:
            test_mask = np.ones(n_configs, dtype=bool)
            test_mask[indices] = False
            model = fit_learner(dataset.X[indices], dataset.y[indices], learner=effective_learner, alpha=alpha)
            y_pred = predict(model, dataset.X[test_mask])
            mre = mean_relative_error(dataset.y[test_mask], y_pred)
            cache[cache_key] = mre

        n = int(len(indices))
        train_cost = float(np.sum(cost_values[indices]))
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
                "learner": effective_learner,
                "zip_member": sample.ref.zip_member,
            }
        )
        if progress_every and sample_idx % progress_every == 0:
            label = f" {progress_label}" if progress_label else ""
            print(f"  evaluated{label}: {sample_idx}/{len(dataset.samples)} samples", flush=True)

    records.sort(key=lambda row: (strategy_sort_key(row["strategy"]), level_sort_key(row["level"]), row["run"]))
    return records


def cost_heterogeneity_summary(dataset: RunDataset) -> list[dict[str, Any]]:
    values = dataset.cost_values
    q1, q3 = iqr(values)
    return [
        {
            "context": dataset.context,
            "target_context": dataset.context,
            "cost_context": dataset.effective_cost_context,
            "n_configurations": len(values),
            "full_cost": dataset.full_cost,
            "min_cost": float(np.min(values)),
            "q1_cost": q1,
            "median_cost": float(np.median(values)),
            "mean_cost": float(np.mean(values)),
            "q3_cost": q3,
            "max_cost": float(np.max(values)),
            "std_cost": float(np.std(values, ddof=1)),
            "cv_cost": float(np.std(values, ddof=1) / np.mean(values)),
            "p90_over_p10": float(np.percentile(values, 90) / np.percentile(values, 10)),
        }
    ]


def _groups(rows: list[dict[str, Any]], keys: tuple[str, ...]) -> dict[tuple[Any, ...], list[dict[str, Any]]]:
    grouped: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(row)
    return grouped


def strategy_summary(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    target_context = records[0].get("target_context", records[0].get("context")) if records else ""
    cost_context = records[0].get("cost_context", target_context) if records else ""
    by_level_strategy = _groups(records, ("level", "strategy"))
    random_cost_by_level: dict[str, float] = {}
    for (level, strategy), rows in by_level_strategy.items():
        if strategy == "random":
            random_cost_by_level[level] = float(np.median([row["train_cost"] for row in rows]))

    rows_out: list[dict[str, Any]] = []
    for (level, strategy), rows in by_level_strategy.items():
        cost = np.array([row["train_cost"] for row in rows], dtype=float)
        pct_cost = np.array([row["pct_cost"] for row in rows], dtype=float)
        ratio = np.array([row["calibration_ratio"] for row in rows], dtype=float)
        mre = np.array([row["mre"] for row in rows], dtype=float)
        q1_cost, q3_cost = iqr(cost)
        q1_ratio, q3_ratio = iqr(ratio)
        q1_mre, q3_mre = iqr(mre)
        median_cost = float(np.median(cost))
        rows_out.append(
            {
                "target_context": target_context,
                "cost_context": cost_context,
                "level": level,
                "strategy": strategy,
                "runs": len(rows),
                "n": int(round(float(np.median([row["n"] for row in rows])))),
                "pct_n": float(np.median([row["pct_n"] for row in rows])),
                "median_train_cost": median_cost,
                "q1_train_cost": q1_cost,
                "q3_train_cost": q3_cost,
                "median_pct_cost": float(np.median(pct_cost)),
                "median_calibration_ratio": float(np.median(ratio)),
                "q1_calibration_ratio": q1_ratio,
                "q3_calibration_ratio": q3_ratio,
                "median_mre": float(np.median(mre)),
                "q1_mre": q1_mre,
                "q3_mre": q3_mre,
                "cost_over_random": (
                    median_cost / random_cost_by_level[level]
                    if level in random_cost_by_level and random_cost_by_level[level] > 0
                    else float("nan")
                ),
            }
        )

    rows_out.sort(key=lambda row: (level_sort_key(row["level"]), strategy_sort_key(row["strategy"])))
    return rows_out


def proxy_summary(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    target_context = records[0].get("target_context", records[0].get("context")) if records else ""
    cost_context = records[0].get("cost_context", target_context) if records else ""
    out: list[dict[str, Any]] = []
    for key, rows in [(("ALL",), records), *_groups(records, ("strategy",)).items()]:
        label = key[0]
        n = np.array([row["n"] for row in rows], dtype=float)
        cost = np.array([row["train_cost"] for row in rows], dtype=float)
        ratio = np.array([row["calibration_ratio"] for row in rows], dtype=float)
        q1_ratio, q3_ratio = iqr(ratio)
        out.append(
            {
                "target_context": target_context,
                "cost_context": cost_context,
                "strategy": label,
                "records": len(rows),
                "spearman_n_train_cost": spearman(n, cost),
                "median_calibration_ratio": float(np.median(ratio)),
                "q1_calibration_ratio": q1_ratio,
                "q3_calibration_ratio": q3_ratio,
                "median_bias": float(np.median(ratio) - 1.0),
            }
        )
    out.sort(key=lambda row: strategy_sort_key(row["strategy"]) if row["strategy"] != "ALL" else (-1, "ALL"))
    return out


def rank_stability(summary: list[dict[str, Any]], lambdas: list[float]) -> list[dict[str, Any]]:
    target_context = summary[0].get("target_context", "") if summary else ""
    cost_context = summary[0].get("cost_context", target_context) if summary else ""
    labels = [f"{row['strategy']}_{row['level']}" for row in summary]
    mre = np.array([row["median_mre"] for row in summary], dtype=float)
    pct_n = np.array([row["pct_n"] for row in summary], dtype=float)
    pct_cost = np.array([row["median_pct_cost"] for row in summary], dtype=float)
    mre_norm = minmax(mre)
    n_norm = minmax(pct_n)
    cost_norm = minmax(pct_cost)
    out: list[dict[str, Any]] = []

    for lam in lambdas:
        j_size = mre_norm + lam * n_norm
        j_time = mre_norm + lam * cost_norm
        rank_size = np.argsort(np.argsort(j_size)) + 1
        rank_time = np.argsort(np.argsort(j_time)) + 1
        top3_size = set(np.argsort(j_size)[:3])
        top3_time = set(np.argsort(j_time)[:3])
        out.append(
            {
                "target_context": target_context,
                "cost_context": cost_context,
                "lambda": lam,
                "top1_size": labels[int(np.argmin(j_size))],
                "top1_time": labels[int(np.argmin(j_time))],
                "top1_agreement": int(np.argmin(j_size) == np.argmin(j_time)),
                "top3_overlap": len(top3_size & top3_time) / 3.0,
                "kendall_tau": kendall_tau_from_scores(j_size, j_time),
                "mean_abs_rank_difference": float(np.mean(np.abs(rank_size - rank_time))),
            }
        )
    return out


def pareto_summary(summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    target_context = summary[0].get("target_context", "") if summary else ""
    cost_context = summary[0].get("cost_context", target_context) if summary else ""
    count_cost = np.array([row["pct_n"] for row in summary], dtype=float)
    empirical_cost = np.array([row["median_pct_cost"] for row in summary], dtype=float)
    error = np.array([row["median_mre"] for row in summary], dtype=float)
    count_mask = pareto_mask(count_cost, error)
    empirical_mask = pareto_mask(empirical_cost, error)
    out: list[dict[str, Any]] = []
    for idx, row in enumerate(summary):
        out.append(
            {
                "target_context": target_context,
                "cost_context": cost_context,
                "strategy": row["strategy"],
                "level": row["level"],
                "n": row["n"],
                "pct_n": row["pct_n"],
                "median_pct_cost": row["median_pct_cost"],
                "median_train_cost": row["median_train_cost"],
                "median_mre": row["median_mre"],
                "pareto_count": int(count_mask[idx]),
                "pareto_empirical": int(empirical_mask[idx]),
            }
        )
    return out


def write_csv(path: str | Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
