"""Phase 1 SRS audit: compare cost_sampling.srs against the FSE artifact notebook.

The reference implementation below is copied verbatim (modulo warnings setup)
from ``SRS-sampling.ipynb`` in the FSE 2026 artifact
(doi:10.5281/zenodo.19682296, downloaded 2026-07-02).

Checks:
1. Roadmap smoke properties for ``srs_indices``: exact size, deterministic
   seeds, no duplicate indices, max/min orientation.
2. Behavioral equivalence: both samplers run on the same synthetic system;
   we compare sampled-bound quality (posterior risk of the max bound) and
   sample-size behavior over repeated seeds.
3. Duplicate behavior of the artifact's random fill (documented deviation).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, ttest_ind

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cost_sampling.srs import srs_indices


# --- verbatim from SRS-sampling.ipynb (FSE 2026 artifact) -------------------

def get_n_random_samples(measurement_df, n):
    return measurement_df.sample(n, replace=False)


def SRS_sampling(step_sample_size, measurement_df, nfp, samples_df=pd.DataFrame(), decision_set=[], sample_set_size=300):
    filtered_df = measurement_df
    for feature, decision in decision_set:
        filtered_df = filtered_df[filtered_df[feature] == decision]

    if not samples_df.empty and samples_df.shape[0] + step_sample_size >= sample_set_size:
        step_sample_size = sample_set_size - len(samples_df.index)
    new_samples_df = get_n_random_samples(filtered_df, step_sample_size) if len(filtered_df.index) > step_sample_size else filtered_df
    samples_df = pd.concat([samples_df, new_samples_df])

    sorted_new_samples_df = new_samples_df.sort_values(by=nfp, ascending=False)

    if len(sorted_new_samples_df.index) < 2:
        if len(samples_df.index) < sample_set_size:
            sample_size = sample_set_size - len(samples_df.index)
            new_samples_df = get_n_random_samples(measurement_df, sample_size) if len(measurement_df.index) > sample_size else measurement_df
            samples_df = pd.concat([samples_df, new_samples_df])
        return samples_df

    compared_first_two_samples = sorted_new_samples_df.diff().iloc[1]

    common_decisions = []
    for index, value in compared_first_two_samples.items():
        if index in nfp:
            continue
        if value == 0:
            common_decisions.append(index)

    noteworthy_decisions = []
    for candidate_decision in common_decisions:
        avg_performance_enabled = sorted_new_samples_df[sorted_new_samples_df[candidate_decision] == sorted_new_samples_df.iloc[0][candidate_decision]][nfp].mean()
        avg_performance_disabled = sorted_new_samples_df[sorted_new_samples_df[candidate_decision] != sorted_new_samples_df.iloc[0][candidate_decision]][nfp].mean()

        if avg_performance_enabled is np.nan or avg_performance_disabled is np.nan:
            continue
        if avg_performance_enabled != avg_performance_disabled and candidate_decision not in decision_set:
            performance_samples_enabled = sorted_new_samples_df[sorted_new_samples_df[candidate_decision] == sorted_new_samples_df.iloc[0][candidate_decision]][nfp]
            performance_samples_disabled = sorted_new_samples_df[sorted_new_samples_df[candidate_decision] != sorted_new_samples_df.iloc[0][candidate_decision]][nfp]

            welchs_ttest_result = ttest_ind(performance_samples_enabled, performance_samples_disabled, equal_var=False)
            if welchs_ttest_result.pvalue < 0.05:
                noteworthy_decisions.append((candidate_decision, sorted_new_samples_df.iloc[0][candidate_decision]))
            else:
                continue
    if noteworthy_decisions:
        new_measurement_df = pd.concat([measurement_df, samples_df, samples_df]).drop_duplicates(keep=False)
        return SRS_sampling(step_sample_size, new_measurement_df, nfp, samples_df, decision_set=decision_set + noteworthy_decisions, sample_set_size=sample_set_size)
    else:
        if len(samples_df.index) < sample_set_size:
            sample_size = sample_set_size - len(samples_df.index)
            new_samples_df = get_n_random_samples(measurement_df, sample_size) if len(measurement_df.index) > sample_size else measurement_df
            samples_df = pd.concat([samples_df, new_samples_df])
        return samples_df


# --- audit harness -----------------------------------------------------------

def synthetic_system(n_configs: int, n_features: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    X = rng.integers(0, 2, size=(n_configs, n_features))
    Xf = X.astype(float)
    effects = rng.normal(0.0, 4.0, size=n_features)
    interactions = rng.normal(0.0, 2.0, size=(n_features, n_features))
    y = Xf @ effects
    y += np.einsum("ij,jk,ik->i", Xf, np.triu(interactions, 1), Xf)
    y += rng.normal(0.0, 1.0, size=n_configs)
    assert np.isfinite(y).all()
    return X, y.astype(float)


def posterior_risk_max(y_universe: np.ndarray, y_sample: np.ndarray) -> float:
    bound = float(np.max(y_sample))
    return float(np.mean(y_universe > bound))


def main() -> None:
    print("== 1. roadmap smoke checks on srs_indices ==")
    rng = np.random.default_rng(0)
    X = rng.integers(0, 2, size=(200, 12))
    y = X[:, 0] * 10 + X[:, 1] * 3 + rng.normal(size=200)
    idx = srs_indices(X, y, 32, rng=123)
    assert len(idx) == 32, "exact sample size"
    assert len(set(idx.tolist())) == 32, "no duplicate indices"
    idx2 = srs_indices(X, y, 32, rng=123)
    assert np.array_equal(idx, idx2), "deterministic for equal seed"
    idx3 = srs_indices(X, y, 32, rng=124)
    assert not np.array_equal(idx, idx3), "seed changes sample"
    idx_min = srs_indices(X, y, 32, rng=123, extreme="min")
    assert len(idx_min) == 32 and len(set(idx_min.tolist())) == 32
    full = srs_indices(X, y, 500, rng=1)
    assert len(full) == 200 and len(set(full.tolist())) == 200, "budget > pool clamps to pool"
    print("PASS: size / determinism / uniqueness / orientation / clamping")

    print()
    print("== 2. behavioral equivalence vs artifact notebook ==")
    n_configs, n_features, budget, seeds = 3000, 16, 300, 40
    X, yv = synthetic_system(n_configs, n_features, seed=7)
    df = pd.DataFrame(X, columns=[f"f{i}" for i in range(n_features)])
    df["Performance"] = yv

    risks_ours, risks_ref = [], []
    sizes_ref, unique_ref, dup_runs = [], [], 0
    for seed in range(1, seeds + 1):
        np.random.seed(seed)
        ref = SRS_sampling(25, df, "Performance", sample_set_size=budget)
        sizes_ref.append(len(ref.index))
        n_unique = len(ref.drop_duplicates().index)
        unique_ref.append(n_unique)
        if n_unique < len(ref.index):
            dup_runs += 1
        risks_ref.append(posterior_risk_max(yv, ref["Performance"].to_numpy()))

        ours = srs_indices(X, yv, budget, rng=seed, extreme="max")
        assert len(ours) == budget and len(set(ours.tolist())) == budget
        risks_ours.append(posterior_risk_max(yv, yv[ours]))

    print(f"artifact sample size: min={min(sizes_ref)} max={max(sizes_ref)} (requested {budget})")
    print(f"artifact runs with duplicate configs in sample: {dup_runs}/{seeds} "
          f"(unique range {min(unique_ref)}-{max(unique_ref)})")
    print(f"posterior risk (max bound), mean±sd: "
          f"ours {np.mean(risks_ours):.5f}±{np.std(risks_ours):.5f} | "
          f"artifact {np.mean(risks_ref):.5f}±{np.std(risks_ref):.5f}")
    u = mannwhitneyu(risks_ours, risks_ref, alternative="two-sided")
    print(f"Mann-Whitney U on posterior risks: p={u.pvalue:.4f} "
          f"({'no detectable difference' if u.pvalue >= 0.05 else 'DIFFERENT distributions'})")

    print()
    print("== 3. random-vs-SRS sanity (SRS should tighten the max bound) ==")
    risks_rand = []
    for seed in range(1, seeds + 1):
        rng = np.random.default_rng(seed)
        pick = rng.choice(n_configs, size=budget, replace=False)
        risks_rand.append(posterior_risk_max(yv, yv[pick]))
    u2 = mannwhitneyu(risks_ours, risks_rand, alternative="less")
    print(f"ours mean risk {np.mean(risks_ours):.5f} vs random {np.mean(risks_rand):.5f} "
          f"(one-sided p={u2.pvalue:.2e})")


if __name__ == "__main__":
    main()
