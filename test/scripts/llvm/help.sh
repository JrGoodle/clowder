#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

print_double_separator
echo 'TEST: llvm projects example test script'
print_double_separator

cd "$LLVM_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh

test_help() {
    $COMMAND link || exit 1
    $COMMAND herd $PARALLEL || exit 1
    "$TEST_SCRIPT_DIR/test_help.sh" "$LLVM_EXAMPLE_DIR" || exit 1
}
test_help
