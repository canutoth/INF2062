#!/bin/sh
# Resumable full Linux pass: one release per invocation; rerun to resume.
cd "$(dirname "$0")/.." || exit 1
for rel in 413 415 420 500 504 507 508; do
  out="artifacts/fse_posterior_linux_full_parts/r${rel}"
  if [ -f "$out/posterior_linux_release_summary.csv" ]; then
    echo "[parts] $rel already done, skipping"
    continue
  fi
  echo "[parts] running release $rel"
  python3.13 scripts/run_fse_posterior_linux_batch.py \
    --releases "$rel" \
    --output-dir "$out" \
    --target-column vmlinux \
    --levels 0.01,0.02,0.05 \
    --stochastic-runs 100 \
    --diversity-runs 20 --uncertainty-runs 20 --coverage-runs 20 \
    --srs-seeds 100 --top-k-features 512 \
    --extreme max --prior-offset 1 || echo "[parts] release $rel FAILED (exit $?)"
done
echo "[parts] sweep complete"
