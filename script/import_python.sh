# shellcheck shell=bash
# shellcheck disable=SC1090
# shellcheck disable=SC2153

# Homebrew Python
if command -v brew 1>/dev/null 2>&1; then
    homebrew_python_path="$(brew --prefix)/opt/python/libexec/bin"
    export PATH="$homebrew_python_path:$PATH"
fi

# Pipenv
# Depending on whether pyenv is automatically detected, the user site packages could be in different locations.
# Manually set it to the ~/.local/bin directory if it exists, otherwise use the directory python returns.
local_python_bin="$HOME/.local/bin"
if [ -d "$local_python_bin" ]; then
    export PATH="$local_python_bin:$PATH"
else
    if command -v python 1>/dev/null 2>&1; then
        user_python_bin="$(python -m site --user-base)/bin"
        export PATH="$user_python_bin:$PATH"
    fi
fi

# pyenv
if command -v pyenv 1>/dev/null 2>&1; then eval "$(pyenv init -)" || true; fi
