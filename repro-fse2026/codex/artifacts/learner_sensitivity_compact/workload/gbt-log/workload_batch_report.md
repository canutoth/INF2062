# Workload-impact cross-system report

Input batch: `/Users/mathieuacher/SANDBOX/cost-sampling-matters/artifacts/learner_sensitivity_compact/workload/gbt-log`.

## Scope

Systems covered: `9`. Workload contexts covered: `93`.

Target/cost setup: `8` runtime systems plus `1` throughput-oriented system (`h2`, with cost = `1/throughput`).

## Readout

Highest observed cost heterogeneity: `kanzi` with workload-level CV up to `2.367`.

Weakest count-cost proxy: `z3` with workload-level Spearman rho down to `0.1321`.

Least stable top-1 decisions: `dconvert` with workload-level agreement as low as `0`.

Strongest Pareto disagreement: `h2` with workload-level Jaccard down to `0.2`.

H5a workload sensitivity is supported in `0 / 9` systems.

## Systems

| System | Workloads | Cost CV range | Spearman rho range | Median %cost/%n range | Top-1 agreement range | Pareto Jaccard range | H5a |
|---|---:|---:|---:|---:|---:|---:|---|
| `batik` | 11 | 0.1195-1.027 | 0.5896-0.8671 | 0.7883-1.006 | 0.1429-0.7143 | 0.25-0.6667 | `refutes` |
| `dconvert` | 12 | 0.02639-0.3828 | 0.711-0.8681 | 0.9359-1 | 0-1 | 0.2857-0.6667 | `inconclusive` |
| `h2` | 8 | 0.1053-0.2994 | 0.6763-0.8671 | 0.9865-1.007 | 0.1429-0.8571 | 0.2-0.4 | `refutes` |
| `jump3r` | 6 | 0.3606-0.5851 | 0.5029-0.659 | 0.9661-0.9939 | 0.4286-0.7143 | 0.3333-0.6667 | `refutes` |
| `kanzi` | 9 | 0.8084-2.367 | 0.2601-0.4856 | 0.6399-1.009 | 0-1 | 0.3333-1 | `refutes` |
| `lrzip` | 13 | 0.188-1.559 | 0.4434-0.8821 | 1.008-1.128 | 0.1429-1 | 0.5-1 | `refutes` |
| `x264` | 9 | 0.8459-0.9509 | 0.3468-0.5723 | 0.8077-0.9885 | 0-0.2857 | 0.2-0.5 | `refutes` |
| `xz` | 13 | 0.3067-1.534 | 0.4336-0.6858 | 0.6066-1.037 | 0-0.5714 | 0.2222-0.5 | `refutes` |
| `z3` | 12 | 0.2434-1.861 | 0.1321-0.8397 | 0.6137-1.009 | 0-1 | 0.3-1 | `inconclusive` |

## Files

- `all_workload_summary.csv`: concatenated workload rows from every system.
- `system_summary.csv`: one row per system with workload ranges and H5a verdicts.
- `fig_cost_cv_range_by_system.png`: cost heterogeneity range by system.
- `fig_rq2_proxy_spearman_range_by_system.png`: sample-size ordering quality by system.
- `fig_rq2_median_calibration_range_by_system.png`: calibration range by system.
- `fig_rq3_rq4_decision_range_by_system.png`: top-1 agreement and Pareto Jaccard ranges by system.

