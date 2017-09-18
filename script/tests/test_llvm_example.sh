#!/usr/bin/env bash

# set -xv

echo 'TEST: llvm projects example test script'

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

SCRIPTS_DIR="$(pwd)/.."
LLVM_EXAMPLE_DIR="$(pwd)/../../examples/llvm-projects"

. test_utilities.sh
"$LLVM_EXAMPLE_DIR/clean.sh"

if [ -n "$TRAVIS_OS_NAME" ]; then
    cd "$LLVM_EXAMPLE_DIR" || exit 1
else
    rm -rf "$HOME/.clowder_tests"
    mkdir -p "$HOME/.clowder_tests" && cp -r "$LLVM_EXAMPLE_DIR" "$HOME/.clowder_tests/llvm-projects"
    cd "$HOME/.clowder_tests/llvm-projects" || exit 1
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

test_status_groups 'clang' 'llvm'
test_status_projects 'llvm-mirror/llvm' 'llvm-mirror/clang'

print_separator
clowder forall -c 'git checkout -b v0.1'
echo "TEST: Check current branches"
for project in "${projects[@]}"; do
	pushd $project
    test_branch v0.1
    popd
done

test_herd_dirty_repos "${projects[@]}"

test_clean()
{
    print_separator
    echo "TEST: Clean repos"
    make_dirty_repos "${projects[@]}"
    echo "TEST: Clean specific group when dirty"
    clowder clean -g "$@" || exit 1
    clowder status || exit 1
    echo "TEST: Clean all when dirty"
    clowder clean || exit 1
    clowder status || exit 1
    echo "TEST: Clean when clean"
    clowder clean || exit 1
}
test_clean 'clang' 'llvm'

test_clean_projects()
{
    print_separator
    echo "TEST: Clean projects"
    make_dirty_repos "${projects[@]}"
    echo "TEST: Clean specific project when dirty"
    clowder clean -p "$@" || exit 1
    clowder status || exit 1
    echo "TEST: Clean all when dirty"
    clowder clean || exit 1
    clowder status || exit 1
}
test_clean_projects 'llvm-mirror/clang'

test_clean_missing_directories()
{
    rm -rf "$@"
    echo "TEST: Discard all changes when directories are missing"
    clowder clean || exit 1
    clowder status || exit 1
    clowder herd || exit 1
}
test_clean_missing_directories 'zorg'

test_herd_detached_heads "${projects[@]}"
test_forall 'clang' 'llvm'
test_forall_projects 'llvm-mirror/clang' 'llvm-mirror/llvm'

test_stash()
{
    print_separator
    echo "TEST: Stash changes"
    make_dirty_repos "${projects[@]}"
    echo "TEST: Fail herd with dirty repos"
    clowder herd && exit 1
    echo "TEST: Stash specific groups when dirty"
    clowder stash -g "$@" || exit 1
    clowder status || exit 1
    echo "TEST: Stash all changes when dirty"
    clowder stash || exit 1
    clowder status || exit 1
    echo "TEST: Stash changes when clean"
    clowder stash || exit 1
}
test_stash 'clang' 'llvm'

test_stash_projects()
{
    print_separator
    echo "TEST: Stash projects"
    make_dirty_repos "${projects[@]}"
    echo "TEST: Stash specific projects when dirty"
    clowder stash -p "$@" || exit 1
    clowder status || exit 1
    echo "TEST: Stash all changes when dirty"
    clowder stash || exit 1
    clowder status || exit 1
}
test_stash_projects 'llvm-mirror/clang'

test_stash_missing_directories 'zorg'

test_save_missing_directories 'llvm/tools/clang/tools/extra' \
                              'llvm/projects/dragonegg'
test_herd_projects 'llvm-mirror/lld'

test_start()
{
    print_separator
    echo "TEST: Start new feature branch"
    clowder herd

    clowder start start_branch
    # TODO: clowder herd -b
    # clowder herd -b master -g llvm
    clowder forall -g llvm -c 'git fetch origin master'
    clowder forall -g llvm -c 'git checkout master'

    pushd 'llvm/tools/clang'
    test_branch start_branch
    popd
    pushd 'llvm/tools/clang/tools/extra'
    test_branch start_branch
    popd
    pushd llvm
    test_branch master
    popd

    clowder start start_branch

    pushd llvm
    test_branch start_branch
    popd
}
test_start

print_help
