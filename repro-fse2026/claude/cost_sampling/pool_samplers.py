"""Pool-based subsampling strategies for the LinuxData experiment.

All samplers operate on a fixed measurement pool; they select indices into
that pool rather than synthesising new configurations.  Each sampler returns
an `np.ndarray` of distinct indices of length `n`.

The function signatures are kept narrow — all of them accept the pool size
plus whatever side-channel information they need (cost values, active-option
counts, the option matrix), and a `numpy.random.Generator`.  This keeps run
seeding centralised.
"""

from __future__ import annotations

from typing import Callable

import numpy as np


SamplerFn = Callable[..., np.ndarray]


STRATEGY_RANDOM = "random"
STRATEGY_BALANCED = "balanced"
STRATEGY_DIVERSITY = "diversity"
STRATEGY_UNCERTAINTY = "uncertainty"
STRATEGY_COVERAGE = "coverage"
STRATEGY_CHEAP = "cheapOracle"
STRATEGY_EXPENSIVE = "expensiveOracle"


def random_sample(n: int, *, pool_size: int, rng: np.random.Generator) -> np.ndarray:
    return rng.choice(pool_size, size=n, replace=False)


def balanced_sample(
    n: int,
    *,
    active_options: np.ndarray,
    rng: np.random.Generator,
    n_strata: int = 10,
) -> np.ndarray:
    """Stratified random by `active_options` decile.

    Configurations are partitioned into `n_strata` quantile strata of
    `active_options`.  Each stratum receives a share of `n` proportional to
    its population size; remainders are distributed by largest fractional
    part to keep the totals exact.
    """

    pool_size = len(active_options)
    if n > pool_size:
        raise ValueError(f"n={n} exceeds pool size {pool_size}")

    quantiles = np.linspace(0.0, 1.0, n_strata + 1)
    edges = np.quantile(active_options, quantiles)
    edges[0] = -np.inf
    edges[-1] = np.inf
    stratum_id = np.digitize(active_options, edges[1:-1], right=False)

    sizes = np.array([np.sum(stratum_id == s) for s in range(n_strata)], dtype=int)
    raw_share = sizes * (n / pool_size)
    base = np.floor(raw_share).astype(int)
    remainder = n - int(base.sum())
    if remainder > 0:
        order = np.argsort(-(raw_share - base))
        for k in order[:remainder]:
            base[k] += 1

    indices: list[np.ndarray] = []
    for s in range(n_strata):
        members = np.flatnonzero(stratum_id == s)
        take = min(base[s], len(members))
        if take == 0:
            continue
        indices.append(rng.choice(members, size=take, replace=False))
    selected = np.concatenate(indices) if indices else np.empty(0, dtype=int)
    if len(selected) < n:
        # Fallback if quantile ties starved a stratum.
        remaining = np.setdiff1d(np.arange(pool_size), selected, assume_unique=True)
        extra = rng.choice(remaining, size=n - len(selected), replace=False)
        selected = np.concatenate([selected, extra])
    return selected


def diversity_sample(
    n: int,
    *,
    X: np.ndarray,
    rng: np.random.Generator,
    candidate_size: int = 1024,
) -> np.ndarray:
    """Greedy farthest-first traversal under Hamming distance, with a
    candidate-batch trick to keep cost sublinear in the pool.

    The seed is drawn uniformly.  At each step a fresh batch of
    `candidate_size` candidates is sampled from the unselected pool, and the
    candidate that maximises minimum Hamming distance to the current
    selection is added.  Hamming distance between binary vectors `a` and `b`
    is `sum(a) + sum(b) - 2 * a @ b`; we track `popcount(selected_or)` and a
    running dot-product with each candidate batch instead of materialising a
    full distance matrix.
    """

    pool_size = X.shape[0]
    if n > pool_size:
        raise ValueError(f"n={n} exceeds pool size {pool_size}")

    selected = np.empty(n, dtype=np.int64)
    seed = int(rng.integers(0, pool_size))
    selected[0] = seed
    selected_set = {seed}

    selected_X = X[selected[:1]].astype(np.int32)
    row_popcount = X.sum(axis=1).astype(np.int32)

    for k in range(1, n):
        cand_count = min(candidate_size, pool_size - k)
        candidates = rng.choice(pool_size, size=cand_count * 2, replace=False)
        candidates = np.array([c for c in candidates if c not in selected_set][:cand_count], dtype=np.int64)
        if len(candidates) == 0:
            break
        cand_X = X[candidates].astype(np.int32)
        cand_pop = row_popcount[candidates]
        # min over already-selected of Hamming distance: keep the running
        # minimum by streaming over selected rows.
        # dist(c, s) = pop(c) + pop(s) - 2 * <c, s>
        sel_pop = row_popcount[selected[:k]]
        # (cand x k)
        dots = cand_X @ selected_X.T
        dist = cand_pop[:, None] + sel_pop[None, :] - 2 * dots
        min_dist = dist.min(axis=1)
        winner_local = int(np.argmax(min_dist))
        winner = int(candidates[winner_local])
        selected[k] = winner
        selected_set.add(winner)
        selected_X = np.vstack([selected_X, cand_X[winner_local : winner_local + 1]])

    return selected[: len(selected_set)]


def uncertainty_sample(
    n: int,
    *,
    X: np.ndarray,
    y: np.ndarray,
    rng: np.random.Generator,
    seed_fraction: float = 0.25,
    seed_min: int = 50,
    alpha: float = 1.0,
    log_target: bool = True,
    predict_chunk: int = 4096,
) -> np.ndarray:
    """Residual-driven active learning (a deployable, cost-blind strategy).

    1. Draw a uniform-random seed of size `max(seed_min, ceil(n * seed_fraction))`.
    2. Fit ridge / log-linear ridge on the seed.
    3. Predict on the rest of the pool.
    4. Add the top `n - seed_size` configurations by absolute relative residual.

    The strategy never reads `cost_values`; it operates on the same option
    matrix and target the runner uses for evaluation.  This is realistic:
    a practitioner running active learning sees their target's residuals,
    not its acquisition cost.
    """

    from .metrics import fit_ridge, predict

    pool_size = X.shape[0]
    if n > pool_size:
        raise ValueError(f"n={n} exceeds pool size {pool_size}")

    seed_size = max(seed_min, int(np.ceil(n * seed_fraction)))
    seed_size = min(seed_size, max(1, n - 1), pool_size - 1)
    seed_idx = rng.choice(pool_size, size=seed_size, replace=False)

    X_train = X[seed_idx].astype(np.float64, copy=False)
    model = fit_ridge(X_train, y[seed_idx], alpha=alpha, log_target=log_target)
    del X_train

    remaining_mask = np.ones(pool_size, dtype=bool)
    remaining_mask[seed_idx] = False
    remaining_idx = np.flatnonzero(remaining_mask)

    abs_resid = np.empty(len(remaining_idx), dtype=np.float64)
    for start in range(0, len(remaining_idx), predict_chunk):
        block = remaining_idx[start : start + predict_chunk]
        X_chunk = X[block].astype(np.float64, copy=False)
        y_pred = predict(model, X_chunk)
        y_true = y[block]
        denom = np.maximum(np.abs(y_true), 1e-12)
        abs_resid[start : start + len(block)] = np.abs(y_true - y_pred) / denom

    n_extra = n - seed_size
    if n_extra <= 0:
        return seed_idx[:n]
    if n_extra >= len(remaining_idx):
        return np.concatenate([seed_idx, remaining_idx])
    top_extra_local = np.argpartition(-abs_resid, n_extra - 1)[:n_extra]
    top_extra = remaining_idx[top_extra_local]
    return np.concatenate([seed_idx, top_extra])


def coverage_sample(
    n: int,
    *,
    X: np.ndarray,
    rng: np.random.Generator,
    candidate_size: int = 512,
) -> np.ndarray:
    """Greedy option-frequency matching (pool-based marginal coverage).

    Targets the per-option enabled-frequency of the full pool.  At each step
    a fresh batch of `candidate_size` candidates is drawn from the unselected
    pool, and the candidate whose addition minimises the L1 distance between
    `selected_frequency_per_option` and `pool_frequency_per_option` is kept.

    Mimics what a 1-wise / marginal-coverage sampler would aim for *on the
    pool* without requiring a feature model.  Tests whether option-coverage-
    seeking pulls toward big or small kernels.
    """

    pool_size, n_features = X.shape
    if n > pool_size:
        raise ValueError(f"n={n} exceeds pool size {pool_size}")

    target_freq = X.mean(axis=0).astype(np.float64)
    selected_sum = np.zeros(n_features, dtype=np.float64)
    selected = np.empty(n, dtype=np.int64)
    selected_set: set[int] = set()

    seed = int(rng.integers(0, pool_size))
    selected[0] = seed
    selected_set.add(seed)
    selected_sum += X[seed].astype(np.float64)

    for k in range(1, n):
        cand_count = min(candidate_size, pool_size - k)
        candidates = rng.choice(pool_size, size=cand_count * 2, replace=False)
        candidates = np.array(
            [c for c in candidates if c not in selected_set][:cand_count],
            dtype=np.int64,
        )
        if len(candidates) == 0:
            break
        cand_X = X[candidates].astype(np.float64, copy=False)
        new_sums = selected_sum[None, :] + cand_X
        new_freq = new_sums / (k + 1)
        l1 = np.abs(new_freq - target_freq[None, :]).sum(axis=1)
        winner_local = int(np.argmin(l1))
        winner = int(candidates[winner_local])
        selected[k] = winner
        selected_set.add(winner)
        selected_sum += cand_X[winner_local]

    return selected[: len(selected_set)]


def cheap_oracle_sample(n: int, *, cost_values: np.ndarray) -> np.ndarray:
    return np.argsort(cost_values, kind="mergesort")[:n]


def expensive_oracle_sample(n: int, *, cost_values: np.ndarray) -> np.ndarray:
    order = np.argsort(cost_values, kind="mergesort")
    return order[-n:][::-1]
