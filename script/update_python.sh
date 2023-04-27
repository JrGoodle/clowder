#!/usr/bin/env bash
# shellcheck disable=SC1091

set -euo pipefail
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."
. 'script/utils.sh'

h1 'Update Python Dependencies'

h2 'Update pip'
run python -m pip install --upgrade pip

h2 'Pipenv'

h3 'Update pipenv'
run pip install --user --upgrade pipenv

h3 'Update pipenv dependencies'
run pipenv install --dev --site-packages
