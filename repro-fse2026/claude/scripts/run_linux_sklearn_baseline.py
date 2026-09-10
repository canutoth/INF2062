#!/usr/bin/env python3
"""Run stronger sklearn baselines for Linux kernel-size prediction.

This script is intentionally separate from the sampling-cost runners.  Its
purpose is to sanity-check the Linux learner gap against the published Linux
kernel-size results by using stronger off-the-shelf learners, fixed training
budgets, and an explicit held-out-complement evaluation.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
import sys
import time

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from cost_sampling.linux_data import load_linux_dataset


LINUX_RELEASES = {
    "413": "ICPE-rawdata/linux/tuxkconfig_413.parquet",
    "415": "ICPE-rawdata/linux/tuxkconfig_415.parquet",
    "420": "ICPE-rawdata/linux/tuxkconfig_420.parquet",
    "500": "ICPE-rawdata/linux/tuxkconfig_500.parquet",
    "504": "ICPE-rawdata/linux/tuxkconfig_504.parquet",
    "507": "ICPE-rawdata/linux/tuxkconfig_507.parquet",
    "508": "ICPE-rawdata/linux/tuxkconfig_508.parquet",
}


@dataclass(frozen=True)
class LearnerSpec:
    name: str
    log_target: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="artifacts/linux_sklearn_baseline")
    parser.add_argument("--releases", default="413", help="Comma-separated releases, or all.")
    parser.add_argument("--budgets", default="1000,5000,10000")
    parser.add_argument(
        "--feature-sets",
        default="topk512,all",
        help="Comma-separated subset of topk512,all.",
    )
    parser.add_argument(
        "--learners",
        default="rf-log,hgbt-log,gbrt-log,ridge-log",
        help="Comma-separated subset of rf-log,hgbt-log,gbrt-log,ridge-log.",
    )
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--seed", type=int, default=20260511)
    parser.add_argument("--target-column", default="vmlinux")
    parser.add_argument("--predict-chunk", type=int, default=8192)
    parser.add_argument("--n-jobs", type=int, default=-1)
    parser.add_argument("--rf-trees", type=int, default=200)
    parser.add_argument("--rf-max-depth", type=int, default=None)
    parser.add_argument("--hgbt-iter", type=int, default=300)
    parser.add_argument("--gbrt-trees", type=int, default=300)
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    return parser.parse_args()


def split_csv(raw: str) -> list[str]:
    return [item.strip() for item in raw.split(",") if item.strip()]


def mape_chunked(model, X: np.ndarray, y: np.ndarray, test_idx: np.ndarray, *, predict_chunk: int) -> float:
    error_sum = 0.0
    count = 0
    for start in range(0, len(test_idx), predict_chunk):
        chunk = test_idx[start : start + predict_chunk]
        pred = np.asarray(model.predict(X[chunk]), dtype=np.float64)
        pred = np.maximum(pred, 1e-12)
        true = y[chunk]
        error_sum += float(np.sum(np.abs(true - pred) / np.maximum(np.abs(true), 1e-12)))
        count += len(chunk)
    return error_sum / max(count, 1)


def make_model(name: str, *, n_jobs: int, rf_trees: int, rf_max_depth: int | None, hgbt_iter: int, gbrt_trees: int):
    if name.startswith("rf-"):
        from sklearn.ensemble import RandomForestRegressor

        return RandomForestRegressor(
            n_estimators=rf_trees,
            max_depth=rf_max_depth,
            min_samples_leaf=1,
            max_features="sqrt",
            bootstrap=True,
            n_jobs=n_jobs,
            random_state=1729,
        )
    if name.startswith("hgbt-"):
        from sklearn.ensemble import HistGradientBoostingRegressor

        return HistGradientBoostingRegressor(
            max_iter=hgbt_iter,
            learning_rate=0.08,
            max_leaf_nodes=31,
            l2_regularization=0.0,
            random_state=4242,
        )
    if name.startswith("gbrt-"):
        from sklearn.ensemble import GradientBoostingRegressor

        return GradientBoostingRegressor(
            n_estimators=gbrt_trees,
            learning_rate=0.05,
            max_depth=5,
            min_samples_leaf=2,
            subsample=0.8,
            max_features="sqrt",
            random_state=4242,
        )
    if name.startswith("ridge-"):
        from sklearn.linear_model import Ridge

        return Ridge(alpha=1.0, fit_intercept=True, random_state=31337)
    raise ValueError(f"unsupported learner: {name}")


def fit_model(model, X_train: np.ndarray, y_train: np.ndarray, *, log_target: bool):
    target = np.log(y_train) if log_target else y_train
    model.fit(X_train, target)
    if not log_target:
        return model
    return LogTargetWrapper(model)


class LogTargetWrapper:
    def __init__(self, model):
        self.model = model

    def predict(self, X):
        return np.exp(np.clip(self.model.predict(X), -700, 700))


def append_row(path: Path, row: dict[str, object], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists() and path.stat().st_size > 0
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def load_feature_set(parquet: Path, release: str, feature_set: str):
    if feature_set == "topk512":
        top_k = 512
    elif feature_set == "all":
        top_k = None
    else:
        raise ValueError(f"unsupported feature set: {feature_set}")
    return load_linux_dataset(
        parquet,
        context=f"linux{release}_vmlinux_{feature_set}",
        top_k_features=top_k,
    )


def write_report(output_dir: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    by_key: dict[tuple[str, str, str, int], list[float]] = {}
    for row in rows:
        key = (
            str(row["release"]),
            str(row["feature_set"]),
            str(row["learner"]),
            int(row["budget"]),
        )
        by_key.setdefault(key, []).append(float(row["mape"]))

    summary_rows: list[dict[str, object]] = []
    for (release, feature_set, learner, budget), values in sorted(by_key.items()):
        arr = np.asarray(values, dtype=np.float64)
        summary_rows.append(
            {
                "release": release,
                "feature_set": feature_set,
                "learner": learner,
                "budget": budget,
                "runs": len(values),
                "median_mape": float(np.median(arr)),
                "mean_mape": float(np.mean(arr)),
                "min_mape": float(np.min(arr)),
                "max_mape": float(np.max(arr)),
            }
        )

    summary_path = output_dir / "linux_sklearn_baseline_summary.csv"
    fields = [
        "release",
        "feature_set",
        "learner",
        "budget",
        "runs",
        "median_mape",
        "mean_mape",
        "min_mape",
        "max_mape",
    ]
    with summary_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(summary_rows)

    best_by_release: dict[tuple[str, str], dict[str, object]] = {}
    for row in summary_rows:
        key = (str(row["release"]), str(row["feature_set"]))
        if key not in best_by_release or float(row["median_mape"]) < float(best_by_release[key]["median_mape"]):
            best_by_release[key] = row

    best_path = output_dir / "linux_sklearn_baseline_best.csv"
    with best_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(best_by_release[key] for key in sorted(best_by_release))

    lines = [
        "# Linux sklearn baseline",
        "",
        "This artifact checks Linux kernel-size prediction with stronger off-the-shelf sklearn learners.",
        "It is not the paper RQ sampling-cost pipeline; it is a diagnostic baseline against published Linux results.",
        "",
        "## Best median MAPE",
        "",
        "| Release | Feature set | Learner | Budget | Median MAPE | Runs |",
        "|---|---|---|---:|---:|---:|",
    ]
    for key in sorted(best_by_release):
        row = best_by_release[key]
        lines.append(
            f"| `{row['release']}` | `{row['feature_set']}` | `{row['learner']}` | "
            f"{row['budget']} | {float(row['median_mape']):.4f} | {row['runs']} |"
        )
    lines.extend(
        [
            "",
            "## Files",
            "",
            "- `linux_sklearn_baseline_long.csv`: one row per release, feature set, learner, budget, and run.",
            "- `linux_sklearn_baseline_summary.csv`: median/mean/min/max MAPE.",
            "- `linux_sklearn_baseline_best.csv`: best median MAPE per release and feature set.",
        ]
    )
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    try:
        import sklearn  # noqa: F401
    except ImportError as exc:
        raise SystemExit("scikit-learn is required. Install it in .venv-linux first.") from exc

    output_dir = REPO_ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    long_path = output_dir / "linux_sklearn_baseline_long.csv"
    row_fields = [
        "release",
        "feature_set",
        "learner",
        "budget",
        "run_id",
        "n_rows",
        "n_features",
        "train_n",
        "test_n",
        "mape",
        "elapsed_seconds",
    ]

    releases = list(LINUX_RELEASES) if args.releases == "all" else split_csv(args.releases)
    budgets = [int(item) for item in split_csv(args.budgets)]
    feature_sets = split_csv(args.feature_sets)
    learners = split_csv(args.learners)
    rng_master = np.random.default_rng(args.seed)
    rows: list[dict[str, object]] = []

    if args.skip_existing and long_path.exists():
        with long_path.open(encoding="utf-8", newline="") as handle:
            rows.extend(csv.DictReader(handle))

    done = {
        (str(row["release"]), str(row["feature_set"]), str(row["learner"]), int(row["budget"]), int(row["run_id"]))
        for row in rows
    }

    for release in releases:
        parquet = REPO_ROOT / LINUX_RELEASES[release]
        for feature_set in feature_sets:
            dataset = load_feature_set(parquet, release, feature_set)
            X = dataset.X
            y = dataset.y
            n_rows = X.shape[0]
            for learner in learners:
                log_target = learner.endswith("-log")
                for budget in budgets:
                    train_n = min(int(budget), n_rows - 1)
                    for run_id in range(1, args.runs + 1):
                        key = (release, feature_set, learner, budget, run_id)
                        if key in done:
                            continue
                        seed = int(rng_master.integers(0, 2**63 - 1))
                        rng = np.random.default_rng(seed)
                        train_idx = np.sort(rng.choice(n_rows, size=train_n, replace=False))
                        test_mask = np.ones(n_rows, dtype=bool)
                        test_mask[train_idx] = False
                        test_idx = np.flatnonzero(test_mask)

                        start = time.time()
                        try:
                            model = make_model(
                                learner,
                                n_jobs=args.n_jobs,
                                rf_trees=args.rf_trees,
                                rf_max_depth=args.rf_max_depth,
                                hgbt_iter=args.hgbt_iter,
                                gbrt_trees=args.gbrt_trees,
                            )
                            fitted = fit_model(model, X[train_idx], y[train_idx], log_target=log_target)
                            mape = mape_chunked(fitted, X, y, test_idx, predict_chunk=args.predict_chunk)
                            elapsed = time.time() - start
                            row = {
                                "release": release,
                                "feature_set": feature_set,
                                "learner": learner,
                                "budget": budget,
                                "run_id": run_id,
                                "n_rows": n_rows,
                                "n_features": X.shape[1],
                                "train_n": train_n,
                                "test_n": len(test_idx),
                                "mape": mape,
                                "elapsed_seconds": round(elapsed, 3),
                            }
                            append_row(long_path, row, row_fields)
                            rows.append(row)
                            print(
                                f"{release} {feature_set} {learner} budget={budget} "
                                f"run={run_id}: MAPE={mape:.4f} ({elapsed:.1f}s)",
                                flush=True,
                            )
                        except Exception as exc:  # pragma: no cover - diagnostic script
                            print(f"ERROR {release} {feature_set} {learner} budget={budget} run={run_id}: {exc}", flush=True)
                            if not args.continue_on_error:
                                raise
            del dataset

    write_report(output_dir, rows)
    print(f"Wrote Linux sklearn baseline under {output_dir}")


if __name__ == "__main__":
    main()
