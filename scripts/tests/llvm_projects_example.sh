#! /bin/bash

# set -xv

cd "$( dirname "${BASH_SOURCE[0]}" )"
source functional_tests.sh
cd ../../examples/llvm-projects

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

    local CLANG_TOOLS_EXTRA_DIR="$LLVM_PROJECTS_DIR/llvm/tools/clang/tools/extra"
    rm -rf $CLANG_TOOLS_EXTRA_DIR
    mkdir -p $CLANG_TOOLS_EXTRA_DIR
    pushd $CLANG_TOOLS_EXTRA_DIR &>/dev/null
    git clone https://github.com/JrGoodle/clang-tools-extra.git . &>/dev/null
    git remote remove origin &>/dev/null
    git remote add origin https://github.com/llvm-mirror/clang-tools-extra.git &>/dev/null
    git fetch &>/dev/null
    git branch -u origin/master &>/dev/null
    popd &>/dev/null

    local COMPILER_RT_DIR="$LLVM_PROJECTS_DIR/llvm/projects/compiler-rt"
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

test_herd_old_repos()
{
    setup_old_repos
    echo "TEST: Normal herd with out of date repos"
    clowder herd || exit 1
    clowder meow || exit 1
}

export projects=( 'llvm' \
                  'llvm/tools/clang' \
                  'llvm/tools/clang/tools/extra' \
                  'llvm/projects/compiler-rt' \
                  'llvm/projects/libunwind' \
                  'llvm/projects/dragonegg' )

test_command

test_breed_herd
test_branch_master
test_herd_old_repos
test_meow_groups 'clang' 'llvm'
test_herd 'llvm/tools/clang/tools/extra' \
          'llvm/projects/dragonegg'
test_branch_version
test_herd_dirty_repos
test_groom 'clang' 'llvm'
test_groom_projects 'llvm-mirror/clang'
test_sync
test_herd_detached_heads
test_forall 'clang' 'llvm'
test_fix
test_stash 'clang' 'llvm'
test_herd_groups 'clang' 'llvm'
test_fix_missing_directories 'llvm/tools/clang/tools/extra' \
                             'llvm/projects/dragonegg'
test_herd_projects 'llvm-mirror/lld'

print_help
