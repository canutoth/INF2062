#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

pandoc FSE2026_POSTERIOR_EMSE_MANUSCRIPT_DRAFT.md \
  --from markdown+pipe_tables+yaml_metadata_block+raw_tex+implicit_figures \
  --standalone \
  --number-sections \
  --shift-heading-level-by=-1 \
  --include-in-header=paper/emse-svjour3/svjour3-header.tex \
  -V documentclass=svjour3 \
  -V classoption=smallcondensed \
  -o paper/emse-svjour3/main.tex

python3 - <<'PY'
from pathlib import Path
import re

path = Path("paper/emse-svjour3/main.tex")
tex = path.read_text()

tex = re.sub(
    r"\\documentclass(?:\[[^\]]*\])?\{svjour3\}",
    r"\\documentclass[smallcondensed]{svjour3}",
    tex,
    count=1,
)

abstract_marker = r"\section{Abstract}\label{abstract}"
intro_marker = r"\section{Introduction}\label{introduction}"
keywords = (
    r"\keywords{configurable software systems \and performance sampling \and "
    r"posterior risk \and posterior confidence \and sampling cost \and "
    r"empirical cost \and replication \and SRS}"
)
if abstract_marker in tex and intro_marker in tex:
    tex = tex.replace(abstract_marker, r"\begin{abstract}", 1)
    tex = tex.replace(intro_marker, keywords + "\n\\end{abstract}\n\n" + intro_marker, 1)

path.write_text(tex)
PY

latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -output-directory=paper/emse-svjour3 \
  paper/emse-svjour3/main.tex
