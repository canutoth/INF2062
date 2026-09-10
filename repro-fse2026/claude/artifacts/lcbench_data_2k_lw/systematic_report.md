# LCBench systematic study

## Scope

Workloads analyzed: `35` OpenML datasets.

Configurations per dataset: `2000`. Seeds per budget: `30`.

Target: `final_val_accuracy`. Cost: `time_total`.

## Aggregate signal

- Cost heterogeneity spans CV `0.5947` to `2.247`.
- Count-cost Spearman spans `0.5433` to `0.9177`.
- Median `%cost/%n` spans `0.6694` to `1.012`.
- Top-1 agreement spans `0` to `1`.
- Pareto Jaccard spans `0.1818` to `1`.

## Hypothesis robustness across datasets

- `H1a`: 35/35 support, 0 refute, 0 inconclusive (fully robust)
- `H1b`: 35/35 support, 0 refute, 0 inconclusive (fully robust)
- `H2a`: 35/35 support, 0 refute, 0 inconclusive (fully robust)
- `H2b`: 31/35 support, 3 refute, 1 inconclusive (mostly robust)
- `H2c`: 35/35 support, 0 refute, 0 inconclusive (fully robust)
- `H3a`: 33/35 support, 2 refute, 0 inconclusive (mostly robust)
- `H3b`: --
- `H4a`: 32/35 support, 3 refute, 0 inconclusive (mostly robust)
- `H4b`: 32/35 support, 3 refute, 0 inconclusive (mostly robust)
- `H5a`: supports (dataset-level ratio spread=0.3423; stored H5a verdict=supports)
- `H5c`: supports (mean Kendall tau range 0.3292-0.7043; median Pareto Jaccard=0.5)

## Readout

- Weakest workload-level hypothesis by support rate: `H2b` with `0.8857` support rate.
- H5a stored verdict: `supports` (p=`4.489e-71`, spread=`0.3423`).

## Aggregate verdict table

| Hypothesis | Supports | Refutes | Inconclusive | Global verdict |
|---|---:|---:|---:|---|
| `H1a` | 35 | 0 | 0 | `supported (35/35)` |
| `H1b` | 35 | 0 | 0 | `supported (35/35)` |
| `H2a` | 35 | 0 | 0 | `supported (35/35)` |
| `H2b` | 31 | 3 | 1 | `supported (31/35)` |
| `H2c` | 35 | 0 | 0 | `supported (35/35)` |
| `H3a` | 33 | 2 | 0 | `supported (33/35)` |
| `H4a` | 32 | 3 | 0 | `supported (32/35)` |
| `H4b` | 32 | 3 | 0 | `supported (32/35)` |
| `H5a` | 1 | 0 | 0 | `supported (1/1)` |
| `H5c` | 1 | 0 | 0 | `supported (1/1)` |
