# Workload-impact cross-system report

Input batch: `/Users/mathieuacher/SANDBOX/cost-sampling-matters/artifacts/strong_learner_overnight/workload/sk-hgbt-log`.

## Scope

Systems covered: `9`. Workload contexts covered: `93`.

Target/cost setup: `8` runtime systems plus `1` throughput-oriented system (`h2`, with cost = `1/throughput`).

## Readout

Highest observed cost heterogeneity: `kanzi` with workload-level CV up to `2.367`.

Weakest count-cost proxy: `kanzi` with workload-level Spearman rho down to `0.5724`.

Least stable top-1 decisions: `dconvert` with workload-level agreement as low as `0`.

Strongest Pareto disagreement: `kanzi` with workload-level Jaccard down to `0.25`.

H5a workload sensitivity is supported in `5 / 9` systems.

## Systems

| System | Workloads | Cost CV range | Spearman rho range | Median %cost/%n range | Top-1 agreement range | Pareto Jaccard range | H5a |
|---|---:|---:|---:|---:|---:|---:|---|
| `batik` | 11 | 0.1195-1.027 | 0.8932-0.9847 | 0.8599-0.9882 | 0.4286-1 | 0.4-0.8 | `supports` |
| `dconvert` | 12 | 0.02639-0.3828 | 0.9217-0.9683 | 0.9525-0.9989 | 0-1 | 0.2857-0.5714 | `supports` |
| `h2` | 8 | 0.1053-0.2994 | 0.9715-0.9849 | 0.9784-0.9955 | 0.5714-1 | 0.2857-0.375 | `inconclusive` |
| `jump3r` | 6 | 0.3606-0.5851 | 0.8996-0.9552 | 0.9657-0.977 | 0.5714-0.7143 | 0.375-0.5714 | `refutes` |
| `kanzi` | 9 | 0.8084-2.367 | 0.5724-0.9385 | 0.8229-1.002 | 0-1 | 0.25-1 | `supports` |
| `lrzip` | 13 | 0.188-1.559 | 0.8971-0.9884 | 0.9824-1.055 | 0-1 | 0.3333-1 | `inconclusive` |
| `x264` | 9 | 0.8459-0.9509 | 0.7312-0.7725 | 0.9326-0.9508 | 0.2857-0.5714 | 0.25-0.6667 | `refutes` |
| `xz` | 13 | 0.3067-1.534 | 0.6615-0.9726 | 0.8191-0.9847 | 0-0.8571 | 0.375-0.75 | `supports` |
| `z3` | 12 | 0.2434-1.861 | 0.6808-0.9853 | 0.6576-0.9961 | 0.2857-1 | 0.3333-1 | `supports` |

## Files

- `all_workload_summary.csv`: concatenated workload rows from every system.
- `system_summary.csv`: one row per system with workload ranges and H5a verdicts.
- `fig_cost_cv_range_by_system.png`: cost heterogeneity range by system.
- `fig_rq2_proxy_spearman_range_by_system.png`: sample-size ordering quality by system.
- `fig_rq2_median_calibration_range_by_system.png`: calibration range by system.
- `fig_rq3_rq4_decision_range_by_system.png`: top-1 agreement and Pareto Jaccard ranges by system.

