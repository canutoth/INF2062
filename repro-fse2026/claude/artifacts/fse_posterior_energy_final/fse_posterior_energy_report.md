# FSE 2026 posterior-risk revisit on the ENERGY (Twins) family

## Scope

This applies the FSE posterior-risk/posterior-confidence framework to the
TwinsOrFalseFriends energy corpus. Each scenario is one (system, cost property,
target property) combination; acquisition cost is the measured cost property
(energy or runtime), so the same sampling question is asked under a different
notion of cost. Posterior risk is relative to the measured configuration table.

Source archive: `/Users/mathieuacher/SANDBOX/cost-sampling-icse2027/data/curated/energy/twins_energy_subset.zip`.
Systems analyzed: `7z, Apache, HSQLDB, LLVM, MongoDB, PostgreSQL, VP8, brotli, exastencils, jump3r, kanzi, lrzip, nginx, x264`.
Cost properties: `energy, performance`; target properties: `energy, performance`.
SRS generated: `True` with `100` seeds per scenario/level.
Diagnostic oracles included: `False`.

## Headline

Strategy posterior-risk distributions differ in 212/220 scenario-level scopes.
SRS is the best empirical-cost-normalized recommendation in 9/220 scopes and appears on the empirical cost/confidence Pareto frontier in 77/220 scopes.
Cost-normalization changes the top recommendation in 31/220 scopes and changes the confidence Pareto frontier in 220/220 scopes.
SRS has lower posterior risk than random in 52/220 scopes; its empirical acquisition cost differs from random in 94/220 scopes.

Best empirical-cost-normalized pairs:

- `diversity_n32`: 30/220
- `diversity_n16`: 27/220
- `diversity_n8`: 26/220
- `diversity_n64`: 25/220
- `pairwise_n64`: 19/220
- `pairwise_n8`: 19/220
- `pairwise_n32`: 18/220
- `pairwise_n16`: 18/220
- `balanced_n16`: 11/220
- `SRSSampling_n64`: 7/220
- `balanced_n8`: 6/220
- `pilotCost_n8`: 5/220
- `random_n32`: 4/220
- `SRSSampling_n32`: 2/220
- `balanced_n32`: 2/220
- `balanced_n64`: 1/220

## Scenario-Level Summary

| Scenario | Level | n | Best cost pair | SRS best? | SRS on front? | Jaccard |
|---|---|---:|---|---:|---:|---:|
| `7z__cost_energy__target_energy` | `n8` | 8 | `balanced_n8` | 0 | 0 | 0.25 |
| `7z__cost_energy__target_energy` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.3333 |
| `7z__cost_energy__target_energy` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.25 |
| `7z__cost_energy__target_energy` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.25 |
| `7z__cost_energy__target_performance` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.3333 |
| `7z__cost_energy__target_performance` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.3333 |
| `7z__cost_energy__target_performance` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.25 |
| `7z__cost_energy__target_performance` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.2 |
| `7z__cost_performance__target_energy` | `n8` | 8 | `balanced_n8` | 0 | 1 | 0.2 |
| `7z__cost_performance__target_energy` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.2 |
| `7z__cost_performance__target_energy` | `n32` | 32 | `pairwise_n32` | 0 | 1 | 0.2 |
| `7z__cost_performance__target_energy` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.25 |
| `7z__cost_performance__target_performance` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.25 |
| `7z__cost_performance__target_performance` | `n16` | 16 | `diversity_n16` | 0 | 1 | 0.1667 |
| `7z__cost_performance__target_performance` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.25 |
| `7z__cost_performance__target_performance` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.2 |
| `Apache__cost_energy__target_energy` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.3333 |
| `Apache__cost_energy__target_energy` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.5 |
| `Apache__cost_energy__target_energy` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.5 |
| `Apache__cost_energy__target_energy` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.5 |
| `Apache__cost_energy__target_performance` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.3333 |
| `Apache__cost_energy__target_performance` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.5 |
| `Apache__cost_energy__target_performance` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.3333 |
| `Apache__cost_energy__target_performance` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.3333 |
| `Apache__cost_performance__target_energy` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.3333 |
| `Apache__cost_performance__target_energy` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.5 |
| `Apache__cost_performance__target_energy` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.5 |
| `Apache__cost_performance__target_energy` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.5 |
| `Apache__cost_performance__target_performance` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.3333 |
| `Apache__cost_performance__target_performance` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.5 |
| `Apache__cost_performance__target_performance` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.3333 |
| `Apache__cost_performance__target_performance` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.3333 |
| `HSQLDB__cost_energy__target_energy` | `n8` | 8 | `diversity_n8` | 0 | 1 | 0.2 |
| `HSQLDB__cost_energy__target_energy` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.5 |
| `HSQLDB__cost_energy__target_energy` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `HSQLDB__cost_energy__target_energy` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.5 |
| `HSQLDB__cost_energy__target_performance` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.25 |
| `HSQLDB__cost_energy__target_performance` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.5 |
| `HSQLDB__cost_energy__target_performance` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `HSQLDB__cost_energy__target_performance` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.25 |
| `HSQLDB__cost_performance__target_energy` | `n8` | 8 | `diversity_n8` | 0 | 1 | 0.2 |
| `HSQLDB__cost_performance__target_energy` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.5 |
| `HSQLDB__cost_performance__target_energy` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `HSQLDB__cost_performance__target_energy` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.5 |
| `HSQLDB__cost_performance__target_performance` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.25 |
| `HSQLDB__cost_performance__target_performance` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.5 |
| `HSQLDB__cost_performance__target_performance` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `HSQLDB__cost_performance__target_performance` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.25 |
| `LLVM__cost_energy__target_energy` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.2 |
| `LLVM__cost_energy__target_energy` | `n16` | 16 | `balanced_n16` | 0 | 0 | 0.3333 |
| `LLVM__cost_energy__target_energy` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.5 |
| `LLVM__cost_energy__target_energy` | `n64` | 64 | `SRSSampling_n64` | 1 | 1 | 0.3333 |
| `LLVM__cost_energy__target_performance` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.2 |
| `LLVM__cost_energy__target_performance` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.3333 |
| `LLVM__cost_energy__target_performance` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.5 |
| `LLVM__cost_energy__target_performance` | `n64` | 64 | `SRSSampling_n64` | 1 | 1 | 0.3333 |
| `LLVM__cost_performance__target_energy` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.1667 |
| `LLVM__cost_performance__target_energy` | `n16` | 16 | `balanced_n16` | 0 | 0 | 0.3333 |
| `LLVM__cost_performance__target_energy` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.5 |
| `LLVM__cost_performance__target_energy` | `n64` | 64 | `SRSSampling_n64` | 1 | 1 | 0.3333 |
| `LLVM__cost_performance__target_performance` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.1667 |
| `LLVM__cost_performance__target_performance` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.3333 |
| `LLVM__cost_performance__target_performance` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.5 |
| `LLVM__cost_performance__target_performance` | `n64` | 64 | `SRSSampling_n64` | 1 | 1 | 0.3333 |
| `MongoDB__cost_energy__target_energy` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.3333 |
| `MongoDB__cost_energy__target_energy` | `n16` | 16 | `balanced_n16` | 0 | 1 | 0.2 |
| `MongoDB__cost_energy__target_energy` | `n32` | 32 | `SRSSampling_n32` | 1 | 1 | 0.25 |
| `MongoDB__cost_energy__target_energy` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.3333 |
| `MongoDB__cost_energy__target_performance` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.3333 |
| `MongoDB__cost_energy__target_performance` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.3333 |
| `MongoDB__cost_energy__target_performance` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `MongoDB__cost_energy__target_performance` | `n64` | 64 | `SRSSampling_n64` | 1 | 1 | 0.25 |
| `MongoDB__cost_performance__target_energy` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.3333 |
| `MongoDB__cost_performance__target_energy` | `n16` | 16 | `balanced_n16` | 0 | 1 | 0.1667 |
| `MongoDB__cost_performance__target_energy` | `n32` | 32 | `SRSSampling_n32` | 1 | 1 | 0.25 |
| `MongoDB__cost_performance__target_energy` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.3333 |
| `MongoDB__cost_performance__target_performance` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.3333 |
| `MongoDB__cost_performance__target_performance` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.3333 |
| `MongoDB__cost_performance__target_performance` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `MongoDB__cost_performance__target_performance` | `n64` | 64 | `SRSSampling_n64` | 1 | 1 | 0.25 |
| `PostgreSQL__cost_energy__target_energy` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.25 |
| `PostgreSQL__cost_energy__target_energy` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.25 |
| `PostgreSQL__cost_energy__target_energy` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.2 |
| `PostgreSQL__cost_energy__target_energy` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.3333 |
| `PostgreSQL__cost_energy__target_performance` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.25 |
| `PostgreSQL__cost_energy__target_performance` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.3333 |
| `PostgreSQL__cost_energy__target_performance` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.25 |
| `PostgreSQL__cost_energy__target_performance` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.5 |
| `PostgreSQL__cost_performance__target_energy` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.2 |
| `PostgreSQL__cost_performance__target_energy` | `n16` | 16 | `pairwise_n16` | 0 | 1 | 0.1667 |
| `PostgreSQL__cost_performance__target_energy` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.2 |
| `PostgreSQL__cost_performance__target_energy` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.3333 |
| `PostgreSQL__cost_performance__target_performance` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.2 |
| `PostgreSQL__cost_performance__target_performance` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.3333 |
| `PostgreSQL__cost_performance__target_performance` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.25 |
| `PostgreSQL__cost_performance__target_performance` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.5 |
| `VP8__cost_energy__target_energy` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.25 |
| `VP8__cost_energy__target_energy` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.25 |
| `VP8__cost_energy__target_energy` | `n32` | 32 | `diversity_n32` | 0 | 1 | 0.1667 |
| `VP8__cost_energy__target_energy` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.3333 |
| `VP8__cost_energy__target_performance` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.25 |
| `VP8__cost_energy__target_performance` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.25 |
| `VP8__cost_energy__target_performance` | `n32` | 32 | `diversity_n32` | 0 | 1 | 0.1667 |
| `VP8__cost_energy__target_performance` | `n64` | 64 | `diversity_n64` | 0 | 1 | 0.1667 |
| `VP8__cost_performance__target_energy` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.2 |
| `VP8__cost_performance__target_energy` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.2 |
| `VP8__cost_performance__target_energy` | `n32` | 32 | `diversity_n32` | 0 | 1 | 0.1667 |
| `VP8__cost_performance__target_energy` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.3333 |
| `VP8__cost_performance__target_performance` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.2 |
| `VP8__cost_performance__target_performance` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.25 |
| `VP8__cost_performance__target_performance` | `n32` | 32 | `diversity_n32` | 0 | 1 | 0.1667 |
| `VP8__cost_performance__target_performance` | `n64` | 64 | `diversity_n64` | 0 | 1 | 0.1667 |
| `brotli__cost_energy__target_energy` | `n8` | 8 | `pilotCost_n8` | 0 | 1 | 0.1667 |
| `brotli__cost_energy__target_energy` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.25 |
| `brotli__cost_energy__target_energy` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `brotli__cost_energy__target_performance` | `n8` | 8 | `pilotCost_n8` | 0 | 1 | 0.1667 |
| `brotli__cost_energy__target_performance` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.25 |
| `brotli__cost_energy__target_performance` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `brotli__cost_performance__target_energy` | `n8` | 8 | `pilotCost_n8` | 0 | 0 | 0.2 |
| `brotli__cost_performance__target_energy` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.25 |
| `brotli__cost_performance__target_energy` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `brotli__cost_performance__target_performance` | `n8` | 8 | `pilotCost_n8` | 0 | 0 | 0.2 |
| `brotli__cost_performance__target_performance` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.25 |
| `brotli__cost_performance__target_performance` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `exastencils__cost_energy__target_energy` | `n8` | 8 | `balanced_n8` | 0 | 1 | 0.2 |
| `exastencils__cost_energy__target_energy` | `n16` | 16 | `balanced_n16` | 0 | 1 | 0.1667 |
| `exastencils__cost_energy__target_energy` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.2 |
| `exastencils__cost_energy__target_energy` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.2 |
| `exastencils__cost_energy__target_performance` | `n8` | 8 | `balanced_n8` | 0 | 1 | 0.2 |
| `exastencils__cost_energy__target_performance` | `n16` | 16 | `pairwise_n16` | 0 | 1 | 0.2 |
| `exastencils__cost_energy__target_performance` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.2 |
| `exastencils__cost_energy__target_performance` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.2 |
| `exastencils__cost_performance__target_energy` | `n8` | 8 | `balanced_n8` | 0 | 1 | 0.1667 |
| `exastencils__cost_performance__target_energy` | `n16` | 16 | `balanced_n16` | 0 | 1 | 0.1667 |
| `exastencils__cost_performance__target_energy` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.2 |
| `exastencils__cost_performance__target_energy` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.2 |
| `exastencils__cost_performance__target_performance` | `n8` | 8 | `balanced_n8` | 0 | 1 | 0.1667 |
| `exastencils__cost_performance__target_performance` | `n16` | 16 | `pairwise_n16` | 0 | 1 | 0.2 |
| `exastencils__cost_performance__target_performance` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.2 |
| `exastencils__cost_performance__target_performance` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.2 |
| `jump3r__cost_energy__target_energy` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.3333 |
| `jump3r__cost_energy__target_energy` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.25 |
| `jump3r__cost_energy__target_energy` | `n32` | 32 | `random_n32` | 0 | 1 | 0.1667 |
| `jump3r__cost_energy__target_energy` | `n64` | 64 | `SRSSampling_n64` | 1 | 1 | 0.2 |
| `jump3r__cost_energy__target_performance` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.3333 |
| `jump3r__cost_energy__target_performance` | `n16` | 16 | `balanced_n16` | 0 | 1 | 0.1667 |
| `jump3r__cost_energy__target_performance` | `n32` | 32 | `random_n32` | 0 | 1 | 0.1667 |
| `jump3r__cost_energy__target_performance` | `n64` | 64 | `balanced_n64` | 0 | 1 | 0.1667 |
| `jump3r__cost_performance__target_energy` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.3333 |
| `jump3r__cost_performance__target_energy` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.25 |
| `jump3r__cost_performance__target_energy` | `n32` | 32 | `random_n32` | 0 | 1 | 0.1667 |
| `jump3r__cost_performance__target_energy` | `n64` | 64 | `pairwise_n64` | 0 | 1 | 0.2 |
| `jump3r__cost_performance__target_performance` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.3333 |
| `jump3r__cost_performance__target_performance` | `n16` | 16 | `pairwise_n16` | 0 | 1 | 0.1667 |
| `jump3r__cost_performance__target_performance` | `n32` | 32 | `random_n32` | 0 | 1 | 0.1667 |
| `jump3r__cost_performance__target_performance` | `n64` | 64 | `pairwise_n64` | 0 | 1 | 0.1667 |
| `kanzi__cost_energy__target_energy` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.2 |
| `kanzi__cost_energy__target_energy` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.25 |
| `kanzi__cost_energy__target_energy` | `n32` | 32 | `pairwise_n32` | 0 | 1 | 0.25 |
| `kanzi__cost_energy__target_energy` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.2 |
| `kanzi__cost_energy__target_performance` | `n8` | 8 | `pilotCost_n8` | 0 | 1 | 0.2 |
| `kanzi__cost_energy__target_performance` | `n16` | 16 | `diversity_n16` | 0 | 1 | 0.2 |
| `kanzi__cost_energy__target_performance` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.2 |
| `kanzi__cost_energy__target_performance` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.25 |
| `kanzi__cost_performance__target_energy` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.2 |
| `kanzi__cost_performance__target_energy` | `n16` | 16 | `pairwise_n16` | 0 | 1 | 0.25 |
| `kanzi__cost_performance__target_energy` | `n32` | 32 | `pairwise_n32` | 0 | 1 | 0.25 |
| `kanzi__cost_performance__target_energy` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.2 |
| `kanzi__cost_performance__target_performance` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.2 |
| `kanzi__cost_performance__target_performance` | `n16` | 16 | `pairwise_n16` | 0 | 1 | 0.25 |
| `kanzi__cost_performance__target_performance` | `n32` | 32 | `pairwise_n32` | 0 | 1 | 0.1667 |
| `kanzi__cost_performance__target_performance` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.25 |
| `lrzip__cost_energy__target_energy` | `n8` | 8 | `diversity_n8` | 0 | 1 | 0.25 |
| `lrzip__cost_energy__target_energy` | `n16` | 16 | `diversity_n16` | 0 | 1 | 0.1667 |
| `lrzip__cost_energy__target_energy` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.2 |
| `lrzip__cost_energy__target_energy` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.5 |
| `lrzip__cost_energy__target_performance` | `n8` | 8 | `diversity_n8` | 0 | 1 | 0.2 |
| `lrzip__cost_energy__target_performance` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.3333 |
| `lrzip__cost_energy__target_performance` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.2 |
| `lrzip__cost_energy__target_performance` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.5 |
| `lrzip__cost_performance__target_energy` | `n8` | 8 | `diversity_n8` | 0 | 1 | 0.2 |
| `lrzip__cost_performance__target_energy` | `n16` | 16 | `diversity_n16` | 0 | 1 | 0.1667 |
| `lrzip__cost_performance__target_energy` | `n32` | 32 | `diversity_n32` | 0 | 1 | 0.1667 |
| `lrzip__cost_performance__target_energy` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.5 |
| `lrzip__cost_performance__target_performance` | `n8` | 8 | `diversity_n8` | 0 | 1 | 0.1667 |
| `lrzip__cost_performance__target_performance` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.3333 |
| `lrzip__cost_performance__target_performance` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.2 |
| `lrzip__cost_performance__target_performance` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.5 |
| `nginx__cost_energy__target_energy` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.25 |
| `nginx__cost_energy__target_energy` | `n16` | 16 | `balanced_n16` | 0 | 1 | 0.2 |
| `nginx__cost_energy__target_energy` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `nginx__cost_energy__target_energy` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.3333 |
| `nginx__cost_energy__target_performance` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.25 |
| `nginx__cost_energy__target_performance` | `n16` | 16 | `balanced_n16` | 0 | 1 | 0.1667 |
| `nginx__cost_energy__target_performance` | `n32` | 32 | `balanced_n32` | 0 | 1 | 0.2 |
| `nginx__cost_energy__target_performance` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.3333 |
| `nginx__cost_performance__target_energy` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.25 |
| `nginx__cost_performance__target_energy` | `n16` | 16 | `balanced_n16` | 0 | 1 | 0.2 |
| `nginx__cost_performance__target_energy` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `nginx__cost_performance__target_energy` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.3333 |
| `nginx__cost_performance__target_performance` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.25 |
| `nginx__cost_performance__target_performance` | `n16` | 16 | `balanced_n16` | 0 | 0 | 0.2 |
| `nginx__cost_performance__target_performance` | `n32` | 32 | `balanced_n32` | 0 | 1 | 0.2 |
| `nginx__cost_performance__target_performance` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.3333 |
| `x264__cost_energy__target_energy` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.25 |
| `x264__cost_energy__target_energy` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.3333 |
| `x264__cost_energy__target_energy` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.25 |
| `x264__cost_energy__target_energy` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.3333 |
| `x264__cost_energy__target_performance` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.25 |
| `x264__cost_energy__target_performance` | `n16` | 16 | `diversity_n16` | 0 | 1 | 0.3333 |
| `x264__cost_energy__target_performance` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.25 |
| `x264__cost_energy__target_performance` | `n64` | 64 | `pairwise_n64` | 0 | 1 | 0.25 |
| `x264__cost_performance__target_energy` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.25 |
| `x264__cost_performance__target_energy` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.3333 |
| `x264__cost_performance__target_energy` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.2 |
| `x264__cost_performance__target_energy` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.25 |
| `x264__cost_performance__target_performance` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.25 |
| `x264__cost_performance__target_performance` | `n16` | 16 | `diversity_n16` | 0 | 1 | 0.3333 |
| `x264__cost_performance__target_performance` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.2 |
| `x264__cost_performance__target_performance` | `n64` | 64 | `pairwise_n64` | 0 | 1 | 0.2 |

## Budget Scaling

| Strategy | Risk non-increasing | Posterior area non-decreasing | Omega(size) >= 0 all scenarios | Omega(cost) >= 0 all scenarios |
|---|---:|---:|---:|---:|
| `random` | 56/56 | 56/56 | 4/56 | 10/56 |
| `balanced` | 54/56 | 56/56 | 22/56 | 25/56 |
| `diversity` | 56/56 | 56/56 | 30/56 | 29/56 |
| `SRSSampling` | 56/56 | 56/56 | 4/56 | 3/56 |
| `pairwise` | 22/56 | 22/56 | 16/56 | 17/56 |
| `pilotCost` | 13/56 | 12/56 | 0/56 | 4/56 |

For SRS, posterior risk is non-increasing in 56/56 scenarios and posterior area is non-decreasing in 56/56 scenarios.
