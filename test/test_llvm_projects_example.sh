#! /bin/bash

function setup_old_repos() {
    local CLANG_TOOLS_EXTRA_DIR="$LLVM_PROJECTS_DIR/llvm/tools/clang/tools/extra"
    rm -rf $CLANG_TOOLS_EXTRA_DIR
    mkdir -p $CLANG_TOOLS_EXTRA_DIR
    pushd $CLANG_TOOLS_EXTRA_DIR
    git clone https://github.com/JrGoodle/clang-tools-extra.git .
    git remote remove origin
    git remote add origin https://github.com/llvm-mirror/clang-tools-extra.git
    git fetch
    git branch -u origin/master
    popd

    local CLANG_DIR="$LLVM_PROJECTS_DIR/llvm/tools/clang"
    rm -rf $CLANG_DIR
    mkdir -p $CLANG_DIR
    pushd $CLANG_DIR
    git clone https://github.com/JrGoodle/clang.git .
    git remote remove origin
    git remote add origin https://github.com/llvm-mirror/clang.git
    git fetch
    git branch -u origin/master
    popd

    local COMPILER_RT_DIR="$LLVM_PROJECTS_DIR/llvm/projects/compiler-rt"
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

export LLVM_PROJECTS_DIR="$TRAVIS_BUILD_DIR/examples/llvm-projects"
pushd $LLVM_PROJECTS_DIR

# Test breed and herding all
./breed.sh && clowder herd -a && ./clean.sh || exit 1

# Test breed and herding defaults
./breed.sh && clowder herd || exit 1
setup_old_repos # configur repo's for testing pulling new commits
clowder herd && ./clean.sh || exit 1

# Test breed and herding all for a version
./breed.sh && clowder herd -a -v v0.1 && clowder herd -a && ./clean.sh || exit 1

# Test breed and herding defaults for a version
./breed.sh || exit 1
setup_old_repos # configur repo's for testing pulling new commits
clowder herd -v v0.1 || exit 1
clowder herd && ./clean.sh || exit 1
