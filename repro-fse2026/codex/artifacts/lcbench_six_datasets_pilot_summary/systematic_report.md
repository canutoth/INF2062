# LCBench systematic study

## Scope

Workloads analyzed: `6` OpenML datasets.

Configurations per dataset: `2000`. Seeds per budget: `10`.

Target: `final_val_accuracy`. Cost: `time_total`.

## Aggregate signal

- Cost heterogeneity spans CV `0.5947` to `1.314`.
- Count-cost Spearman spans `0.6997` to `0.8828`.
- Median `%cost/%n` spans `0.675` to `0.9848`.
- Top-1 agreement spans `0.1429` to `0.5714`.
- Pareto Jaccard spans `0.2` to `0.6667`.

## Hypothesis robustness across datasets

- `H1a`: 6/6 support, 0 refute, 0 inconclusive (fully robust)
- `H1b`: 6/6 support, 0 refute, 0 inconclusive (fully robust)
- `H2a`: 6/6 support, 0 refute, 0 inconclusive (fully robust)
- `H2b`: 5/6 support, 1 refute, 0 inconclusive (mostly robust)
- `H2c`: 6/6 support, 0 refute, 0 inconclusive (fully robust)
- `H3a`: 6/6 support, 0 refute, 0 inconclusive (fully robust)
- `H3b`: --
- `H4a`: 6/6 support, 0 refute, 0 inconclusive (fully robust)
- `H4b`: 6/6 support, 0 refute, 0 inconclusive (fully robust)
- `H5a`: supports (dataset-level ratio spread=0.3098; stored H5a verdict=supports)
- `H5c`: supports (mean Kendall tau range 0.408-0.6947; median Pareto Jaccard=0.4444)

## Readout

- Weakest workload-level hypothesis by support rate: `H2b` with `0.8333` support rate.
- H5a stored verdict: `supports` (p=`1.184e-05`, spread=`0.3098`).

## Aggregate verdict table

| Hypothesis | Supports | Refutes | Inconclusive | Global verdict |
|---|---:|---:|---:|---|
| `H1a` | 6 | 0 | 0 | `supported (6/6)` |
| `H1b` | 6 | 0 | 0 | `supported (6/6)` |
| `H2a` | 6 | 0 | 0 | `supported (6/6)` |
| `H2b` | 5 | 1 | 0 | `supported (5/6)` |
| `H2c` | 6 | 0 | 0 | `supported (6/6)` |
| `H3a` | 6 | 0 | 0 | `supported (6/6)` |
| `H4a` | 6 | 0 | 0 | `supported (6/6)` |
| `H4b` | 6 | 0 | 0 | `supported (6/6)` |
| `H5a` | 1 | 0 | 0 | `supported (1/1)` |
| `H5c` | 1 | 0 | 0 | `supported (1/1)` |
