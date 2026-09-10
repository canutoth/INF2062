# Multiple-comparison sensitivity (Benjamini-Hochberg, FDR 0.05)

BH applied within each (corpus, hypothesis) family over all conducted
tests; a scope stays supported only if its uncorrected verdict was
`supports` and its BH q-value is <= 0.05. FSE2/3/4 are decision rules
without p-values and are unaffected by correction.

| Corpus | Hypothesis | Tests | Supports (raw) | Supports (BH) | Lost |
|---|---|---:|---:|---:|---:|
| fse_artifact | FSE1 | 7 | 7 | 7 | 0 |
| fse_artifact | FSE5 | 7 | 6 | 6 | 0 |
| fse_artifact | FSE6 | 7 | 7 | 7 | 0 |
| x264 | FSE1 | 102 | 102 | 102 | 0 |
| x264 | FSE5 | 102 | 68 | 68 | 0 |
| x264 | FSE6 | 102 | 65 | 65 | 0 |
| energy | FSE1 | 220 | 212 | 212 | 0 |
| energy | FSE5 | 220 | 52 | 42 | 10 |
| energy | FSE6 | 220 | 94 | 90 | 4 |
| workload | FSE1 | 359 | 341 | 341 | 0 |
| workload | FSE5 | 359 | 84 | 70 | 14 |
| workload | FSE6 | 359 | 149 | 146 | 3 |
| linux_full | FSE1 | 21 | 21 | 21 | 0 |
| linux_full | FSE5 | 21 | 5 | 1 | 4 |
| linux_full | FSE6 | 21 | 21 | 21 | 0 |
| lcbench | FSE1 | 210 | 154 | 144 | 10 |
| lcbench | FSE5 | 204 | 0 | 0 | 0 |
| lcbench | FSE6 | 210 | 10 | 1 | 9 |

Across all families: 1398 raw supports, 1344 after BH (54 lost, 3.9%).
