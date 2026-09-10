"""Statistical hypothesis tests for the cost-sampling study.

This module operationalizes the H1a-H5c hypotheses from `4-study_design.tex`.
Each hypothesis test returns a dict with: hypothesis id, statistic name and
value, p-value (when applicable), effect size, qualitative effect label, and
verdict in {"supports", "refutes", "inconclusive"}.

All tests are pure-numpy/stdlib (no scipy dependency).
"""

from __future__ import annotations

from collections import defaultdict
import math
from typing import Any, Iterable, Sequence

import numpy as np

from .metrics import rankdata, spearman, pareto_mask

# --------------------------------------------------------------------------- #
# Statistical primitives                                                      #
# --------------------------------------------------------------------------- #


def _norm_sf(z: float) -> float:
    """Two-tailed survival is `2 * _norm_sf(abs(z))`; this returns one-tailed."""
    if not math.isfinite(z):
        return float("nan")
    return 0.5 * math.erfc(z / math.sqrt(2.0))


def _gser(a: float, x: float) -> float:
    if x <= 0.0:
        return 0.0
    eps = 1e-14
    summ = 1.0 / a
    term = summ
    ap = a
    for _ in range(2000):
        ap += 1.0
        term *= x / ap
        summ += term
        if abs(term) < abs(summ) * eps:
            break
    return summ * math.exp(-x + a * math.log(x) - math.lgamma(a))


def _gcf(a: float, x: float) -> float:
    eps = 1e-14
    fpmin = 1e-300
    b = x + 1.0 - a
    c = 1.0 / fpmin
    d = 1.0 / b
    h = d
    for i in range(1, 2000):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < fpmin:
            d = fpmin
        c = b + an / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return math.exp(-x + a * math.log(x) - math.lgamma(a)) * h


def _gammainc_q(a: float, x: float) -> float:
    if x < 0.0 or a <= 0.0:
        return float("nan")
    if x == 0.0:
        return 1.0
    if x < a + 1.0:
        return max(0.0, 1.0 - _gser(a, x))
    return _gcf(a, x)


def chi2_sf(x: float, df: int) -> float:
    """Survival function of chi-squared with `df` degrees of freedom."""
    if df <= 0 or not math.isfinite(x) or x < 0:
        return float("nan")
    return _gammainc_q(df / 2.0, x / 2.0)


def student_sf(t: float, df: float) -> float:
    """Two-tailed Student-t survival is `2 * student_sf(abs(t), df)`."""
    if df <= 0 or not math.isfinite(t):
        return float("nan")
    x = df / (df + t * t)
    # Regularized incomplete beta I_x(df/2, 1/2). For t-test SF we want
    # 0.5 * I_x(df/2, 1/2). Use continued fraction for I_x via betainc.
    return 0.5 * _betainc_regularized(df / 2.0, 0.5, x)


def _betainc_regularized(a: float, b: float, x: float) -> float:
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    bt = math.exp(
        math.lgamma(a + b)
        - math.lgamma(a)
        - math.lgamma(b)
        + a * math.log(x)
        + b * math.log(1.0 - x)
    )
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def _betacf(a: float, b: float, x: float) -> float:
    eps = 1e-14
    fpmin = 1e-300
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < fpmin:
        d = fpmin
    d = 1.0 / d
    h = d
    for m in range(1, 2000):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return h


# --------------------------------------------------------------------------- #
# Group-comparison tests                                                      #
# --------------------------------------------------------------------------- #


def kruskal_wallis(groups: Sequence[Sequence[float]]) -> dict[str, float]:
    """Kruskal-Wallis H test with tie correction; returns H, p, eta_squared."""
    arrays = [np.asarray(g, dtype=float) for g in groups if len(g) > 0]
    if len(arrays) < 2:
        return {"H": float("nan"), "p_value": float("nan"), "eta_squared": float("nan"), "k": len(arrays), "N": 0}
    sizes = np.array([len(a) for a in arrays], dtype=float)
    pooled = np.concatenate(arrays)
    N = float(pooled.size)
    if N < 3:
        return {"H": float("nan"), "p_value": float("nan"), "eta_squared": float("nan"), "k": len(arrays), "N": int(N)}
    ranks = rankdata(pooled)
    rank_groups: list[np.ndarray] = []
    start = 0
    for n in sizes.astype(int):
        rank_groups.append(ranks[start : start + n])
        start += n
    rank_sums = np.array([rg.sum() for rg in rank_groups], dtype=float)
    H = (12.0 / (N * (N + 1.0))) * np.sum(rank_sums ** 2 / sizes) - 3.0 * (N + 1.0)
    # Tie correction.
    _, counts = np.unique(pooled, return_counts=True)
    tie_terms = counts[counts > 1]
    if tie_terms.size:
        T = 1.0 - float(np.sum(tie_terms ** 3 - tie_terms)) / (N ** 3 - N)
        if T > 0:
            H = H / T
    k = len(arrays)
    df = k - 1
    p = chi2_sf(float(H), df)
    eta_sq = max(0.0, (H - df) / (N - k)) if (N - k) > 0 else float("nan")
    return {"H": float(H), "p_value": float(p), "eta_squared": float(eta_sq), "k": k, "N": int(N)}


def mann_whitney_u(x: Sequence[float], y: Sequence[float]) -> dict[str, float]:
    """Two-sided MWU with tie correction and Vargha-Delaney A12."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n1, n2 = len(x), len(y)
    if n1 == 0 or n2 == 0:
        return {"U": float("nan"), "p_value": float("nan"), "A12": float("nan"), "n1": n1, "n2": n2}
    pooled = np.concatenate([x, y])
    ranks = rankdata(pooled)
    R1 = float(ranks[:n1].sum())
    U1 = R1 - n1 * (n1 + 1) / 2.0
    U2 = n1 * n2 - U1
    U = min(U1, U2)
    A12 = U1 / (n1 * n2)
    mu = n1 * n2 / 2.0
    N = n1 + n2
    _, counts = np.unique(pooled, return_counts=True)
    tie_terms = counts[counts > 1]
    if tie_terms.size and N > 1:
        T = float(np.sum(tie_terms ** 3 - tie_terms))
        sigma2 = (n1 * n2 / 12.0) * ((N + 1) - T / (N * (N - 1)))
    else:
        sigma2 = (n1 * n2 * (N + 1)) / 12.0
    if sigma2 <= 0:
        return {"U": float(U), "p_value": float("nan"), "A12": float(A12), "n1": n1, "n2": n2}
    z = (U - mu) / math.sqrt(sigma2)
    if z != 0:
        z = (abs(z) - 0.5) * (1.0 if z > 0 else -1.0)  # continuity correction
    p = 2.0 * _norm_sf(abs(float(z)))
    return {"U": float(U), "p_value": float(p), "A12": float(A12), "n1": n1, "n2": n2, "z": float(z)}


def vd_magnitude(a12: float) -> str:
    if not math.isfinite(a12):
        return "nan"
    delta = abs(a12 - 0.5)
    if delta < 0.06:
        return "negligible"
    if delta < 0.14:
        return "small"
    if delta < 0.21:
        return "medium"
    return "large"


def spearman_with_p(x: Sequence[float], y: Sequence[float]) -> dict[str, float]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = min(len(x), len(y))
    if n < 4:
        return {"rho": float("nan"), "p_value": float("nan"), "n": n}
    rho = spearman(x[:n], y[:n])
    if not math.isfinite(rho) or abs(rho) >= 1.0:
        return {"rho": float(rho), "p_value": 0.0 if abs(rho) >= 1.0 else float("nan"), "n": n}
    df = n - 2
    t = rho * math.sqrt(df / (1.0 - rho ** 2))
    p = 2.0 * student_sf(abs(t), df)
    return {"rho": float(rho), "p_value": float(p), "n": n, "t_stat": float(t)}


def bootstrap_median_ci(
    values: Sequence[float],
    *,
    n_boot: int = 2000,
    alpha: float = 0.05,
    seed: int = 0,
) -> dict[str, float]:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size < 3:
        return {"median": float("nan"), "ci_low": float("nan"), "ci_high": float("nan"), "n": arr.size}
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, arr.size, size=(n_boot, arr.size))
    medians = np.median(arr[idx], axis=1)
    lo, hi = np.percentile(medians, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return {
        "median": float(np.median(arr)),
        "ci_low": float(lo),
        "ci_high": float(hi),
        "n": int(arr.size),
    }


# --------------------------------------------------------------------------- #
# Hypothesis tests                                                            #
# --------------------------------------------------------------------------- #


_VERDICT_LABELS = ("supports", "refutes", "inconclusive")


def _row(
    *,
    hypothesis: str,
    scope: str,
    scope_value: str,
    statistic: str,
    statistic_value: float,
    p_value: float | None,
    effect: str,
    effect_value: float,
    effect_label: str,
    verdict: str,
    notes: str,
) -> dict[str, Any]:
    assert verdict in _VERDICT_LABELS, verdict
    return {
        "hypothesis": hypothesis,
        "scope": scope,
        "scope_value": scope_value,
        "statistic": statistic,
        "statistic_value": float(statistic_value) if statistic_value is not None else float("nan"),
        "p_value": float(p_value) if p_value is not None else float("nan"),
        "effect": effect,
        "effect_value": float(effect_value) if effect_value is not None else float("nan"),
        "effect_label": effect_label,
        "verdict": verdict,
        "notes": notes,
    }


def test_h1a_cost_heterogeneity(
    heterogeneity_row: dict[str, Any],
    *,
    cost_values: np.ndarray | None = None,
    scope_value: str,
) -> dict[str, Any]:
    """H1a: per-configuration cost CV is non-negligible.

    Verdict thresholds (from the paper's overhead classification, transposed
    onto CV/p90-p10): supports if CV >= 0.20 or p90/p10 >= 1.5; refutes if
    CV < 0.10 and p90/p10 < 1.25; inconclusive otherwise.
    """
    cv = float(heterogeneity_row.get("cv_cost", float("nan")))
    p90p10 = float(heterogeneity_row.get("p90_over_p10", float("nan")))
    ci_text = ""
    if cost_values is not None and len(cost_values) >= 10:
        rng = np.random.default_rng(0)
        idx = rng.integers(0, len(cost_values), size=(2000, len(cost_values)))
        sample = cost_values[idx]
        cvs = np.std(sample, axis=1, ddof=1) / np.mean(sample, axis=1)
        cv_lo, cv_hi = np.percentile(cvs, [2.5, 97.5])
        ci_text = f"; CV 95% CI [{cv_lo:.3g},{cv_hi:.3g}]"
    if cv >= 0.20 or p90p10 >= 1.5:
        verdict = "supports"
    elif cv < 0.10 and p90p10 < 1.25:
        verdict = "refutes"
    else:
        verdict = "inconclusive"
    if cv >= 1.0:
        label = "very large"
    elif cv >= 0.4:
        label = "large"
    elif cv >= 0.2:
        label = "moderate"
    elif cv >= 0.1:
        label = "small"
    else:
        label = "negligible"
    notes = f"CV={cv:.3g}; p90/p10={p90p10:.3g}{ci_text}"
    return _row(
        hypothesis="H1a",
        scope="system",
        scope_value=scope_value,
        statistic="cv_cost",
        statistic_value=cv,
        p_value=None,
        effect="p90_over_p10",
        effect_value=p90p10,
        effect_label=label,
        verdict=verdict,
        notes=notes,
    )


def test_h1b_strategy_effect(
    records: list[dict[str, Any]],
    *,
    scope_value: str,
) -> dict[str, Any]:
    """H1b: at fixed n, train_cost differs across strategies (Kruskal-Wallis per level)."""
    by_level: dict[str, list[list[float]]] = defaultdict(list)
    levels = sorted({r["level"] for r in records})
    strategies = sorted({r["strategy"] for r in records if r["strategy"] not in ("cheapOracle", "expensiveOracle")})
    for level in levels:
        groups = []
        for strategy in strategies:
            vals = [r["train_cost"] for r in records if r["level"] == level and r["strategy"] == strategy]
            if vals:
                groups.append(vals)
        if len(groups) >= 2:
            by_level[level] = groups
    if not by_level:
        return _row(
            hypothesis="H1b",
            scope="system",
            scope_value=scope_value,
            statistic="kruskal_wallis_min_p",
            statistic_value=float("nan"),
            p_value=float("nan"),
            effect="eta_squared_max",
            effect_value=float("nan"),
            effect_label="nan",
            verdict="inconclusive",
            notes="no level with >=2 strategies",
        )
    results = {level: kruskal_wallis(grps) for level, grps in by_level.items()}
    n_significant = sum(1 for r in results.values() if math.isfinite(r["p_value"]) and r["p_value"] < 0.05)
    min_p = min(r["p_value"] for r in results.values() if math.isfinite(r["p_value"]))
    max_eta = max(r["eta_squared"] for r in results.values() if math.isfinite(r["eta_squared"]))
    if max_eta >= 0.14:
        label = "large"
    elif max_eta >= 0.06:
        label = "medium"
    elif max_eta >= 0.01:
        label = "small"
    else:
        label = "negligible"
    if n_significant == len(results) and max_eta >= 0.06:
        verdict = "supports"
    elif n_significant >= 1 and max_eta >= 0.01:
        verdict = "supports"
    elif n_significant == 0 and max_eta < 0.01:
        verdict = "refutes"
    else:
        verdict = "inconclusive"
    notes = (
        f"K-W per level: {n_significant}/{len(results)} levels with p<0.05; "
        f"min p={min_p:.3g}; max eta^2={max_eta:.3g}"
    )
    return _row(
        hypothesis="H1b",
        scope="system",
        scope_value=scope_value,
        statistic="kruskal_wallis_min_p",
        statistic_value=min_p,
        p_value=min_p,
        effect="eta_squared_max",
        effect_value=max_eta,
        effect_label=label,
        verdict=verdict,
        notes=notes,
    )


def test_h2a_correlation(
    records: list[dict[str, Any]],
    *,
    scope_value: str,
) -> dict[str, Any]:
    """H2a: n is positively rank-correlated with TrainCost."""
    n_arr = np.array([r["n"] for r in records], dtype=float)
    cost_arr = np.array([r["train_cost"] for r in records], dtype=float)
    res = spearman_with_p(n_arr, cost_arr)
    rho = res["rho"]
    p = res["p_value"]
    if not math.isfinite(rho):
        verdict = "inconclusive"
        label = "nan"
    elif rho >= 0.7 and (not math.isfinite(p) or p < 0.05):
        verdict = "supports"
        label = "strong positive"
    elif rho >= 0.3 and p < 0.05:
        verdict = "supports"
        label = "moderate positive"
    elif rho > 0 and p < 0.05:
        verdict = "supports"
        label = "weak positive"
    elif rho <= 0 and p < 0.05:
        verdict = "refutes"
        label = "non-positive"
    else:
        verdict = "inconclusive"
        label = "no significant trend"
    notes = f"Spearman rho={rho:.3g} on n={res['n']} (records-level)"
    return _row(
        hypothesis="H2a",
        scope="system",
        scope_value=scope_value,
        statistic="spearman_rho",
        statistic_value=rho,
        p_value=p,
        effect="rho",
        effect_value=rho,
        effect_label=label,
        verdict=verdict,
        notes=notes,
    )


def test_h2b_calibration_offset(
    records: list[dict[str, Any]],
    *,
    scope_value: str,
) -> dict[str, Any]:
    """H2b: median calibration ratio differs from 1 (95% bootstrap CI excludes 1)."""
    ratios = np.array([r["calibration_ratio"] for r in records], dtype=float)
    ratios = ratios[np.isfinite(ratios)]
    if ratios.size < 10:
        return _row(
            hypothesis="H2b",
            scope="system",
            scope_value=scope_value,
            statistic="median_ratio",
            statistic_value=float("nan"),
            p_value=float("nan"),
            effect="abs_deviation_from_1",
            effect_value=float("nan"),
            effect_label="nan",
            verdict="inconclusive",
            notes="insufficient ratio samples",
        )
    ci = bootstrap_median_ci(ratios)
    median = ci["median"]
    deviation = abs(median - 1.0)
    excludes_one = (ci["ci_low"] > 1.0) or (ci["ci_high"] < 1.0)
    if excludes_one and deviation >= 0.05:
        verdict = "supports"
    elif (not excludes_one) and deviation < 0.05:
        verdict = "refutes"
    else:
        verdict = "inconclusive"
    if deviation >= 0.30:
        label = "severe miscalibration"
    elif deviation >= 0.15:
        label = "moderate miscalibration"
    elif deviation >= 0.05:
        label = "mild miscalibration"
    else:
        label = "calibrated"
    notes = (
        f"median ratio={median:.3g}; 95% CI [{ci['ci_low']:.3g},{ci['ci_high']:.3g}]; "
        f"|median-1|={deviation:.3g}"
    )
    return _row(
        hypothesis="H2b",
        scope="system",
        scope_value=scope_value,
        statistic="median_ratio",
        statistic_value=median,
        p_value=None,
        effect="abs_deviation_from_1",
        effect_value=deviation,
        effect_label=label,
        verdict=verdict,
        notes=notes,
    )


def test_h2c_calibration_strategy_dep(
    records: list[dict[str, Any]],
    *,
    scope_value: str,
) -> dict[str, Any]:
    """H2c: calibration depends on strategy (K-W of calibration ratio across strategies)."""
    strategies = sorted({r["strategy"] for r in records if r["strategy"] not in ("cheapOracle", "expensiveOracle")})
    groups = []
    for strategy in strategies:
        vals = [r["calibration_ratio"] for r in records if r["strategy"] == strategy and math.isfinite(r["calibration_ratio"])]
        if vals:
            groups.append(vals)
    if len(groups) < 2:
        return _row(
            hypothesis="H2c",
            scope="system",
            scope_value=scope_value,
            statistic="kruskal_wallis_p",
            statistic_value=float("nan"),
            p_value=float("nan"),
            effect="eta_squared",
            effect_value=float("nan"),
            effect_label="nan",
            verdict="inconclusive",
            notes="not enough strategies",
        )
    res = kruskal_wallis(groups)
    p = res["p_value"]
    eta = res["eta_squared"]
    if eta >= 0.14:
        label = "large"
    elif eta >= 0.06:
        label = "medium"
    elif eta >= 0.01:
        label = "small"
    else:
        label = "negligible"
    if math.isfinite(p) and p < 0.05 and eta >= 0.01:
        verdict = "supports"
    elif math.isfinite(p) and p >= 0.10 and eta < 0.01:
        verdict = "refutes"
    else:
        verdict = "inconclusive"
    notes = f"K-W p={p:.3g}; eta^2={eta:.3g}; k={res['k']} strategies"
    return _row(
        hypothesis="H2c",
        scope="system",
        scope_value=scope_value,
        statistic="kruskal_wallis_p",
        statistic_value=p,
        p_value=p,
        effect="eta_squared",
        effect_value=eta,
        effect_label=label,
        verdict=verdict,
        notes=notes,
    )


def test_h3a_rank_flips(
    rank_rows: list[dict[str, Any]],
    *,
    scope_value: str,
) -> dict[str, Any]:
    """H3a: rankings sometimes diverge between count and empirical cost."""
    if not rank_rows:
        return _row(
            hypothesis="H3a",
            scope="system",
            scope_value=scope_value,
            statistic="top1_flips",
            statistic_value=float("nan"),
            p_value=float("nan"),
            effect="flip_fraction",
            effect_value=float("nan"),
            effect_label="nan",
            verdict="inconclusive",
            notes="no rank rows",
        )
    flips = sum(1 for r in rank_rows if not r["top1_agreement"])
    total = len(rank_rows)
    fraction = flips / total
    mean_tau = float(np.mean([r["kendall_tau"] for r in rank_rows]))
    if flips >= 1:
        verdict = "supports"
    else:
        verdict = "refutes"
    if fraction >= 0.5:
        label = "frequent flips"
    elif fraction >= 0.15:
        label = "occasional flips"
    elif fraction > 0:
        label = "rare flips"
    else:
        label = "no flips"
    notes = f"top-1 flips {flips}/{total}; mean Kendall tau={mean_tau:.3g}"
    return _row(
        hypothesis="H3a",
        scope="system",
        scope_value=scope_value,
        statistic="top1_flips",
        statistic_value=flips,
        p_value=None,
        effect="flip_fraction",
        effect_value=fraction,
        effect_label=label,
        verdict=verdict,
        notes=notes,
    )


def test_h4a_h4b_pareto(
    pareto_rows: list[dict[str, Any]],
    *,
    scope_value: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """H4a: at least one (s,n) flips Pareto status. H4b: frontiers differ."""
    if not pareto_rows:
        nan_row_a = _row(
            hypothesis="H4a",
            scope="system",
            scope_value=scope_value,
            statistic="exclusive_pairs",
            statistic_value=float("nan"),
            p_value=float("nan"),
            effect="pareto_jaccard",
            effect_value=float("nan"),
            effect_label="nan",
            verdict="inconclusive",
            notes="no pareto rows",
        )
        nan_row_b = dict(nan_row_a, hypothesis="H4b")
        return nan_row_a, nan_row_b
    count_set = {(r["strategy"], r["level"]) for r in pareto_rows if int(r["pareto_count"]) == 1}
    emp_set = {(r["strategy"], r["level"]) for r in pareto_rows if int(r["pareto_empirical"]) == 1}
    only_count = count_set - emp_set
    only_emp = emp_set - count_set
    union = count_set | emp_set
    intersection = count_set & emp_set
    jaccard = len(intersection) / len(union) if union else float("nan")
    exclusive = len(only_count) + len(only_emp)
    if exclusive >= 1:
        verdict_a = "supports"
    else:
        verdict_a = "refutes"
    notes_a = (
        f"|count|={len(count_set)}; |empirical|={len(emp_set)}; "
        f"only_count={len(only_count)}; only_empirical={len(only_emp)}; Jaccard={jaccard:.3g}"
    )
    h4a = _row(
        hypothesis="H4a",
        scope="system",
        scope_value=scope_value,
        statistic="exclusive_pairs",
        statistic_value=exclusive,
        p_value=None,
        effect="pareto_jaccard",
        effect_value=jaccard,
        effect_label=("identical" if jaccard == 1.0 else "different"),
        verdict=verdict_a,
        notes=notes_a,
    )
    if not math.isfinite(jaccard):
        verdict_b = "inconclusive"
        label_b = "nan"
    elif jaccard < 0.999:
        verdict_b = "supports"
        label_b = "frontiers differ"
    elif len(count_set) != len(emp_set):
        verdict_b = "supports"
        label_b = "frontier sizes differ"
    else:
        verdict_b = "refutes"
        label_b = "frontiers coincide"
    h4b = _row(
        hypothesis="H4b",
        scope="system",
        scope_value=scope_value,
        statistic="pareto_jaccard",
        statistic_value=jaccard,
        p_value=None,
        effect="frontier_size_diff",
        effect_value=abs(len(count_set) - len(emp_set)),
        effect_label=label_b,
        verdict=verdict_b,
        notes=f"|count|={len(count_set)}; |empirical|={len(emp_set)}; Jaccard={jaccard:.3g}",
    )
    return h4a, h4b


# --------------------------------------------------------------------------- #
# Per-context driver                                                          #
# --------------------------------------------------------------------------- #


def evaluate_per_context_hypotheses(
    *,
    scope_value: str,
    records: list[dict[str, Any]],
    heterogeneity: list[dict[str, Any]],
    rank_rows: list[dict[str, Any]],
    pareto_rows: list[dict[str, Any]],
    cost_values: np.ndarray | None = None,
) -> list[dict[str, Any]]:
    """Run H1a-H4b on a single (system or context) scope."""
    out: list[dict[str, Any]] = []
    if heterogeneity:
        out.append(test_h1a_cost_heterogeneity(heterogeneity[0], cost_values=cost_values, scope_value=scope_value))
    out.append(test_h1b_strategy_effect(records, scope_value=scope_value))
    out.append(test_h2a_correlation(records, scope_value=scope_value))
    out.append(test_h2b_calibration_offset(records, scope_value=scope_value))
    out.append(test_h2c_calibration_strategy_dep(records, scope_value=scope_value))
    out.append(test_h3a_rank_flips(rank_rows, scope_value=scope_value))
    h4a, h4b = test_h4a_h4b_pareto(pareto_rows, scope_value=scope_value)
    out.append(h4a)
    out.append(h4b)
    return out


# --------------------------------------------------------------------------- #
# Cross-system / cross-context tests                                          #
# --------------------------------------------------------------------------- #


def test_h3b_flip_correlation(per_system_summary: list[dict[str, Any]]) -> dict[str, Any]:
    """H3b: rank-flip rate correlates with cost heterogeneity (Spearman across systems)."""
    cv = np.array([row.get("cost_cv", float("nan")) for row in per_system_summary], dtype=float)
    flips = np.array([row.get("rank_top1_flips", float("nan")) for row in per_system_summary], dtype=float)
    mask = np.isfinite(cv) & np.isfinite(flips)
    if mask.sum() < 4:
        return _row(
            hypothesis="H3b",
            scope="global",
            scope_value="all_systems",
            statistic="spearman_rho_cv_flips",
            statistic_value=float("nan"),
            p_value=float("nan"),
            effect="rho",
            effect_value=float("nan"),
            effect_label="nan",
            verdict="inconclusive",
            notes=f"only {int(mask.sum())} systems available",
        )
    res = spearman_with_p(cv[mask], flips[mask])
    rho, p = res["rho"], res["p_value"]
    if math.isfinite(rho) and rho > 0 and math.isfinite(p) and p < 0.05:
        verdict = "supports"
    elif math.isfinite(rho) and rho > 0.3:
        verdict = "supports"
    elif math.isfinite(rho) and rho <= 0 and math.isfinite(p) and p < 0.05:
        verdict = "refutes"
    else:
        verdict = "inconclusive"
    if abs(rho) >= 0.7:
        label = "strong"
    elif abs(rho) >= 0.4:
        label = "moderate"
    elif abs(rho) >= 0.2:
        label = "weak"
    else:
        label = "negligible"
    notes = f"Spearman(CV, flips) rho={rho:.3g} on n={int(mask.sum())} systems"
    return _row(
        hypothesis="H3b",
        scope="global",
        scope_value="all_systems",
        statistic="spearman_rho_cv_flips",
        statistic_value=rho,
        p_value=p,
        effect="rho",
        effect_value=rho,
        effect_label=label,
        verdict=verdict,
        notes=notes,
    )


def test_h5a_input_sensitivity(per_input_rows: list[dict[str, Any]], *, scope_value: str) -> dict[str, Any]:
    """H5a: cost-proxy validity differs across inputs/workloads.

    Operationalized as: spread of the median calibration ratio across inputs
    must be non-trivial, and a Kruskal-Wallis on per-input ratios across inputs
    rejects equality.
    """
    by_input: dict[str, list[float]] = defaultdict(list)
    for row in per_input_rows:
        key = row.get("target_context") or row.get("cost_context") or row.get("context")
        ratio = row.get("calibration_ratio")
        if ratio is None or not math.isfinite(ratio):
            continue
        by_input[key].append(ratio)
    if len(by_input) < 3:
        return _row(
            hypothesis="H5a",
            scope=scope_value.split("|")[0] if "|" in scope_value else "scenario",
            scope_value=scope_value,
            statistic="kruskal_wallis_p",
            statistic_value=float("nan"),
            p_value=float("nan"),
            effect="ratio_spread",
            effect_value=float("nan"),
            effect_label="nan",
            verdict="inconclusive",
            notes="not enough inputs",
        )
    groups = list(by_input.values())
    res = kruskal_wallis(groups)
    medians = np.array([np.median(g) for g in groups])
    spread = float(np.max(medians) - np.min(medians))
    p, eta = res["p_value"], res["eta_squared"]
    if eta >= 0.14:
        label = "large"
    elif eta >= 0.06:
        label = "medium"
    elif eta >= 0.01:
        label = "small"
    else:
        label = "negligible"
    if math.isfinite(p) and p < 0.05 and eta >= 0.06:
        verdict = "supports"
    elif math.isfinite(p) and p < 0.05 and spread >= 0.1:
        verdict = "supports"
    elif math.isfinite(p) and p >= 0.20 and eta < 0.01:
        verdict = "refutes"
    else:
        verdict = "inconclusive"
    notes = f"K-W on {len(groups)} inputs: p={p:.3g}; eta^2={eta:.3g}; ratio spread={spread:.3g}"
    return _row(
        hypothesis="H5a",
        scope="scenario",
        scope_value=scope_value,
        statistic="kruskal_wallis_p",
        statistic_value=p,
        p_value=p,
        effect="ratio_spread",
        effect_value=spread,
        effect_label=label,
        verdict=verdict,
        notes=notes,
    )


def test_h5b_target_property_gap(scenario_summaries: list[dict[str, Any]]) -> dict[str, Any]:
    """H5b: x264 size-as-cost gap differs between target=time and target=size."""
    by_target: dict[str, list[float]] = defaultdict(list)
    for row in scenario_summaries:
        target = row.get("target_property")
        flips = row.get("rank_top1_flips")
        cases = row.get("rank_cases")
        if target is None or flips is None or cases in (None, 0):
            continue
        by_target[target].append(flips / cases)
    if "time" not in by_target or "size" not in by_target:
        return _row(
            hypothesis="H5b",
            scope="global",
            scope_value="x264_matrix",
            statistic="flip_rate_diff",
            statistic_value=float("nan"),
            p_value=float("nan"),
            effect="abs_diff",
            effect_value=float("nan"),
            effect_label="nan",
            verdict="inconclusive",
            notes="time/size targets not both present",
        )
    rate_time = float(np.mean(by_target["time"]))
    rate_size = float(np.mean(by_target["size"]))
    diff = rate_size - rate_time
    abs_diff = abs(diff)
    if abs_diff >= 0.05:
        verdict = "supports"
    elif abs_diff < 0.01:
        verdict = "refutes"
    else:
        verdict = "inconclusive"
    if abs_diff >= 0.20:
        label = "large gap"
    elif abs_diff >= 0.10:
        label = "moderate gap"
    elif abs_diff >= 0.05:
        label = "small gap"
    else:
        label = "negligible gap"
    notes = (
        f"flip rate target=time={rate_time:.3g}; target=size={rate_size:.3g}; "
        f"diff (size-time)={diff:+.3g}"
    )
    return _row(
        hypothesis="H5b",
        scope="global",
        scope_value="x264_matrix",
        statistic="flip_rate_diff",
        statistic_value=diff,
        p_value=None,
        effect="abs_diff",
        effect_value=abs_diff,
        effect_label=label,
        verdict=verdict,
        notes=notes,
    )


def test_h5c_rank_stability_compare(scenario_summaries: list[dict[str, Any]]) -> dict[str, Any]:
    """H5c: under empirical cost, rankings/frontiers are less stable across contexts.

    Operationalized as: the mean Kendall tau between count and empirical
    rankings is below 1, and median Pareto Jaccard is below 1, on average
    across the four scenarios.
    """
    if not scenario_summaries:
        return _row(
            hypothesis="H5c",
            scope="global",
            scope_value="x264_matrix",
            statistic="mean_kendall_tau",
            statistic_value=float("nan"),
            p_value=float("nan"),
            effect="median_jaccard",
            effect_value=float("nan"),
            effect_label="nan",
            verdict="inconclusive",
            notes="no scenarios",
        )
    taus = [row["rank_mean_kendall_tau"] for row in scenario_summaries if math.isfinite(row.get("rank_mean_kendall_tau", float("nan")))]
    jaccards = [row["pareto_median_jaccard"] for row in scenario_summaries if math.isfinite(row.get("pareto_median_jaccard", float("nan")))]
    if not taus or not jaccards:
        return _row(
            hypothesis="H5c",
            scope="global",
            scope_value="x264_matrix",
            statistic="mean_kendall_tau",
            statistic_value=float("nan"),
            p_value=float("nan"),
            effect="median_jaccard",
            effect_value=float("nan"),
            effect_label="nan",
            verdict="inconclusive",
            notes="missing tau or jaccard",
        )
    mean_tau = float(np.mean(taus))
    med_jaccard = float(np.median(jaccards))
    instability = (1.0 - mean_tau) + (1.0 - med_jaccard)
    if mean_tau < 0.95 or med_jaccard < 0.9:
        verdict = "supports"
    elif mean_tau >= 0.99 and med_jaccard >= 0.99:
        verdict = "refutes"
    else:
        verdict = "inconclusive"
    if instability >= 0.5:
        label = "large instability"
    elif instability >= 0.2:
        label = "moderate instability"
    elif instability >= 0.05:
        label = "small instability"
    else:
        label = "stable"
    notes = (
        f"mean Kendall tau={mean_tau:.3g}; median Pareto Jaccard={med_jaccard:.3g}; "
        f"composite instability={instability:.3g}"
    )
    return _row(
        hypothesis="H5c",
        scope="global",
        scope_value="x264_matrix",
        statistic="mean_kendall_tau",
        statistic_value=mean_tau,
        p_value=None,
        effect="median_jaccard",
        effect_value=med_jaccard,
        effect_label=label,
        verdict=verdict,
        notes=notes,
    )


# --------------------------------------------------------------------------- #
# Aggregation                                                                 #
# --------------------------------------------------------------------------- #


def aggregate_verdicts(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Aggregate per-scope rows into a per-hypothesis summary."""
    by_h: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_h[row["hypothesis"]].append(row)
    out: list[dict[str, Any]] = []
    order = [
        "H1a", "H1b",
        "H2a", "H2b", "H2c",
        "H3a", "H3b",
        "H4a", "H4b",
        "H5a", "H5b", "H5c",
    ]
    for h in order:
        items = by_h.get(h, [])
        if not items:
            continue
        n = len(items)
        sup = sum(1 for r in items if r["verdict"] == "supports")
        ref = sum(1 for r in items if r["verdict"] == "refutes")
        inc = sum(1 for r in items if r["verdict"] == "inconclusive")
        if sup >= max(ref, inc) and sup >= 0.5 * n:
            global_v = f"supported ({sup}/{n})"
        elif ref >= max(sup, inc) and ref >= 0.5 * n:
            global_v = f"refuted ({ref}/{n})"
        else:
            global_v = f"mixed (sup={sup}, ref={ref}, inc={inc} of {n})"
        out.append(
            {
                "hypothesis": h,
                "scopes": n,
                "supports": sup,
                "refutes": ref,
                "inconclusive": inc,
                "global_verdict": global_v,
            }
        )
    return out
