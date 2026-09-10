# Workload-impact cross-system report

Input batch: `/Users/mathieuacher/SANDBOX/cost-sampling-matters/artifacts/workload_batch_overnight`.

## Scope

Systems covered: `9`. Workload contexts covered: `93`.

Target/cost setup: `8` runtime systems plus `1` throughput-oriented system (`h2`, with cost = `1/throughput`).

## Readout

Highest observed cost heterogeneity: `kanzi` with workload-level CV up to `2.367`.

Weakest count-cost proxy: `kanzi` with workload-level Spearman rho down to `0.5694`.

Least stable top-1 decisions: `xz` with workload-level agreement as low as `0`.

Strongest Pareto disagreement: `xz` with workload-level Jaccard down to `0.1429`.

H5a workload sensitivity is supported in `5 / 9` systems.

## Systems

| System | Workloads | Cost CV range | Spearman rho range | Median %cost/%n range | Top-1 agreement range | Pareto Jaccard range | H5a |
|---|---:|---:|---:|---:|---:|---:|---|
| `batik` | 11 | 0.1195-1.027 | 0.8932-0.9847 | 0.8599-0.9882 | 0.2857-0.8571 | 0.4167-0.8 | `supports` |
| `dconvert` | 12 | 0.02639-0.3828 | 0.922-0.9683 | 0.9525-0.9987 | 0.4286-1 | 0.4-0.75 | `supports` |
| `h2` | 8 | 0.1053-0.2994 | 0.9714-0.9849 | 0.9788-0.9932 | 0.2857-0.8571 | 0.375-0.6 | `inconclusive` |
| `jump3r` | 6 | 0.3606-0.5851 | 0.8995-0.9552 | 0.9638-0.9768 | 0.4286-0.5714 | 0.4444-0.625 | `refutes` |
| `kanzi` | 9 | 0.8084-2.367 | 0.5694-0.9386 | 0.8229-1.002 | 0.2857-1 | 0.25-1 | `supports` |
| `lrzip` | 13 | 0.188-1.559 | 0.8958-0.9884 | 0.9885-1.059 | 0.7143-1 | 0.75-1 | `inconclusive` |
| `x264` | 9 | 0.8459-0.9509 | 0.7315-0.7725 | 0.9308-0.9529 | 0.1429-0.4286 | 0.1765-0.5 | `refutes` |
| `xz` | 13 | 0.3067-1.534 | 0.6622-0.9734 | 0.8191-0.9847 | 0-0.7143 | 0.1429-0.5 | `supports` |
| `z3` | 12 | 0.2434-1.861 | 0.6783-0.9849 | 0.6611-0.9958 | 0-1 | 0.4167-1 | `supports` |

## Files

- `all_workload_summary.csv`: concatenated workload rows from every system.
- `system_summary.csv`: one row per system with workload ranges and H5a verdicts.
- `fig_cost_cv_range_by_system.png`: cost heterogeneity range by system.
- `fig_rq2_proxy_spearman_range_by_system.png`: sample-size ordering quality by system.
- `fig_rq2_median_calibration_range_by_system.png`: calibration range by system.
- `fig_rq3_rq4_decision_range_by_system.png`: top-1 agreement and Pareto Jaccard ranges by system.

