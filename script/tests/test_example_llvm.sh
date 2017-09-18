#!/usr/bin/env bash

# set -xv

echo 'TEST: llvm projects example test script'

pushd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

export EXAMPLES_DIR
export TEST_SCRIPT_DIR
export LLVM_EXAMPLE_DIR
TEST_SCRIPT_DIR="$(pwd)/.."
EXAMPLES_DIR="$(pwd)/../../examples"

if [ -n "$TRAVIS_OS_NAME" ]; then
    LLVM_EXAMPLE_DIR="$(pwd)/../../examples/llvm-projects"
    cd "$LLVM_EXAMPLE_DIR" || exit 1
else
    LLVM_EXAMPLE_DIR="$HOME/.clowder_tests/llvm-projects"
    rm -rf "$HOME/.clowder_tests"
    mkdir -p "$HOME/.clowder_tests" && cp -r "$EXAMPLES_DIR/llvm-projects" "$LLVM_EXAMPLE_DIR"
    cd "$LLVM_EXAMPLE_DIR" || exit 1
fi

export projects=( 'llvm' \
                  'llvm/tools/clang' \
                  'llvm/tools/clang/tools/extra' \
                  'llvm/projects/compiler-rt' \
                  'llvm/projects/libunwind' \
                  'llvm/projects/dragonegg' )

setup_old_repos()
{
    echo 'TEST: Set up older copies of repos'

    # local CLANG_DIR="$LLVM_PROJECTS_DIR/llvm/tools/clang"
    # rm -rf $CLANG_DIR
    # mkdir -p $CLANG_DIR
    # pushd $CLANG_DIR
    # git clone https://github.com/JrGoodle/clang.git .
    # git remote remove origin
    # git remote add origin https://github.com/llvm-mirror/clang.git
    # git fetch
    # git branch -u origin/master
    # popd

    local CLANG_TOOLS_EXTRA_DIR="llvm/tools/clang/tools/extra"
    rm -rf $CLANG_TOOLS_EXTRA_DIR
    mkdir -p $CLANG_TOOLS_EXTRA_DIR
    pushd $CLANG_TOOLS_EXTRA_DIR
    git clone https://github.com/JrGoodle/clang-tools-extra.git .
    git remote remove origin
    git remote add origin https://github.com/llvm-mirror/clang-tools-extra.git
    git fetch
    git branch -u origin/master
    popd

    local COMPILER_RT_DIR="llvm/projects/compiler-rt"
    rm -rf $COMPILER_RT_DIR
    mkdir -p $COMPILER_RT_DIR
    pushd $COMPILER_RT_DIR
    git clone https://github.com/JrGoodle/compiler-rt.git .
    git remote remove origin
    git remote add origin https://github.com/llvm-mirror/compiler-rt.git
    git fetch
    git branch -u origin/master
    popd
}

test_clowder_version

test_init_herd()
{
    print_separator
    echo "TEST: Normal herd after init"
    "$LLVM_EXAMPLE_DIR/clean.sh"
    "$LLVM_EXAMPLE_DIR/init.sh"  || exit 1
    clowder herd  || exit 1
    clowder status -f || exit 1
}
test_init_herd

print_separator

echo "TEST: Check current branches are on master"
for project in "${projects[@]}"; do
	pushd $project
    test_branch master
    popd
done

test_herd_old_repos()
{
    print_separator
    echo "TEST: Normal herd with out of date repos"
    setup_old_repos
    clowder herd || exit 1
    clowder status || exit 1
}
test_herd_old_repos

print_separator
clowder forall -c 'git checkout -b v0.1'
echo "TEST: Check current branches"
for project in "${projects[@]}"; do
	pushd $project
    test_branch v0.1
    popd
done

test_print()
{
    print_separator
    clowder link
    clowder herd
    "$TEST_SCRIPT_DIR/tests/test_help.sh" "$LLVM_EXAMPLE_DIR"
}
test_print

popd
