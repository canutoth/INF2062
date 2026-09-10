# Specification 04 — Phase 4: ENERGY and WORKLOAD Posterior Extension (BUILD phase)

Scripts to **create**:
`cost_sampling/posterior_batch.py` (shared module),
`scripts/run_fse_posterior_twins_batch.py` (ENERGY),
`scripts/run_fse_posterior_workload_batch.py` (WORKLOAD)
Corpus labels: `ENERGY`, `WORKLOAD`
Output directories: `artifacts/fse_posterior_energy_<suffix>/`,
`artifacts/fse_posterior_workload_<suffix>/`

See Spec 00 §6 (metrics), §7 (hypotheses), §11 (terminology). This is the one
phase whose task is code generation, not just execution — implement §4–§7 exactly,
then run the §8 commands.

---

## 1. Goal

Extend the FSE-posterior outcome to two generated-sampling families, **reusing the
repo's existing generated-sampling engines** rather than inventing a second
protocol:

- `ENERGY`: does guarantee-per-acquisition-cost behave differently when cost means
  energy (or another measured property) instead of runtime?
- `WORKLOAD`: are posterior guarantees and SRS/cost tradeoffs sensitive to the
  workload/input context inside a configurable system?

## 2. Assets to reuse (import — do NOT reimplement or fork)

```text
cost_sampling/posterior.py            # posterior risk / confidence / prior conf / integrated conf / ICD
cost_sampling/srs.py                  # srs_indices(X, y, k, rng=<int>) -> exactly k unique indices
cost_sampling/pool_samplers.py        # pool-based sampling strategy registry
cost_sampling/generated_sampling.py   # generated-sampling helpers (LCBench + generated families)
scripts/run_fse_posterior.py          # generic one-context runner — SOURCE of the logic to factor out
scripts/run_twins_generated.py        # ENERGY/Twins data loader + sample builders
scripts/run_workload_generated.py     # WORKLOAD data loader + sample builders
scripts/kw_cost_vs_size.py            # reference for --mode {twins,workload} column choices
artifacts/generated_sampling_protocol.md   # the protocol the generated samplers must match
```

Discovery step before writing code: open `scripts/run_fse_posterior.py` and the
existing `scripts/run_fse_posterior_x264_batch.py`. Identify the function(s) that,
given one context, compute the per-strategy posterior metrics, run the hypothesis
tests, and emit the per-context report + figures. If a reusable entry point
already exists, move it into `cost_sampling/posterior_batch.py` unchanged and have
all batch scripts import it. If it is inlined, factor it out — same behaviour,
same output columns.

## 3. Current gap

- No `cost_sampling/posterior_batch.py`.
- No `scripts/run_fse_posterior_twins_batch.py`.
- No `scripts/run_fse_posterior_workload_batch.py`.

## 4. `cost_sampling/posterior_batch.py` — shared contract

Factor out (do not duplicate) the per-context posterior pipeline. Minimum public
surface:

```python
def run_posterior_for_context(
    *,
    context_id: str,
    target: np.ndarray,          # 1-D, over the reference universe V (the measured pool)
    cost: np.ndarray,            # 1-D, per-config acquisition cost, aligned to `target`
    config_matrix: np.ndarray,   # encoded config features over V, for SRS
    strategies: dict,            # name -> sampler callable (see §5)
    levels: list[int],           # absolute sample sizes, e.g. [8, 16, 32, 64]
    fixed_level: int,            # budget at which H1/H5/H6 are computed
    n_seeds: int,                # repeated runs for stochastic strategies
    n_srs_seeds: int,            # repeated runs for SRS
    extreme: str,                # "max" | "min"
    prior_offset: int,           # 1 -> (1-eps)**(N+1) ; 0 -> (1-eps)**N
    out_dir: str,                # <output-dir>/<context_id>/
    base_seed: int = 42,
) -> ContextResult
```

`ContextResult` carries the rows for every summary CSV in §7 plus the hypothesis
verdicts. Per `(strategy, level, seed)` it records: sampled bound, posterior risk
(Spec 00 §6), `pct_n`, `pct_cost`, `calibration_ratio`, `effective_n_by_cost`.
Per `(strategy, level)` it aggregates over seeds: mean posterior risk, integrated
posterior confidence `= 1 - mean(risk)`, prior area (count variant with `N = k`
and empirical-cost variant with `N = effective_n_by_cost`), `omega =
posterior_area - prior_area`.

Hypothesis tests at `fixed_level` (Spec 00 §7):

| ID | Test | Inputs |
|---|---|---|
| H1 | Kruskal–Wallis | posterior-risk samples across all strategies |
| H2 | top-choice comparison | best strategy on the `pct_n` axis vs on the `pct_cost` axis |
| H3 | cost-normalized ranking | is SRS the best on the `pct_cost`-normalized guarantee? |
| H4 | Jaccard + changed-frontier flag | Pareto set on `pct_n` axis vs on `pct_cost` axis |
| H5 | Mann–Whitney U + Vargha–Delaney A12 | SRS vs `random` posterior risk |
| H6 | Mann–Whitney U + Vargha–Delaney A12 | SRS vs `random` `pct_cost` |

Multiple-comparison correction policy is still open (Spec 00 §8 item 8) — record
raw p-values now; do not bake a correction into the module.

## 5. Strategy set

- `strategies` maps a name to a sampler. Non-SRS samplers come from
  `cost_sampling.pool_samplers`; each draws `k` indices from the pool given a
  seeded RNG. SRS is `cost_sampling.srs.srs_indices(config_matrix, target, k,
  rng=seed)`.
- Default set = the **non-oracle** generated-sampling strategies defined by
  `artifacts/generated_sampling_protocol.md` (Spec 00 §8 item 7). Oracle /
  diagnostic strategies are included only when `--include-oracles` is passed, and
  never in the headline output.
- `--strategies` overrides the set with an explicit comma list. `SRS` must always
  be one of the strategies.

## 6. Wrapper scripts — thin, no posterior logic of their own

Each wrapper: parse args → load the family's contexts via the reused loader →
build `config_matrix`, `target`, `cost` per context → call
`run_posterior_for_context` per context → aggregate `ContextResult`s → write §7 →
write the family report.

### 6.1 `scripts/run_fse_posterior_twins_batch.py` (ENERGY)

Context = `(system, target_prop, cost_prop)`;
`context_id = f"{system}__t-{target_prop}__c-{cost_prop}"`.
Load each system's measured pool with the loader used by
`scripts/run_twins_generated.py` (Twins / `twins_energy_subset.zip`).

argparse:

| Flag | Type / default | Meaning |
|---|---|---|
| `--zip` | path, required | `ICPE-rawdata/twins_energy_subset.zip` |
| `--systems` | list or `ALL`, required | system names to include |
| `--target-props` | csv, required | e.g. `energy,performance` |
| `--cost-props` | csv, required | acquisition-cost properties, e.g. `energy,performance` |
| `--levels` | csv, required | budgets as `nXX` tokens, e.g. `n8,n16,n32,n64` |
| `--fixed-level` | token, default = largest `--levels` | budget for H1/H5/H6 |
| `--seeds` | int, default 100 | repeated runs for stochastic strategies |
| `--srs-seeds` | int, default 100 | repeated runs for SRS |
| `--strategies` | csv, optional | override the default strategy set |
| `--include-oracles` | flag, default off | add diagnostic oracle strategies |
| `--output-dir` | path, required | `artifacts/fse_posterior_energy_<suffix>/` |
| `--extreme` | `max`/`min`, default `max` | bound orientation |
| `--prior-offset` | `0`/`1`, default `1` | prior-confidence convention |
| `--quick` | flag | smoke mode: cap levels to `n8,n16,n32`, seeds to 30 |

`--target-props` × `--cost-props` are crossed: every target is evaluated under
every acquisition-cost property. A context row must never have `cost_prop` equal
to `target_prop` silently treated as "no cost" — keep them explicit.

### 6.2 `scripts/run_fse_posterior_workload_batch.py` (WORKLOAD)

Context = `(system, workload)`; `context_id = f"{system}__{workload}"`.
Load contexts with the loader used by `scripts/run_workload_generated.py`
(`workload_artifact.zip`).

argparse: same as §6.1 except —

| Flag | Type / default | Meaning |
|---|---|---|
| `--zip` | path, required | `ICPE-rawdata/workload_artifact.zip` |
| `--systems` | list or `ALL`, required | configurable systems to include |
| `--workloads` | list or `ALL`, default `ALL` | workloads per system |
| `--workload-limit` | int, optional | cap workloads per system (smoke runs) |
| `--target-prop` | str, default per artifact schema | performance target column |
| `--cost-prop` | str, default per artifact schema | acquisition-cost column |

(No `--cost-props` cross-product for WORKLOAD — one target, one cost.)

## 7. Output schema (per `--output-dir`) — parallel to the other posterior scripts

```text
fse_posterior_<family>_report.md            # <family> ∈ {energy, workload}
posterior_<family>_context_summary.csv      # one row per context
posterior_<family>_budget_trends.csv        # one row per (context, level)
posterior_strategy_summary.csv              # one row per (context, strategy, level)
posterior_hypothesis_summary.csv            # one row per context: H1..H6 verdict + key stat
posterior_hypothesis_tests.csv              # one row per (context, hypothesis): statistic, p, effect_size, n
<context_id>/
  <context_id>_report.md
  guarantee_cost_frontier.png               # posterior guarantee vs pct_cost, strategies coloured, SRS marked
  posterior_risk_by_strategy.png            # posterior-risk distribution per strategy at fixed_level
```

`posterior_strategy_summary.csv` columns (at least): `family, context_id, system,
strategy, level, n, mean_posterior_risk, integrated_conf, prior_area_count,
prior_area_cost, omega_count, omega_cost, mean_pct_n, mean_pct_cost,
mean_calibration_ratio, srs_is_best_count, srs_is_best_cost, on_pareto_count,
on_pareto_cost`.

`posterior_hypothesis_summary.csv` columns: `family, context_id, H1_p, H1_sig,
H2_top_changed, H3_srs_best_cost, H4_jaccard, H4_frontier_changed, H5_p, H5_A12,
H6_p, H6_A12`.

## 8. Commands

### 8.1 ENERGY — smoke

```bash
python3 scripts/run_fse_posterior_twins_batch.py \
  --zip ICPE-rawdata/twins_energy_subset.zip \
  --systems brotli lrzip \
  --target-props energy,performance \
  --cost-props energy,performance \
  --levels n8,n16,n32 \
  --seeds 30 \
  --srs-seeds 30 \
  --output-dir artifacts/fse_posterior_energy_smoke \
  --extreme max \
  --prior-offset 1
```

### 8.2 ENERGY — final (if runtime permits)

```bash
python3 scripts/run_fse_posterior_twins_batch.py \
  --zip ICPE-rawdata/twins_energy_subset.zip \
  --systems 7z Apache HSQLDB LLVM MongoDB PostgreSQL VP8 brotli exastencils \
            jump3r kanzi lrzip nginx x264 \
  --target-props energy,performance \
  --cost-props energy,performance \
  --levels n8,n16,n32,n64 \
  --seeds 100 \
  --srs-seeds 100 \
  --output-dir artifacts/fse_posterior_energy_final \
  --extreme max \
  --prior-offset 1
```

### 8.3 WORKLOAD — smoke

```bash
python3 scripts/run_fse_posterior_workload_batch.py \
  --zip ICPE-rawdata/workload_artifact.zip \
  --systems xz \
  --workload-limit 3 \
  --levels n8,n16,n32 \
  --seeds 30 \
  --srs-seeds 30 \
  --output-dir artifacts/fse_posterior_workload_smoke \
  --extreme max \
  --prior-offset 1
```

### 8.4 WORKLOAD — final

```bash
python3 scripts/run_fse_posterior_workload_batch.py \
  --zip ICPE-rawdata/workload_artifact.zip \
  --systems ALL \
  --workloads ALL \
  --levels n8,n16,n32,n64 \
  --seeds 100 \
  --srs-seeds 100 \
  --output-dir artifacts/fse_posterior_workload_final \
  --extreme max \
  --prior-offset 1
```

## 9. Required validation checks

- **Build:** all three files exist; the existing batch scripts still import the
  factored-out logic from `cost_sampling/posterior_batch.py` and still pass their
  own smoke runs (no behavioural regression).
- **Smoke output:** each smoke `--output-dir` contains all five top-level CSVs,
  the family report, and at least one `<context_id>/` dir with both figures.
- **Strategy coverage:** every strategy in the resolved set appears in
  `posterior_strategy_summary.csv` for every context; `SRS` is present.
- **SRS budget:** for every `nXX` level, SRS returns exactly `XX` unique indices.
- **Protocol match:** generated samplers reproduce the counts / behaviour in
  `artifacts/generated_sampling_protocol.md` (spot-check at least one context).
- **No column conflation:** in every context row `cost_prop != target_prop` is
  recorded explicitly, and the cost array is never the target array.
- **Separation:** ENERGY and WORKLOAD write to different `--output-dir`s and
  different `fse_posterior_<family>_report.md` files (Spec 00 §11).
- Confirm target orientation `max` is correct per property; note any property
  where `min` is the true bound.

## 10. Interpretation target

- If ENERGY/WORKLOAD posterior-risk results align with the ICSE count-vs-cost
  findings: posterior guarantees become another outcome supporting "sample size
  is not sampling cost."
- If they diverge: document the boundary condition — posterior-bound quality may
  respond differently from prediction-error quality. Keep the claim
  reference-relative (measured pool, not exhaustive space).

## 11. Libraries

`numpy`, `pandas`, `scipy.stats`, `matplotlib`; repo modules
`cost_sampling.posterior`, `cost_sampling.srs`, `cost_sampling.generated_sampling`,
`cost_sampling.pool_samplers`, and the new `cost_sampling.posterior_batch`. No new
third-party dependencies.
