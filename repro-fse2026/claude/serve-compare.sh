#!/usr/bin/env bash
# Serves the paper variant comparison tool
# Open http://localhost:8765/compare-variants.html
cd "$(dirname "$0")"
echo "Open http://localhost:8765/compare-variants.html"
python3 -m http.server 8765
