#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

print_double_separator
echo 'TEST: cats help test script'
print_double_separator

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh || exit 1
begin_command
$COMMAND herd $PARALLEL || exit 1
end_command

export commands=( 'branch' \
                  'checkout' \
                  'clean' \
                  'config' \
                  'config clear' \
                  'config get' \
                  'config set' \
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
                  'status' \
                  'yaml' )

_test_help() {
    print_single_separator
    echo "TEST: clowder -h"
    begin_command
    $COMMAND -h || exit 1
    end_command
    begin_command
    $COMMAND || exit 1
    end_command
    begin_command
    $COMMAND config set || exit 1
    end_command

    for cmd in "${commands[@]}"; do
        print_single_separator
        echo "TEST: clowder $cmd -h"
        begin_command
        $COMMAND $cmd -h || exit 1
        end_command
    done
}

test_help() {
    print_double_separator

    begin_command
    $COMMAND repo checkout yaml-validation || exit 1
    end_command
    pushd .clowder || exit 1
    test_branch yaml-validation
    popd || exit 1

    echo "TEST: Print help with invalid clowder.yaml"
    begin_command
    $COMMAND link 'test-empty-project' || exit 1
    end_command
    _test_help

    print_double_separator
    echo "TEST: Print help with valid clowder.yaml"
    begin_command
    $COMMAND link || exit 1
    end_command
    _test_help
}
test_help
