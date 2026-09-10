# Strong learner decision robustness

This diagnostic separates prediction accuracy from decision-level conclusions.

Scope note: this is not yet a full paper update. The broad RF run was stopped
because repeated 200-tree RF fits were too slow in the matrix protocol. ENERGY
and LCBENCH could not be rerun in this session because their source files are no
longer present at the expected `/private/tmp` paths. Existing earlier artifacts
still cover the lightweight learner sensitivity for those families.

## Workload slices

| System | Contexts | Ridge MRE | HGBT MRE | Ridge top-1 | HGBT top-1 | Ridge Pareto | HGBT Pareto | Best pair changed | Best strategy changed |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `batik` | 11 | 0.0584 | 0.1186 | 0.7143 | 0.7143 | 0.5000 | 0.5000 | 11 | 10 |
| `dconvert` | 12 | 0.0411 | 0.0485 | 0.9286 | 0.4286 | 0.4444 | 0.4643 | 9 | 9 |
| `h2` | 8 | 0.0660 | 0.0555 | 0.8571 | 0.7143 | 0.4580 | 0.3205 | 7 | 3 |
| `jump3r` | 6 | 0.2069 | 0.2118 | 0.4286 | 0.6429 | 0.5000 | 0.4722 | 5 | 5 |
| `kanzi` | 9 | 0.8506 | 0.8632 | 0.5714 | 0.7143 | 1.0000 | 1.0000 | 4 | 4 |
| `lrzip` | 13 | 0.4693 | 0.4544 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 4 | 3 |

## Linux feature effect

| Release | HGBT all features, 10k | HGBT top-k 512, 10k | Top-k / all ratio |
|---|---:|---:|---:|
| `413` | 0.0645 | 0.1896 | 2.94 |
| `415` | 0.0586 | 0.3046 | 5.20 |
| `420` | 0.0581 | 0.3141 | 5.41 |
| `500` | 0.0572 | 0.2922 | 5.11 |
| `504` | 0.0585 | 0.3140 | 5.37 |
| `507` | 0.0592 | 0.3152 | 5.33 |
| `508` | 0.0561 | 0.2852 | 5.09 |

## Linux 4.13 Decision Check

A focused Linux 4.13 all-feature HGBT run used 1k, 5k, and 10k-scale budgets
with `random`, `balanced`, `cheapOracle`, and `expensiveOracle`.

| Learner/features | Best MRE pair | Best MRE | Top-1 agreement | Pareto Jaccard | Main decision reading |
|---|---|---:|---:|---:|---|
| `sk-hgbt-log`, all features | `balanced_n09997` | 0.0630 | 5/7 | 0.5000 | `balanced` remains the accuracy winner; empirical cost still changes high-cost-penalty recommendations. |

The high-accuracy learner does not make a dominated strategy suddenly become
the universally best sampling strategy. It does, however, change the useful
frontier: `cheapOracle_n01000` becomes empirically Pareto-efficient because it
is extremely cheap, even though its MRE is poor. At high cost penalty
(`lambda` 4 and 10), empirical-cost ranking switches from `balanced_n01000` to
`cheapOracle_n01000`.

## Reading

- RQ1/RQ2 remain learner-independent because they use sampled configurations and empirical costs.
- Strong learners can substantially change MRE and the selected best pair.
- The count-cost versus empirical-cost disagreement does not disappear in the completed workload slices.
- For Linux, feature representation dominates: HGBT with all features is paper-like, while HGBT with top-k 512 remains poor.
