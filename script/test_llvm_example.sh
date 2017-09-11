#!/usr/bin/env bash

# set -xv

echo 'TEST: llvm projects example test script'

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1
source test_utilities.sh
cd ../examples/llvm-projects || exit 1
./clean.sh

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
    # pushd $CLANG_DIR &>/dev/null
    # git clone https://github.com/JrGoodle/clang.git . &>/dev/null
    # git remote remove origin &>/dev/null
    # git remote add origin https://github.com/llvm-mirror/clang.git &>/dev/null
    # git fetch &>/dev/null
    # git branch -u origin/master &>/dev/null
    # popd &>/dev/null

    local CLANG_TOOLS_EXTRA_DIR="llvm/tools/clang/tools/extra"
    rm -rf $CLANG_TOOLS_EXTRA_DIR
    mkdir -p $CLANG_TOOLS_EXTRA_DIR
    pushd $CLANG_TOOLS_EXTRA_DIR &>/dev/null
    git clone https://github.com/JrGoodle/clang-tools-extra.git . &>/dev/null
    git remote remove origin &>/dev/null
    git remote add origin https://github.com/llvm-mirror/clang-tools-extra.git &>/dev/null
    git fetch &>/dev/null
    git branch -u origin/master &>/dev/null
    popd &>/dev/null

    local COMPILER_RT_DIR="llvm/projects/compiler-rt"
    rm -rf $COMPILER_RT_DIR
    mkdir -p $COMPILER_RT_DIR
    pushd $COMPILER_RT_DIR &>/dev/null
    git clone https://github.com/JrGoodle/compiler-rt.git . &>/dev/null
    git remote remove origin &>/dev/null
    git remote add origin https://github.com/llvm-mirror/compiler-rt.git &>/dev/null
    git fetch &>/dev/null
    git branch -u origin/master &>/dev/null
    popd &>/dev/null
}

test_command
test_clowder_version

test_init_herd
test_branch_master "${projects[@]}"

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
# test_herd 'llvm/tools/clang/tools/extra' \
#           'llvm/projects/dragonegg'
test_branch_version "${projects[@]}"
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

test_clean_missing_directories 'zorg'
test_herd_detached_heads "${projects[@]}"
test_forall 'clang' 'llvm'
test_forall_projects 'llvm-mirror/clang' 'llvm-mirror/llvm'
# test_save

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
# test_herd_groups 'clang' 'llvm'
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

    pushd 'llvm/tools/clang' &>/dev/null
    test_branch start_branch
    popd &>/dev/null
    pushd 'llvm/tools/clang/tools/extra' &>/dev/null
    test_branch start_branch
    popd &>/dev/null
    pushd llvm &>/dev/null
    test_branch master
    popd &>/dev/null

    clowder start start_branch

    pushd llvm &>/dev/null
    test_branch start_branch
    popd &>/dev/null
}
test_start

print_help
