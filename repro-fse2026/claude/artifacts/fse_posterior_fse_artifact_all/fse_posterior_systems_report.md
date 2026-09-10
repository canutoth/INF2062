# FSE-style posterior cross-system cost-normalization report

## Scope

This is the FSE posterior-risk/posterior-confidence experiment mapped onto the paper's RQ1-RQ5 protocol. Posterior risk/confidence replaces MRE as the outcome for ranking and Pareto decisions.

Systems: 7z, BerkeleyDBC, Dune, Hipacc, JavaGC, LLVM, Polly.
Strategies: `random,solverBased,divDistBased,twise,SRSSampling`. Levels: `t2`.

## Headline

Cost-normalization changed the top integrated-confidence recommendation in 2/7 systems. The empirical confidence Pareto frontier changed in 6/7 systems.

SRS was the single best empirical-cost-normalized recommendation in 3/7 systems and appeared on the empirical cost/confidence Pareto frontier in 6/7 systems.

Best empirical-cost-normalized pairs by system:

- `SRSSampling_t2`: 3/7
- `divDistBased_t2`: 2/7
- `twise_t2`: 1/7
- `random_t2`: 1/7

## RQ1: Empirical Cost Heterogeneity

| System | #configs | Cost CV | p90/p10 | Calibration range |
|---|---:|---:|---:|---:|
| `7z` | 68640 | 1.188 | 10.13 | 0.6284-1.716 |
| `BerkeleyDBC` | 2560 | 1.42 | 47.9 | 0.1863-3.112 |
| `Dune` | 2304 | 0.3438 | 1.827 | 0.9981-1.082 |
| `Hipacc` | 13485 | 0.4352 | 2.59 | 0.792-1.135 |
| `JavaGC` | 193536 | 1.025 | 7.842 | 0.6251-1.704 |
| `LLVM` | 1024 | 0.07236 | 1.212 | 0.9161-1.04 |
| `Polly` | 60000 | 0.2389 | 2.076 | 0.7189-1.016 |

Take-away: fixed sample size is not fixed empirical effort. The same t2 budget can select substantially cheaper or costlier configurations depending on the system and strategy.

## RQ2: Sample Size As Cost Proxy

| System | Median %cost/%n | Min %cost/%n | Max %cost/%n |
|---|---:|---:|---:|
| `7z` | 0.9888 | 0.6284 | 1.716 |
| `BerkeleyDBC` | 0.8503 | 0.1863 | 3.112 |
| `Dune` | 0.9997 | 0.9981 | 1.082 |
| `Hipacc` | 1.096 | 0.792 | 1.135 |
| `JavaGC` | 0.9931 | 0.6251 | 1.704 |
| `LLVM` | 1.001 | 0.9161 | 1.04 |
| `Polly` | 0.9987 | 0.7189 | 1.016 |

Take-away: in this fixed-budget FSE run, RQ2 is mainly about calibration rather than correlation across many n values. The count budget is useful for experiment design, but it does not represent the actual acquisition budget equally across strategies.

## RQ3: Cost-Normalized Recommendation

| System | Best by size baseline | Best by empirical-cost baseline | Changed? | SRS best? |
|---|---|---|---:|---:|
| `7z` | `SRSSampling_t2` | `twise_t2` | 1 | 0 |
| `BerkeleyDBC` | `SRSSampling_t2` | `random_t2` | 1 | 0 |
| `Dune` | `SRSSampling_t2` | `SRSSampling_t2` | 0 | 1 |
| `Hipacc` | `divDistBased_t2` | `divDistBased_t2` | 0 | 0 |
| `JavaGC` | `SRSSampling_t2` | `SRSSampling_t2` | 0 | 1 |
| `LLVM` | `divDistBased_t2` | `divDistBased_t2` | 0 | 0 |
| `Polly` | `SRSSampling_t2` | `SRSSampling_t2` | 0 | 1 |

Take-away: posterior guarantees can change the recommendation once empirical cost is used. SRS often remains competitive, but it is not a universal cost-normalized winner.

## RQ4: Pareto-Efficient Choices

| System | Jaccard | Count confidence front | Empirical confidence front | SRS on empirical front? |
|---|---:|---|---|---:|
| `7z` | 0.5 | `SRSSampling_t2` | `twise_t2,SRSSampling_t2` | 1 |
| `BerkeleyDBC` | 0.2 | `SRSSampling_t2` | `random_t2,solverBased_t2,divDistBased_t2,twise_t2,SRSSampling_t2` | 1 |
| `Dune` | 0.25 | `SRSSampling_t2` | `random_t2,divDistBased_t2,twise_t2,SRSSampling_t2` | 1 |
| `Hipacc` | 0.25 | `divDistBased_t2` | `random_t2,divDistBased_t2,twise_t2,SRSSampling_t2` | 1 |
| `JavaGC` | 0.3333 | `SRSSampling_t2` | `divDistBased_t2,twise_t2,SRSSampling_t2` | 1 |
| `LLVM` | 1 | `divDistBased_t2,twise_t2` | `divDistBased_t2,twise_t2` | 0 |
| `Polly` | 0.2 | `SRSSampling_t2` | `random_t2,solverBased_t2,divDistBased_t2,twise_t2,SRSSampling_t2` | 1 |

Take-away: the empirical-cost Pareto front is often not the same front as the count-cost front. This is the clearest decision-level evidence that sample size hides cost/guarantee tradeoffs.

## RQ5: Cross-System Sensitivity

| System | Best risk pair | Best cost pair | SRS risk | SRS %cost | SRS-vs-random risk | SRS-vs-random cost |
|---|---|---|---:|---:|---|---|
| `7z` | `SRSSampling_t2` | `twise_t2` | 0.0001311 | 0.015 | `supports` | `supports` |
| `BerkeleyDBC` | `SRSSampling_t2` | `random_t2` | 0.0007813 | 0.1179 | `supports` | `supports` |
| `Dune` | `SRSSampling_t2` | `SRSSampling_t2` | 0.000434 | 0.1242 | `supports` | `supports` |
| `Hipacc` | `solverBased_t2` | `divDistBased_t2` | 0.0002595 | 0.06855 | `supports` | `supports` |
| `JavaGC` | `SRSSampling_t2` | `SRSSampling_t2` | 0.0001576 | 0.004121 | `supports` | `supports` |
| `LLVM` | `solverBased_t2` | `divDistBased_t2` | 0.003906 | 0.05685 | `supports` | `supports` |
| `Polly` | `divDistBased_t2` | `SRSSampling_t2` | 0.0016 | 0.005841 | `inconclusive` | `supports` |

Take-away: the answer is system-dependent. The FSE posterior framework is useful because it makes this variability visible: a strategy may be excellent for low posterior risk yet lose when the empirical cost of acquiring its configurations is included.

## Hypothesis Verdict Counts

| Hypothesis | Supports | Refutes | Inconclusive |
|---|---:|---:|---:|
| `FSE1` | 7 | 0 | 0 |
| `FSE2` | 2 | 5 | 0 |
| `FSE3` | 3 | 4 | 0 |
| `FSE4` | 6 | 1 | 0 |
| `FSE5` | 6 | 0 | 1 |
| `FSE6` | 7 | 0 | 0 |

## Per-System Reports

- [`7z`](7z/7z_fse_posterior_report.md)
- [`BerkeleyDBC`](BerkeleyDBC/BerkeleyDBC_fse_posterior_report.md)
- [`Dune`](Dune/Dune_fse_posterior_report.md)
- [`Hipacc`](Hipacc/Hipacc_fse_posterior_report.md)
- [`JavaGC`](JavaGC/JavaGC_fse_posterior_report.md)
- [`LLVM`](LLVM/LLVM_fse_posterior_report.md)
- [`Polly`](Polly/Polly_fse_posterior_report.md)
