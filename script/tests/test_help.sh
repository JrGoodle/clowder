#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

cd "$1" || exit 1

export commands=( 'clean' \
                  'diff' \
                  'forall' \
                  'herd' \
                  'init' \
                  'link' \
                  'prune' \
                  'repo' \
                  'repo add' \
                  'repo checkout' \
                  'repo clean' \
                  'repo commit' \
                  'repo pull' \
                  'repo push' \
                  'repo run' \
                  'repo status' \
                  'save' \
                  'start' \
                  'stash' \
                  'status')

print_separator
echo "TEST: Clowder help output"

print_separator
echo "TEST: clowder -h"
clowder -h

for command in "${commands[@]}"; do
	print_separator
    echo "TEST: clowder $command -h"
    clowder $command -h
done
