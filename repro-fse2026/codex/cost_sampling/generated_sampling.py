"""Generated sampling strategies for measured configuration tables."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from io import StringIO
import json
from math import ceil, floor
from pathlib import Path
import zipfile

import numpy as np

from .metrics import fit_ridge, predict


DEFAULT_PERCENTAGES = (0.01, 0.02, 0.05, 0.10, 0.20, 0.30)
DEFAULT_ANCHORS = (8, 16, 32, 64, 128, 256)
LABEL_COLUMNS = {
    "performance",
    "energy",
    "fixed-energy",
    "benchmark-energy",
    "cpu",
}
CONTEXT_COLUMNS = {"revision", "workload"}
WORKLOAD_CONTEXT_HINTS = {"workload", "input", "video", "query", "task"}
WORKLOAD_LABEL_HINTS = {
    "performance",
    "runtime",
    "time",
    "throughput",
    "latency",
    "energy",
    "memory",
    "size",
    "bitrate",
    "fps",
}
JOIN_KEY_HINTS = (
    "config_id",
    "configuration_id",
    "configurationid",
    "configid",
    "config",
    "id",
)
METADATA_HINTS = {
    "partition",
    "partitionid",
    "repetition",
    "repetitionid",
    "run",
    "runid",
    "seed",
    "index",
    "idx",
}


@dataclass(frozen=True)
class GeneratedSampleRef:
    context: str
    run_id: int
    strategy: str
    level: str
    zip_member: str


@dataclass(frozen=True)
class GeneratedSample:
    ref: GeneratedSampleRef
    indices: tuple[int, ...]


@dataclass
class GeneratedDataset:
    context: str
    effective_cost_context: str
    X: np.ndarray
    y: np.ndarray
    cost_values: np.ndarray
    full_cost: float
    samples: list[GeneratedSample]
    system: str
    feature_names: list[str]
    target_property: str
    cost_property: str
    cost_orientation: str
    source_member: str
    n_configurations: int


@dataclass(frozen=True)
class MeasuredTable:
    system: str
    source_member: str
    rows: list[dict[str, str]]
    feature_columns: list[str]
    context_columns: list[str]
    label_columns: list[str]
    X: np.ndarray
    feature_names: list[str]
    raw_feature_values: list[tuple[str, ...]]
    analysis_name: str | None = None


TwinsTable = MeasuredTable


def budget_grid(
    n_configurations: int,
    *,
    percentages: tuple[float, ...] = DEFAULT_PERCENTAGES,
    anchors: tuple[int, ...] = DEFAULT_ANCHORS,
    max_fraction: float = 0.30,
    max_absolute: int = 256,
    min_n: int = 8,
) -> list[int]:
    """Return the generated-protocol sample-size grid for a measured universe."""

    if n_configurations <= 1:
        return []
    max_n = max(1, min(int(floor(max_fraction * n_configurations)), max_absolute, n_configurations - 1))
    values: set[int] = set()
    for pct in percentages:
        values.add(min(int(ceil(pct * n_configurations)), max_n))
    for anchor in anchors:
        if anchor <= max_n:
            values.add(anchor)
    if min_n <= n_configurations - 1:
        values.add(min(min_n, max_n))
    lower = min_n if max_n >= min_n else 1
    return sorted(n for n in values if lower <= n <= max_n)


def parse_where(items: list[str] | None) -> dict[str, str]:
    filters: dict[str, str] = {}
    for item in items or []:
        if "=" not in item:
            raise ValueError(f"Expected KEY=VALUE filter, got {item!r}")
        key, value = item.split("=", 1)
        filters[key] = value
    return filters


def _sniff_csv(text: str) -> csv.Dialect:
    return csv.Sniffer().sniff(text[:20000], delimiters=",;\t")


def _to_float_or_none(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None


def _encode_features(rows: list[dict[str, str]], feature_columns: list[str]) -> tuple[np.ndarray, list[str]]:
    matrices: list[np.ndarray] = []
    names: list[str] = []
    for column in feature_columns:
        values = [row[column] for row in rows]
        numeric = [_to_float_or_none(value) for value in values]
        if all(value is not None for value in numeric):
            arr = np.asarray([float(value) for value in numeric if value is not None], dtype=float)
            lo = float(np.min(arr))
            hi = float(np.max(arr))
            scaled = np.zeros_like(arr) if hi == lo else (arr - lo) / (hi - lo)
            matrices.append(scaled.reshape(-1, 1))
            names.append(column)
        else:
            categories = sorted(set(values))
            for category in categories:
                matrices.append(np.asarray([1.0 if value == category else 0.0 for value in values]).reshape(-1, 1))
                names.append(f"{column}={category}")
    if not matrices:
        raise ValueError("No feature columns available after excluding labels/context columns.")
    return np.hstack(matrices), names


def _normalized(name: str) -> str:
    return "".join(ch for ch in name.lower() if ch.isalnum())


def _read_csv_from_archive(archive: zipfile.ZipFile, member: str) -> list[dict[str, str]]:
    text = archive.read(member).decode("utf-8", errors="replace")
    dialect = _sniff_csv(text)
    return list(csv.DictReader(StringIO(text), dialect=dialect))


def _find_member(archive: zipfile.ZipFile, suffixes: tuple[str, ...]) -> str | None:
    names = archive.namelist()
    for suffix in suffixes:
        for name in names:
            if name.endswith(suffix):
                return name
    return None


def _guess_context_columns(header: list[str]) -> list[str]:
    out: list[str] = []
    for column in header:
        norm = _normalized(column)
        if norm in CONTEXT_COLUMNS or any(hint in norm for hint in WORKLOAD_CONTEXT_HINTS):
            out.append(column)
    return out


def _guess_label_columns(header: list[str], rows: list[dict[str, str]], *, exclude: set[str]) -> list[str]:
    out: list[str] = []
    for column in header:
        if column in exclude:
            continue
        norm = _normalized(column)
        looks_like_label = norm in LABEL_COLUMNS or any(hint in norm for hint in WORKLOAD_LABEL_HINTS)
        numeric = all(_to_float_or_none(row[column]) is not None for row in rows[: min(len(rows), 50)])
        if looks_like_label or numeric:
            out.append(column)
    return out


def _filter_rows(rows: list[dict[str, str]], where: dict[str, str]) -> list[dict[str, str]]:
    if not where:
        return rows
    out = rows
    for key, value in where.items():
        out = [row for row in out if row.get(key) == value]
    return out


def _subsample_rows(rows: list[dict[str, str]], *, max_rows: int | None, row_seed: int) -> list[dict[str, str]]:
    if max_rows is None or max_rows <= 0 or len(rows) <= max_rows:
        return rows
    rng = np.random.default_rng(row_seed)
    keep = sorted(rng.choice(len(rows), size=max_rows, replace=False).astype(int).tolist())
    return [rows[idx] for idx in keep]


def _join_key(shared_columns: list[str]) -> str | None:
    normalized = {_normalized(column): column for column in shared_columns}
    for hint in JOIN_KEY_HINTS:
        if hint in normalized:
            return normalized[hint]
    for column in shared_columns:
        norm = _normalized(column)
        if norm.endswith("id"):
            return column
    return None


def load_twins_table(
    zip_path: str | Path,
    system: str,
    *,
    where: dict[str, str] | None = None,
    max_rows: int | None = None,
    row_seed: int = 0,
) -> MeasuredTable:
    """Load one `data/<system>/measurements.csv` table from TwinsOrFalseFriends."""

    where = where or {}
    zip_path = Path(zip_path)
    with zipfile.ZipFile(zip_path) as archive:
        root = archive.namelist()[0].split("/")[0] + "/"
        member = f"{root}data/{system}/measurements.csv"
        if member not in archive.namelist():
            available = sorted(
                name.split("/")[2]
                for name in archive.namelist()
                if name.startswith(root + "data/") and name.endswith("/measurements.csv")
            )
            raise FileNotFoundError(f"Missing {member}; available systems: {', '.join(available)}")
        text = archive.read(member).decode("utf-8", errors="replace")

    dialect = _sniff_csv(text)
    rows = list(csv.DictReader(StringIO(text), dialect=dialect))
    for key, value in where.items():
        rows = [row for row in rows if row.get(key) == value]
    if not rows:
        raise ValueError(f"No rows left for {system} after filters {where}.")
    if max_rows is not None and max_rows > 0 and len(rows) > max_rows:
        rng = np.random.default_rng(row_seed)
        keep = sorted(rng.choice(len(rows), size=max_rows, replace=False).astype(int).tolist())
        rows = [rows[idx] for idx in keep]

    header = list(rows[0].keys())
    label_columns = [
        column
        for column in header
        if column.lower() in LABEL_COLUMNS or "energy" in column.lower() or "performance" in column.lower()
    ]
    context_columns = [column for column in header if column.lower() in CONTEXT_COLUMNS]
    feature_columns = [
        column
        for column in header
        if column not in label_columns and column not in context_columns and column != "root"
    ]
    X, feature_names = _encode_features(rows, feature_columns)
    raw_values = [tuple(row[column] for column in feature_columns) for row in rows]
    return MeasuredTable(
        system=system,
        source_member=member,
        rows=rows,
        feature_columns=feature_columns,
        context_columns=context_columns,
        label_columns=label_columns,
        X=X,
        feature_names=feature_names,
        raw_feature_values=raw_values,
    )


def load_workload_table(
    zip_path: str | Path,
    system: str,
    *,
    where: dict[str, str] | None = None,
    max_rows: int | None = None,
    row_seed: int = 0,
) -> MeasuredTable:
    """Load one system from the ICSE 2023 workload-impact archive.

    Expected primary layout:
    - `.../dashboard/resources/<system>/sample.csv`
    - `.../dashboard/resources/<system>/measurements.csv`
    """

    where = where or {}
    zip_path = Path(zip_path)
    with zipfile.ZipFile(zip_path) as archive:
        sample_member = _find_member(
            archive,
            (
                f"/dashboard/resources/{system}/sample.csv",
                f"/resources/{system}/sample.csv",
                f"/{system}/sample.csv",
            ),
        )
        measurements_member = _find_member(
            archive,
            (
                f"/dashboard/resources/{system}/measurements.csv",
                f"/resources/{system}/measurements.csv",
                f"/{system}/measurements.csv",
            ),
        )
        if measurements_member is None:
            raise FileNotFoundError(f"Could not locate measurements.csv for system {system!r} in {zip_path}")
        measurement_rows = _filter_rows(_read_csv_from_archive(archive, measurements_member), where)
        if not measurement_rows:
            raise ValueError(f"No measurement rows left for {system} after filters {where}.")
        sample_rows = _read_csv_from_archive(archive, sample_member) if sample_member else []

    merged_rows: list[dict[str, str]]
    feature_columns: list[str]
    source_member = measurements_member if sample_member is None else f"{sample_member} + {measurements_member}"
    if sample_rows:
        sample_header = list(sample_rows[0].keys())
        measurement_header = list(measurement_rows[0].keys())
        shared = [column for column in sample_header if column in measurement_header]
        join_key = _join_key(shared)
        if join_key is None:
            raise ValueError(
                f"Could not infer a sample/measurement join key for {system}; shared columns are {shared!r}."
            )
        sample_map = {row[join_key]: row for row in sample_rows if row.get(join_key) is not None}
        merged_rows = []
        for row in measurement_rows:
            key = row.get(join_key)
            if key is None or key not in sample_map:
                continue
            merged_rows.append({**sample_map[key], **row})
        if not merged_rows:
            raise ValueError(f"Join on {join_key!r} produced no merged rows for {system}.")
        feature_columns = [
            column
            for column in sample_header
            if column != join_key and _normalized(column) not in METADATA_HINTS
        ]
    else:
        merged_rows = measurement_rows
        header = list(merged_rows[0].keys())
        context_columns = _guess_context_columns(header)
        label_columns = _guess_label_columns(header, merged_rows, exclude=set(context_columns))
        exclude = set(context_columns) | set(label_columns)
        feature_columns = [
            column
            for column in header
            if column not in exclude and _normalized(column) not in METADATA_HINTS
        ]

    merged_rows = _subsample_rows(merged_rows, max_rows=max_rows, row_seed=row_seed)
    header = list(merged_rows[0].keys())
    context_columns = _guess_context_columns(header)
    label_columns = _guess_label_columns(header, merged_rows, exclude=set(context_columns) | set(feature_columns))
    X, feature_names = _encode_features(merged_rows, feature_columns)
    raw_values = [tuple(row[column] for column in feature_columns) for row in merged_rows]
    return MeasuredTable(
        system=system,
        source_member=source_member,
        rows=merged_rows,
        feature_columns=feature_columns,
        context_columns=context_columns,
        label_columns=label_columns,
        X=X,
        feature_names=feature_names,
        raw_feature_values=raw_values,
    )


def load_lcbench_table(
    json_path: str | Path,
    *,
    datasets: list[str] | None = None,
    where: dict[str, str] | None = None,
    max_rows: int | None = None,
    row_seed: int = 0,
    runtime_tag: str = "time",
    runtime_mode: str = "last",
) -> MeasuredTable:
    """Load an LCBench JSON file as a workload-style measured table.

    The OpenML dataset name is exposed as `workload`, so downstream workload-
    sensitivity analyses can reuse the same generated-sampling protocol.
    Runtime is flattened into a scalar `time_total`, derived from the logged
    `runtime_tag` learning curve.
    """

    where = where or {}
    json_path = Path(json_path)
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    chosen = set(datasets or payload.keys())
    rows: list[dict[str, str]] = []
    feature_columns: list[str] | None = None

    def runtime_value(series: list[float]) -> float:
        arr = np.asarray(series, dtype=float)
        if arr.size == 0:
            raise ValueError("LCBench runtime trace is empty.")
        if runtime_mode == "last":
            return float(arr[-1])
        if runtime_mode == "sum":
            diffs = np.diff(arr, prepend=0.0)
            return float(np.sum(diffs))
        raise ValueError(f"Unsupported runtime_mode {runtime_mode!r}; use last or sum.")

    for dataset_name in sorted(chosen):
        if dataset_name not in payload:
            raise ValueError(f"Dataset {dataset_name!r} not found in {json_path}.")
        for config_id, record in payload[dataset_name].items():
            config = {key: str(value) for key, value in record["config"].items()}
            results = {key: str(value) for key, value in record["results"].items()}
            log = record["log"]
            if runtime_tag not in log:
                raise ValueError(f"Runtime tag {runtime_tag!r} missing for dataset {dataset_name!r}, config {config_id}.")
            row: dict[str, str] = {
                "workload": dataset_name,
                "config_id": str(config_id),
                "time_total": str(runtime_value(log[runtime_tag])),
                "epochs_recorded": str(len(log.get("epoch", []))),
            }
            row.update(config)
            row.update(results)
            rows.append(row)
            if feature_columns is None:
                feature_columns = list(config.keys())

    rows = _filter_rows(rows, where)
    if not rows:
        raise ValueError(f"No LCBench rows left after filters {where} and datasets {sorted(chosen)}.")
    rows = _subsample_rows(rows, max_rows=max_rows, row_seed=row_seed)
    feature_columns = feature_columns or []
    X, feature_names = _encode_features(rows, feature_columns)
    raw_values = [tuple(row[column] for column in feature_columns) for row in rows]
    header = list(rows[0].keys())
    context_columns = _guess_context_columns(header)
    label_columns = _guess_label_columns(header, rows, exclude=set(context_columns) | set(feature_columns))
    return MeasuredTable(
        system="lcbench",
        source_member=str(json_path),
        rows=rows,
        feature_columns=feature_columns,
        context_columns=context_columns,
        label_columns=label_columns,
        X=X,
        feature_names=feature_names,
        raw_feature_values=raw_values,
    )


def subset_measured_table(
    table: MeasuredTable,
    row_indices: list[int] | np.ndarray,
    *,
    analysis_name: str | None = None,
) -> MeasuredTable:
    indices = np.asarray(row_indices, dtype=int)
    rows = [table.rows[int(idx)] for idx in indices.tolist()]
    raw_values = [table.raw_feature_values[int(idx)] for idx in indices.tolist()]
    return MeasuredTable(
        system=table.system,
        source_member=table.source_member,
        rows=rows,
        feature_columns=table.feature_columns,
        context_columns=table.context_columns,
        label_columns=table.label_columns,
        X=table.X[indices],
        feature_names=table.feature_names,
        raw_feature_values=raw_values,
        analysis_name=analysis_name,
    )


def _column_values(table: MeasuredTable, column: str) -> np.ndarray:
    if column not in table.rows[0]:
        raise ValueError(f"Column {column!r} not available in {table.system}; labels are {table.label_columns}")
    return np.asarray([float(row[column]) for row in table.rows], dtype=float)


def oriented_cost(values: np.ndarray, orientation: str) -> np.ndarray:
    if orientation == "lower":
        cost = np.asarray(values, dtype=float)
    elif orientation == "inverse":
        cost = 1.0 / np.maximum(np.asarray(values, dtype=float), 1e-12)
    else:
        raise ValueError(f"Unsupported cost orientation {orientation!r}; use lower or inverse.")
    if np.any(~np.isfinite(cost)) or np.any(cost < 0):
        raise ValueError("Cost values must be finite and non-negative after orientation.")
    return cost


def _value_codes(raw_feature_values: list[tuple[str, ...]]) -> list[tuple[int, ...]]:
    if not raw_feature_values:
        return []
    n_features = len(raw_feature_values[0])
    maps: list[dict[str, int]] = []
    next_id = 0
    for col in range(n_features):
        mapping: dict[str, int] = {}
        for row in raw_feature_values:
            value = row[col]
            if value not in mapping:
                mapping[value] = next_id
                next_id += 1
        maps.append(mapping)
    return [tuple(maps[col][value] for col, value in enumerate(row)) for row in raw_feature_values]


def _balanced_sample(value_codes: list[tuple[int, ...]], n: int, rng: np.random.Generator) -> tuple[int, ...]:
    n_rows = len(value_codes)
    n_tokens = max(token for row in value_codes for token in row) + 1
    full_counts = np.zeros(n_tokens, dtype=float)
    for row in value_codes:
        full_counts[list(row)] += 1.0
    target = full_counts / n_rows * n
    selected_counts = np.zeros(n_tokens, dtype=float)
    remaining = set(range(n_rows))
    selected: list[int] = []
    while len(selected) < n:
        pool = list(remaining)
        if len(pool) > 512:
            pool = rng.choice(pool, size=512, replace=False).tolist()
        best_idx = None
        best_score = float("inf")
        for idx in pool:
            tokens = value_codes[idx]
            after = selected_counts[list(tokens)] + 1.0
            before = selected_counts[list(tokens)]
            score = float(np.sum((after - target[list(tokens)]) ** 2 - (before - target[list(tokens)]) ** 2))
            score += float(rng.random()) * 1e-9
            if score < best_score:
                best_score = score
                best_idx = idx
        assert best_idx is not None
        selected.append(best_idx)
        remaining.remove(best_idx)
        selected_counts[list(value_codes[best_idx])] += 1.0
    return tuple(sorted(selected))


def _diversity_sample(
    X: np.ndarray,
    n: int,
    rng: np.random.Generator,
    *,
    initial: list[int] | None = None,
    candidates: np.ndarray | None = None,
) -> tuple[int, ...]:
    n_rows = X.shape[0]
    candidate_set = set(range(n_rows) if candidates is None else (int(idx) for idx in candidates))
    selected = list(dict.fromkeys(int(idx) for idx in (initial or []) if int(idx) in candidate_set))
    for idx in selected:
        candidate_set.discard(idx)
    if not selected:
        first = int(rng.choice(list(candidate_set)))
        selected.append(first)
        candidate_set.remove(first)
    min_dist = np.full(n_rows, np.inf)
    for idx in selected:
        dist = np.sum((X - X[idx]) ** 2, axis=1)
        min_dist = np.minimum(min_dist, dist)
    while len(selected) < n and candidate_set:
        pool = np.asarray(list(candidate_set), dtype=int)
        if len(pool) > 4096:
            pool = rng.choice(pool, size=4096, replace=False)
        best = int(pool[int(np.argmax(min_dist[pool] + rng.random(len(pool)) * 1e-12))])
        selected.append(best)
        candidate_set.remove(best)
        dist = np.sum((X - X[best]) ** 2, axis=1)
        min_dist = np.minimum(min_dist, dist)
    return tuple(sorted(selected[:n]))


def _pair_sets(value_codes: list[tuple[int, ...]]) -> list[frozenset[tuple[int, int, int, int]]]:
    out: list[frozenset[tuple[int, int, int, int]]] = []
    if not value_codes:
        return out
    n_features = len(value_codes[0])
    for row in value_codes:
        pairs = set()
        for left in range(n_features):
            for right in range(left + 1, n_features):
                pairs.add((left, row[left], right, row[right]))
        out.append(frozenset(pairs))
    return out


def _pairwise_sample(pair_sets: list[frozenset[tuple[int, int, int, int]]], n: int, rng: np.random.Generator) -> tuple[int, ...]:
    remaining = set(range(len(pair_sets)))
    uncovered = set().union(*pair_sets)
    selected: list[int] = []
    while len(selected) < n and remaining:
        pool = list(remaining)
        if len(pool) > 4096:
            pool = rng.choice(pool, size=4096, replace=False).tolist()
        best_idx = None
        best_gain = -1
        for idx in pool:
            gain = len(pair_sets[idx] & uncovered)
            if gain > best_gain or (gain == best_gain and rng.random() < 0.5):
                best_gain = gain
                best_idx = idx
        assert best_idx is not None
        selected.append(best_idx)
        remaining.remove(best_idx)
        uncovered.difference_update(pair_sets[best_idx])
        if not uncovered:
            uncovered = set().union(*(pair_sets[idx] for idx in remaining)) if remaining else set()
    return tuple(sorted(selected))


def _pilot_cost_sample(X: np.ndarray, cost_values: np.ndarray, n: int, rng: np.random.Generator) -> tuple[int, ...]:
    pilot_n = min(max(4, int(ceil(0.20 * n))), max(1, n // 2))
    pilot = rng.choice(X.shape[0], size=pilot_n, replace=False).astype(int).tolist()
    if n <= pilot_n:
        return tuple(sorted(pilot[:n]))
    model = fit_ridge(X[pilot], cost_values[pilot], alpha=1.0, log_target=True)
    predicted_cost = predict(model, X)
    remaining = np.asarray([idx for idx in range(X.shape[0]) if idx not in set(pilot)], dtype=int)
    order = remaining[np.argsort(predicted_cost[remaining], kind="mergesort")]
    pool_size = min(len(order), max(128, (n - pilot_n) * 12))
    candidate_pool = order[:pool_size]
    return _diversity_sample(X, n, rng, initial=pilot, candidates=candidate_pool)


def generate_samples(
    *,
    X: np.ndarray,
    raw_feature_values: list[tuple[str, ...]],
    cost_values: np.ndarray,
    budgets: list[int],
    seeds: int,
    context: str,
    source_member: str,
    include_oracles: bool = True,
) -> list[GeneratedSample]:
    """Generate protocol samples for a cost-target scenario."""

    samples: list[GeneratedSample] = []
    value_codes = _value_codes(raw_feature_values)
    pair_sets = _pair_sets(value_codes)

    def add(strategy: str, n: int, run_id: int, indices: tuple[int, ...]) -> None:
        samples.append(
            GeneratedSample(
                ref=GeneratedSampleRef(
                    context=context,
                    run_id=run_id,
                    strategy=strategy,
                    level=f"n{n}",
                    zip_member=source_member,
                ),
                indices=indices,
            )
        )

    for n in budgets:
        for seed in range(seeds):
            rng = np.random.default_rng(seed)
            add("random", n, seed, tuple(sorted(rng.choice(X.shape[0], size=n, replace=False).astype(int).tolist())))
            add("balanced", n, seed, _balanced_sample(value_codes, n, rng))
            add("pilotCost", n, seed, _pilot_cost_sample(X, cost_values, n, rng))

        deterministic_rng = np.random.default_rng(0)
        add("diversity", n, 0, _diversity_sample(X, n, deterministic_rng))
        add("pairwise", n, 0, _pairwise_sample(pair_sets, n, deterministic_rng))

        if include_oracles:
            tie_break = np.random.default_rng(0).random(X.shape[0]) * 1e-12
            cheap = tuple(sorted(np.argsort(cost_values + tie_break, kind="mergesort")[:n].astype(int).tolist()))
            expensive = tuple(sorted(np.argsort(-(cost_values + tie_break), kind="mergesort")[:n].astype(int).tolist()))
            add("cheapOracle", n, 0, cheap)
            add("expensiveOracle", n, 0, expensive)
    return samples


def build_generated_dataset(
    table: MeasuredTable,
    *,
    target_property: str,
    cost_property: str,
    cost_orientation: str = "lower",
    budgets: list[int] | None = None,
    seeds: int = 30,
    include_oracles: bool = True,
    samples: list[GeneratedSample] | None = None,
) -> GeneratedDataset:
    target = _column_values(table, target_property)
    raw_cost = _column_values(table, cost_property)
    cost_values = oriented_cost(raw_cost, cost_orientation)
    analysis_name = table.analysis_name or table.system
    scenario = f"{analysis_name}__cost_{cost_property}__target_{target_property}"
    sample_budgets = budgets or budget_grid(len(table.rows))
    if samples is None:
        samples = generate_samples(
            X=table.X,
            raw_feature_values=table.raw_feature_values,
            cost_values=cost_values,
            budgets=sample_budgets,
            seeds=seeds,
            context=f"{analysis_name}__cost_{cost_property}",
            source_member=table.source_member,
            include_oracles=include_oracles,
        )
    return GeneratedDataset(
        context=scenario,
        effective_cost_context=f"{analysis_name}::{cost_property}",
        X=table.X,
        y=target,
        cost_values=cost_values,
        full_cost=float(np.sum(cost_values)),
        samples=samples,
        system=table.system,
        feature_names=table.feature_names,
        target_property=target_property,
        cost_property=cost_property,
        cost_orientation=cost_orientation,
        source_member=table.source_member,
        n_configurations=len(table.rows),
    )
