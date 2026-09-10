"""Load the FSE 2026 artifact's data/sampling directory layout."""

from __future__ import annotations

import csv
import re
from pathlib import Path

import numpy as np

from .archive_runs import RunDataset, Sample, SampleRef


SAMPLED_RE = re.compile(r"sampledConfigurations_(?P<strategy>.+)_(?P<level>[^/]+)\.csv$")


def _resolve_sampling_root(root: str | Path) -> Path:
    path = Path(root)
    candidates = [
        path / "data" / "sampling",
        path / "sampling",
        path,
    ]
    for candidate in candidates:
        if candidate.exists() and any(child.is_dir() for child in candidate.iterdir()):
            return candidate
    raise FileNotFoundError(f"Cannot find FSE data/sampling directory under {root}")


def _detect_delimiter(path: Path) -> str:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        header = handle.readline()
    return ";" if header.count(";") > header.count(",") else ","


def _read_dicts(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    delimiter = _detect_delimiter(path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header: {path}")
        return list(reader.fieldnames), [row for row in reader]


def _run_id(path: Path, context: str) -> int:
    try:
        return int(path.parent.name.rsplit("_", 1)[1])
    except (IndexError, ValueError) as exc:
        raise ValueError(f"Cannot parse run id from {path.parent.name!r} for {context}") from exc


def _coerce_matrix(config_keys: list[tuple[str, ...]]) -> np.ndarray:
    try:
        return np.array([[float(value) for value in key] for key in config_keys], dtype=float)
    except ValueError:
        columns = list(zip(*config_keys))
        encoded_columns = []
        for column in columns:
            mapping = {value: idx for idx, value in enumerate(sorted(set(column)))}
            encoded_columns.append([float(mapping[value]) for value in column])
        return np.array(list(zip(*encoded_columns)), dtype=float)


def load_fse_directory_dataset(
    root: str | Path,
    context: str,
    *,
    max_runs: int | None = 100,
    strategies: set[str] | None = None,
    levels: set[str] | None = None,
    performance_name: str = "Performance",
) -> RunDataset:
    """Load measurements and sample sets from the FSE artifact layout.

    ``root`` can be the extracted artifact root, ``data/``, or
    ``data/sampling/``. Sample files are expected under
    ``<root>/<context>/<context>_<run>/sampledConfigurations_*_<level>.csv``.
    """

    sampling_root = _resolve_sampling_root(root)
    context_dir = sampling_root / context
    measurements_path = context_dir / "measurements.csv"
    if not measurements_path.exists():
        raise FileNotFoundError(f"Missing measurements file: {measurements_path}")

    sample_paths: list[tuple[Path, str, str, int]] = []
    for path in sorted(context_dir.glob(f"{context}_*/sampledConfigurations_*_*.csv")):
        match = SAMPLED_RE.fullmatch(path.name)
        if match is None:
            continue
        strategy = match.group("strategy")
        level = match.group("level")
        run_id = _run_id(path, context)
        if max_runs is not None and run_id > max_runs:
            continue
        if strategies is not None and strategy not in strategies:
            continue
        if levels is not None and level not in levels:
            continue
        sample_paths.append((path, strategy, level, run_id))
    if not sample_paths:
        raise ValueError(f"No FSE sample files matched context={context!r}, levels={levels}, strategies={strategies}")

    first_fields, _ = _read_dicts(sample_paths[0][0])
    feature_names = list(first_fields)

    measurement_fields, measurement_rows = _read_dicts(measurements_path)
    if performance_name not in measurement_fields:
        raise ValueError(f"{performance_name!r} column missing in {measurements_path}")
    missing_features = [name for name in feature_names if name not in measurement_fields]
    if missing_features:
        raise ValueError(f"Measurement file is missing sample feature columns: {missing_features}")

    perf_by_key: dict[tuple[str, ...], float] = {}
    for row in measurement_rows:
        key = tuple(row[name].strip() for name in feature_names)
        perf_by_key[key] = float(row[performance_name])

    config_keys = sorted(perf_by_key)
    key_to_idx = {key: idx for idx, key in enumerate(config_keys)}
    samples: list[Sample] = []
    for path, strategy, level, run_id in sample_paths:
        fields, rows = _read_dicts(path)
        if fields != feature_names:
            raise ValueError(f"Inconsistent sample feature columns in {path}")
        indices = []
        for row in rows:
            key = tuple(row[name].strip() for name in feature_names)
            if key not in key_to_idx:
                raise ValueError(f"Sample configuration from {path} is absent from measurements.csv")
            indices.append(key_to_idx[key])
        samples.append(
            Sample(
                ref=SampleRef(
                    context=context,
                    run_id=run_id,
                    strategy=strategy,
                    level=level,
                    zip_member=str(path),
                ),
                indices=np.array(indices, dtype=int),
            )
        )

    return RunDataset(
        context=context,
        feature_names=feature_names,
        config_keys=config_keys,
        X=_coerce_matrix(config_keys),
        y=np.array([perf_by_key[key] for key in config_keys], dtype=float),
        samples=samples,
        performance_name=performance_name,
        cost_name=performance_name,
    )
