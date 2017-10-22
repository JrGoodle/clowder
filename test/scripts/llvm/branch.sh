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

if [ -z "$TRAVIS_OS_NAME" ]; then
    setup_local_test_directory
fi

cd "$LLVM_EXAMPLE_DIR" || exit 1

print_double_separator
echo "TEST: Test clowder branch"
# ./clean.sh || exit 1
./init.sh || exit 1

test_branch() {
    echo "TEST: clowder branch"
    clowder link || exit 1
    clowder herd $PARALLEL || exit 1
    clowder branch || exit 1
    clowder branch -r || exit 1
    clowder branch -a || exit 1
    clowder branch -p 'llvm-mirror/llvm' || exit 1
    clowder branch -rp 'llvm-mirror/llvm' || exit 1
    clowder branch -ap 'llvm-mirror/llvm' || exit 1
    clowder branch -g 'clang' || exit 1
    clowder branch -rg 'clang' || exit 1
    clowder branch -ag 'clang' || exit 1
}
test_branch
