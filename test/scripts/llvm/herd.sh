#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

export project_paths=( 'llvm' \
                       'klee' \
                       'libclc' \
                       'llvm/projects/dragonegg' \
                       'llvm/projects/libunwind' \
                       'openmp' \
                       'polly' \
                       'poolalloc' \
                       'vmkit' \
                       'zorg' \
                       'lldb' \
                       'llvm/tools/lld' \
                       'llvm/projects/libcxx' \
                       'llvm/projects/libcxxabi' \
                       'lnt' \
                       'test-suite' )

export fork_paths=( 'llvm/tools/clang' \
                    'llvm/tools/clang/tools/extra' \
                    'llvm/projects/compiler-rt' )

print_double_separator
echo 'TEST: Test clowder herd'
print_double_separator
cd "$LLVM_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh

test_init_herd() {
    print_double_separator
    echo "TEST: Normal herd after init"
    $COMMAND herd $PARALLEL || exit 1
    echo "TEST: Check current branches are on master"
    for project in "${project_paths[@]}"; do
        pushd $project || exit 1
        test_branch master
        test_tracking_branch_exists master
        popd || exit 1
    done
    for project in "${fork_paths[@]}"; do
        pushd $project || exit 1
        test_branch master
        test_tracking_branch_exists master
        popd || exit 1
    done
}
test_init_herd

$COMMAND status || exit 1
