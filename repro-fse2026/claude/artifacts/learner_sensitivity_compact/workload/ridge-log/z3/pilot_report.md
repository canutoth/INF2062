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
| `AUFNIRA_z3.637557.smt2` | 1.458 | 0.1509 | 0.651 | 6 / 7 | 0.6667 | `pilotCost_n16` |
| `LRA_formula_277.smt2` | 0.3453 | 0.7547 | 1.009 | 3 / 7 | 0.75 | `diversity_n16` |
| `QF_AUFBV_891_sqlite3.smt2` | 1.006 | 0.3632 | 0.9608 | 0 / 7 | 1 | `cheapOracle_n8` |
| `QF_AUFLIA_swap_t1_pp_nf_ai_00010_002.cvc.smt2` | 0.5021 | 0.5754 | 0.9761 | 7 / 7 | 0.3333 | `diversity_n16` |
| `QF_BV_bench_3176.smt2` | 1.611 | 0.3066 | 0.878 | 0 / 7 | 1 | `pilotCost_n16` |
| `QF_BV_bench_935.smt2` | 1.553 | 0.3066 | 0.8198 | 0 / 7 | 1 | `cheapOracle_n8` |
| `QF_LIA_tightrhombus` | 0.7036 | 0.4386 | 0.9767 | 7 / 7 | 0.4 | `pairwise_n16` |
| `QF_LRA_clocksynchro_7clocks.worst_case_skew.induct.smt2` | 0.2555 | 0.7971 | 0.9845 | 3 / 7 | 0.4286 | `pairwise_n16` |
| `QF_NRA_hong_9.smt2` | 0.2833 | 0.8397 | 0.9959 | 4 / 7 | 0.4286 | `diversity_n16` |
| `QF_RDL_orb08_888.smt2` | 0.2434 | 0.8254 | 0.9963 | 6 / 7 | 0.4286 | `diversity_n16` |
| `QF_UFLIA_xs_23_43.smt2` | 0.6626 | 0.4952 | 0.9119 | 7 / 7 | 0.6 | `diversity_n16` |
| `QF_UF_PEQ018_size6.smt2` | 1.861 | 0.1321 | 0.6137 | 5 / 7 | 0.5 | `pilotCost_n8` |

## Readout

Highest heterogeneity: `QF_UF_PEQ018_size6.smt2` with CV=1.861.

Least count-stable workload: `QF_AUFLIA_swap_t1_pp_nf_ai_00010_002.cvc.smt2` with 7 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `QF_UF_PEQ018_size6.smt2` with Spearman rho=0.1321.

## H5a

Verdict: `inconclusive`. K-W on 12 inputs: p=0.127; eta^2=0.0155; ratio spread=0.395

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
