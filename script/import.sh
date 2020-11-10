# shellcheck shell=bash

# Homebrew
homebrew_path='/usr/local/bin:/usr/local/sbin'
export PATH="$homebrew_path:$PATH"

# Homebrew Python
homebrew_python_path='/usr/local/opt/python/libexec/bin'
export PATH="$homebrew_python_path:$PATH"

# Pipenv
user_python_bin="$(python -m site --user-base)/bin"
local_python_bin="$HOME/.local/bin"
export PATH="$user_python_bin:$local_python_bin:$PATH"

# pyenv
if command -v pyenv 1>/dev/null 2>&1; then eval "$(pyenv init -)"; fi

# PYTHONPATH
repo_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."
export PYTHONPATH="${repo_dir}:${PYTHONPATH-}"
