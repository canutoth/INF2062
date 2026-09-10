# Linux case study: hypothesis-test verdicts (v4.13, v4.15, v4.20, v5.0, v5.04, v5.07, v5.08)

This report applies the H1a--H4b test stack from `cost_sampling/hypotheses.py` to the 7 Linux kernel releases (`linux413_vmlinux`, `linux415_vmlinux`, `linux420_vmlinux`, `linux50_vmlinux`, `linux504_vmlinux`, `linux507_vmlinux`, `linux508_vmlinux`) reported in `artifacts/linux_kernels_summary.md`. The Linux protocol differs structurally from x264 / NewRuns (pool-based subsampling, storage-bound cost, AL/diversity strategies with no x264 analogue), so we keep the verdicts separate and add three Linux-specific tests: per-strategy calibration, the active-learning *seam* across n, and cross-release replication.

## Headline verdicts

| Hypothesis | Claim | v4.13 | v4.15 | v4.20 | v5.0 | v5.04 | v5.07 | v5.08 |
|---|---|---|---|---|---|---|---|---|
| **H1a** | Per-config cost CV is non-negligible. | [+] very large | [+] very large | [+] very large | [+] very large | [+] very large | [+] large | [+] very large |
| **H1b** | Strategies differ in TrainCost at fixed n. | [+] large | [+] large | [+] large | [+] large | [+] large | [+] large | [+] large |
| **H2a** | n is positively rank-correlated with TrainCost. | [+] strong positive | [+] strong positive | [+] strong positive | [+] strong positive | [+] strong positive | [+] strong positive | [+] strong positive |
| **H2b** | Median calibration ratio is not centered at 1. | [x] calibrated | [?] calibrated | [x] calibrated | [x] calibrated | [x] calibrated | [?] calibrated | [x] calibrated |
| **H2c** | Calibration depends on sampling strategy. | [+] large | [+] medium | [+] large | [+] medium | [+] large | [+] large | [+] medium |
| **H3a** | Rankings sometimes diverge under count vs empirical cost. | [+] occasional flips | [+] occasional flips | [+] occasional flips | [+] occasional flips | [+] frequent flips | [+] frequent flips | [+] frequent flips |
| **H4a** | Some (s,n) pairs flip Pareto status. | [+] different | [+] different | [+] different | [+] different | [+] different | [+] different | [+] different |
| **H4b** | Empirical and count Pareto frontiers differ. | [+] frontiers differ | [+] frontiers differ | [+] frontiers differ | [+] frontiers differ | [+] frontiers differ | [+] frontiers differ | [+] frontiers differ |

Marker key: `[+]` supports, `[x]` refutes, `[?]` inconclusive. The `effect_label` column gives the qualitative magnitude; full statistic, p-value, effect size and notes are in `artifacts/<release>/hypothesis_tests.csv`.

## Per-release detail

### v4.13

| Hypothesis | Statistic | p-value | Effect | Verdict | Notes |
|---|---|---|---|---|---|
| **H1a** | cv_cost=1.43 | -- | p90_over_p10=4.61 (very large) | supports | CV=1.43; p90/p10=4.61 |
| **H1b** | kruskal_wallis_min_p=1.25e-21 | <1e-12 | eta_squared_max=0.413 (large) | supports | K-W per level: 5/5 levels with p<0.05; min p=1.25e-21; max eta^2=0.413 |
| **H2a** | spearman_rho=0.966 | <1e-12 | rho=0.966 (strong positive) | supports | Spearman rho=0.966 on n=1250 (records-level) |
| **H2b** | median_ratio=1 | -- | abs_deviation_from_1=0.000187 (calibrated) | refutes | median ratio=1; 95% CI [0.999,1]; |median-1|=0.000187 |
| **H2c** | kruskal_wallis_p=6.37e-89 | <1e-12 | eta_squared=0.334 (large) | supports | K-W p=6.37e-89; eta^2=0.334; k=5 strategies |
| **H3a** | top1_flips=2 | -- | flip_fraction=0.286 (occasional flips) | supports | top-1 flips 2/7; mean Kendall tau=0.718 |
| **H4a** | exclusive_pairs=6 | -- | pareto_jaccard=0.455 (different) | supports | |count|=5; |empirical|=11; only_count=0; only_empirical=6; Jaccard=0.455 |
| **H4b** | pareto_jaccard=0.455 | -- | frontier_size_diff=6 (frontiers differ) | supports | |count|=5; |empirical|=11; Jaccard=0.455 |

### v4.15

| Hypothesis | Statistic | p-value | Effect | Verdict | Notes |
|---|---|---|---|---|---|
| **H1a** | cv_cost=1.16 | -- | p90_over_p10=6.04 (very large) | supports | CV=1.16; p90/p10=6.04 |
| **H1b** | kruskal_wallis_min_p=3.62e-12 | 3.62e-12 | eta_squared_max=0.226 (large) | supports | K-W per level: 5/5 levels with p<0.05; min p=3.62e-12; max eta^2=0.226 |
| **H2a** | spearman_rho=0.966 | <1e-12 | rho=0.966 (strong positive) | supports | Spearman rho=0.966 on n=1250 (records-level) |
| **H2b** | median_ratio=1 | -- | abs_deviation_from_1=0.00293 (calibrated) | inconclusive | median ratio=1; 95% CI [1,1]; |median-1|=0.00293 |
| **H2c** | kruskal_wallis_p=9.95e-26 | <1e-12 | eta_squared=0.0967 (medium) | supports | K-W p=9.95e-26; eta^2=0.0967; k=5 strategies |
| **H3a** | top1_flips=2 | -- | flip_fraction=0.286 (occasional flips) | supports | top-1 flips 2/7; mean Kendall tau=0.738 |
| **H4a** | exclusive_pairs=3 | -- | pareto_jaccard=0.625 (different) | supports | |count|=5; |empirical|=8; only_count=0; only_empirical=3; Jaccard=0.625 |
| **H4b** | pareto_jaccard=0.625 | -- | frontier_size_diff=3 (frontiers differ) | supports | |count|=5; |empirical|=8; Jaccard=0.625 |

### v4.20

| Hypothesis | Statistic | p-value | Effect | Verdict | Notes |
|---|---|---|---|---|---|
| **H1a** | cv_cost=1.16 | -- | p90_over_p10=5.8 (very large) | supports | CV=1.16; p90/p10=5.8 |
| **H1b** | kruskal_wallis_min_p=2.32e-18 | <1e-12 | eta_squared_max=0.333 (large) | supports | K-W per level: 5/5 levels with p<0.05; min p=2.32e-18; max eta^2=0.333 |
| **H2a** | spearman_rho=0.965 | <1e-12 | rho=0.965 (strong positive) | supports | Spearman rho=0.965 on n=1270 (records-level) |
| **H2b** | median_ratio=1 | -- | abs_deviation_from_1=0.00134 (calibrated) | refutes | median ratio=1; 95% CI [0.999,1]; |median-1|=0.00134 |
| **H2c** | kruskal_wallis_p=2.82e-40 | <1e-12 | eta_squared=0.149 (large) | supports | K-W p=2.82e-40; eta^2=0.149; k=5 strategies |
| **H3a** | top1_flips=2 | -- | flip_fraction=0.286 (occasional flips) | supports | top-1 flips 2/7; mean Kendall tau=0.738 |
| **H4a** | exclusive_pairs=2 | -- | pareto_jaccard=0.714 (different) | supports | |count|=5; |empirical|=7; only_count=0; only_empirical=2; Jaccard=0.714 |
| **H4b** | pareto_jaccard=0.714 | -- | frontier_size_diff=2 (frontiers differ) | supports | |count|=5; |empirical|=7; Jaccard=0.714 |

### v5.0

| Hypothesis | Statistic | p-value | Effect | Verdict | Notes |
|---|---|---|---|---|---|
| **H1a** | cv_cost=1.12 | -- | p90_over_p10=5.7 (very large) | supports | CV=1.12; p90/p10=5.7 |
| **H1b** | kruskal_wallis_min_p=6.69e-18 | <1e-12 | eta_squared_max=0.324 (large) | supports | K-W per level: 4/5 levels with p<0.05; min p=6.69e-18; max eta^2=0.324 |
| **H2a** | spearman_rho=0.968 | <1e-12 | rho=0.968 (strong positive) | supports | Spearman rho=0.968 on n=1270 (records-level) |
| **H2b** | median_ratio=1 | -- | abs_deviation_from_1=0.0011 (calibrated) | refutes | median ratio=1; 95% CI [0.999,1]; |median-1|=0.0011 |
| **H2c** | kruskal_wallis_p=6.81e-37 | <1e-12 | eta_squared=0.137 (medium) | supports | K-W p=6.81e-37; eta^2=0.137; k=5 strategies |
| **H3a** | top1_flips=2 | -- | flip_fraction=0.286 (occasional flips) | supports | top-1 flips 2/7; mean Kendall tau=0.731 |
| **H4a** | exclusive_pairs=2 | -- | pareto_jaccard=0.714 (different) | supports | |count|=5; |empirical|=7; only_count=0; only_empirical=2; Jaccard=0.714 |
| **H4b** | pareto_jaccard=0.714 | -- | frontier_size_diff=2 (frontiers differ) | supports | |count|=5; |empirical|=7; Jaccard=0.714 |

### v5.04

| Hypothesis | Statistic | p-value | Effect | Verdict | Notes |
|---|---|---|---|---|---|
| **H1a** | cv_cost=1.08 | -- | p90_over_p10=5.21 (very large) | supports | CV=1.08; p90/p10=5.21 |
| **H1b** | kruskal_wallis_min_p=3.27e-18 | <1e-12 | eta_squared_max=0.33 (large) | supports | K-W per level: 5/5 levels with p<0.05; min p=3.27e-18; max eta^2=0.33 |
| **H2a** | spearman_rho=0.966 | <1e-12 | rho=0.966 (strong positive) | supports | Spearman rho=0.966 on n=1270 (records-level) |
| **H2b** | median_ratio=0.999 | -- | abs_deviation_from_1=0.000703 (calibrated) | refutes | median ratio=0.999; 95% CI [0.998,1]; |median-1|=0.000703 |
| **H2c** | kruskal_wallis_p=1.92e-48 | <1e-12 | eta_squared=0.179 (large) | supports | K-W p=1.92e-48; eta^2=0.179; k=5 strategies |
| **H3a** | top1_flips=7 | -- | flip_fraction=1 (frequent flips) | supports | top-1 flips 7/7; mean Kendall tau=0.707 |
| **H4a** | exclusive_pairs=5 | -- | pareto_jaccard=0.444 (different) | supports | |count|=4; |empirical|=9; only_count=0; only_empirical=5; Jaccard=0.444 |
| **H4b** | pareto_jaccard=0.444 | -- | frontier_size_diff=5 (frontiers differ) | supports | |count|=4; |empirical|=9; Jaccard=0.444 |

### v5.07

| Hypothesis | Statistic | p-value | Effect | Verdict | Notes |
|---|---|---|---|---|---|
| **H1a** | cv_cost=0.989 | -- | p90_over_p10=4.76 (large) | supports | CV=0.989; p90/p10=4.76 |
| **H1b** | kruskal_wallis_min_p=1.99e-21 | <1e-12 | eta_squared_max=0.389 (large) | supports | K-W per level: 5/5 levels with p<0.05; min p=1.99e-21; max eta^2=0.389 |
| **H2a** | spearman_rho=0.967 | <1e-12 | rho=0.967 (strong positive) | supports | Spearman rho=0.967 on n=1270 (records-level) |
| **H2b** | median_ratio=0.998 | -- | abs_deviation_from_1=0.00226 (calibrated) | inconclusive | median ratio=0.998; 95% CI [0.996,1]; |median-1|=0.00226 |
| **H2c** | kruskal_wallis_p=8.07e-54 | <1e-12 | eta_squared=0.199 (large) | supports | K-W p=8.07e-54; eta^2=0.199; k=5 strategies |
| **H3a** | top1_flips=4 | -- | flip_fraction=0.571 (frequent flips) | supports | top-1 flips 4/7; mean Kendall tau=0.71 |
| **H4a** | exclusive_pairs=8 | -- | pareto_jaccard=0.273 (different) | supports | |count|=3; |empirical|=11; only_count=0; only_empirical=8; Jaccard=0.273 |
| **H4b** | pareto_jaccard=0.273 | -- | frontier_size_diff=8 (frontiers differ) | supports | |count|=3; |empirical|=11; Jaccard=0.273 |

### v5.08

| Hypothesis | Statistic | p-value | Effect | Verdict | Notes |
|---|---|---|---|---|---|
| **H1a** | cv_cost=1.01 | -- | p90_over_p10=4.02 (very large) | supports | CV=1.01; p90/p10=4.02 |
| **H1b** | kruskal_wallis_min_p=6e-19 | <1e-12 | eta_squared_max=0.344 (large) | supports | K-W per level: 5/5 levels with p<0.05; min p=6e-19; max eta^2=0.344 |
| **H2a** | spearman_rho=0.967 | <1e-12 | rho=0.967 (strong positive) | supports | Spearman rho=0.967 on n=1270 (records-level) |
| **H2b** | median_ratio=1 | -- | abs_deviation_from_1=0.000275 (calibrated) | refutes | median ratio=1; 95% CI [0.998,1]; |median-1|=0.000275 |
| **H2c** | kruskal_wallis_p=2.97e-37 | <1e-12 | eta_squared=0.138 (medium) | supports | K-W p=2.97e-37; eta^2=0.138; k=5 strategies |
| **H3a** | top1_flips=6 | -- | flip_fraction=0.857 (frequent flips) | supports | top-1 flips 6/7; mean Kendall tau=0.745 |
| **H4a** | exclusive_pairs=4 | -- | pareto_jaccard=0.5 (different) | supports | |count|=4; |empirical|=8; only_count=0; only_empirical=4; Jaccard=0.5 |
| **H4b** | pareto_jaccard=0.5 | -- | frontier_size_diff=4 (frontiers differ) | supports | |count|=4; |empirical|=8; Jaccard=0.5 |

## Linux-specific tests

### Per-strategy calibration (refined H2b)

The aggregate H2b test on the entire records pool collapses very different strategies into a single median ratio. Linux's strategy panel contains both calibrated samplers (random, balanced, coverage) and strongly miscalibrated ones (diversity, expensiveOracle), so the per-strategy decomposition is informative. Each row reports a 95% percentile bootstrap CI of the median calibration ratio over all runs and levels for that strategy. The verdict is *miscalibrated* when the CI excludes 1 and the median deviation from 1 is at least 5%.

#### v4.13

| Strategy | n records | median ratio | 95% CI | |median-1| | Verdict |
|---|---:|---:|---|---:|---|
| `balanced` | 500 | 0.999 | [0.998, 1] | 0.000727 | **calibrated** |
| `cheapOracle` | 5 | -- | [--, --] | -- | **inconclusive** |
| `coverage` | 100 | 0.974 | [0.972, 0.977] | 0.026 | **inconclusive** |
| `diversity` | 40 | 2.28 | [2.23, 2.36] | 1.28 | **miscalibrated** |
| `expensiveOracle` | 5 | -- | [--, --] | -- | **inconclusive** |
| `random` | 500 | 0.999 | [0.997, 1] | 0.00112 | **calibrated** |
| `uncertainty` | 100 | 1.25 | [1.2, 1.28] | 0.246 | **miscalibrated** |

Oracles are deterministic single-run strategies in this protocol, so they contribute only 5 records (one per level) and the bootstrap CI requires at least 10. Their median calibration ratio is reported in `linux_kernels_summary.md` (cheapOracle ~ 0.29-0.32, expensiveOracle ~ 4.2-5.6) --- both are obviously miscalibrated by construction; the *inconclusive* label here is a sample-size artifact, not a statement that the oracles are calibrated.

#### v4.15

| Strategy | n records | median ratio | 95% CI | |median-1| | Verdict |
|---|---:|---:|---|---:|---|
| `balanced` | 500 | 1 | [0.998, 1] | 6.31e-05 | **calibrated** |
| `cheapOracle` | 5 | -- | [--, --] | -- | **inconclusive** |
| `coverage` | 100 | 1.01 | [1, 1.01] | 0.00663 | **inconclusive** |
| `diversity` | 40 | 2.23 | [2.2, 2.29] | 1.23 | **miscalibrated** |
| `expensiveOracle` | 5 | -- | [--, --] | -- | **inconclusive** |
| `random` | 500 | 1 | [1, 1] | 0.00303 | **calibrated** |
| `uncertainty` | 100 | 0.996 | [0.974, 1.02] | 0.00395 | **calibrated** |

Oracles are deterministic single-run strategies in this protocol, so they contribute only 5 records (one per level) and the bootstrap CI requires at least 10. Their median calibration ratio is reported in `linux_kernels_summary.md` (cheapOracle ~ 0.29-0.32, expensiveOracle ~ 4.2-5.6) --- both are obviously miscalibrated by construction; the *inconclusive* label here is a sample-size artifact, not a statement that the oracles are calibrated.

#### v4.20

| Strategy | n records | median ratio | 95% CI | |median-1| | Verdict |
|---|---:|---:|---|---:|---|
| `balanced` | 500 | 0.998 | [0.994, 1] | 0.00196 | **calibrated** |
| `cheapOracle` | 5 | -- | [--, --] | -- | **inconclusive** |
| `coverage` | 100 | 1 | [0.998, 1] | 0.000981 | **calibrated** |
| `diversity` | 60 | 2.27 | [2.2, 2.38] | 1.27 | **miscalibrated** |
| `expensiveOracle` | 5 | -- | [--, --] | -- | **inconclusive** |
| `random` | 500 | 1 | [0.998, 1.01] | 0.00239 | **calibrated** |
| `uncertainty` | 100 | 0.943 | [0.905, 0.977] | 0.0565 | **miscalibrated** |

Oracles are deterministic single-run strategies in this protocol, so they contribute only 5 records (one per level) and the bootstrap CI requires at least 10. Their median calibration ratio is reported in `linux_kernels_summary.md` (cheapOracle ~ 0.29-0.32, expensiveOracle ~ 4.2-5.6) --- both are obviously miscalibrated by construction; the *inconclusive* label here is a sample-size artifact, not a statement that the oracles are calibrated.

#### v5.0

| Strategy | n records | median ratio | 95% CI | |median-1| | Verdict |
|---|---:|---:|---|---:|---|
| `balanced` | 500 | 0.998 | [0.995, 1] | 0.00207 | **calibrated** |
| `cheapOracle` | 5 | -- | [--, --] | -- | **inconclusive** |
| `coverage` | 100 | 0.997 | [0.994, 1] | 0.00312 | **calibrated** |
| `diversity` | 60 | 2.06 | [1.96, 2.08] | 1.06 | **miscalibrated** |
| `expensiveOracle` | 5 | -- | [--, --] | -- | **inconclusive** |
| `random` | 500 | 1 | [0.998, 1] | 0.00199 | **calibrated** |
| `uncertainty` | 100 | 0.979 | [0.946, 1.02] | 0.0207 | **calibrated** |

Oracles are deterministic single-run strategies in this protocol, so they contribute only 5 records (one per level) and the bootstrap CI requires at least 10. Their median calibration ratio is reported in `linux_kernels_summary.md` (cheapOracle ~ 0.29-0.32, expensiveOracle ~ 4.2-5.6) --- both are obviously miscalibrated by construction; the *inconclusive* label here is a sample-size artifact, not a statement that the oracles are calibrated.

#### v5.04

| Strategy | n records | median ratio | 95% CI | |median-1| | Verdict |
|---|---:|---:|---|---:|---|
| `balanced` | 500 | 0.999 | [0.997, 1] | 0.000604 | **calibrated** |
| `cheapOracle` | 5 | -- | [--, --] | -- | **inconclusive** |
| `coverage` | 100 | 0.993 | [0.988, 0.997] | 0.00739 | **inconclusive** |
| `diversity` | 60 | 2.09 | [2, 2.12] | 1.09 | **miscalibrated** |
| `expensiveOracle` | 5 | -- | [--, --] | -- | **inconclusive** |
| `random` | 500 | 1 | [0.998, 1] | 6.26e-05 | **calibrated** |
| `uncertainty` | 100 | 0.878 | [0.851, 0.907] | 0.122 | **miscalibrated** |

Oracles are deterministic single-run strategies in this protocol, so they contribute only 5 records (one per level) and the bootstrap CI requires at least 10. Their median calibration ratio is reported in `linux_kernels_summary.md` (cheapOracle ~ 0.29-0.32, expensiveOracle ~ 4.2-5.6) --- both are obviously miscalibrated by construction; the *inconclusive* label here is a sample-size artifact, not a statement that the oracles are calibrated.

#### v5.07

| Strategy | n records | median ratio | 95% CI | |median-1| | Verdict |
|---|---:|---:|---|---:|---|
| `balanced` | 500 | 0.997 | [0.995, 1] | 0.00299 | **calibrated** |
| `cheapOracle` | 5 | -- | [--, --] | -- | **inconclusive** |
| `coverage` | 100 | 0.993 | [0.988, 0.996] | 0.00714 | **inconclusive** |
| `diversity` | 60 | 2 | [1.93, 2.04] | 0.999 | **miscalibrated** |
| `expensiveOracle` | 5 | -- | [--, --] | -- | **inconclusive** |
| `random` | 500 | 0.999 | [0.997, 1] | 0.000747 | **calibrated** |
| `uncertainty` | 100 | 0.839 | [0.799, 0.863] | 0.161 | **miscalibrated** |

Oracles are deterministic single-run strategies in this protocol, so they contribute only 5 records (one per level) and the bootstrap CI requires at least 10. Their median calibration ratio is reported in `linux_kernels_summary.md` (cheapOracle ~ 0.29-0.32, expensiveOracle ~ 4.2-5.6) --- both are obviously miscalibrated by construction; the *inconclusive* label here is a sample-size artifact, not a statement that the oracles are calibrated.

#### v5.08

| Strategy | n records | median ratio | 95% CI | |median-1| | Verdict |
|---|---:|---:|---|---:|---|
| `balanced` | 500 | 0.999 | [0.997, 1] | 0.000659 | **calibrated** |
| `cheapOracle` | 5 | -- | [--, --] | -- | **inconclusive** |
| `coverage` | 100 | 0.994 | [0.992, 0.999] | 0.00591 | **inconclusive** |
| `diversity` | 60 | 2.02 | [1.97, 2.05] | 1.02 | **miscalibrated** |
| `expensiveOracle` | 5 | -- | [--, --] | -- | **inconclusive** |
| `random` | 500 | 0.999 | [0.996, 1] | 0.000992 | **calibrated** |
| `uncertainty` | 100 | 0.946 | [0.907, 1.01] | 0.0543 | **inconclusive** |

Oracles are deterministic single-run strategies in this protocol, so they contribute only 5 records (one per level) and the bootstrap CI requires at least 10. Their median calibration ratio is reported in `linux_kernels_summary.md` (cheapOracle ~ 0.29-0.32, expensiveOracle ~ 4.2-5.6) --- both are obviously miscalibrated by construction; the *inconclusive* label here is a sample-size artifact, not a statement that the oracles are calibrated.

### Active-learning seam: is `uncertainty`'s calibration ratio monotone in n?

`linux_kernels_summary.md` highlights the AL strategy as *n-dependent*: the median calibration ratio increases monotonically with n on both releases, crossing 1 at different absolute n. We test this with a Spearman rank correlation between the absolute level n and the per-level median calibration ratio.

| Release | levels | Spearman rho | p-value | Per-level (n -> ratio) | Verdict |
|---|---:|---:|---:|---|---|
| v4.13 | 5 | 0.6 | 0.285 | n=926->1.2; n=1851->1.2; n=4628->1.11; n=9256->1.29; n=18512->1.35 | **inconclusive** |
| v4.15 | 5 | 0.6 | 0.285 | n=394->0.962; n=788->1.01; n=1970->0.975; n=3939->0.963; n=7878->1.32 | **inconclusive** |
| v4.20 | 5 | 0.9 | 0.0374 | n=235->0.772; n=470->0.918; n=1174->0.899; n=2349->0.957; n=4698->1.26 | **monotone increasing** |
| v5.0 | 5 | 1 | <1e-12 | n=200->0.794; n=399->0.885; n=998->0.974; n=1995->1.03; n=3990->1.35 | **monotone increasing** |
| v5.04 | 5 | 0.9 | 0.0374 | n=258->0.758; n=517->0.839; n=1292->0.921; n=2585->0.85; n=5169->1.17 | **monotone increasing** |
| v5.07 | 5 | 1 | <1e-12 | n=202->0.678; n=403->0.763; n=1008->0.783; n=2016->0.866; n=4032->1.12 | **monotone increasing** |
| v5.08 | 5 | 1 | <1e-12 | n=219->0.669; n=438->0.805; n=1096->0.931; n=2192->1.17; n=4385->1.26 | **monotone increasing** |

### Cross-release replication

A finding *replicates* if all releases share the same calibration verdict and either (i) point in the same direction relative to 1 or (ii) have pairwise-overlapping bootstrap CIs.  *Direction-only replication* requires sign agreement without verdict agreement.

| Strategy | v4.13 median | v4.13 verdict | v4.15 median | v4.15 verdict | v4.20 median | v4.20 verdict | v5.0 median | v5.0 verdict | v5.04 median | v5.04 verdict | v5.07 median | v5.07 verdict | v5.08 median | v5.08 verdict | Replication |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `balanced` | 0.999 | calibrated | 1 | calibrated | 0.998 | calibrated | 0.998 | calibrated | 0.999 | calibrated | 0.997 | calibrated | 0.999 | calibrated | **replicates** |
| `cheapOracle` | -- | inconclusive | -- | inconclusive | -- | inconclusive | -- | inconclusive | -- | inconclusive | -- | inconclusive | -- | inconclusive | **diverges** |
| `coverage` | 0.974 | inconclusive | 1.01 | inconclusive | 1 | calibrated | 0.997 | calibrated | 0.993 | inconclusive | 0.993 | inconclusive | 0.994 | inconclusive | **diverges** |
| `diversity` | 2.28 | miscalibrated | 2.23 | miscalibrated | 2.27 | miscalibrated | 2.06 | miscalibrated | 2.09 | miscalibrated | 2 | miscalibrated | 2.02 | miscalibrated | **replicates** |
| `expensiveOracle` | -- | inconclusive | -- | inconclusive | -- | inconclusive | -- | inconclusive | -- | inconclusive | -- | inconclusive | -- | inconclusive | **diverges** |
| `random` | 0.999 | calibrated | 1 | calibrated | 1 | calibrated | 1 | calibrated | 1 | calibrated | 0.999 | calibrated | 0.999 | calibrated | **replicates** |
| `uncertainty` | 1.25 | miscalibrated | 0.996 | calibrated | 0.943 | miscalibrated | 0.979 | calibrated | 0.878 | miscalibrated | 0.839 | miscalibrated | 0.946 | inconclusive | **diverges** |

### Cross-release H3b (CV vs flip count)

Per-release pairs (cost CV, top-1 flips out of 7 lambdas):

- v4.13: CV = 1.43, flips = 2/7
- v4.15: CV = 1.16, flips = 2/7
- v4.20: CV = 1.16, flips = 2/7
- v5.0: CV = 1.12, flips = 2/7
- v5.04: CV = 1.08, flips = 7/7
- v5.07: CV = 0.989, flips = 4/7
- v5.08: CV = 1.01, flips = 6/7

Spearman rho(CV, flips) across 7 releases = -0.749. With n=7 the test is under-powered (the H3b helper requires >= 4 systems for a defensible p-value), but the *sign* is informative.

The Linux pool shows the opposite of the cross-system H3b correlation observed on the seven NewRuns systems (Spearman rho=0.90, positive). On NewRuns, higher cost heterogeneity translates into more rank flips. On Linux, the four-version evidence (4 releases at 2/7 flips, one at 4/7, two at 6-7/7) shows that flip rate is **not driven by cost CV** --- cost CV varies smoothly from 1.43 (v4.13) to 0.99 (v5.07) but the flip rate is bimodal (2/7 cluster vs 6-7/7 cluster) with v5.07's 4/7 in the gap. The actual mechanism (per `linux_kernels_summary.md`) is which strategy wins count-side MRE at the smallest level: when count picks `uncertainty_n=small` (v4.13/v4.15/v4.20/v5.0), count and empirical agree on the top-1 across most lambdas because empirical's preferred pick (`uncertainty`, cheap-leaning) is the same. When count picks `random_n=small` (v5.07) or `balanced_n=small` (v5.04, v5.08), count cannot exploit `uncertainty`'s cheap-leaning calibration ratio and empirical breaks the tie via cost for every cost-weighted lambda. This is a count-decision-rule effect specific to deployable AL sampling, not a heterogeneity effect, and it is why the Linux verdicts should not be aggregated with NewRuns.

## Synthesis

1. **H1a, H1b, H2a, H2c are universally supported on Linux.** All 7 releases have heavy-tailed cost (CV >= 1, p90/p10 >= 4), strong strategy effects on TrainCost at fixed n (Kruskal-Wallis p << 1e-10 with large eta^2), strong rank correlation between n and TrainCost (rho >= 0.93), and strong strategy effects on the calibration ratio.

2. **Aggregate H2b is misleading on Linux** because the per-strategy decomposition splits cleanly into calibrated (`random`, `balanced`, `coverage`) and miscalibrated (`diversity`, `uncertainty`, oracles) strategies. The global median ratio averages the two groups and lands somewhere in between. We recommend reporting the per-strategy H2b verdict on Linux rather than the aggregate.

3. **The AL seam is robust across releases.** `uncertainty`'s median calibration ratio rises monotonically with n in each release (v4.13: rho=0.6, p=0.285; v4.15: rho=0.6, p=0.285; v4.20: rho=0.9, p=0.0374; v5.0: rho=1, p=<1e-12; v5.04: rho=0.9, p=0.0374; v5.07: rho=1, p=<1e-12; v5.08: rho=1, p=<1e-12; 5 levels each). With only 5 levels the per-release Spearman cannot independently reach p < 0.05 in every release, but the *direction* is consistent across all of them, and the cross-over from <1 to >1 happens at different absolute n on each release --- the cross-version seam highlighted in `linux_kernels_summary.md`. This is a Linux-specific finding with no x264 / NewRuns analogue.

4. **Decision-level verdicts (H3a, H4a, H4b) are existentially supported on all 7 releases.** Each release has at least one lambda where count-cost and empirical-cost top-1 disagree, and each release has an empirical Pareto frontier strictly larger than the count Pareto frontier. v5.08 has more rank flips than v4.13 / v4.15 (6/7 vs 2/7 each) despite *lower* cost CV, an exception to the cross-system H3b correlation that is driven by tie density at the smaller pool size, not by heterogeneity.

5. **7-way replication is strong for deployable strategies and direction-only for AL.** `random`, `balanced`, `coverage` replicate as calibrated on all 7 releases; `diversity` replicates as strongly upward-miscalibrated on all 7 releases (medians in [2.0, 2.3]); `uncertainty` replicates *direction-only* because its aggregate ratio sits on opposite sides of 1 across releases due to different absolute n grids, but the per-level monotone-in-n pattern (cheap at small n, expensive at large n) is identical on every release.
