"""Posterior risk/confidence metrics for performance-bound sampling.

The functions mirror the FSE 2026 artifact's notebook formulas:

* posterior risk is the fraction of measured configurations beyond the
  sampled bound;
* posterior confidence is the empirical CDF of posterior risks over repeated
  samples;
* prior confidence is ``1 - (1 - epsilon) ** (N + 1)`` by default, matching
  the artifact code's ``calculate_prior_beta`` helper.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np


Extreme = Literal["max", "min"]


@dataclass(frozen=True)
class RiskBound:
    risk: float
    bound: float
    n_violations: int


@dataclass(frozen=True)
class IntegratedConfidence:
    posterior_area: float
    prior_area: float
    omega: float
    omega_over_max: float


def prior_confidence(
    epsilon: np.ndarray | float,
    sample_size: int | float,
    *,
    exponent_offset: int = 1,
) -> np.ndarray | float:
    """Return the scenario-theory confidence curve.

    The paper text writes the simplified form with exponent ``N``. The
    released notebook computes beta as ``(1 - epsilon) ** (N + 1)`` and plots
    ``1 - beta``.  The default ``exponent_offset=1`` follows the artifact; set
    it to ``0`` for the simplified equation.
    """

    eps = np.asarray(epsilon, dtype=float)
    confidence = 1.0 - np.power(1.0 - eps, float(sample_size) + exponent_offset)
    if np.isscalar(epsilon):
        return float(confidence)
    return confidence


def prior_confidence_area(sample_size: int | float, *, exponent_offset: int = 1) -> float:
    """Exact integral of :func:`prior_confidence` over epsilon in [0, 1]."""

    exponent = float(sample_size) + exponent_offset
    return float(1.0 - 1.0 / (exponent + 1.0))


def sample_risk_bound(values: np.ndarray, indices: np.ndarray, *, extreme: Extreme = "max") -> RiskBound:
    """Compute posterior risk for one sample.

    For ``extreme='max'``, the sampled maximum is treated as the observed
    worst-case bound and risk is the fraction of all configurations with a
    larger value. For ``extreme='min'``, the inequality is reversed.
    """

    universe = np.asarray(values, dtype=float)
    sample_idx = np.asarray(indices, dtype=int)
    if universe.size == 0:
        raise ValueError("Cannot compute posterior risk over an empty universe")
    if sample_idx.size == 0:
        raise ValueError("Cannot compute posterior risk for an empty sample")

    sample_values = universe[sample_idx]
    if extreme == "max":
        bound = float(np.max(sample_values))
        violations = int(np.sum(universe > bound))
    elif extreme == "min":
        bound = float(np.min(sample_values))
        violations = int(np.sum(universe < bound))
    else:
        raise ValueError(f"Unsupported extreme {extreme!r}; expected 'max' or 'min'")

    return RiskBound(risk=float(violations / universe.size), bound=bound, n_violations=violations)


def posterior_confidence(epsilon: np.ndarray, risks: np.ndarray) -> np.ndarray:
    """Empirical posterior confidence for each epsilon value.

    This implements Equation (5) from the paper, i.e. the fraction of repeated
    samples whose posterior risk is at most the accepted risk epsilon.
    """

    eps = np.asarray(epsilon, dtype=float)
    sorted_risks = np.sort(np.asarray(risks, dtype=float))
    if sorted_risks.size == 0:
        raise ValueError("Cannot compute posterior confidence without risks")
    counts = np.searchsorted(sorted_risks, eps, side="right")
    return counts / sorted_risks.size


def integrated_confidence(
    risks: np.ndarray,
    sample_size: int | float,
    *,
    exponent_offset: int = 1,
) -> IntegratedConfidence:
    """Integrate posterior/prior confidence over epsilon in [0, 1].

    For an empirical CDF over risks in [0, 1], the integral over [0, 1] is
    exactly ``1 - mean(risks)``. This avoids numerical quadrature while matching
    the FSE definition of integrated posterior confidence.
    """

    risk_values = np.asarray(risks, dtype=float)
    if risk_values.size == 0:
        raise ValueError("Cannot integrate confidence without risks")
    if np.any((risk_values < 0.0) | (risk_values > 1.0)):
        raise ValueError("Posterior risks must lie in [0, 1]")

    posterior_area = float(1.0 - np.mean(risk_values))
    prior_area = prior_confidence_area(sample_size, exponent_offset=exponent_offset)
    omega = posterior_area - prior_area
    omega_max = 1.0 - prior_area
    omega_over_max = omega / omega_max if omega_max > 0 else float("nan")
    return IntegratedConfidence(
        posterior_area=posterior_area,
        prior_area=prior_area,
        omega=float(omega),
        omega_over_max=float(omega_over_max),
    )


def confidence_curve_rows(
    *,
    context: str,
    strategy: str,
    level: str,
    risks: np.ndarray,
    sample_size: int | float,
    epsilon_grid: np.ndarray,
    exponent_offset: int = 1,
) -> list[dict[str, object]]:
    """Build CSV-ready posterior/prior confidence curve rows."""

    posterior = posterior_confidence(epsilon_grid, risks)
    prior = prior_confidence(epsilon_grid, sample_size, exponent_offset=exponent_offset)
    return [
        {
            "context": context,
            "strategy": strategy,
            "level": level,
            "epsilon": float(epsilon),
            "posterior_confidence": float(post),
            "prior_confidence": float(base),
            "confidence_discrepancy": float(post - base),
        }
        for epsilon, post, base in zip(epsilon_grid, posterior, prior)
    ]
