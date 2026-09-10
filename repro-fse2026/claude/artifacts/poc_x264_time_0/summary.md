# Proof of concept: x264_time_0

## Data

- Reconstructed configurations: 1152 / 1152 listed in AllSummary
- Full empirical cost: 3948
- Per-configuration cost CV: 0.301
- p90/p10 per-configuration cost ratio: 2.212

## RQ snapshots

- RQ1: median fixed-size overhead vs random ranges from 0.7101 to 1.112.
- RQ2: Spearman rho(n, TrainCost) = 0.9431; median calibration ratio = 1.005.
- RQ3: top-1 strategy-size pair changes for 1 / 7 lambda values.
- RQ4: empirical frontier = henard_t1, distBased_t1, divDistBased_t1, random_t2, distBased_t2, divDistBased_t2, divDistBased_t3.
- Count frontier = divDistBased_t1, divDistBased_t2, divDistBased_t3.

## Useful first read

The lowest simple combined median MRE + empirical-cost point is divDistBased_t2 (MRE=0.08307, cost=5.845% of full cost).

Generated files in this directory contain the raw records, strategy summaries, rank stability sweep, Pareto labels, and figures.
