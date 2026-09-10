# FSE 2026 posterior-risk revisit on the WORKLOAD family

## Scope

This applies the FSE posterior-risk/posterior-confidence framework to the
ICSE 2023 workload-impact corpus. Each context is one (system, workload)
pair; the measured wall time (throughput for h2) is both the bound target
and the empirical acquisition cost, so the analysis asks how posterior
guarantees per cost react to workload/input context. Posterior risk is
relative to the measured configuration table of that context.

Source archive: `/Users/mathieuacher/SANDBOX/cost-sampling-matters/workload-impact-ICSE2023/artifact_excluding_raw_coverage.zip`.
Systems analyzed: `batik, dconvert, h2, jump3r, kanzi, lrzip, x264, xz, z3`.
SRS generated: `True` with `100` seeds per context/level.
Diagnostic oracles included: `False`.

## Headline

Strategy posterior-risk distributions differ in 341/359 context-level scopes.
SRS is the best empirical-cost-normalized recommendation in 31/359 scopes and appears on the empirical cost/confidence Pareto frontier in 139/359 scopes.
Cost-normalization changes the top recommendation in 61/359 scopes and changes the confidence Pareto frontier in 346/359 scopes.
SRS has lower posterior risk than random in 84/359 scopes; its empirical acquisition cost differs from random in 149/359 scopes.

Best empirical-cost-normalized pairs:

- `pairwise_n16`: 43/359
- `pairwise_n32`: 41/359
- `pairwise_n8`: 37/359
- `pairwise_n64`: 34/359
- `diversity_n16`: 32/359
- `diversity_n8`: 31/359
- `diversity_n32`: 24/359
- `diversity_n64`: 21/359
- `balanced_n8`: 19/359
- `SRSSampling_n64`: 16/359
- `balanced_n32`: 12/359
- `SRSSampling_n32`: 11/359
- `balanced_n16`: 11/359
- `balanced_n64`: 6/359
- `pilotCost_n16`: 3/359
- `pilotCost_n32`: 3/359
- `random_n64`: 3/359
- `SRSSampling_n16`: 2/359
- `pilotCost_n8`: 2/359
- `SRSSampling_n8`: 2/359
- `random_n32`: 2/359
- `random_n8`: 2/359
- `random_n16`: 2/359

## Context-Level Summary

| Context | Level | n | Best cost pair | SRS best? | SRS on front? | Jaccard |
|---|---|---:|---|---:|---:|---:|
| `batik__corona` | `n8` | 8 | `diversity_n8` | 0 | 1 | 0.1667 |
| `batik__corona` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.3333 |
| `batik__corona` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.5 |
| `batik__corona` | `n64` | 64 | `diversity_n64` | 0 | 1 | 0.2 |
| `batik__cranium` | `n8` | 8 | `diversity_n8` | 0 | 1 | 0.2 |
| `batik__cranium` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.25 |
| `batik__cranium` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.3333 |
| `batik__cranium` | `n64` | 64 | `pairwise_n64` | 0 | 1 | 0.25 |
| `batik__cubus` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.25 |
| `batik__cubus` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.5 |
| `batik__cubus` | `n32` | 32 | `pairwise_n32` | 0 | 1 | 0.3333 |
| `batik__cubus` | `n64` | 64 | `SRSSampling_n64` | 1 | 1 | 0.2 |
| `batik__flame` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.25 |
| `batik__flame` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.5 |
| `batik__flame` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.5 |
| `batik__flame` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.5 |
| `batik__france` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.5 |
| `batik__france` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.25 |
| `batik__france` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.3333 |
| `batik__france` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.3333 |
| `batik__frisco` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.2 |
| `batik__frisco` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.3333 |
| `batik__frisco` | `n32` | 32 | `balanced_n32` | 0 | 0 | 0.3333 |
| `batik__frisco` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.3333 |
| `batik__jelly` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.25 |
| `batik__jelly` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.25 |
| `batik__jelly` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.2 |
| `batik__jelly` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.3333 |
| `batik__karte` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.25 |
| `batik__karte` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.5 |
| `batik__karte` | `n32` | 32 | `balanced_n32` | 0 | 1 | 0.2 |
| `batik__karte` | `n64` | 64 | `SRSSampling_n64` | 1 | 1 | 0.2 |
| `batik__mandelbrot` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.25 |
| `batik__mandelbrot` | `n16` | 16 | `diversity_n16` | 0 | 1 | 0.25 |
| `batik__mandelbrot` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `batik__mandelbrot` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.3333 |
| `batik__strawberry` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.25 |
| `batik__strawberry` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.25 |
| `batik__strawberry` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `batik__strawberry` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.3333 |
| `batik__village` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.3333 |
| `batik__village` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.25 |
| `batik__village` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.25 |
| `batik__village` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.3333 |
| `dconvert__jpeg-large` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.25 |
| `dconvert__jpeg-large` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.5 |
| `dconvert__jpeg-large` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.5 |
| `dconvert__jpeg-large` | `n64` | 64 | `diversity_n64` | 0 | 1 | 0.1667 |
| `dconvert__jpeg-medium` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.2 |
| `dconvert__jpeg-medium` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.5 |
| `dconvert__jpeg-medium` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.5 |
| `dconvert__jpeg-medium` | `n64` | 64 | `diversity_n64` | 0 | 1 | 0.2 |
| `dconvert__jpeg-small` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.3333 |
| `dconvert__jpeg-small` | `n16` | 16 | `pairwise_n16` | 0 | 1 | 0.25 |
| `dconvert__jpeg-small` | `n32` | 32 | `SRSSampling_n32` | 1 | 1 | 0.2 |
| `dconvert__jpeg-small` | `n64` | 64 | `SRSSampling_n64` | 1 | 1 | 0.2 |
| `dconvert__png-large` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.3333 |
| `dconvert__png-large` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.5 |
| `dconvert__png-large` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.5 |
| `dconvert__png-large` | `n64` | 64 | `diversity_n64` | 0 | 1 | 0.2 |
| `dconvert__png-medium` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.5 |
| `dconvert__png-medium` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.5 |
| `dconvert__png-medium` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.5 |
| `dconvert__png-medium` | `n64` | 64 | `pairwise_n64` | 0 | 1 | 0.3333 |
| `dconvert__png-small` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.25 |
| `dconvert__png-small` | `n16` | 16 | `diversity_n16` | 0 | 1 | 0.25 |
| `dconvert__png-small` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.25 |
| `dconvert__png-small` | `n64` | 64 | `SRSSampling_n64` | 1 | 1 | 0.3333 |
| `dconvert__psd-large` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.3333 |
| `dconvert__psd-large` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.3333 |
| `dconvert__psd-large` | `n32` | 32 | `SRSSampling_n32` | 1 | 1 | 0.25 |
| `dconvert__psd-large` | `n64` | 64 | `diversity_n64` | 0 | 1 | 0.25 |
| `dconvert__psd-medium` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.5 |
| `dconvert__psd-medium` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.5 |
| `dconvert__psd-medium` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.5 |
| `dconvert__psd-medium` | `n64` | 64 | `SRSSampling_n64` | 1 | 1 | 0.2 |
| `dconvert__psd-small` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.3333 |
| `dconvert__psd-small` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.5 |
| `dconvert__psd-small` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `dconvert__psd-small` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.3333 |
| `dconvert__svg-large` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 1 |
| `dconvert__svg-large` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.25 |
| `dconvert__svg-large` | `n32` | 32 | `balanced_n32` | 0 | 0 | 0.3333 |
| `dconvert__svg-large` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 1 |
| `dconvert__svg-medium` | `n8` | 8 | `balanced_n8` | 0 | 0 | 0.3333 |
| `dconvert__svg-medium` | `n16` | 16 | `SRSSampling_n16` | 1 | 1 | 0.2 |
| `dconvert__svg-medium` | `n32` | 32 | `SRSSampling_n32` | 1 | 1 | 0.2 |
| `dconvert__svg-medium` | `n64` | 64 | `SRSSampling_n64` | 1 | 1 | 0.1667 |
| `dconvert__svg-small` | `n8` | 8 | `balanced_n8` | 0 | 1 | 0.3333 |
| `dconvert__svg-small` | `n16` | 16 | `diversity_n16` | 0 | 1 | 0.25 |
| `dconvert__svg-small` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.2 |
| `dconvert__svg-small` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.25 |
| `h2__smallbank-1` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.5 |
| `h2__smallbank-1` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.5 |
| `h2__smallbank-1` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.5 |
| `h2__smallbank-1` | `n64` | 64 | `SRSSampling_n64` | 1 | 1 | 1 |
| `h2__smallbank-10` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.5 |
| `h2__smallbank-10` | `n16` | 16 | `pilotCost_n16` | 0 | 0 | 0.5 |
| `h2__smallbank-10` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.5 |
| `h2__smallbank-10` | `n64` | 64 | `SRSSampling_n64` | 1 | 1 | 1 |
| `h2__tpcc-2` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.3333 |
| `h2__tpcc-2` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.3333 |
| `h2__tpcc-2` | `n32` | 32 | `SRSSampling_n32` | 1 | 1 | 0.5 |
| `h2__tpcc-2` | `n64` | 64 | `pairwise_n64` | 0 | 1 | 0.5 |
| `h2__tpcc-8` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.5 |
| `h2__tpcc-8` | `n16` | 16 | `SRSSampling_n16` | 1 | 1 | 0.5 |
| `h2__tpcc-8` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 1 |
| `h2__tpcc-8` | `n64` | 64 | `SRSSampling_n64` | 1 | 1 | 0.5 |
| `h2__voter-16` | `n8` | 8 | `pilotCost_n8` | 0 | 0 | 1 |
| `h2__voter-16` | `n16` | 16 | `pilotCost_n16` | 0 | 0 | 1 |
| `h2__voter-16` | `n32` | 32 | `pilotCost_n32` | 0 | 0 | 1 |
| `h2__voter-16` | `n64` | 64 | `SRSSampling_n64` | 1 | 1 | 1 |
| `h2__voter-2` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.3333 |
| `h2__voter-2` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.5 |
| `h2__voter-2` | `n32` | 32 | `pilotCost_n32` | 0 | 0 | 0.5 |
| `h2__voter-2` | `n64` | 64 | `SRSSampling_n64` | 1 | 1 | 1 |
| `h2__ycsb-2400` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.5 |
| `h2__ycsb-2400` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.5 |
| `h2__ycsb-2400` | `n32` | 32 | `pairwise_n32` | 0 | 1 | 0.25 |
| `h2__ycsb-2400` | `n64` | 64 | `pairwise_n64` | 0 | 1 | 0.5 |
| `h2__ycsb-600` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.3333 |
| `h2__ycsb-600` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.5 |
| `h2__ycsb-600` | `n32` | 32 | `pairwise_n32` | 0 | 1 | 0.3333 |
| `h2__ycsb-600` | `n64` | 64 | `pairwise_n64` | 0 | 1 | 0.5 |
| `jump3r__beethoven.wav` | `n8` | 8 | `SRSSampling_n8` | 1 | 1 | 0.3333 |
| `jump3r__beethoven.wav` | `n16` | 16 | `diversity_n16` | 0 | 1 | 0.25 |
| `jump3r__beethoven.wav` | `n32` | 32 | `diversity_n32` | 0 | 1 | 0.2 |
| `jump3r__beethoven.wav` | `n64` | 64 | `diversity_n64` | 0 | 1 | 0.2 |
| `jump3r__dual-channel.wav` | `n8` | 8 | `diversity_n8` | 0 | 1 | 0.2 |
| `jump3r__dual-channel.wav` | `n16` | 16 | `diversity_n16` | 0 | 1 | 0.2 |
| `jump3r__dual-channel.wav` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `jump3r__dual-channel.wav` | `n64` | 64 | `diversity_n64` | 0 | 1 | 0.25 |
| `jump3r__helix.wav` | `n8` | 8 | `diversity_n8` | 0 | 1 | 0.3333 |
| `jump3r__helix.wav` | `n16` | 16 | `diversity_n16` | 0 | 1 | 0.25 |
| `jump3r__helix.wav` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `jump3r__helix.wav` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.3333 |
| `jump3r__single-channel.wav` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.5 |
| `jump3r__single-channel.wav` | `n16` | 16 | `diversity_n16` | 0 | 1 | 0.2 |
| `jump3r__single-channel.wav` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `jump3r__single-channel.wav` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.25 |
| `jump3r__speech.wav` | `n8` | 8 | `SRSSampling_n8` | 1 | 1 | 0.25 |
| `jump3r__speech.wav` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.25 |
| `jump3r__speech.wav` | `n32` | 32 | `SRSSampling_n32` | 1 | 1 | 0.2 |
| `jump3r__speech.wav` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.25 |
| `jump3r__sweep.wav` | `n8` | 8 | `balanced_n8` | 0 | 1 | 0.3333 |
| `jump3r__sweep.wav` | `n16` | 16 | `diversity_n16` | 0 | 1 | 0.2 |
| `jump3r__sweep.wav` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.25 |
| `jump3r__sweep.wav` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.25 |
| `kanzi__ambivert` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.2 |
| `kanzi__ambivert` | `n16` | 16 | `pairwise_n16` | 0 | 1 | 0.2 |
| `kanzi__ambivert` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.25 |
| `kanzi__ambivert` | `n64` | 64 | `balanced_n64` | 0 | 1 | 0.25 |
| `kanzi__artificl` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.3333 |
| `kanzi__artificl` | `n16` | 16 | `diversity_n16` | 0 | 1 | 0.2 |
| `kanzi__artificl` | `n32` | 32 | `diversity_n32` | 0 | 1 | 0.1667 |
| `kanzi__artificl` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.25 |
| `kanzi__deepfield` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.1667 |
| `kanzi__deepfield` | `n16` | 16 | `pairwise_n16` | 0 | 1 | 0.25 |
| `kanzi__deepfield` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.25 |
| `kanzi__deepfield` | `n64` | 64 | `balanced_n64` | 0 | 1 | 0.25 |
| `kanzi__enwik8` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.2 |
| `kanzi__enwik8` | `n16` | 16 | `pairwise_n16` | 0 | 1 | 0.25 |
| `kanzi__enwik8` | `n32` | 32 | `pairwise_n32` | 0 | 1 | 0.2 |
| `kanzi__enwik8` | `n64` | 64 | `balanced_n64` | 0 | 1 | 0.25 |
| `kanzi__fannie_mae_500k` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.25 |
| `kanzi__fannie_mae_500k` | `n16` | 16 | `pairwise_n16` | 0 | 1 | 0.25 |
| `kanzi__fannie_mae_500k` | `n32` | 32 | `pairwise_n32` | 0 | 1 | 0.2 |
| `kanzi__fannie_mae_500k` | `n64` | 64 | `SRSSampling_n64` | 1 | 1 | 0.25 |
| `kanzi__large` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.2 |
| `kanzi__large` | `n16` | 16 | `pairwise_n16` | 0 | 1 | 0.25 |
| `kanzi__large` | `n32` | 32 | `pairwise_n32` | 0 | 1 | 0.2 |
| `kanzi__large` | `n64` | 64 | `SRSSampling_n64` | 1 | 1 | 0.25 |
| `kanzi__misc` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.2 |
| `kanzi__misc` | `n16` | 16 | `pairwise_n16` | 0 | 1 | 0.25 |
| `kanzi__misc` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.25 |
| `kanzi__misc` | `n64` | 64 | `balanced_n64` | 0 | 1 | 0.25 |
| `kanzi__silesia` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.25 |
| `kanzi__silesia` | `n16` | 16 | `pairwise_n16` | 0 | 1 | 0.25 |
| `kanzi__silesia` | `n32` | 32 | `pairwise_n32` | 0 | 1 | 0.2 |
| `kanzi__silesia` | `n64` | 64 | `balanced_n64` | 0 | 1 | 0.25 |
| `kanzi__vmlinux` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.1667 |
| `kanzi__vmlinux` | `n16` | 16 | `pilotCost_n16` | 0 | 0 | 0.3333 |
| `kanzi__vmlinux` | `n32` | 32 | `pilotCost_n32` | 0 | 0 | 0.3333 |
| `kanzi__vmlinux` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.5 |
| `lrzip__ambivert.wav.tar` | `n8` | 8 | `balanced_n8` | 0 | 0 | 0.25 |
| `lrzip__ambivert.wav.tar` | `n16` | 16 | `balanced_n16` | 0 | 1 | 0.2 |
| `lrzip__ambivert.wav.tar` | `n32` | 32 | `balanced_n32` | 0 | 0 | 0.3333 |
| `lrzip__artificl.tar` | `n8` | 8 | `balanced_n8` | 0 | 1 | 0.25 |
| `lrzip__artificl.tar` | `n16` | 16 | `balanced_n16` | 0 | 0 | 0.3333 |
| `lrzip__artificl.tar` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.5 |
| `lrzip__deepfield.tar` | `n8` | 8 | `balanced_n8` | 0 | 0 | 0.3333 |
| `lrzip__deepfield.tar` | `n16` | 16 | `balanced_n16` | 0 | 1 | 0.2 |
| `lrzip__deepfield.tar` | `n32` | 32 | `balanced_n32` | 0 | 1 | 0.2 |
| `lrzip__enwik8.tar` | `n8` | 8 | `balanced_n8` | 0 | 0 | 0.5 |
| `lrzip__enwik8.tar` | `n16` | 16 | `diversity_n16` | 0 | 1 | 0.25 |
| `lrzip__enwik8.tar` | `n32` | 32 | `diversity_n32` | 0 | 0 | 1 |
| `lrzip__fannie_mae_500k.tar` | `n8` | 8 | `balanced_n8` | 0 | 0 | 0.25 |
| `lrzip__fannie_mae_500k.tar` | `n16` | 16 | `diversity_n16` | 0 | 1 | 0.25 |
| `lrzip__fannie_mae_500k.tar` | `n32` | 32 | `diversity_n32` | 0 | 0 | 1 |
| `lrzip__large.tar` | `n8` | 8 | `balanced_n8` | 0 | 0 | 0.5 |
| `lrzip__large.tar` | `n16` | 16 | `balanced_n16` | 0 | 0 | 0.5 |
| `lrzip__large.tar` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.5 |
| `lrzip__misc.tar` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.2 |
| `lrzip__misc.tar` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.5 |
| `lrzip__misc.tar` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `lrzip__silesia.tar` | `n8` | 8 | `balanced_n8` | 0 | 1 | 0.2 |
| `lrzip__silesia.tar` | `n16` | 16 | `balanced_n16` | 0 | 1 | 0.25 |
| `lrzip__silesia.tar` | `n32` | 32 | `balanced_n32` | 0 | 1 | 0.25 |
| `lrzip__uiq-32.bin` | `n8` | 8 | `balanced_n8` | 0 | 0 | 0.3333 |
| `lrzip__uiq-32.bin` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.3333 |
| `lrzip__uiq-32.bin` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.5 |
| `lrzip__uiq2-16.bin` | `n8` | 8 | `balanced_n8` | 0 | 1 | 0.25 |
| `lrzip__uiq2-16.bin` | `n16` | 16 | `balanced_n16` | 0 | 1 | 0.25 |
| `lrzip__uiq2-16.bin` | `n32` | 32 | `diversity_n32` | 0 | 0 | 1 |
| `lrzip__uiq2-4.bin` | `n8` | 8 | `balanced_n8` | 0 | 1 | 0.25 |
| `lrzip__uiq2-4.bin` | `n16` | 16 | `balanced_n16` | 0 | 1 | 0.3333 |
| `lrzip__uiq2-4.bin` | `n32` | 32 | `random_n32` | 0 | 0 | 0.3333 |
| `lrzip__uiq2-8.bin` | `n8` | 8 | `balanced_n8` | 0 | 0 | 0.3333 |
| `lrzip__uiq2-8.bin` | `n16` | 16 | `balanced_n16` | 0 | 1 | 0.25 |
| `lrzip__uiq2-8.bin` | `n32` | 32 | `balanced_n32` | 0 | 1 | 0.25 |
| `lrzip__vmlinux-5.10.tar` | `n8` | 8 | `balanced_n8` | 0 | 0 | 0.25 |
| `lrzip__vmlinux-5.10.tar` | `n16` | 16 | `balanced_n16` | 0 | 1 | 0.2 |
| `lrzip__vmlinux-5.10.tar` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.5 |
| `x264__Johnny_1280x720_60_short.y4m` | `n8` | 8 | `diversity_n8` | 0 | 1 | 0.1667 |
| `x264__Johnny_1280x720_60_short.y4m` | `n16` | 16 | `diversity_n16` | 0 | 1 | 0.2 |
| `x264__Johnny_1280x720_60_short.y4m` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.25 |
| `x264__Johnny_1280x720_60_short.y4m` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.25 |
| `x264__Netflix_Crosswalk_4096x2160_60fps_10bit_420_short.y4m` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.3333 |
| `x264__Netflix_Crosswalk_4096x2160_60fps_10bit_420_short.y4m` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.3333 |
| `x264__Netflix_Crosswalk_4096x2160_60fps_10bit_420_short.y4m` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.5 |
| `x264__Netflix_Crosswalk_4096x2160_60fps_10bit_420_short.y4m` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.25 |
| `x264__blue_sky_1080p25_short.y4m` | `n8` | 8 | `diversity_n8` | 0 | 1 | 0.1667 |
| `x264__blue_sky_1080p25_short.y4m` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.2 |
| `x264__blue_sky_1080p25_short.y4m` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.3333 |
| `x264__blue_sky_1080p25_short.y4m` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.3333 |
| `x264__pedestrian_area_1080p25_short.y4m` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.3333 |
| `x264__pedestrian_area_1080p25_short.y4m` | `n16` | 16 | `pairwise_n16` | 0 | 1 | 0.2 |
| `x264__pedestrian_area_1080p25_short.y4m` | `n32` | 32 | `balanced_n32` | 0 | 0 | 0.2 |
| `x264__pedestrian_area_1080p25_short.y4m` | `n64` | 64 | `random_n64` | 0 | 0 | 0.3333 |
| `x264__riverbed_1080p25_short.y4m` | `n8` | 8 | `balanced_n8` | 0 | 1 | 0.2 |
| `x264__riverbed_1080p25_short.y4m` | `n16` | 16 | `diversity_n16` | 0 | 1 | 0.25 |
| `x264__riverbed_1080p25_short.y4m` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.3333 |
| `x264__riverbed_1080p25_short.y4m` | `n64` | 64 | `random_n64` | 0 | 0 | 0.25 |
| `x264__sd_bridge_close_cif_short.y4m` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.3333 |
| `x264__sd_bridge_close_cif_short.y4m` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.3333 |
| `x264__sd_bridge_close_cif_short.y4m` | `n32` | 32 | `balanced_n32` | 0 | 0 | 0.2 |
| `x264__sd_bridge_close_cif_short.y4m` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.3333 |
| `x264__sd_city_4cif_short.y4m` | `n8` | 8 | `balanced_n8` | 0 | 0 | 0.3333 |
| `x264__sd_city_4cif_short.y4m` | `n16` | 16 | `pairwise_n16` | 0 | 1 | 0.2 |
| `x264__sd_city_4cif_short.y4m` | `n32` | 32 | `balanced_n32` | 0 | 0 | 0.3333 |
| `x264__sd_city_4cif_short.y4m` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.5 |
| `x264__sd_crew_cif_short.y4m` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.2 |
| `x264__sd_crew_cif_short.y4m` | `n16` | 16 | `pairwise_n16` | 0 | 1 | 0.2 |
| `x264__sd_crew_cif_short.y4m` | `n32` | 32 | `balanced_n32` | 0 | 0 | 0.3333 |
| `x264__sd_crew_cif_short.y4m` | `n64` | 64 | `random_n64` | 0 | 0 | 0.3333 |
| `x264__sintel_trailer_2k_720p24_short.y4m` | `n8` | 8 | `diversity_n8` | 0 | 1 | 0.2 |
| `x264__sintel_trailer_2k_720p24_short.y4m` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.5 |
| `x264__sintel_trailer_2k_720p24_short.y4m` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `x264__sintel_trailer_2k_720p24_short.y4m` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.5 |
| `xz__ambivert.wav.tar` | `n8` | 8 | `diversity_n8` | 0 | 1 | 0.1667 |
| `xz__ambivert.wav.tar` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.25 |
| `xz__ambivert.wav.tar` | `n32` | 32 | `SRSSampling_n32` | 1 | 1 | 0.2 |
| `xz__ambivert.wav.tar` | `n64` | 64 | `pairwise_n64` | 0 | 1 | 0.2 |
| `xz__artificl.tar` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.5 |
| `xz__artificl.tar` | `n16` | 16 | `pairwise_n16` | 0 | 1 | 0.25 |
| `xz__artificl.tar` | `n32` | 32 | `random_n32` | 0 | 0 | 0.3333 |
| `xz__artificl.tar` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.5 |
| `xz__deepfield.tar` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.25 |
| `xz__deepfield.tar` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.3333 |
| `xz__deepfield.tar` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.3333 |
| `xz__deepfield.tar` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.25 |
| `xz__enwik8.tar` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.3333 |
| `xz__enwik8.tar` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.2 |
| `xz__enwik8.tar` | `n32` | 32 | `pairwise_n32` | 0 | 1 | 0.1667 |
| `xz__enwik8.tar` | `n64` | 64 | `diversity_n64` | 0 | 1 | 0.2 |
| `xz__fannie_mae_500k.tar` | `n8` | 8 | `random_n8` | 0 | 1 | 0.1667 |
| `xz__fannie_mae_500k.tar` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.25 |
| `xz__fannie_mae_500k.tar` | `n32` | 32 | `SRSSampling_n32` | 1 | 1 | 0.1667 |
| `xz__fannie_mae_500k.tar` | `n64` | 64 | `SRSSampling_n64` | 1 | 1 | 0.2 |
| `xz__large.tar` | `n8` | 8 | `random_n8` | 0 | 1 | 0.1667 |
| `xz__large.tar` | `n16` | 16 | `random_n16` | 0 | 1 | 0.2 |
| `xz__large.tar` | `n32` | 32 | `pairwise_n32` | 0 | 1 | 0.3333 |
| `xz__large.tar` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.3333 |
| `xz__misc.tar` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.1667 |
| `xz__misc.tar` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.25 |
| `xz__misc.tar` | `n32` | 32 | `SRSSampling_n32` | 1 | 1 | 0.2 |
| `xz__misc.tar` | `n64` | 64 | `diversity_n64` | 0 | 1 | 0.3333 |
| `xz__silesia.tar` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.3333 |
| `xz__silesia.tar` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.25 |
| `xz__silesia.tar` | `n32` | 32 | `SRSSampling_n32` | 1 | 1 | 0.1667 |
| `xz__silesia.tar` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.25 |
| `xz__uiq-32.bin` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.3333 |
| `xz__uiq-32.bin` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.25 |
| `xz__uiq-32.bin` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.3333 |
| `xz__uiq-32.bin` | `n64` | 64 | `SRSSampling_n64` | 1 | 1 | 0.2 |
| `xz__uiq2-16.bin` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.3333 |
| `xz__uiq2-16.bin` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.25 |
| `xz__uiq2-16.bin` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `xz__uiq2-16.bin` | `n64` | 64 | `diversity_n64` | 0 | 1 | 0.3333 |
| `xz__uiq2-4.bin` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.25 |
| `xz__uiq2-4.bin` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.25 |
| `xz__uiq2-4.bin` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `xz__uiq2-4.bin` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.5 |
| `xz__uiq2-8.bin` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.1667 |
| `xz__uiq2-8.bin` | `n16` | 16 | `balanced_n16` | 0 | 0 | 0.3333 |
| `xz__uiq2-8.bin` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.3333 |
| `xz__uiq2-8.bin` | `n64` | 64 | `diversity_n64` | 0 | 1 | 0.25 |
| `xz__vmlinux-5.10.tar` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.3333 |
| `xz__vmlinux-5.10.tar` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.25 |
| `xz__vmlinux-5.10.tar` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.3333 |
| `xz__vmlinux-5.10.tar` | `n64` | 64 | `balanced_n64` | 0 | 1 | 0.25 |
| `z3__AUFNIRA_z3.637557.smt2` | `n8` | 8 | `pilotCost_n8` | 0 | 0 | 0.5 |
| `z3__AUFNIRA_z3.637557.smt2` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.25 |
| `z3__AUFNIRA_z3.637557.smt2` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.5 |
| `z3__AUFNIRA_z3.637557.smt2` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.5 |
| `z3__LRA_formula_277.smt2` | `n8` | 8 | `balanced_n8` | 0 | 1 | 0.25 |
| `z3__LRA_formula_277.smt2` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.25 |
| `z3__LRA_formula_277.smt2` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `z3__LRA_formula_277.smt2` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.5 |
| `z3__QF_AUFBV_891_sqlite3.smt2` | `n8` | 8 | `balanced_n8` | 0 | 1 | 0.2 |
| `z3__QF_AUFBV_891_sqlite3.smt2` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.25 |
| `z3__QF_AUFBV_891_sqlite3.smt2` | `n32` | 32 | `SRSSampling_n32` | 1 | 1 | 0.2 |
| `z3__QF_AUFBV_891_sqlite3.smt2` | `n64` | 64 | `pairwise_n64` | 0 | 1 | 0.25 |
| `z3__QF_AUFLIA_swap_t1_pp_nf_ai_00010_002.cvc.smt2` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.2 |
| `z3__QF_AUFLIA_swap_t1_pp_nf_ai_00010_002.cvc.smt2` | `n16` | 16 | `balanced_n16` | 0 | 1 | 0.2 |
| `z3__QF_AUFLIA_swap_t1_pp_nf_ai_00010_002.cvc.smt2` | `n32` | 32 | `SRSSampling_n32` | 1 | 1 | 0.2 |
| `z3__QF_AUFLIA_swap_t1_pp_nf_ai_00010_002.cvc.smt2` | `n64` | 64 | `pairwise_n64` | 0 | 1 | 0.3333 |
| `z3__QF_BV_bench_3176.smt2` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.25 |
| `z3__QF_BV_bench_3176.smt2` | `n16` | 16 | `random_n16` | 0 | 0 | 0.3333 |
| `z3__QF_BV_bench_3176.smt2` | `n32` | 32 | `balanced_n32` | 0 | 1 | 0.25 |
| `z3__QF_BV_bench_3176.smt2` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.3333 |
| `z3__QF_BV_bench_935.smt2` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.25 |
| `z3__QF_BV_bench_935.smt2` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.3333 |
| `z3__QF_BV_bench_935.smt2` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.25 |
| `z3__QF_BV_bench_935.smt2` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.25 |
| `z3__QF_LIA_tightrhombus` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.5 |
| `z3__QF_LIA_tightrhombus` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.25 |
| `z3__QF_LIA_tightrhombus` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.25 |
| `z3__QF_LIA_tightrhombus` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.3333 |
| `z3__QF_LRA_clocksynchro_7clocks.worst_case_skew.induct.smt2` | `n8` | 8 | `diversity_n8` | 0 | 1 | 0.2 |
| `z3__QF_LRA_clocksynchro_7clocks.worst_case_skew.induct.smt2` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.3333 |
| `z3__QF_LRA_clocksynchro_7clocks.worst_case_skew.induct.smt2` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.3333 |
| `z3__QF_LRA_clocksynchro_7clocks.worst_case_skew.induct.smt2` | `n64` | 64 | `SRSSampling_n64` | 1 | 1 | 0.25 |
| `z3__QF_NRA_hong_9.smt2` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.25 |
| `z3__QF_NRA_hong_9.smt2` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.25 |
| `z3__QF_NRA_hong_9.smt2` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.25 |
| `z3__QF_NRA_hong_9.smt2` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.3333 |
| `z3__QF_RDL_orb08_888.smt2` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.2 |
| `z3__QF_RDL_orb08_888.smt2` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.5 |
| `z3__QF_RDL_orb08_888.smt2` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.25 |
| `z3__QF_RDL_orb08_888.smt2` | `n64` | 64 | `diversity_n64` | 0 | 1 | 0.25 |
| `z3__QF_UFLIA_xs_23_43.smt2` | `n8` | 8 | `diversity_n8` | 0 | 1 | 0.1667 |
| `z3__QF_UFLIA_xs_23_43.smt2` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.5 |
| `z3__QF_UFLIA_xs_23_43.smt2` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `z3__QF_UFLIA_xs_23_43.smt2` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.3333 |
| `z3__QF_UF_PEQ018_size6.smt2` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.2 |
| `z3__QF_UF_PEQ018_size6.smt2` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.5 |
| `z3__QF_UF_PEQ018_size6.smt2` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.25 |
| `z3__QF_UF_PEQ018_size6.smt2` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.25 |

## Budget Scaling

| Strategy | Risk non-increasing | Posterior area non-decreasing | Omega(size) >= 0 all contexts | Omega(cost) >= 0 all contexts |
|---|---:|---:|---:|---:|
| `random` | 93/93 | 93/93 | 11/93 | 11/93 |
| `balanced` | 81/93 | 83/93 | 44/93 | 45/93 |
| `diversity` | 93/93 | 93/93 | 28/93 | 27/93 |
| `SRSSampling` | 93/93 | 93/93 | 11/93 | 12/93 |
| `pairwise` | 30/93 | 30/93 | 19/93 | 19/93 |
| `pilotCost` | 62/93 | 60/93 | 9/93 | 9/93 |

For SRS, posterior risk is non-increasing in 93/93 contexts and posterior area is non-decreasing in 93/93 contexts.
