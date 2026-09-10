# Workload-impact hypothesis report

Input batch: `/Users/mathieuacher/SANDBOX/cost-sampling-matters/artifacts/strong_learner_overnight/workload/sk-hgbt-log`.

## Global verdicts

- `H1a`: supported (9/9) (9 support, 0 refute, 0 inconclusive)
- `H2a`: supported (9/9) (9 support, 0 refute, 0 inconclusive)
- `H2b`: supported (6/9) (6 support, 0 refute, 3 inconclusive)
- `H3a`: supported (9/9) (9 support, 0 refute, 0 inconclusive)
- `H3b`: supported (1/1) (1 support, 0 refute, 0 inconclusive)
- `H4a`: supported (9/9) (9 support, 0 refute, 0 inconclusive)
- `H4b`: supported (9/9) (9 support, 0 refute, 0 inconclusive)
- `H5a`: supported (5/9) (5 support, 2 refute, 2 inconclusive)
- `H5c`: supported (9/9) (9 support, 0 refute, 0 inconclusive)

## Readout

- Strongest H1a case: `kanzi` with max CV `2.367`.
- Weakest H2a case: `kanzi` with min Spearman rho `0.5724`.
- Least stable H3a case: `dconvert` with min top-1 agreement `0`.
- Strongest H4b disagreement: `kanzi` with min Pareto Jaccard `0.25`.

## Per-system workload hypotheses

| System | H1a | H2a | H2b | H3a | H4b | H5a | H5c |
|---|---|---|---|---|---|---|---|
| `batik` | `supports` | `supports` | `supports` | `supports` | `supports` | `supports` | `supports` |
| `dconvert` | `supports` | `supports` | `inconclusive` | `supports` | `supports` | `supports` | `supports` |
| `h2` | `supports` | `supports` | `inconclusive` | `supports` | `supports` | `inconclusive` | `supports` |
| `jump3r` | `supports` | `supports` | `inconclusive` | `supports` | `supports` | `refutes` | `supports` |
| `kanzi` | `supports` | `supports` | `supports` | `supports` | `supports` | `supports` | `supports` |
| `lrzip` | `supports` | `supports` | `supports` | `supports` | `supports` | `inconclusive` | `supports` |
| `x264` | `supports` | `supports` | `supports` | `supports` | `supports` | `refutes` | `supports` |
| `xz` | `supports` | `supports` | `supports` | `supports` | `supports` | `supports` | `supports` |
| `z3` | `supports` | `supports` | `supports` | `supports` | `supports` | `supports` | `supports` |

## Output Files

- `hypothesis_tests.csv`: one row per system-level or global workload-batch hypothesis test.
- `hypothesis_summary.csv`: support/refute/inconclusive counts per hypothesis.
- `fig_workload_hypothesis_verdicts.png`: stacked verdict-count figure.
