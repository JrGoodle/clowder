#!/usr/bin/env bash

set -euo pipefail
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export examples=( \
    # 'init' \
    # 'herd' \
    'status' \
)

for example in "${examples[@]}"; do
    terminalizer render $example -o "clowder-${example}.gif"
    # imageoptim --imagealpha "clowder-${example}.gif"
    imageoptim "clowder-${example}.gif"
done
