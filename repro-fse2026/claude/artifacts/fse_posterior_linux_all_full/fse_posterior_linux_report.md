# Full Linux pass (merged from per-release parts)

Protocol: levels 0.01/0.02/0.05, 100 stochastic runs, 20 runs per
deterministic family, 100 SRS seeds, top-k 512 features, extreme max,
prior offset 1. Run release-by-release for jetsam resilience
(`scripts/run_linux_full_parts.sh`), merged by this script.

Scopes (release x level): 21
- risk distributions differ: 21/21
- SRS best cost-normalized: 0/21
- SRS on empirical frontier: 19/21
- top changed by cost: 13/21
- frontier changed by cost: 21/21
- SRS lower risk than random: 5/21
- SRS cost differs from random: 21/21

Per-release reports live in the part directories
(`artifacts/fse_posterior_linux_full_parts/r<release>/`).
