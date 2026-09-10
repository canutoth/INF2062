# Learner Sensitivity Protocol

This artifact treats the learner as a variation point while keeping each family-specific sampling/cost protocol fixed.

| Family | Units | Sampling protocol | Primary learner in main artifacts | Learners varied here | Notes |
|---|---|---|---|---|---|
| `REPLICATION` | x264 input/scenario rows and NewRuns systems | Published sample traces; budgeted rerun uses a capped number of published repetitions | Literature-aligned regression where possible; current scripts use ridge/log-linear as the reproducible implementation | `ridge-log`, `rf-log`, `gbt-log` | This is the family where the original rationale for the baseline learner is strongest. RQ1/RQ2 are learner-independent. |
| `ENERGY` | Twins cost-target scenarios | Generated common pool sampling | `ridge-log` | `ridge-log`, `rf-log`, `gbt-log` | Learner affects only MRE-driven RQ3/RQ4 and any RQ5 claim using MRE. |
| `WORKLOAD` | System-workload contexts | Generated common pool sampling per workload | `ridge-log` | `ridge-log`, `rf-log`, `gbt-log` | Workload sensitivity in RQ1/RQ2 is unchanged; decision stability can move with learner accuracy. |
| `LCBENCH` | OpenML datasets | Generated common pool sampling per dataset | `ridge-raw` | `ridge-raw`, `rf-raw`, `gbt-raw` | Accuracy is bounded in [0,1], so raw-target learners are the cleaner default. |
| `LINUX` | Kernel releases | Pool subsampling on TuxKConfig releases | `ridge-log` | `ridge-log`, `rf-log`, `gbt-log` | The sensitivity pass uses reduced levels/runs by default because full Linux learner sweeps are expensive. |

Interpretation rule: do not compare families as if they shared identical sampling protocols. Compare whether learner changes alter the within-family RQ3/RQ4 conclusions.
