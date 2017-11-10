#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

print_double_separator
echo 'TEST: llvm projects example test script'
print_double_separator

"$TEST_SCRIPT_DIR/llvm/herd.sh" || exit 1
"$TEST_SCRIPT_DIR/llvm/forks.sh" || exit 1
"$TEST_SCRIPT_DIR/llvm/sync.sh" || exit 1
"$TEST_SCRIPT_DIR/llvm/branch.sh" || exit 1
"$TEST_SCRIPT_DIR/llvm/reset.sh" || exit 1
"$TEST_SCRIPT_DIR/llvm/help.sh" || exit 1
