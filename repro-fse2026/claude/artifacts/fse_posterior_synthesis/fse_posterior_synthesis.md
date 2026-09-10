# Cross-corpus synthesis: posterior guarantees per empirical acquisition cost

Scope = one (context, budget-level) decision cell of the corpus (x264 restricted to the fixed `t2` level; FSE artifact is per system at `t2`).
Counts are scopes where the outcome holds.

| Corpus | Scopes | Risk differs | SRS best (cost) | SRS on front | Top changes | Frontier changes | SRS < random risk | SRS cost != random | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| FSE artifact (REPLICATION-FSE26) | 7 | 7/7 | 3/7 | 6/7 | 2/7 | 6/7 | 6/7 | 7/7 | direct replication |
| x264 (REPLICATION-ICPE20) | 34 | 34/34 | 26/34 | 29/34 | 2/34 | 30/34 | 34/34 | 32/34 | published-study replication |
| ENERGY (Twins) | 220 | 212/220 | 9/220 | 77/220 | 31/220 | 220/220 | 52/220 | 94/220 | generated protocol, energy cost |
| WORKLOAD (ICSE'23) | 359 | 341/359 | 31/359 | 139/359 | 61/359 | 346/359 | 84/359 | 149/359 | generated protocol, workload contexts |
| Linux (TuxKConfig pools) | 21 | 21/21 | 0/21 | 19/21 | 13/21 | 21/21 | 5/21 | 21/21 | external validity, pool-relative |
| LCBench (HPO pools) | 210 | 154/210 | 0/210 | 21/210 | 120/210 | 207/210 | 0/210 | 10/210 | external validity, pool-relative |

Reading guide:

- `Risk differs`: Kruskal-Wallis on posterior-risk distributions across strategies (H1).
- `SRS best (cost)`: SRS is the top integrated-confidence pick against the empirical-cost prior baseline (H3).
- `Top changes` / `Frontier changes`: switching the cost axis from sample count to measured cost changes the top pick (H2) / the confidence Pareto frontier (H4).
- Linux and LCBench statements are pool-relative (measured reference universes, not exhaustive spaces).
