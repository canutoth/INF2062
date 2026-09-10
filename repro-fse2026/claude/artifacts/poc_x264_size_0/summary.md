# Proof of concept: x264_size_0

## Data

- Prediction target context: `x264_size_0`
- Empirical acquisition-cost context: `x264_time_0`
- Reconstructed configurations: 1152 / 1152 listed in AllSummary
- Full empirical cost: 3948
- Per-configuration cost CV: 0.301
- p90/p10 per-configuration cost ratio: 2.212

## RQ snapshots

- RQ1: median fixed-size overhead vs random ranges from 0.7101 to 1.112.
- RQ2: Spearman rho(n, TrainCost) = 0.9431; median calibration ratio = 1.005.
- RQ3: top-1 strategy-size pair changes for 0 / 7 lambda values.
- RQ4: empirical frontier = random_t1, solverBased_t1, henard_t1, distBased_t1, divDistBased_t1, random_t2, henard_t2, divDistBased_t3.
- Count frontier = solverBased_t1, random_t2, divDistBased_t3.

## Useful first read

The lowest simple combined median MRE + empirical-cost point is random_t2 (MRE=0.02807, cost=5.662% of full cost).

Generated files in this directory contain the raw records, strategy summaries, rank stability sweep, Pareto labels, and figures.
