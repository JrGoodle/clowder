#! /bin/bash

setup_old_repos()
{
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

test_branch()
{
    local git_branch
    git_branch=$(git rev-parse --abbrev-ref HEAD)
    echo "Current branch: $git_branch"
    echo "Test branch: $1"
    [[ "$1" = "$git_branch" ]] && echo "On correct branch: $1" || exit 1
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
# ./breed.sh && clowder herd -a -v v0.1 && clowder herd -a && ./clean.sh || exit 1

# Test breed and herding defaults for a version
./breed.sh || exit 1

setup_old_repos # configur repo's for testing pulling new commits

clowder herd -v v0.1 || exit 1

pushd llvm/tools/clang
test_branch fix/v1.0
popd
pushd llvm/tools/clang/tools/extra
test_branch fix/v1.0
popd
pushd llvm/projects/compiler-rt
test_branch fix/v1.0
popd
pushd llvm/projects/libunwind
test_branch fix/v1.0
popd
pushd llvm/projects/dragonegg
test_branch fix/v1.0
popd
pushd llvm
test_branch fix/v1.0
popd

clowder herd || exit 1

pushd llvm/tools/clang
test_branch master
popd
pushd llvm/tools/clang/tools/extra
test_branch master
popd
pushd llvm/projects/compiler-rt
test_branch master
popd
pushd llvm/projects/libunwind
test_branch master
popd
pushd llvm/projects/dragonegg
test_branch master
popd
pushd llvm
test_branch master
popd
