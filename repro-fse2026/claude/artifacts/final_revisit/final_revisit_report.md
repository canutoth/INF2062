# Final revisit learner-policy bundle

## Methodological policy

For `REPLICATION-ICSE19` and `REPLICATION-ICPE20`, the main paper should present the original/literature-aligned learner as the primary result because the scientific question is a revisit of published sampling assessments. Strong sklearn learners are robustness checks, not replacements for the replication baseline.

For generated or newly framed families, the main paper should present the strongest validated learner available for the family. In the final completed artifacts this means sklearn HGBT for `WORKLOAD` and `LINUX`; `LCBENCH` and `ENERGY` remain reported with their completed generated-sampling artifacts unless stronger reruns are available. Random forests and boosted trees are treated as strong off-the-shelf sensitivity baselines, using sklearn implementations.

RQ1 and RQ2 are learner-independent by construction. Learner sensitivity is therefore evaluated through RQ3/RQ4: prediction error, top-1 agreement, and Pareto-front overlap.

## Primary artifacts

| Family | Learner | Scope | Root |
|---|---|---|---|
| `REPLICATION-ICSE19` | `original/literature regression` | full 7-system published-trace revisit | `artifacts/newruns_systems` |
| `REPLICATION-ICPE20` | `original/literature regression` | full 17-input published-trace x264 revisit | `artifacts/x264_matrix` |
| `ENERGY` | `ridge-log` | representative generated-sampling energy/performance batch | `artifacts/twins_generated_representative_100s` |
| `WORKLOAD` | `sk-hgbt-log` | full 9-system workload batch with sklearn HGBT | `artifacts/strong_learner_overnight/workload/sk-hgbt-log` |
| `LCBENCH` | `ridge-raw` | 35-dataset external-validation batch | `artifacts/lcbench_data_2k_lw` |
| `LINUX` | `sk-hgbt-log` | full 7-release all-feature full-strategy sklearn HGBT batch | `artifacts/linux_hgbt_full_strategy` |

## Sensitivity artifacts

| Family | Learner | Scope | Root |
|---|---|---|---|
| `REPLICATION-ICSE19` | `sk-rf-log` | full 7-system sklearn random-forest sensitivity | `artifacts/strong_learner_overnight/replication/sk-rf-log/newruns` |
| `REPLICATION-ICSE19` | `sk-hgbt-log` | full 7-system sklearn HGBT sensitivity | `artifacts/strong_learner_overnight/replication/sk-hgbt-log/newruns` |
| `REPLICATION-ICPE20` | `sk-hgbt-log` | bounded 3-input HGBT slice; not a replacement for the full x264 result | `artifacts/strong_learner_overnight/replication/sk-hgbt-log/x264_matrix_slice` |
| `WORKLOAD` | `ridge-log` | full 9-system workload batch with lightweight learner | `artifacts/workload_batch_overnight` |
| `LCBENCH` | `sk-hgbt-raw` | 35-dataset sklearn HGBT revisit | `artifacts/lcbench_data_2k_lw_skhgbt` |

## Headline learner-sensitivity reading

- Stronger learners improve absolute prediction accuracy in the Linux all-feature setting, reaching best MRE around 6--11% across releases.
- The main count-vs-empirical-cost conclusion survives: RQ3/RQ4 decision disagreements remain visible under sklearn HGBT/RF.
- In `REPLICATION-ICSE19`, HGBT/RF leave H1/H2 verdicts unchanged and keep H3a refuted globally; H4 support strengthens from 5/7 to 6/7.
- In `WORKLOAD`, HGBT leaves all system-level verdicts unchanged except H3b becomes supported rather than inconclusive.
- In `LINUX`, full-strategy all-feature HGBT supports H1a, H1b, H2a, H2c, H3a, H4a, and H4b; H2b is refuted because aggregate calibration is close to 1 even though strategy-specific calibration differs.

## Generated files

- `manifest.csv`: source roots and report paths.
- `hypothesis_by_family_learner.csv`: final hypothesis verdicts by learner/family.
- `decision_by_family_learner.csv`: MRE and decision metrics where available.
- `fig_hypothesis_support_by_family.png`: hypothesis support heatmap.
- `fig_decision_sensitivity.png`: top-1/Pareto decision comparison.
