"""Statistical Recursive Search sampling.

This is a code-native adaptation of the FSE 2026 artifact's
``SRS-sampling.ipynb``. The artifact uses a recursive pandas implementation
with a step size of 25, Welch's t-test at p < 0.05, and a final random fill to
reach the requested sample size. This module keeps those defaults and returns
indices into an in-memory configuration table.
"""

from __future__ import annotations

import math
from typing import Literal

import numpy as np


Extreme = Literal["max", "min"]


def _welch_pvalue(a: np.ndarray, b: np.ndarray) -> float:
    """Two-sided Welch t-test p-value.

    SciPy is used when available, matching the notebook. The fallback uses a
    normal approximation so the sampler remains usable in the repo's
    no-scipy-by-default environment.
    """

    if a.size < 2 or b.size < 2:
        return 1.0
    try:
        from scipy.stats import ttest_ind

        result = ttest_ind(a, b, equal_var=False, nan_policy="omit")
        pvalue = float(result.pvalue)
        return pvalue if math.isfinite(pvalue) else 1.0
    except Exception:
        var_a = float(np.var(a, ddof=1))
        var_b = float(np.var(b, ddof=1))
        se = math.sqrt(var_a / a.size + var_b / b.size)
        if se <= 0.0:
            return 1.0
        z = abs(float(np.mean(a) - np.mean(b))) / se
        return float(math.erfc(z / math.sqrt(2.0)))


def _draw(pool: np.ndarray, size: int, rng: np.random.Generator) -> np.ndarray:
    if size <= 0 or pool.size == 0:
        return np.array([], dtype=int)
    if pool.size <= size:
        return np.array(pool, dtype=int, copy=True)
    return np.array(rng.choice(pool, size=size, replace=False), dtype=int)


def srs_indices(
    X: np.ndarray,
    y: np.ndarray,
    sample_size: int,
    *,
    rng: np.random.Generator | int | None = None,
    step_sample_size: int = 25,
    p_threshold: float = 0.05,
    extreme: Extreme = "max",
) -> np.ndarray:
    """Return SRS-selected row indices.

    The sampler repeatedly draws a small random batch from the current
    decision-restricted space, identifies common decisions among the two best
    configurations, keeps decisions whose enabled/disabled performance differs
    significantly, and recurses. If recursion stops before ``sample_size``, the
    remaining budget is filled with random configurations, matching the FSE
    paper footnote.
    """

    X = np.asarray(X)
    y = np.asarray(y, dtype=float)
    if X.ndim != 2:
        raise ValueError("X must be a 2D configuration matrix")
    if y.ndim != 1 or y.size != X.shape[0]:
        raise ValueError("y must be a 1D vector aligned with X")
    if sample_size <= 0:
        raise ValueError("sample_size must be positive")
    if step_sample_size <= 0:
        raise ValueError("step_sample_size must be positive")
    if extreme not in {"max", "min"}:
        raise ValueError("extreme must be 'max' or 'min'")

    generator = np.random.default_rng(rng)
    target_size = min(int(sample_size), X.shape[0])
    available = np.arange(X.shape[0], dtype=int)
    selected: list[int] = []
    decisions: list[tuple[int, float]] = []

    while len(selected) < target_size and available.size > 0:
        filtered = available
        for feature, value in decisions:
            filtered = filtered[X[filtered, feature] == value]
        if filtered.size == 0:
            break

        draw_size = min(step_sample_size, target_size - len(selected))
        new_indices = _draw(filtered, draw_size, generator)
        if new_indices.size == 0:
            break
        selected.extend(int(idx) for idx in new_indices)
        selected_set = set(new_indices.tolist())
        available = np.array([idx for idx in available if idx not in selected_set], dtype=int)

        if new_indices.size < 2:
            break

        order = np.argsort(y[new_indices], kind="mergesort")
        if extreme == "max":
            order = order[::-1]
        best = int(new_indices[order[0]])
        second = int(new_indices[order[1]])
        common_features = np.flatnonzero(X[best] == X[second])
        decided_features = {feature for feature, _ in decisions}

        noteworthy: list[tuple[int, float]] = []
        for feature in common_features:
            feature_int = int(feature)
            if feature_int in decided_features:
                continue
            value = X[best, feature_int]
            enabled = new_indices[X[new_indices, feature_int] == value]
            disabled = new_indices[X[new_indices, feature_int] != value]
            if enabled.size == 0 or disabled.size == 0:
                continue
            enabled_perf = y[enabled]
            disabled_perf = y[disabled]
            if float(np.mean(enabled_perf)) == float(np.mean(disabled_perf)):
                continue
            if _welch_pvalue(enabled_perf, disabled_perf) < p_threshold:
                noteworthy.append((feature_int, float(value)))

        if noteworthy:
            decisions.extend(noteworthy)
            continue
        break

    if len(selected) < target_size and available.size > 0:
        fill = _draw(available, target_size - len(selected), generator)
        selected.extend(int(idx) for idx in fill)

    return np.array(selected[:target_size], dtype=int)
