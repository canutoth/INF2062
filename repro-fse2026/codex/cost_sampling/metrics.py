"""Small numerical helpers without scipy/sklearn dependencies."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np


@dataclass(frozen=True)
class RidgeModel:
    beta: np.ndarray
    log_target: bool


@dataclass(frozen=True)
class CartNode:
    value: float
    feature: int | None = None
    threshold: float = 0.0
    left: "CartNode | None" = None
    right: "CartNode | None" = None


@dataclass(frozen=True)
class CartModel:
    root: CartNode
    log_target: bool


@dataclass(frozen=True)
class ForestModel:
    trees: tuple[CartModel, ...]
    log_target: bool


@dataclass(frozen=True)
class GradientBoostedTreesModel:
    init: float
    trees: tuple[CartModel, ...]
    learning_rate: float
    log_target: bool


@dataclass(frozen=True)
class SklearnModel:
    estimator: object
    log_target: bool


LearnerName = Literal[
    "ridge-log",
    "ridge-raw",
    "cart-log",
    "cart-raw",
    "rf-log",
    "rf-raw",
    "gbt-log",
    "gbt-raw",
    "sk-rf-log",
    "sk-rf-raw",
    "sk-hgbt-log",
    "sk-hgbt-raw",
    "sk-gbrt-log",
    "sk-gbrt-raw",
]
LEARNER_CHOICES: tuple[str, ...] = (
    "ridge-log",
    "ridge-raw",
    "cart-log",
    "cart-raw",
    "rf-log",
    "rf-raw",
    "gbt-log",
    "gbt-raw",
    "sk-rf-log",
    "sk-rf-raw",
    "sk-hgbt-log",
    "sk-hgbt-raw",
    "sk-gbrt-log",
    "sk-gbrt-raw",
)
Model = RidgeModel | CartModel | ForestModel | GradientBoostedTreesModel | SklearnModel


def fit_ridge(X: np.ndarray, y: np.ndarray, *, alpha: float = 1.0, log_target: bool = True) -> RidgeModel:
    if log_target and np.any(y <= 0):
        log_target = False
    target = np.log(y) if log_target else y
    Xf = np.asarray(X, dtype=float)
    x_mean = np.mean(Xf, axis=0)
    y_mean = float(np.mean(target))
    centered_y = target - y_mean

    if Xf.shape[1] > Xf.shape[0]:
        centered_X = Xf - x_mean
        gram = centered_X @ centered_X.T
        gram.flat[:: gram.shape[0] + 1] += alpha
        dual = np.linalg.solve(gram, centered_y)
        coef = centered_X.T @ dual
    else:
        centered_X = Xf - x_mean
        penalty = np.eye(centered_X.shape[1]) * alpha
        coef = np.linalg.solve(centered_X.T @ centered_X + penalty, centered_X.T @ centered_y)

    intercept = y_mean - float(x_mean @ coef)
    beta = np.concatenate([[intercept], coef])
    return RidgeModel(beta=beta, log_target=log_target)


def _sse(values: np.ndarray) -> float:
    if len(values) == 0:
        return 0.0
    centered = values - float(np.mean(values))
    return float(centered @ centered)


def _best_cart_split(
    X: np.ndarray,
    y: np.ndarray,
    *,
    min_samples_leaf: int,
    feature_indices: np.ndarray | None = None,
    max_thresholds: int | None = None,
) -> tuple[int, float, float] | None:
    parent_sse = _sse(y)
    best: tuple[int, float, float] | None = None
    n_samples, n_features = X.shape
    features = np.arange(n_features) if feature_indices is None else feature_indices
    for feature in features:
        values = X[:, feature]
        unique = np.unique(values)
        if len(unique) <= 1:
            continue
        if max_thresholds is not None and len(unique) - 1 > max_thresholds:
            quantiles = np.linspace(0.0, 1.0, max_thresholds + 2)[1:-1]
            thresholds = np.unique(np.quantile(unique, quantiles))
        else:
            thresholds = (unique[:-1] + unique[1:]) / 2.0
        for threshold in thresholds:
            left = values <= threshold
            left_n = int(np.sum(left))
            right_n = n_samples - left_n
            if left_n < min_samples_leaf or right_n < min_samples_leaf:
                continue
            gain = parent_sse - _sse(y[left]) - _sse(y[~left])
            if best is None or gain > best[2]:
                best = (feature, float(threshold), float(gain))
    if best is None or best[2] <= 1e-12:
        return None
    return best


def _build_cart(
    X: np.ndarray,
    y: np.ndarray,
    *,
    depth: int,
    max_depth: int,
    min_samples_leaf: int,
    rng: np.random.Generator | None = None,
    max_features: int | None = None,
    max_thresholds: int | None = None,
) -> CartNode:
    value = float(np.mean(y))
    if depth >= max_depth or len(y) < 2 * min_samples_leaf:
        return CartNode(value=value)
    feature_indices = None
    if rng is not None and max_features is not None and 0 < max_features < X.shape[1]:
        feature_indices = np.sort(rng.choice(X.shape[1], size=max_features, replace=False))
    split = _best_cart_split(
        X,
        y,
        min_samples_leaf=min_samples_leaf,
        feature_indices=feature_indices,
        max_thresholds=max_thresholds,
    )
    if split is None:
        return CartNode(value=value)
    feature, threshold, _gain = split
    left_mask = X[:, feature] <= threshold
    return CartNode(
        value=value,
        feature=feature,
        threshold=threshold,
        left=_build_cart(
            X[left_mask],
            y[left_mask],
            depth=depth + 1,
            max_depth=max_depth,
            min_samples_leaf=min_samples_leaf,
            rng=rng,
            max_features=max_features,
            max_thresholds=max_thresholds,
        ),
        right=_build_cart(
            X[~left_mask],
            y[~left_mask],
            depth=depth + 1,
            max_depth=max_depth,
            min_samples_leaf=min_samples_leaf,
            rng=rng,
            max_features=max_features,
            max_thresholds=max_thresholds,
        ),
    )


def fit_cart(
    X: np.ndarray,
    y: np.ndarray,
    *,
    log_target: bool = True,
    max_depth: int = 6,
    min_samples_leaf: int = 3,
    rng: np.random.Generator | None = None,
    max_features: int | None = None,
    max_thresholds: int | None = None,
) -> CartModel:
    if log_target and np.any(y <= 0):
        log_target = False
    target = np.log(y) if log_target else y
    leaf = max(1, min(min_samples_leaf, max(1, len(target) // 2)))
    root = _build_cart(
        X,
        target,
        depth=0,
        max_depth=max_depth,
        min_samples_leaf=leaf,
        rng=rng,
        max_features=max_features,
        max_thresholds=max_thresholds,
    )
    return CartModel(root=root, log_target=log_target)


def _target_for_tree(y: np.ndarray, log_target: bool) -> tuple[np.ndarray, bool]:
    if log_target and np.any(y <= 0):
        log_target = False
    return (np.log(y) if log_target else y), log_target


def fit_random_forest(
    X: np.ndarray,
    y: np.ndarray,
    *,
    log_target: bool = True,
    n_estimators: int = 16,
    max_depth: int = 7,
    min_samples_leaf: int = 2,
    random_state: int = 1729,
) -> ForestModel:
    target, effective_log = _target_for_tree(y, log_target)
    rng = np.random.default_rng(random_state)
    n_samples, n_features = X.shape
    max_features = max(1, int(np.sqrt(max(n_features, 1))))
    leaf = max(1, min(min_samples_leaf, max(1, n_samples // 2)))
    trees: list[CartModel] = []
    for _ in range(n_estimators):
        sample_idx = rng.choice(n_samples, size=n_samples, replace=True)
        tree = fit_cart(
            X[sample_idx],
            target[sample_idx],
            log_target=False,
            max_depth=max_depth,
            min_samples_leaf=leaf,
            rng=rng,
            max_features=max_features,
            max_thresholds=32,
        )
        trees.append(tree)
    return ForestModel(trees=tuple(trees), log_target=effective_log)


def fit_gradient_boosted_trees(
    X: np.ndarray,
    y: np.ndarray,
    *,
    log_target: bool = True,
    n_estimators: int = 24,
    learning_rate: float = 0.08,
    max_depth: int = 3,
    min_samples_leaf: int = 2,
    random_state: int = 4242,
) -> GradientBoostedTreesModel:
    target, effective_log = _target_for_tree(y, log_target)
    rng = np.random.default_rng(random_state)
    prediction = np.full_like(target, float(np.mean(target)), dtype=float)
    init = float(prediction[0])
    leaf = max(1, min(min_samples_leaf, max(1, len(target) // 2)))
    trees: list[CartModel] = []
    max_features = max(1, int(np.sqrt(max(X.shape[1], 1))))
    for _ in range(n_estimators):
        residual = target - prediction
        tree = fit_cart(
            X,
            residual,
            log_target=False,
            max_depth=max_depth,
            min_samples_leaf=leaf,
            rng=rng,
            max_features=max_features,
            max_thresholds=32,
        )
        update = _predict_cart(tree, X)
        prediction = prediction + learning_rate * update
        trees.append(tree)
    return GradientBoostedTreesModel(
        init=init,
        trees=tuple(trees),
        learning_rate=learning_rate,
        log_target=effective_log,
    )


def fit_sklearn_learner(
    X: np.ndarray,
    y: np.ndarray,
    *,
    learner: LearnerName,
) -> SklearnModel:
    if learner.endswith("-log") and np.any(y <= 0):
        log_target = False
    else:
        log_target = learner.endswith("-log")
    target = np.log(y) if log_target else y

    if learner.startswith("sk-rf-"):
        from sklearn.ensemble import RandomForestRegressor

        estimator = RandomForestRegressor(
            n_estimators=200,
            max_depth=None,
            min_samples_leaf=1,
            max_features="sqrt",
            bootstrap=True,
            n_jobs=-1,
            random_state=1729,
        )
    elif learner.startswith("sk-hgbt-"):
        from sklearn.ensemble import HistGradientBoostingRegressor

        estimator = HistGradientBoostingRegressor(
            max_iter=300,
            learning_rate=0.08,
            max_leaf_nodes=31,
            l2_regularization=0.0,
            random_state=4242,
        )
    elif learner.startswith("sk-gbrt-"):
        from sklearn.ensemble import GradientBoostingRegressor

        estimator = GradientBoostingRegressor(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=5,
            min_samples_leaf=2,
            subsample=0.8,
            max_features="sqrt",
            random_state=4242,
        )
    else:
        raise ValueError(f"Unsupported sklearn learner {learner!r}")

    estimator.fit(X, target)
    return SklearnModel(estimator=estimator, log_target=log_target)


def fit_learner(
    X: np.ndarray,
    y: np.ndarray,
    *,
    learner: LearnerName = "ridge-log",
    alpha: float = 1.0,
) -> Model:
    if learner == "ridge-log":
        return fit_ridge(X, y, alpha=alpha, log_target=True)
    if learner == "ridge-raw":
        return fit_ridge(X, y, alpha=alpha, log_target=False)
    if learner == "cart-log":
        return fit_cart(X, y, log_target=True)
    if learner == "cart-raw":
        return fit_cart(X, y, log_target=False)
    if learner == "rf-log":
        return fit_random_forest(X, y, log_target=True)
    if learner == "rf-raw":
        return fit_random_forest(X, y, log_target=False)
    if learner == "gbt-log":
        return fit_gradient_boosted_trees(X, y, log_target=True)
    if learner == "gbt-raw":
        return fit_gradient_boosted_trees(X, y, log_target=False)
    if learner.startswith("sk-"):
        return fit_sklearn_learner(X, y, learner=learner)
    raise ValueError(f"Unsupported learner {learner!r}")


def _predict_cart_node(node: CartNode, x: np.ndarray) -> float:
    if node.feature is None or node.left is None or node.right is None:
        return node.value
    if x[node.feature] <= node.threshold:
        return _predict_cart_node(node.left, x)
    return _predict_cart_node(node.right, x)


def _predict_cart(model: CartModel, X: np.ndarray) -> np.ndarray:
    raw = np.asarray([_predict_cart_node(model.root, row) for row in X], dtype=float)
    if model.log_target:
        return np.exp(np.clip(raw, -700, 700))
    return raw


def predict(model: Model, X: np.ndarray) -> np.ndarray:
    if isinstance(model, SklearnModel):
        raw = np.asarray(model.estimator.predict(X), dtype=float)
        if model.log_target:
            return np.maximum(np.exp(np.clip(raw, -700, 700)), 1e-12)
        return np.maximum(raw, 1e-12)

    if isinstance(model, CartModel):
        raw = _predict_cart(model, X)
        if model.log_target:
            return np.maximum(raw, 1e-12)
        return np.maximum(raw, 1e-12)

    if isinstance(model, ForestModel):
        tree_predictions = np.vstack([_predict_cart(tree, X) for tree in model.trees])
        raw = np.mean(tree_predictions, axis=0)
        if model.log_target:
            return np.exp(np.clip(raw, -700, 700))
        return np.maximum(raw, 1e-12)

    if isinstance(model, GradientBoostedTreesModel):
        raw = np.full(X.shape[0], model.init, dtype=float)
        for tree in model.trees:
            raw += model.learning_rate * _predict_cart(tree, X)
        if model.log_target:
            return np.exp(np.clip(raw, -700, 700))
        return np.maximum(raw, 1e-12)

    design = np.column_stack([np.ones(X.shape[0]), X])
    raw = design @ model.beta
    if model.log_target:
        return np.exp(np.clip(raw, -700, 700))
    return np.maximum(raw, 1e-12)


def mean_relative_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    denominator = np.maximum(np.abs(y_true), 1e-12)
    return float(np.mean(np.abs(y_true - y_pred) / denominator))


def iqr(values: np.ndarray) -> tuple[float, float]:
    return float(np.percentile(values, 25)), float(np.percentile(values, 75))


def rankdata(values: np.ndarray) -> np.ndarray:
    """Average ranks for ties, 1-based like scipy.stats.rankdata."""

    order = np.argsort(values, kind="mergesort")
    ranks = np.empty(len(values), dtype=float)
    sorted_values = values[order]
    start = 0
    while start < len(values):
        end = start + 1
        while end < len(values) and sorted_values[end] == sorted_values[start]:
            end += 1
        average_rank = (start + 1 + end) / 2.0
        ranks[order[start:end]] = average_rank
        start = end
    return ranks


def spearman(x: np.ndarray, y: np.ndarray) -> float:
    rx = rankdata(np.asarray(x, dtype=float))
    ry = rankdata(np.asarray(y, dtype=float))
    if np.std(rx) == 0 or np.std(ry) == 0:
        return float("nan")
    return float(np.corrcoef(rx, ry)[0, 1])


def kendall_tau_from_scores(a: np.ndarray, b: np.ndarray) -> float:
    concordant = 0
    discordant = 0
    n = len(a)
    for i in range(n):
        for j in range(i + 1, n):
            da = np.sign(a[i] - a[j])
            db = np.sign(b[i] - b[j])
            if da == 0 or db == 0:
                continue
            if da == db:
                concordant += 1
            else:
                discordant += 1
    total = concordant + discordant
    return float((concordant - discordant) / total) if total else float("nan")


def minmax(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    lo = float(np.min(values))
    hi = float(np.max(values))
    if hi == lo:
        return np.zeros_like(values)
    return (values - lo) / (hi - lo)


def pareto_mask(cost: np.ndarray, error: np.ndarray) -> np.ndarray:
    """Return True for non-dominated points in a minimization plane."""

    cost = np.asarray(cost, dtype=float)
    error = np.asarray(error, dtype=float)
    efficient = np.ones(len(cost), dtype=bool)
    for i in range(len(cost)):
        dominated = (
            (cost <= cost[i])
            & (error <= error[i])
            & ((cost < cost[i]) | (error < error[i]))
        )
        if np.any(dominated):
            efficient[i] = False
    return efficient
