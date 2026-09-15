#!/usr/bin/env bash
# Use as both setup and maintenance command after repository checkout.
set -euo pipefail
TASK_REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
python3 "$TASK_REPO/tools/cloud-layer/codex_dependencies.py"
python3 "$TASK_REPO/tools/cloud-layer/codex_boot.py" --setup
