# Paper Figure Sets

This folder contains curated copies of figures that are likely to be reused in
the paper. These files are copies, not the canonical generated outputs. The
source experiment folders remain the provenance source for regeneration.

## Figure Sets

| Folder | Use |
|---|---|
| `twins_brotli_pairwise_n8/` | Caricatural TwinsOrFalseFriends example where a deployable strategy is badly calibrated with respect to empirical cost; includes the paper-facing trajectory + distribution figure and fixed-`n=8` variant. |
| `twins_lrzip_n_proxy_counterexample/` | Within-Twins fixed-`n=16` stress case showing nearly identical MRE but a 16.5x empirical-cost gap; includes the right-side plot used in the paper's integrated Figure 1. Error is high because the budget is small. |
| `twins_jump3r_runlevel_n_proxy_counterexample/` | Within-Twins run-level fixed-`n=128` counterexample: two actual repeated samples have about 17.5% MRE but a 12.5x empirical-cost gap. |
| `lcbench_christine_n_proxy_counterexample/` | Low-MRE fixed-`n=8` counterexample showing 4.1% MRE with a 31.3x empirical-cost gap. |
