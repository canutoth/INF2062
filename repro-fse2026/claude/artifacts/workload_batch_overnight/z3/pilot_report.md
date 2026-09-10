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
| `AUFNIRA_z3.637557.smt2` | 1.458 | 0.7166 | 0.7256 | 0 / 7 | 1 | `cheapOracle_n8` |
| `LRA_formula_277.smt2` | 0.3453 | 0.9719 | 0.9958 | 1 / 7 | 0.6364 | `diversity_n32` |
| `QF_AUFBV_891_sqlite3.smt2` | 1.006 | 0.824 | 0.9294 | 2 / 7 | 1 | `cheapOracle_n51` |
| `QF_AUFLIA_swap_t1_pp_nf_ai_00010_002.cvc.smt2` | 0.5021 | 0.9485 | 0.9433 | 6 / 7 | 0.4286 | `diversity_n21` |
| `QF_BV_bench_3176.smt2` | 1.611 | 0.7127 | 0.8767 | 0 / 7 | 1 | `cheapOracle_n8` |
| `QF_BV_bench_935.smt2` | 1.553 | 0.735 | 0.9144 | 0 / 7 | 1 | `cheapOracle_n8` |
| `QF_LIA_tightrhombus` | 0.7036 | 0.9008 | 0.9308 | 6 / 7 | 0.5 | `pairwise_n64` |
| `QF_LRA_clocksynchro_7clocks.worst_case_skew.induct.smt2` | 0.2555 | 0.9835 | 0.9745 | 3 / 7 | 0.4615 | `diversity_n21` |
| `QF_NRA_hong_9.smt2` | 0.2833 | 0.9832 | 0.9833 | 3 / 7 | 0.4667 | `diversity_n32` |
| `QF_RDL_orb08_888.smt2` | 0.2434 | 0.9849 | 0.9857 | 4 / 7 | 0.4667 | `diversity_n32` |
| `QF_UFLIA_xs_23_43.smt2` | 0.6626 | 0.9341 | 0.8953 | 5 / 7 | 0.4167 | `diversity_n21` |
| `QF_UF_PEQ018_size6.smt2` | 1.861 | 0.6783 | 0.6611 | 7 / 7 | 0.8571 | `pilotCost_n32` |

## Readout

Highest heterogeneity: `QF_UF_PEQ018_size6.smt2` with CV=1.861.

Least count-stable workload: `QF_UF_PEQ018_size6.smt2` with 7 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `QF_UF_PEQ018_size6.smt2` with Spearman rho=0.6783.

## H5a

Verdict: `supports`. K-W on 12 inputs: p=6.85e-102; eta^2=0.063; ratio spread=0.335

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
