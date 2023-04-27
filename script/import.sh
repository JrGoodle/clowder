# shellcheck shell=bash

# Homebrew
# Homebrew
intel_brew_path='/usr/local/bin/brew'
m1_brew_path='/opt/homebrew/bin/brew'
# Export Homebrew variables for current platform
if [[ -x "$m1_brew_path" ]]; then
    eval "$($m1_brew_path shellenv)"
elif [[ -x "$intel_brew_path" ]]; then
    eval "$($intel_brew_path shellenv)"
fi

# Homebrew Python
# homebrew_python_path='/usr/local/opt/python/libexec/bin'
# export PATH="$homebrew_python_path:$PATH"

# PYTHONPATH
# repo_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."
# export PYTHONPATH="${repo_dir}:${PYTHONPATH-}"
