# Generated sampling pilot on workload-impact `z3`

## Scope

Source archive: `workload-impact-ICSE2023/artifact_excluding_raw_coverage.zip`

Source member(s): `icse22_supplementary-main/dashboard/resources/z3/sample.csv + icse22_supplementary-main/dashboard/resources/z3/measurements.csv`

Target column: `time`. Cost column: `time`.

Workloads analyzed: `AUFNIRA_z3.637557.smt2, LRA_formula_277.smt2, QF_AUFBV_891_sqlite3.smt2, QF_AUFLIA_swap_t1_pp_nf_ai_00010_002.cvc.smt2, QF_BV_bench_3176.smt2, QF_BV_bench_935.smt2, QF_LIA_tightrhombus, QF_LRA_clocksynchro_7clocks.worst_case_skew.induct.smt2, QF_NRA_hong_9.smt2, QF_RDL_orb08_888.smt2, QF_UFLIA_xs_23_43.smt2, QF_UF_PEQ018_size6.smt2`

Encoded feature columns: `12`.

This pilot reuses the Twins-style generated-sampling protocol on the measured configuration universe provided by the ICSE 2023 workload dataset. Each workload is treated as a separate context.

## Workload summary

| Workload | Cost CV | Spearman rho | Median %cost/%n | Top-1 flips | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---:|---:|---|
| `AUFNIRA_z3.637557.smt2` | 1.458 | 0.7167 | 0.7241 | 0 / 7 | 1 | `cheapOracle_n8` |
| `LRA_formula_277.smt2` | 0.3453 | 0.9723 | 0.9961 | 2 / 7 | 0.5 | `diversity_n51` |
| `QF_AUFBV_891_sqlite3.smt2` | 1.006 | 0.8233 | 0.9276 | 1 / 7 | 1 | `cheapOracle_n64` |
| `QF_AUFLIA_swap_t1_pp_nf_ai_00010_002.cvc.smt2` | 0.5021 | 0.9486 | 0.9468 | 5 / 7 | 0.6 | `balanced_n51` |
| `QF_BV_bench_3176.smt2` | 1.611 | 0.7161 | 0.8767 | 0 / 7 | 1 | `cheapOracle_n8` |
| `QF_BV_bench_935.smt2` | 1.553 | 0.7356 | 0.9104 | 0 / 7 | 1 | `cheapOracle_n8` |
| `QF_LIA_tightrhombus` | 0.7036 | 0.9 | 0.9318 | 1 / 7 | 0.75 | `balanced_n64` |
| `QF_LRA_clocksynchro_7clocks.worst_case_skew.induct.smt2` | 0.2555 | 0.9834 | 0.9748 | 1 / 7 | 0.4286 | `diversity_n51` |
| `QF_NRA_hong_9.smt2` | 0.2833 | 0.9835 | 0.9833 | 0 / 7 | 1 | `random_n51` |
| `QF_RDL_orb08_888.smt2` | 0.2434 | 0.9853 | 0.9856 | 0 / 7 | 0.6667 | `diversity_n51` |
| `QF_UFLIA_xs_23_43.smt2` | 0.6626 | 0.9347 | 0.8959 | 3 / 7 | 0.3333 | `pairwise_n51` |
| `QF_UF_PEQ018_size6.smt2` | 1.861 | 0.6808 | 0.6576 | 0 / 7 | 0.6667 | `balanced_n51` |

## Readout

Highest heterogeneity: `QF_UF_PEQ018_size6.smt2` with CV=1.861.

Least count-stable workload: `QF_AUFLIA_swap_t1_pp_nf_ai_00010_002.cvc.smt2` with 5 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `QF_UF_PEQ018_size6.smt2` with Spearman rho=0.6808.

## H5a

Verdict: `supports`. K-W on 12 inputs: p=4.82e-103; eta^2=0.0637; ratio spread=0.338

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
