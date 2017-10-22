#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

if [ "$1" = 'parallel' ]; then
    PARALLEL='--parallel'
fi

. test_utilities.sh

print_double_separator
echo 'TEST: llvm projects example test script'
print_double_separator

test_clowder_version

"$TEST_SCRIPT_DIR/llvm/herd.sh" $1 || exit 1
"$TEST_SCRIPT_DIR/llvm/forks.sh" $1 || exit 1
"$TEST_SCRIPT_DIR/llvm/sync.sh" $1 || exit 1
"$TEST_SCRIPT_DIR/llvm/branch.sh" $1 || exit 1
"$TEST_SCRIPT_DIR/llvm/reset.sh" $1 || exit 1

test_help() {
    print_double_separator
    cd "$LLVM_EXAMPLE_DIR" || exit 1
    clowder link || exit 1
    clowder herd $PARALLEL || exit 1
    "$TEST_SCRIPT_DIR/test_help.sh" "$LLVM_EXAMPLE_DIR" || exit 1
}
test_help
