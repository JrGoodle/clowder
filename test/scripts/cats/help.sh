#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

print_double_separator
echo 'TEST: cats help test script'
print_double_separator

cd "$CATS_EXAMPLE_DIR" || exit 1
./init.sh

export commands=( 'branch' \
                  'clean' \
                  'diff' \
                  'forall' \
                  'herd' \
                  'init' \
                  'link' \
                  'prune' \
                  'repo' \
                  'repo add' \
                #   'repo checkout' \
                #   'repo clean' \
                  'repo commit' \
                  'repo pull' \
                  'repo push' \
                  'repo run' \
                #   'repo status' \
                  'save' \
                  'start' \
                  'stash' \
                  'status' \
                  'sync' \
                  'yaml' )

_test_help() {
    print_single_separator
    echo "TEST: clowder -h"
    $COMMAND -h || exit 1

    for cmd in "${commands[@]}"; do
        print_single_separator
        echo "TEST: clowder $cmd -h"
        $COMMAND $cmd -h || exit 1
    done
}

test_help() {
    print_double_separator
    ./clean.sh
    ./init.sh || exit 1

    echo "TEST: Print help with invalid clowder.yaml"
    $COMMAND link -v 'test-missing-default-ref' || exit 1
    _test_help

    print_double_separator
    echo "TEST: Print help with valid clowder.yaml"
    $COMMAND link || exit 1
    _test_help
}
test_help
