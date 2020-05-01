#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

print_double_separator
echo 'TEST: cats help test script'
print_double_separator

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./copy-cache.sh

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
                  'repo commit' \
                  'repo pull' \
                  'repo push' \
                  'repo run' \
                  'save' \
                  'start' \
                  'stash' \
                  'status' \
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

    $COMMAND repo checkout yaml-validation || exit 1
    pushd .clowder || exit 1
    test_branch yaml-validation
    popd || exit 1

    echo "TEST: Print help with invalid clowder.yaml"
    $COMMAND link -v 'test-missing-default-ref' || exit 1
    _test_help

    print_double_separator
    echo "TEST: Print help with valid clowder.yaml"
    $COMMAND link || exit 1
    _test_help

    $COMMAND repo checkout master || exit 1
    pushd .clowder || exit 1
    test_branch master
    popd || exit 1
}
test_help
