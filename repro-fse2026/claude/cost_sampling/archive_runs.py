"""Load sampling runs from the ICPE-style zip archives.

The raw artifacts store each sampled training set as a semicolon-separated CSV
inside a zip archive.  This module keeps the loader zip-native so proof-of-
concept runs do not need to unpack hundreds of thousands of files.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
import csv
import io
from pathlib import PurePosixPath
import re
from typing import Iterable
import zipfile

import numpy as np


SAMPLED_RE = re.compile(r"sampledConfigurations_(?P<strategy>.+)_(?P<level>t\d+)\.csv$")


@dataclass(frozen=True)
class SampleRef:
    context: str
    run_id: int
    strategy: str
    level: str
    zip_member: str


@dataclass(frozen=True)
class Sample:
    ref: SampleRef
    indices: np.ndarray


@dataclass(frozen=True)
class RunDataset:
    context: str
    feature_names: list[str]
    config_keys: list[tuple[str, ...]]
    X: np.ndarray
    y: np.ndarray
    samples: list[Sample]
    cost: np.ndarray | None = None
    performance_name: str = "Performance"
    cost_name: str = "Performance"
    cost_context: str | None = None

    @property
    def full_cost(self) -> float:
        return float(np.sum(self.cost_values))

    @property
    def cost_values(self) -> np.ndarray:
        return self.y if self.cost is None else self.cost

    @property
    def effective_cost_context(self) -> str:
        return self.context if self.cost_context is None else self.cost_context


def _run_id_from_member(member: str) -> int:
    parts = PurePosixPath(member).parts
    if len(parts) < 3:
        raise ValueError(f"Cannot parse run id from malformed zip member: {member}")
    run_dir = parts[2]
    try:
        return int(run_dir.rsplit("_", 1)[1])
    except (IndexError, ValueError) as exc:
        raise ValueError(f"Cannot parse run id from directory name: {run_dir}") from exc


def _sample_ref(context: str, member: str) -> SampleRef | None:
    match = SAMPLED_RE.fullmatch(PurePosixPath(member).name)
    if not match:
        return None
    return SampleRef(
        context=context,
        run_id=_run_id_from_member(member),
        strategy=match.group("strategy"),
        level=match.group("level"),
        zip_member=member,
    )


def _sample_members(
    archive: zipfile.ZipFile,
    context: str,
    max_runs: int | None,
    strategies: set[str] | None,
    levels: set[str] | None,
) -> list[SampleRef]:
    prefixes = [f"AllRuns/{context}/", f"NewRuns/{context}/"]
    available_prefixes = [
        prefix
        for prefix in prefixes
        if any(member.startswith(prefix) for member in archive.namelist())
    ]
    if not available_prefixes:
        available_prefixes = prefixes
    refs: list[SampleRef] = []
    for member in archive.namelist():
        if not any(member.startswith(prefix) for prefix in available_prefixes):
            continue
        ref = _sample_ref(context, member)
        if ref is None:
            continue
        if max_runs is not None and ref.run_id > max_runs:
            continue
        if strategies is not None and ref.strategy not in strategies:
            continue
        if levels is not None and ref.level not in levels:
            continue
        refs.append(ref)
    refs.sort(key=lambda ref: (ref.run_id, ref.strategy, ref.level, ref.zip_member))
    return refs


def _read_rows(archive: zipfile.ZipFile, member: str) -> tuple[list[str], list[dict[str, str]]]:
    with archive.open(member) as raw:
        text = io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")
        reader = csv.DictReader(text, delimiter=";")
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header: {member}")
        return list(reader.fieldnames), [row for row in reader]


def load_runs_dataset(
    runs_zip: str,
    context: str,
    *,
    max_runs: int | None = None,
    strategies: Iterable[str] | None = None,
    levels: Iterable[str] | None = None,
    performance_name: str = "Performance",
) -> RunDataset:
    """Load sampled runs and reconstruct the measured configuration table.

    The full table is reconstructed by unioning sampled configurations.  For
    the x264 proof-of-concept contexts this covers all 1,152 configurations.
    """

    strategy_set = set(strategies) if strategies is not None else None
    level_set = set(levels) if levels is not None else None
    perf_by_key: dict[tuple[str, ...], float] = {}
    sample_keys: list[tuple[SampleRef, list[tuple[str, ...]]]] = []
    feature_names: list[str] | None = None

    with zipfile.ZipFile(runs_zip) as archive:
        refs = _sample_members(archive, context, max_runs, strategy_set, level_set)
        if not refs:
            raise ValueError(f"No sampled configuration CSVs found for context {context!r}")

        for ref in refs:
            fieldnames, rows = _read_rows(archive, ref.zip_member)
            if performance_name not in fieldnames:
                raise ValueError(f"{performance_name!r} column missing in {ref.zip_member}")
            current_features = [name for name in fieldnames if name != performance_name]
            if feature_names is None:
                feature_names = current_features
            elif feature_names != current_features:
                raise ValueError(f"Inconsistent feature columns in {ref.zip_member}")

            keys: list[tuple[str, ...]] = []
            for row in rows:
                key = tuple(row[name].strip() for name in current_features)
                value = float(row[performance_name])
                previous = perf_by_key.get(key)
                if previous is not None and abs(previous - value) > 1e-9:
                    raise ValueError(
                        "Conflicting performance value for configuration "
                        f"in {ref.zip_member}: {previous} != {value}"
                    )
                perf_by_key[key] = value
                keys.append(key)
            sample_keys.append((ref, keys))

    assert feature_names is not None
    config_keys = sorted(perf_by_key)
    key_to_idx = {key: idx for idx, key in enumerate(config_keys)}
    X = np.array([[float(value) for value in key] for key in config_keys], dtype=float)
    y = np.array([perf_by_key[key] for key in config_keys], dtype=float)
    samples = [
        Sample(ref=ref, indices=np.array([key_to_idx[key] for key in keys], dtype=int))
        for ref, keys in sample_keys
    ]

    return RunDataset(
        context=context,
        feature_names=feature_names,
        config_keys=config_keys,
        X=X,
        y=y,
        samples=samples,
        performance_name=performance_name,
        cost_name=performance_name,
    )


def attach_cost_dataset(target: RunDataset, cost: RunDataset, *, cost_name: str | None = None) -> RunDataset:
    """Return a target dataset with cost values aligned by configuration key."""

    if target.feature_names != cost.feature_names:
        raise ValueError(
            f"Cannot align costs: feature columns differ between {target.context} and {cost.context}"
        )

    cost_by_key = {key: value for key, value in zip(cost.config_keys, cost.y)}
    missing = [key for key in target.config_keys if key not in cost_by_key]
    if missing:
        raise ValueError(
            f"Cannot align costs: {len(missing)} configurations in {target.context} "
            f"are missing from {cost.context}"
        )

    aligned = np.array([cost_by_key[key] for key in target.config_keys], dtype=float)
    return replace(
        target,
        cost=aligned,
        cost_name=cost_name or cost.performance_name,
        cost_context=cost.context,
    )


def load_summary_configuration_count(summary_zip: str, context: str) -> int | None:
    member = f"AllSummary/{context}/allConfigurations.csv"
    try:
        with zipfile.ZipFile(summary_zip) as archive:
            with archive.open(member) as raw:
                text = io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")
                reader = csv.reader(text, delimiter=";")
                next(reader, None)
                return sum(1 for _ in reader)
    except (KeyError, FileNotFoundError):
        return None
