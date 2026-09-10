# Linux Learner Sensitivity: Top-K 512, Light Protocol

This run is the matched control for `../learner_sensitivity_linux_allfeatures_light`.

Command:

```bash
.venv-linux/bin/python scripts/run_learner_sensitivity.py \
  --output-dir artifacts/learner_sensitivity_linux_topk512_light \
  --families linux \
  --linux-top-k-features 512 \
  --linux-diversity-runs 0 \
  --linux-uncertainty-runs 0 \
  --linux-coverage-runs 0 \
  --continue-on-error
```

All 21 jobs completed successfully. Under this matched light protocol, `ridge-log` is the best-MRE learner on 6 of 7 Linux releases; `rf-log` narrowly wins Linux 5.04.

