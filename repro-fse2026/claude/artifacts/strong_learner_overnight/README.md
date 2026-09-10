# Strong Learner Overnight Batch

## Purpose

Collect evidence for the learner policy:

- keep original/literature learners for reproducibility-sensitive families;
- use sklearn HGBT as the strong default where we choose the learner;
- report learner sensitivity at the decision level, not only MRE.

## Planned Jobs

| Family | Label | Learner | Output |
|---|---|---|---|
| `REPLICATION` | `x264_matrix` | `sk-hgbt-log` | `/Users/mathieuacher/SANDBOX/cost-sampling-matters/artifacts/strong_learner_overnight/replication/sk-hgbt-log/x264_matrix` |
| `REPLICATION` | `newruns` | `sk-hgbt-log` | `/Users/mathieuacher/SANDBOX/cost-sampling-matters/artifacts/strong_learner_overnight/replication/sk-hgbt-log/newruns` |
| `WORKLOAD` | `all_systems` | `sk-hgbt-log` | `/Users/mathieuacher/SANDBOX/cost-sampling-matters/artifacts/strong_learner_overnight/workload/sk-hgbt-log` |
| `LINUX` | `413` | `sk-hgbt-log-allfeatures` | `/Users/mathieuacher/SANDBOX/cost-sampling-matters/artifacts/strong_learner_overnight/linux/sk-hgbt-log-allfeatures/linux413_vmlinux` |
| `LINUX` | `415` | `sk-hgbt-log-allfeatures` | `/Users/mathieuacher/SANDBOX/cost-sampling-matters/artifacts/strong_learner_overnight/linux/sk-hgbt-log-allfeatures/linux415_vmlinux` |
| `LINUX` | `420` | `sk-hgbt-log-allfeatures` | `/Users/mathieuacher/SANDBOX/cost-sampling-matters/artifacts/strong_learner_overnight/linux/sk-hgbt-log-allfeatures/linux420_vmlinux` |
| `LINUX` | `500` | `sk-hgbt-log-allfeatures` | `/Users/mathieuacher/SANDBOX/cost-sampling-matters/artifacts/strong_learner_overnight/linux/sk-hgbt-log-allfeatures/linux500_vmlinux` |
| `LINUX` | `504` | `sk-hgbt-log-allfeatures` | `/Users/mathieuacher/SANDBOX/cost-sampling-matters/artifacts/strong_learner_overnight/linux/sk-hgbt-log-allfeatures/linux504_vmlinux` |
| `LINUX` | `507` | `sk-hgbt-log-allfeatures` | `/Users/mathieuacher/SANDBOX/cost-sampling-matters/artifacts/strong_learner_overnight/linux/sk-hgbt-log-allfeatures/linux507_vmlinux` |
| `LINUX` | `508` | `sk-hgbt-log-allfeatures` | `/Users/mathieuacher/SANDBOX/cost-sampling-matters/artifacts/strong_learner_overnight/linux/sk-hgbt-log-allfeatures/linux508_vmlinux` |
| `REPLICATION` | `newruns` | `sk-rf-log` | `/Users/mathieuacher/SANDBOX/cost-sampling-matters/artifacts/strong_learner_overnight/replication/sk-rf-log/newruns` |

## Inputs

- Workload seeds: `30`
- Workload max budget: `64`
- x264/NewRuns max runs: `100`
- x264 contexts: `0-16`
- Linux levels: `0.0108,0.0540,0.1080`
- Linux stochastic runs: `3`

ENERGY and LCBENCH jobs are included only if their source files exist at the expected `/private/tmp` paths.
