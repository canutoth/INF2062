# Aborted Linux All-Feature Full-Protocol Attempt

This directory is a partial attempt at running the full Linux protocol with `--top-k-features 0`.

It was stopped because the full protocol combines all retained Linux features with feature-space-heavy samplers (`diversity`, `uncertainty`, `coverage`). That makes it much more expensive and also mixes two questions: feature-set sensitivity and sampler sensitivity.

Use `../learner_sensitivity_linux_allfeatures_light` for the completed all-feature learner comparison.

