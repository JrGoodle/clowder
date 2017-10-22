#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

if [ "$1" = 'parallel' ]; then
    PARALLEL='--parallel'
fi

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

test_clowder_version

# setup_old_repos() {
#     echo 'TEST: Set up older copies of repos'
#
#     # local CLANG_DIR="$LLVM_PROJECTS_DIR/llvm/tools/clang"
#     # rm -rf $CLANG_DIR
#     # mkdir -p $CLANG_DIR
#     # pushd $CLANG_DIR || exit 1
#     # git clone https://github.com/JrGoodle/clang.git .
#     # git remote remove origin
#     # git remote add origin https://github.com/llvm-mirror/clang.git
#     # git fetch
#     # git branch -u origin/master
#     # popd || exit 1
#
#     local CLANG_TOOLS_EXTRA_DIR="llvm/tools/clang/tools/extra"
#     rm -rf $CLANG_TOOLS_EXTRA_DIR
#     mkdir -p $CLANG_TOOLS_EXTRA_DIR
#     pushd $CLANG_TOOLS_EXTRA_DIR || exit 1
#     git clone https://github.com/JrGoodle/clang-tools-extra.git .
#     git remote remove origin
#     git remote add origin https://github.com/llvm-mirror/clang-tools-extra.git
#     git fetch
#     git branch -u origin/master
#     popd || exit 1
#
#     local COMPILER_RT_DIR="llvm/projects/compiler-rt"
#     rm -rf $COMPILER_RT_DIR
#     mkdir -p $COMPILER_RT_DIR
#     pushd $COMPILER_RT_DIR || exit 1
#     git clone https://github.com/JrGoodle/compiler-rt.git .
#     git remote remove origin
#     git remote add origin https://github.com/llvm-mirror/compiler-rt.git
#     git fetch
#     git branch -u origin/master
#     popd || exit 1
# }

print_double_separator
echo 'TEST: llvm projects example test script'
print_double_separator
cd "$LLVM_EXAMPLE_DIR" || exit 1
./init.sh

test_init_herd() {
    print_double_separator
    echo "TEST: Normal herd after init"
    clowder herd $PARALLEL || exit 1
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

clowder status || exit 1

# test_herd_old_repos() {
#     print_double_separator
#     echo "TEST: Normal herd with out of date repos"
#     setup_old_repos
#     clowder herd $PARALLEL || exit 1
#     clowder status || exit 1
# }
# test_herd_old_repos

# print_double_separator
# clowder forall $PARALLEL -c 'git checkout -b v0.1'
# echo "TEST: Check current branches"
# for project in "${projects[@]}"; do
# 	pushd $project || exit 1
#     test_branch v0.1
#     popd || exit 1
# done

"$TEST_SCRIPT_DIR/llvm/forks.sh" $1 || exit 1
"$TEST_SCRIPT_DIR/llvm/sync.sh" $1 || exit 1
"$TEST_SCRIPT_DIR/llvm/branch.sh" $1 || exit 1
"$TEST_SCRIPT_DIR/llvm/reset.sh" $1 || exit 1

test_help() {
    print_double_separator
    clowder link || exit 1
    clowder herd $PARALLEL || exit 1
    "$TEST_SCRIPT_DIR/test_help.sh" "$LLVM_EXAMPLE_DIR" || exit 1
}
test_help
