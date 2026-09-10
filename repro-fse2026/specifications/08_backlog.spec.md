# Specification 08 — Execution Backlog & Open Decisions

Living checklist. Update as items close. Source: the protocol decisions in
Spec 00 §8.

---

## 1. Highest-priority next actions

1. ~~Decide the execution target.~~ **Done** — frozen to the working repo
   `cost-sampling-matters`, data root `ICPE-rawdata/` (Spec 00 §8 item 10).
2. Audit SRS against the FSE artifact implementation. — Spec 01.
3. ~~Freeze the prior-confidence convention.~~ **Done** — `N + 1` headline,
   `N` sensitivity per Spec 02 §3.2 (Spec 00 §8 item 1). Still to run: the
   `--prior-offset 0` sensitivity command.
4. Rerun the direct FSE artifact experiment with a clean final output path. — Spec 02.
5. Rerun the x264 final protocol using `ICPE-rawdata/AllRuns.zip`. — Spec 03.
6. Implement the `ENERGY` and `WORKLOAD` posterior wrappers by reusing the
   repo's generated-sampling code. — Spec 04 §4.
7. Decide whether the Linux quick pass is enough or a fuller run is needed. — Spec 05 §3.
8. Document LCBench JSON provenance and rerun the no-oracle final protocol. — Spec 06.
9. Build the cross-corpus synthesis table and figures. — Spec 07.
10. Write the final interpretation around "posterior guarantees per empirical
    acquisition cost." — Spec 07 §4.

## 2. Open decisions to freeze before paper-grade reruns

| # | Decision | Default / options | Status |
|---|---|---|---|
| 1 | Prior confidence convention | `N + 1` headline; `N` sensitivity | **frozen** |
| 2 | Strategy set per corpus | per Specs 02–06 command blocks | **frozen** |
| 3 | Budget levels per corpus | per Specs 02–06 command blocks | **frozen** |
| 4 | Repeated runs / seeds | smoke 30, final 100 (Specs 02–06) | **frozen** |
| 5 | Target orientation | `--extreme max` for every corpus | **frozen** |
| 6 | Cost column per corpus | x264 `time`; ENERGY `energy,performance`; LCBench `time_total` | **frozen** |
| 7 | Generated oracle strategies | excluded from headline (`--no-oracles`) | **frozen** |
| 8 | Multiple-comparison correction policy | decide before final reruns | open |
| 9 | Which generated artifacts are committed | ask user | open |
| 10 | Final rerun repo | working repo `cost-sampling-matters`, root `ICPE-rawdata/` | **frozen** |
| 11 | Public-repo integration mode | branch/PR vs supplementary vs internal-only | open |

## 3. Known blockers / missing inputs

- `references/WMS+26.pdf` — add manually if absent (Spec 00 §1).
- `$FSE_ROOT` (original FSE artifact) — external, required for Specs 01–02.
- `ICPE-rawdata/lcbench/data_2k_lw.json` — external, required for Spec 06.
- `ICPE-rawdata/twins_energy_subset.zip`, `ICPE-rawdata/workload_artifact.zip`
  — external, required for Spec 04.
- `cost_sampling/posterior_batch.py` (shared module), `scripts/run_fse_posterior_twins_batch.py`,
  `scripts/run_fse_posterior_workload_batch.py` — do not exist yet; creating them
  is part of Spec 04.
