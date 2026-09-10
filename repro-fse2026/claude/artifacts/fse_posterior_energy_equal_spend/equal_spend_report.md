# Equal-measured-spend comparison (ENERGY family)

Budget per scope: B = n_ref x mean pool cost (uniform random's expected
spend at n_ref). Every strategy buys as many configurations as B affords
(binary search on its own sample size, capped at the protocol grid
maximum; cap hits are censoring, counted below). Outcome: realized
max-bound posterior risk at equal spend.

Systems: 7z, Apache, HSQLDB, LLVM, MongoDB, PostgreSQL, VP8, brotli, exastencils, jump3r, kanzi, lrzip, nginx, x264. Properties (cost=target): energy, performance.
Reference levels: n8, n16, n32, n64. Stochastic seeds: 30 (SRS 30).

## Headline

Scopes (scenario x budget level): 110.
pilotCost beats random at equal spend in 11/110 scopes (median affordable-n multiplier 2.05x; capped in 12 scopes).
SRS beats random at equal spend in 49/110 scopes.

Equal-spend winners:

- `diversity`: 47/110
- `pairwise`: 28/110
- `balanced`: 14/110
- `SRSSampling`: 14/110
- `random`: 4/110
- `pilotCost`: 3/110
