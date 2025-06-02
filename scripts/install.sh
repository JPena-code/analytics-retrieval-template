#!/usr/bin/env bash
set -e

# shellcheck source=/opt/.venv/bin/activate
source /opt/.venv/bin/activate

python -m pip install --upgrade --no-cache-dir pip

cd /opt/app || exit 1

pip install --no-cache-dir .
pip cache purge

deactivate
