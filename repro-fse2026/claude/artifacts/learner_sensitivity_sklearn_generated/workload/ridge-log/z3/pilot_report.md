# Generated sampling pilot on workload-impact `z3`

## Scope

Source archive: `/Users/mathieuacher/SANDBOX/cost-sampling-matters/workload-impact-ICSE2023/artifact_excluding_raw_coverage.zip`

Source member(s): `icse22_supplementary-main/dashboard/resources/z3/sample.csv + icse22_supplementary-main/dashboard/resources/z3/measurements.csv`

Target column: `time`. Cost column: `time`.

Workloads analyzed: `AUFNIRA_z3.637557.smt2, LRA_formula_277.smt2, QF_AUFBV_891_sqlite3.smt2, QF_AUFLIA_swap_t1_pp_nf_ai_00010_002.cvc.smt2, QF_BV_bench_3176.smt2, QF_BV_bench_935.smt2, QF_LIA_tightrhombus, QF_LRA_clocksynchro_7clocks.worst_case_skew.induct.smt2, QF_NRA_hong_9.smt2, QF_RDL_orb08_888.smt2, QF_UFLIA_xs_23_43.smt2, QF_UF_PEQ018_size6.smt2`

Encoded feature columns: `12`.

This pilot reuses the Twins-style generated-sampling protocol on the measured configuration universe provided by the ICSE 2023 workload dataset. Each workload is treated as a separate context.

## Workload summary

| Workload | Cost CV | Spearman rho | Median %cost/%n | Top-1 flips | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---:|---:|---|
| `AUFNIRA_z3.637557.smt2` | 1.458 | 0.625 | 0.7495 | 1 / 7 | 1 | `pilotCost_n21` |
| `LRA_formula_277.smt2` | 0.3453 | 0.9595 | 1.005 | 2 / 7 | 0.6364 | `random_n32` |
| `QF_AUFBV_891_sqlite3.smt2` | 1.006 | 0.7239 | 0.9396 | 2 / 7 | 1 | `cheapOracle_n51` |
| `QF_AUFLIA_swap_t1_pp_nf_ai_00010_002.cvc.smt2` | 0.5021 | 0.9032 | 0.9623 | 6 / 7 | 0.3333 | `diversity_n21` |
| `QF_BV_bench_3176.smt2` | 1.611 | 0.6793 | 0.9525 | 7 / 7 | 0.5 | `pilotCost_n8` |
| `QF_BV_bench_935.smt2` | 1.553 | 0.7016 | 0.9536 | 2 / 7 | 1 | `pilotCost_n11` |
| `QF_LIA_tightrhombus` | 0.7036 | 0.806 | 0.9401 | 6 / 7 | 0.4545 | `pairwise_n64` |
| `QF_LRA_clocksynchro_7clocks.worst_case_skew.induct.smt2` | 0.2555 | 0.9725 | 0.9858 | 2 / 7 | 0.4615 | `diversity_n21` |
| `QF_NRA_hong_9.smt2` | 0.2833 | 0.9789 | 0.9845 | 3 / 7 | 0.5385 | `diversity_n32` |
| `QF_RDL_orb08_888.smt2` | 0.2434 | 0.9747 | 0.9876 | 3 / 7 | 0.5385 | `diversity_n32` |
| `QF_UFLIA_xs_23_43.smt2` | 0.6626 | 0.8741 | 0.9063 | 7 / 7 | 0.4 | `diversity_n21` |
| `QF_UF_PEQ018_size6.smt2` | 1.861 | 0.5846 | 0.7023 | 2 / 7 | 1 | `pilotCost_n32` |

## Readout

Highest heterogeneity: `QF_UF_PEQ018_size6.smt2` with CV=1.861.

Least count-stable workload: `QF_BV_bench_3176.smt2` with 7 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `QF_UF_PEQ018_size6.smt2` with Spearman rho=0.5846.

## H5a

Verdict: `supports`. K-W on 12 inputs: p=7.69e-12; eta^2=0.0412; ratio spread=0.302

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
