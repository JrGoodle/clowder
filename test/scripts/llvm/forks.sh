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

export projects=( 'llvm-mirror/llvm' \
                  'llvm-mirror/klee' \
                  'llvm-mirror/libclc' \
                  'llvm-mirror/dragonegg' \
                  'llvm-mirror/libunwind' \
                  'llvm-mirror/openmp' \
                  'llvm-mirror/polly' \
                  'llvm-mirror/poolalloc' \
                  'llvm-mirror/vmkit' \
                  'llvm-mirror/zorg' \
                  'llvm-mirror/lldb' \
                  'llvm/tools/lld' \
                  'llvm-mirror/libcxx' \
                  'llvm-mirror/libcxxabi' \
                  'llvm-mirror/lnt' \
                  'llvm-mirror/test-suite' )

export fork_paths=( 'llvm/tools/clang' \
                    'llvm/tools/clang/tools/extra' \
                    'llvm/projects/compiler-rt' )

export fork_projects=( 'llvm-mirror/clang' \
                       'llvm-mirror/clang-tools-extra' \
                       'llvm-mirror/compiler-rt' )

print_double_separator
echo "TEST: Test clowder forks"
cd "$LLVM_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh || exit 1

"$TEST_SCRIPT_DIR/llvm/write_forks.sh" $1 || exit 1
