#!/usr/bin/env bash
# shellcheck disable=SC1091

set -euo pipefail
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."
. 'script/utils.sh'

h1 'Install pyenv python'

python_version=$(read_trim_file .python-version)
h2 "Install pyenv Python version $python_version"
run pyenv install --skip-existing "$python_version"
