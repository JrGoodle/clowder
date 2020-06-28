#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

export examples=( \
    # 'init' \
    # 'herd' \
    'status' \
)

for example in "${examples[@]}"; do
    terminalizer render $example -o "clowder-${example}.gif" || exit 1
    # imageoptim --imagealpha "clowder-${example}.gif" || exit 1
    imageoptim "clowder-${example}.gif" || exit 1
done
