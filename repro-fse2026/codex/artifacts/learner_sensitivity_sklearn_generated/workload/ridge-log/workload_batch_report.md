# Workload-impact cross-system report

Input batch: `/Users/mathieuacher/SANDBOX/cost-sampling-matters/artifacts/learner_sensitivity_sklearn_generated/workload/ridge-log`.

## Scope

Systems covered: `9`. Workload contexts covered: `93`.

Target/cost setup: `8` runtime systems plus `1` throughput-oriented system (`h2`, with cost = `1/throughput`).

## Readout

Highest observed cost heterogeneity: `kanzi` with workload-level CV up to `2.367`.

Weakest count-cost proxy: `kanzi` with workload-level Spearman rho down to `0.5089`.

Least stable top-1 decisions: `x264` with workload-level agreement as low as `0`.

Strongest Pareto disagreement: `x264` with workload-level Jaccard down to `0.2308`.

H5a workload sensitivity is supported in `5 / 9` systems.

## Systems

| System | Workloads | Cost CV range | Spearman rho range | Median %cost/%n range | Top-1 agreement range | Pareto Jaccard range | H5a |
|---|---:|---:|---:|---:|---:|---:|---|
| `batik` | 11 | 0.1195-1.027 | 0.8118-0.9793 | 0.8729-0.9883 | 0.1429-1 | 0.4-0.6 | `supports` |
| `dconvert` | 12 | 0.02639-0.3828 | 0.9093-0.9684 | 0.9572-0.9982 | 0.1429-1 | 0.3333-0.6 | `supports` |
| `h2` | 8 | 0.1053-0.2994 | 0.942-0.9807 | 0.9877-0.9936 | 0.5714-1 | 0.3846-0.5714 | `refutes` |
| `jump3r` | 6 | 0.3606-0.5851 | 0.8327-0.9201 | 0.974-0.9918 | 0.2857-0.7143 | 0.3846-0.7143 | `refutes` |
| `kanzi` | 9 | 0.8084-2.367 | 0.5089-0.845 | 0.7926-1.001 | 0.4286-1 | 0.25-1 | `supports` |
| `lrzip` | 13 | 0.188-1.559 | 0.7758-0.9835 | 0.9466-1.014 | 0.5714-1 | 0.6667-1 | `refutes` |
| `x264` | 9 | 0.8459-0.9509 | 0.6704-0.7258 | 0.9161-0.9735 | 0-0.4286 | 0.2308-0.5 | `refutes` |
| `xz` | 13 | 0.3067-1.534 | 0.6058-0.9296 | 0.7791-0.9722 | 0-0.7143 | 0.2727-0.7143 | `supports` |
| `z3` | 12 | 0.2434-1.861 | 0.5846-0.9789 | 0.7023-1.005 | 0-0.8571 | 0.3333-1 | `supports` |

## Files

- `all_workload_summary.csv`: concatenated workload rows from every system.
- `system_summary.csv`: one row per system with workload ranges and H5a verdicts.
- `fig_cost_cv_range_by_system.png`: cost heterogeneity range by system.
- `fig_rq2_proxy_spearman_range_by_system.png`: sample-size ordering quality by system.
- `fig_rq2_median_calibration_range_by_system.png`: calibration range by system.
- `fig_rq3_rq4_decision_range_by_system.png`: top-1 agreement and Pareto Jaccard ranges by system.

