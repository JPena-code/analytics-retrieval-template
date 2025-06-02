#!/usr/bin/env bash
set -e

# shellcheck source=/opt/.venv/bin/activate
source /opt/.venv/bin/activate

X_PORT="${PORT:-8000}"
X_HOST="${HOST:-0.0.0.0}"

X_MODULE="${MODULE:-app.scr.main}"

cd /opt || exit 1
python -m uvicorn "$X_MODULE:app" --port "$X_PORT" --host "$X_HOST"
