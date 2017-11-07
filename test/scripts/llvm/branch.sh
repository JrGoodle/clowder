#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

print_double_separator
echo "TEST: Test clowder branch"
cd "$LLVM_EXAMPLE_DIR" || exit 1
./init.sh

test_branch() {
    echo "TEST: clowder branch"
    $COMMAND link || exit 1
    $COMMAND herd $PARALLEL || exit 1
    $COMMAND branch || exit 1
    $COMMAND branch -r || exit 1
    $COMMAND branch -a || exit 1
    $COMMAND branch -p 'llvm-mirror/llvm' || exit 1
    $COMMAND branch -rp 'llvm-mirror/llvm' || exit 1
    $COMMAND branch -ap 'llvm-mirror/llvm' || exit 1
    $COMMAND branch -g 'clang' || exit 1
    $COMMAND branch -rg 'clang' || exit 1
    $COMMAND branch -ag 'clang' || exit 1
}
test_branch
