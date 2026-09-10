# Run Manifest: FSE Posterior Guarantees Under Empirical Acquisition Cost

Execution date: 2026-07-02/03.
Repository: `cost-sampling-matters`, worktree `csm-fse-posterior`,
branch `fse/posterior-cost` (branched from `main` @ `753aa03`).
Interpreter: Homebrew `python3.13` (numpy 2.2.6, pandas 2.2.3, scipy 1.15.3,
matplotlib 3.10.3, scikit-learn 1.6.1) on macOS (Darwin 24.6.0, 16 cores).

## Data provenance

| Input | Source | Local path |
|---|---|---|
| FSE 2026 artifact (`data.zip`, `SRS-sampling.ipynb`) | Zenodo 10.5281/zenodo.19682296 (Weis et al., FSE'26, paper DOI 10.1145/3808147) | scratchpad `fse_artifact/` — `data.zip` sha256 `12ee2295d3d9d596eb57a92008b27562a0bf1882b21fcad9c8cd82082bf654bd`, selectively extracted (7 systems: `measurements.csv` + t2 samples for random/solverBased/divDistBased/twise/SRSSampling, 100 runs each); zip deleted after extraction for disk space, re-downloadable |
| x264 ICPE corpus | ICPE'20 artifact | `ICPE-rawdata/AllRuns.zip` (symlinked from main repo checkout) |
| ENERGY / Twins | Zenodo 7647208 (curated 19 MB subset from public ICSE repo) | `cost-sampling-icse2027/data/curated/energy/twins_energy_subset.zip` (14 systems; identical membership to `/private/tmp/twins_main.zip`) |
| WORKLOAD | Zenodo 7504284, Muehlbauer et al. ICSE'23 | main repo `workload-impact-ICSE2023/artifact_excluding_raw_coverage.zip` |
| Linux/TuxKConfig | TuxKConfig parquet pools | `ICPE-rawdata/linux/tuxkconfig_{413,415,420,500,504,507,508}.parquet` |
| LCBench | figshare `data_2k_lw.json` (~929 MB), file 21188598 | `/private/tmp/lcbench/data_2k_lw.json` |

## Protocol decisions frozen for these runs

1. Prior-confidence convention: artifact-compatible `N+1` (`--prior-offset 1`);
   sensitivity run with `N` (`--prior-offset 0`) produced identical headline
   decisions on the FSE artifact corpus (2/7, 6/7, 3/7, 6/7).
2. Orientation: `--extreme max` (worst-case bound) everywhere.
3. Diagnostic oracle strategies (`cheapOracle`/`expensiveOracle`) excluded
   from headline runs (`--no-oracles`), matching the LCBench no-oracle
   precedent; smoke runs confirmed oracles otherwise pollute best-pair counts.
4. SRS: code-native `srs_indices` (step 25, Welch p<0.05, random fill) for
   x264/ENERGY/WORKLOAD/Linux/LCBench; the FSE-artifact run uses the
   artifact's own shipped `SRSSampling_t2` samples (exact reuse). Audit:
   `artifacts/srs_audit_note.md` + `scripts/audit_srs_vs_artifact.py`.
5. Linux and LCBench claims are measured-pool-relative.
6. ENERGY scenarios cross `{energy,performance}` targets with
   `{energy,performance}` costs; WORKLOAD uses the measured `time` column
   (`throughput` for h2, inverse orientation) as both target and cost.

## Commands (all run from the worktree root)

Phase 2 — FSE artifact replication (+ prior sensitivity):

```bash
python3.13 scripts/run_fse_posterior_batch.py \
  --fse-root <scratchpad>/fse_artifact/extracted/data \
  --output-dir artifacts/fse_posterior_fse_artifact_final_t2 \
  --contexts ALL --strategies random,solverBased,divDistBased,twise,SRSSampling \
  --levels t2 --max-runs 100 --extreme max --prior-offset 1
# sensitivity: same with --output-dir ..._t2_priorN --prior-offset 0
```

Phase 3 — x264:

```bash
python3.13 scripts/run_fse_posterior_x264_batch.py \
  --runs-zip ICPE-rawdata/AllRuns.zip \
  --output-dir artifacts/fse_posterior_x264_icpe_final \
  --contexts 0-16 --target-props time,size --cost-prop time \
  --strategies random,solverBased,divDistBased,twise,distBased,henard \
  --levels t1,t2,t3 --fixed-level t2 --max-runs 100 --srs-seeds 100 \
  --extreme max --prior-offset 1
```

Phase 4 — ENERGY and WORKLOAD (new wrappers, this branch):

```bash
python3.13 scripts/run_fse_posterior_twins_batch.py \
  --zip <public-repo>/data/curated/energy/twins_energy_subset.zip \
  --systems ALL --target-props energy,performance --cost-props energy,performance \
  --levels n8,n16,n32,n64 --seeds 100 --srs-seeds 100 --no-oracles \
  --output-dir artifacts/fse_posterior_energy_final --extreme max --prior-offset 1

python3.13 scripts/run_fse_posterior_workload_batch.py \
  --zip <main-repo>/workload-impact-ICSE2023/artifact_excluding_raw_coverage.zip \
  --systems ALL --workloads ALL --levels n8,n16,n32,n64 --seeds 100 --srs-seeds 100 \
  --no-oracles --output-dir artifacts/fse_posterior_workload_final \
  --extreme max --prior-offset 1
```

Phase 5 — Linux quick pass:

```bash
python3.13 scripts/run_fse_posterior_linux_batch.py \
  --releases ALL --output-dir artifacts/fse_posterior_linux_all_quick_final \
  --target-column vmlinux --levels 0.01,0.02 --stochastic-runs 30 \
  --diversity-runs 5 --uncertainty-runs 5 --coverage-runs 5 --srs-seeds 30 \
  --top-k-features 512 --extreme max --prior-offset 1 --quick
```

Phase 6 — LCBench:

```bash
python3.13 scripts/run_fse_posterior_lcbench_batch.py \
  --json /private/tmp/lcbench/data_2k_lw.json --datasets ALL \
  --output-dir artifacts/fse_posterior_lcbench_no_oracles_final \
  --target-column final_val_accuracy --cost-column time_total \
  --runtime-mode last --max-budget 64 --seeds 30 --srs-seeds 30 --no-oracles \
  --extreme max --prior-offset 1
```

Phase 7 — synthesis:

```bash
python3.13 scripts/build_fse_posterior_synthesis.py
```

## Verification against roadmap sanity targets

| Corpus | Check | Result |
|---|---|---|
| FSE artifact | 7 systems, 5 strategies, no skips | pass |
| FSE artifact | SRS best 3/7, SRS Pareto 6/7, frontier changes 6/7 | exact match |
| FSE artifact | SRS exact t2 sizes | 58-98% of runs exact; deficits of <=5 configs traced to the artifact's duplicate random fill (see `srs_audit_note.md`) |
| x264 | 34 t2 scopes; differ 34/34; SRS best 26/34; Pareto 29/34; frontier 30/34 | exact match |
| Linux | 7 releases x 2 levels; differ 11/14; frontier 14/14 | match (SRS best 2/14 vs previous ~3/14, seed noise) |
| LCBench | 35 datasets, 210 scopes; SRS best 0/210; frontier 207/210 | match (differ 154 vs 155, top-change 120 vs 119) |
| ENERGY | 14 systems, 4 cost/target combos, budgets n8-n64, no skips | 220 scopes (4 of 224 scope-levels dropped by the protocol budget cap); differ 212/220, frontier 220/220, SRS best 9/220 |
| WORKLOAD | 9 systems, all 93 study contexts, no skips | 359 scopes (13 of 372 dropped by the budget cap); differ 341/359, frontier 346/359, SRS best 31/359 |
| Prior sensitivity | offset 0 vs 1 | identical headline decisions |
| Linux full protocol | 7 releases x 3 levels, 100 stochastic runs, 100 SRS seeds (resumable per-release sweep) | 21 scopes: differ 21/21, SRS best 0/21, SRS on frontier 19/21, top changes 13/21, frontier 21/21; strengthens the quick pass |
| Cross-corpus (full Linux) | 851 scopes total | empirical-cost frontier differs from count frontier in 830/851 (97.5%) |
| ENERGY equal-spend | 110 scopes, B = n_ref x mean pool cost, strategies buy what B affords | pilotCost: 2.05x volume, beats random 11/110, risk 6.6x worse; SRS beats random 49/110 with budget gradient (n8 1/28 -> n64 20/26); diversity wins 47/110 |
| LCBench equal-spend | 140 scopes, same protocol, weak cost-target coupling | pilotCost flips: beats random 84/140 (median risk ratio 0.75, 1.66x volume); SRS beats random 46/140; diversity wins 80/140 — confirms the coupling mechanism |
| BH correction (FDR 0.05) | FSE1/5/6 families per corpus | FSE1 intact everywhere except LCBench 154->144; losses only in weak FSE5/FSE6 effects |

## Caveats

- Linux quick-pass uses reduced run counts (30 stochastic / 5 per
  deterministic family); a fuller pass is specified in the roadmap if needed.
- LCBench and Linux posterior risk is pool-relative, not
  configuration-space-exhaustive.
- The FSE-artifact extraction kept only the five headline strategies at t2;
  restricted/noisy artifact variants were not downloaded.
- ENERGY/WORKLOAD final numbers: see `artifacts/fse_posterior_energy_final/`
  and `artifacts/fse_posterior_workload_final/` reports and the synthesis
  table `artifacts/fse_posterior_synthesis/fse_posterior_synthesis.md`.
