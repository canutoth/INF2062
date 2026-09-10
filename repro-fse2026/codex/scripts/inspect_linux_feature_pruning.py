#!/usr/bin/env python3
"""Inspect Linux/TuxKConfig feature pruning before learner fitting."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys
from typing import Any

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from cost_sampling.linux_data import NON_OPTION_COLUMNS

LINUX_RELEASES = {
    "413": "ICPE-rawdata/linux/tuxkconfig_413.parquet",
    "415": "ICPE-rawdata/linux/tuxkconfig_415.parquet",
    "420": "ICPE-rawdata/linux/tuxkconfig_420.parquet",
    "500": "ICPE-rawdata/linux/tuxkconfig_500.parquet",
    "504": "ICPE-rawdata/linux/tuxkconfig_504.parquet",
    "507": "ICPE-rawdata/linux/tuxkconfig_507.parquet",
    "508": "ICPE-rawdata/linux/tuxkconfig_508.parquet",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="artifacts/linux_feature_pruning")
    parser.add_argument("--min-minor-class", type=int, default=50)
    parser.add_argument("--top-k-features", type=int, default=512)
    return parser.parse_args()


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_option_matrix(path: Path, option_columns: list[str]) -> np.ndarray:
    import pyarrow.parquet as pq

    pf = pq.ParquetFile(str(path))
    X = np.empty((pf.metadata.num_rows, len(option_columns)), dtype=np.int8)
    cursor = 0
    for batch in pf.iter_batches(batch_size=8192, columns=option_columns):
        block = np.column_stack(
            [batch.column(i).to_numpy(zero_copy_only=False) for i in range(batch.num_columns)]
        ).astype(np.int8, copy=False)
        X[cursor : cursor + block.shape[0]] = block
        cursor += block.shape[0]
    return X


def duplicate_groups(X: np.ndarray, names: list[str]) -> tuple[list[int], list[dict[str, Any]]]:
    seen: dict[bytes, tuple[int, str]] = {}
    keep_idx: list[int] = []
    rows: list[dict[str, Any]] = []
    for j, name in enumerate(names):
        digest = X[:, j].tobytes()
        if digest in seen:
            representative_index, representative = seen[digest]
            rows.append(
                {
                    "representative_index": representative_index,
                    "representative": representative,
                    "duplicate_index": j,
                    "duplicate": name,
                }
            )
            continue
        seen[digest] = (j, name)
        keep_idx.append(j)
    return keep_idx, rows


def top_k_indices(X: np.ndarray, y: np.ndarray, k: int | None) -> np.ndarray:
    if k is None or X.shape[1] <= k:
        return np.arange(X.shape[1])
    col_sum = X.sum(axis=0).astype(np.float64)
    weighted = (X.astype(np.float32, copy=False).T @ y.astype(np.float32, copy=False)).astype(np.float64)
    mean_on = np.where(col_sum > 0, weighted / np.maximum(col_sum, 1.0), 0.0)
    n = float(X.shape[0])
    total_y = float(np.sum(y))
    mean_off = np.where(col_sum < n, (total_y - weighted) / np.maximum(n - col_sum, 1.0), 0.0)
    importance = np.abs(mean_on - mean_off)
    keep_idx = np.argsort(-importance)[:k]
    keep_idx.sort()
    return keep_idx


def main() -> None:
    args = parse_args()
    output_dir = REPO_ROOT / args.output_dir
    summary_rows: list[dict[str, Any]] = []

    import pyarrow.parquet as pq

    for release, rel_path in LINUX_RELEASES.items():
        path = REPO_ROOT / rel_path
        pf = pq.ParquetFile(str(path))
        schema = pf.schema_arrow
        all_names = [schema.field(i).name for i in range(len(schema))]
        option_columns = [name for name in all_names if name not in set(NON_OPTION_COLUMNS)]
        X = load_option_matrix(path, option_columns)

        active_counts = X.sum(axis=0)
        minor_count = np.minimum(active_counts, X.shape[0] - active_counts)
        rare_keep = minor_count >= int(args.min_minor_class)
        rare_names = [name for name, keep in zip(option_columns, rare_keep) if keep]
        X_rare = X[:, rare_keep]

        all_keep_idx, all_duplicate_rows = duplicate_groups(X_rare, rare_names)
        write_csv(
            output_dir / f"linux{release}_duplicate_groups_all_remaining.csv",
            all_duplicate_rows,
            ["representative_index", "representative", "duplicate_index", "duplicate"],
        )

        y = None
        default_after_topk = ""
        default_duplicate_count = ""
        default_final_features = ""
        if args.top_k_features > 0:
            y = pq.read_table(str(path), columns=["vmlinux"]).column("vmlinux").to_numpy(zero_copy_only=False)
            idx = top_k_indices(X_rare, y.astype(np.float64, copy=False), args.top_k_features)
            default_names = [rare_names[i] for i in idx]
            X_default = X_rare[:, idx]
            default_keep_idx, default_duplicate_rows = duplicate_groups(X_default, default_names)
            default_after_topk = len(default_names)
            default_duplicate_count = len(default_duplicate_rows)
            default_final_features = len(default_keep_idx)
            write_csv(
                output_dir / f"linux{release}_duplicate_groups_topk{args.top_k_features}.csv",
                default_duplicate_rows,
                ["representative_index", "representative", "duplicate_index", "duplicate"],
            )

        summary_rows.append(
            {
                "release": release,
                "rows": X.shape[0],
                "schema_columns": len(all_names),
                "forbidden_columns": len(NON_OPTION_COLUMNS),
                "option_columns_before_pruning": len(option_columns),
                "rare_removed_min_minor_lt_50": len(option_columns) - len(rare_names),
                "after_rare": len(rare_names),
                "duplicates_all_remaining": len(all_duplicate_rows),
                "all_remaining_after_duplicates": len(all_keep_idx),
                f"default_topk_{args.top_k_features}_selected": default_after_topk,
                f"default_topk_{args.top_k_features}_duplicates": default_duplicate_count,
                f"default_topk_{args.top_k_features}_after_duplicates": default_final_features,
            }
        )
        print(
            f"linux{release}: options={len(option_columns)}, after rare={len(rare_names)}, "
            f"all remaining after duplicates={len(all_keep_idx)}"
        )

    write_csv(
        output_dir / "linux_feature_pruning_summary.csv",
        summary_rows,
        [
            "release",
            "rows",
            "schema_columns",
            "forbidden_columns",
            "option_columns_before_pruning",
            "rare_removed_min_minor_lt_50",
            "after_rare",
            "duplicates_all_remaining",
            "all_remaining_after_duplicates",
            f"default_topk_{args.top_k_features}_selected",
            f"default_topk_{args.top_k_features}_duplicates",
            f"default_topk_{args.top_k_features}_after_duplicates",
        ],
    )
    print(f"Wrote Linux feature pruning diagnostics to {output_dir}")


if __name__ == "__main__":
    main()
