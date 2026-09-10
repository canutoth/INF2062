"""Loader for the TuxKConfig (LinuxData) parquet artifact.

The published OpenML datasets store one parquet per kernel release
(`tuxkconfig_413.parquet`, …).  We reuse the existing `RunDataset` shape so
the analysis/plotting pipeline does not need to know about Linux at all.

Forbidden as features
---------------------
Twenty-one columns are forbidden as inputs to the learner because they are
either the prediction target itself, derivatives of the target, or
metadata that would let the learner short-circuit the option vector:

- `vmlinux`                           — the prediction target
- {GZIP, BZIP2, LZMA, XZ, LZO, LZ4} × {bzImage, vmlinux, "raw"} — 18
  compressed-image variants, all functions of the same kernel build and
  therefore tightly correlated with `vmlinux`
- `active_options`                    — count of enabled options, exactly
  derivable from the option vector itself (would let ridge collapse to a
  size-of-config regression)
- `cid`                               — row identifier

`NON_OPTION_COLUMNS` enumerates these and is the single source of truth.
Any other parquet column is treated as a binary Kconfig flag.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np


# Forbidden as features (see module docstring for rationale).
NON_OPTION_COLUMNS: tuple[str, ...] = (
    "cid",
    "active_options",
    "vmlinux",
    "GZIP-bzImage", "GZIP-vmlinux", "GZIP",
    "BZIP2-bzImage", "BZIP2-vmlinux", "BZIP2",
    "LZMA-bzImage", "LZMA-vmlinux", "LZMA",
    "XZ-bzImage", "XZ-vmlinux", "XZ",
    "LZO-bzImage", "LZO-vmlinux", "LZO",
    "LZ4-bzImage", "LZ4-vmlinux", "LZ4",
)


@dataclass(frozen=True)
class LinuxDataset:
    """Pool view of a single Linux release.

    Mirrors the public surface used by `cost_sampling.analysis` so that
    `evaluate_samples` can run on it unchanged: `X`, `y`, `cost_values`,
    `full_cost`, `context`, `effective_cost_context`.  Samples are attached
    later by the runner script.
    """

    context: str
    feature_names: list[str]
    X: np.ndarray  # int8, shape (n_configs, n_features)
    y: np.ndarray  # float64, shape (n_configs,) — prediction target
    cost: np.ndarray | None  # None means cost == y
    cost_context: str | None
    target_name: str
    cost_name: str
    active_options: np.ndarray  # int32, shape (n_configs,)
    samples: list  # filled in by the runner; analysis expects this attribute

    @property
    def cost_values(self) -> np.ndarray:
        return self.y if self.cost is None else self.cost

    @property
    def full_cost(self) -> float:
        return float(np.sum(self.cost_values))

    @property
    def effective_cost_context(self) -> str:
        return self.context if self.cost_context is None else self.cost_context


def _load_parquet_columns(path: str | Path, columns: list[str]) -> dict[str, np.ndarray]:
    import pyarrow.parquet as pq

    pf = pq.ParquetFile(str(path))
    out: dict[str, list[np.ndarray]] = {name: [] for name in columns}
    for batch in pf.iter_batches(batch_size=8192, columns=columns):
        for name in columns:
            out[name].append(batch.column(name).to_numpy(zero_copy_only=False))
    return {name: np.concatenate(parts) for name, parts in out.items()}


def load_linux_dataset(
    parquet_path: str | Path,
    *,
    context: str,
    target_column: str = "vmlinux",
    cost_column: str | None = None,
    min_minor_class: int = 50,
    drop_duplicate_columns: bool = True,
    top_k_features: int | None = 512,
) -> LinuxDataset:
    """Load a TuxKConfig parquet and return a `LinuxDataset`.

    Parameters
    ----------
    parquet_path : path to `tuxkconfig_<release>.parquet`.
    context : human-readable label, e.g. "linux413_vmlinux".
    target_column : column predicted by the learner.
    cost_column : column used as empirical acquisition cost.  Defaults to
        `target_column`, matching the `x264_time_*` design.
    min_minor_class : drop option columns whose minority class has fewer than
        this many configurations in the pool.  This is a one-time, dataset-
        level filter and does not depend on which strategy will sample later.
    drop_duplicate_columns : drop columns with identical values to one already
        kept (one representative survives).
    top_k_features : if set, keep only the K most informative columns ranked
        by absolute mean-difference of the target between the two classes
        (equivalent to |Pearson| up to scaling for binary features).  This is
        purely a learner-efficiency knob — RQ1/RQ2 metrics are computed on
        the full pool and do not depend on which columns the ridge sees.
    """

    import pyarrow.parquet as pq

    parquet_path = Path(parquet_path)
    pf = pq.ParquetFile(str(parquet_path))
    schema = pf.schema_arrow
    all_names = [schema.field(i).name for i in range(len(schema))]

    non_option_set = set(NON_OPTION_COLUMNS)
    option_columns = [name for name in all_names if name not in non_option_set]

    cost_column = cost_column or target_column
    needed_extras = sorted({"active_options", target_column, cost_column})

    # Stream option columns once, accumulate as int8 to keep memory bounded.
    n_rows = pf.metadata.num_rows
    n_options = len(option_columns)
    X = np.empty((n_rows, n_options), dtype=np.int8)
    cursor = 0
    for batch in pf.iter_batches(batch_size=8192, columns=option_columns):
        block = np.column_stack(
            [batch.column(i).to_numpy(zero_copy_only=False) for i in range(batch.num_columns)]
        ).astype(np.int8, copy=False)
        X[cursor : cursor + block.shape[0]] = block
        cursor += block.shape[0]
    assert cursor == n_rows

    extras = _load_parquet_columns(parquet_path, needed_extras)
    y = extras[target_column].astype(np.float64, copy=False)
    cost_values = extras[cost_column].astype(np.float64, copy=False)
    active_options = extras["active_options"].astype(np.int32, copy=False)

    minor_count = np.minimum(X.sum(axis=0), n_rows - X.sum(axis=0))
    keep_mask = minor_count >= int(min_minor_class)
    feature_names = [name for name, keep in zip(option_columns, keep_mask) if keep]
    X = X[:, keep_mask]

    if top_k_features is not None and X.shape[1] > top_k_features:
        # Mean of y where the option is on / off. The absolute difference
        # measures the option's marginal effect on the target. Vectorised:
        # for each column c, mean1 = X[:,c] @ y / sum(X[:,c]).
        col_sum = X.sum(axis=0).astype(np.float64)
        # X is int8; cast to float32 to keep memory bounded.
        weighted = (X.astype(np.float32, copy=False).T @ y.astype(np.float32, copy=False)).astype(np.float64)
        mean_on = np.where(col_sum > 0, weighted / np.maximum(col_sum, 1.0), 0.0)
        total_y = float(np.sum(y))
        n = float(n_rows)
        mean_off = np.where(col_sum < n, (total_y - weighted) / np.maximum(n - col_sum, 1.0), 0.0)
        importance = np.abs(mean_on - mean_off)
        keep_idx = np.argsort(-importance)[:top_k_features]
        keep_idx.sort()
        X = X[:, keep_idx]
        feature_names = [feature_names[j] for j in keep_idx]

    if drop_duplicate_columns and X.shape[1] > 1:
        # Hash each column so we can drop exact duplicates without an O(k^2)
        # comparison.  Hash on the byte representation.
        seen: dict[bytes, int] = {}
        keep_idx: list[int] = []
        for j in range(X.shape[1]):
            digest = X[:, j].tobytes()
            if digest in seen:
                continue
            seen[digest] = j
            keep_idx.append(j)
        if len(keep_idx) < X.shape[1]:
            X = X[:, keep_idx]
            feature_names = [feature_names[j] for j in keep_idx]

    cost = None if cost_column == target_column else cost_values
    cost_context = None if cost_column == target_column else f"linux:{cost_column}"

    return LinuxDataset(
        context=context,
        feature_names=feature_names,
        X=X,
        y=y,
        cost=cost,
        cost_context=cost_context,
        target_name=target_column,
        cost_name=cost_column,
        active_options=active_options,
        samples=[],
    )
