# LCBench systematic study

## Scope

Workloads analyzed: `35` OpenML datasets.

Configurations per dataset: `2000`. Seeds per budget: `2`.

Target: `final_val_accuracy`. Cost: `time_total`.

## Aggregate signal

- Cost heterogeneity spans CV `0.5947` to `2.247`.
- Count-cost Spearman spans `0.2948` to `0.6417`.
- Median `%cost/%n` spans `0.8384` to `1.034`.
- Top-1 agreement spans `0` to `1`.
- Pareto Jaccard spans `0.1667` to `1`.

## Hypothesis robustness across datasets

- `H1a`: 35/35 support, 0 refute, 0 inconclusive (fully robust)
- `H1b`: 0/35 support, 0 refute, 35 inconclusive (never supports)
- `H2a`: 32/35 support, 0 refute, 3 inconclusive (mostly robust)
- `H2b`: 0/35 support, 8 refute, 27 inconclusive (never supports)
- `H2c`: 11/35 support, 0 refute, 24 inconclusive (workload-sensitive)
- `H3a`: 33/35 support, 2 refute, 0 inconclusive (mostly robust)
- `H3b`: --
- `H4a`: 30/35 support, 5 refute, 0 inconclusive (mostly robust)
- `H4b`: 30/35 support, 5 refute, 0 inconclusive (mostly robust)
- `H5a`: refutes (dataset-level ratio spread=0.1954; stored H5a verdict=refutes)
- `H5c`: supports (mean Kendall tau range 0.2684-0.6013; median Pareto Jaccard=0.5)

## Readout

- Weakest workload-level hypothesis by support rate: `H1b` with `0` support rate.
- H5a stored verdict: `refutes` (p=`1`, spread=`0.1954`).

## Aggregate verdict table

| Hypothesis | Supports | Refutes | Inconclusive | Global verdict |
|---|---:|---:|---:|---|
| `H1a` | 35 | 0 | 0 | `supported (35/35)` |
| `H1b` | 0 | 0 | 35 | `mixed (sup=0, ref=0, inc=35 of 35)` |
| `H2a` | 32 | 0 | 3 | `supported (32/35)` |
| `H2b` | 0 | 8 | 27 | `mixed (sup=0, ref=8, inc=27 of 35)` |
| `H2c` | 11 | 0 | 24 | `mixed (sup=11, ref=0, inc=24 of 35)` |
| `H3a` | 33 | 2 | 0 | `supported (33/35)` |
| `H4a` | 30 | 5 | 0 | `supported (30/35)` |
| `H4b` | 30 | 5 | 0 | `supported (30/35)` |
| `H5a` | 0 | 1 | 0 | `refuted (1/1)` |
| `H5c` | 1 | 0 | 0 | `supported (1/1)` |
