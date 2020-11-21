# shellcheck shell=bash

# Homebrew
homebrew_path='/usr/local/bin:/usr/local/sbin'
export PATH="$homebrew_path:$PATH"

# Homebrew Python
homebrew_python_path='/usr/local/opt/python/libexec/bin'
export PATH="$homebrew_python_path:$PATH"

# Pipenv
local_python_bin="$HOME/.local/bin"
export PATH="$local_python_bin:$PATH"
user_python_bin="$(python -m site --user-base)/bin"
export PATH="$user_python_bin:$PATH"

# pyenv
if command -v pyenv 1>/dev/null 2>&1; then eval "$(pyenv init -)" || true; fi

# PYTHONPATH
repo_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."
export PYTHONPATH="${repo_dir}:${PYTHONPATH-}"
