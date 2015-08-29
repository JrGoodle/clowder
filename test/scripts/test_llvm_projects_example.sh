#! /bin/bash

setup_old_repos()
{
    echo 'TEST: Setting up older copies of repos'
    local CLANG_TOOLS_EXTRA_DIR="$LLVM_PROJECTS_DIR/llvm/tools/clang/tools/extra"
    rm -rf $CLANG_TOOLS_EXTRA_DIR
    mkdir -p $CLANG_TOOLS_EXTRA_DIR
    pushd $CLANG_TOOLS_EXTRA_DIR
    git clone https://github.com/JrGoodle/clang-tools-extra.git . &>/dev/null
    git remote remove origin &>/dev/null
    git remote add origin https://github.com/llvm-mirror/clang-tools-extra.git &>/dev/null
    git fetch &>/dev/null
    git branch -u origin/master &>/dev/null
    popd

    local CLANG_DIR="$LLVM_PROJECTS_DIR/llvm/tools/clang"
    rm -rf $CLANG_DIR
    mkdir -p $CLANG_DIR
    pushd $CLANG_DIR
    git clone https://github.com/JrGoodle/clang.git . &>/dev/null
    git remote remove origin &>/dev/null
    git remote add origin https://github.com/llvm-mirror/clang.git &>/dev/null
    git fetch &>/dev/null
    git branch -u origin/master &>/dev/null
    popd

    local COMPILER_RT_DIR="$LLVM_PROJECTS_DIR/llvm/projects/compiler-rt"
    rm -rf $COMPILER_RT_DIR
    mkdir -p $COMPILER_RT_DIR
    pushd $COMPILER_RT_DIR
    git clone https://github.com/JrGoodle/compiler-rt.git . &>/dev/null
    git remote remove origin &>/dev/null
    git remote add origin https://github.com/llvm-mirror/compiler-rt.git &>/dev/null
    git fetch &>/dev/null
    git branch -u origin/master &>/dev/null
    popd
}

test_branch()
{
    local git_branch
    git_branch=$(git rev-parse --abbrev-ref HEAD)
    echo "TEST: Current branch: $git_branch"
    echo "TEST: Test branch: $1"
    [[ "$1" = "$git_branch" ]] && echo "TEST: On correct branch: $1" || exit 1
}

export LLVM_PROJECTS_DIR="$TRAVIS_BUILD_DIR/examples/llvm-projects"
cd $LLVM_PROJECTS_DIR

# Test breed and herding
./breed.sh && clowder herd || exit 1
setup_old_repos # configur repo's for testing pulling new commits
clowder herd || exit 1
clowder meow || exit 1

clowder herd -v v0.1 || exit 1
clowder meow || exit 1

pushd llvm/tools/clang
test_branch clowder-fix/v0.1
popd
pushd llvm/tools/clang/tools/extra
test_branch clowder-fix/v0.1
popd
pushd llvm/projects/compiler-rt
test_branch clowder-fix/v0.1
popd
pushd llvm/projects/libunwind
test_branch clowder-fix/v0.1
popd
pushd llvm/projects/dragonegg
test_branch clowder-fix/v0.1
popd
pushd llvm
test_branch clowder-fix/v0.1
popd

clowder herd || exit 1
clowder meow || exit 1

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

pushd llvm
touch newfile
git add newfile
popd
pushd llvm/tools/clang
touch newfile
git add newfile
popd
pushd llvm/projects/compiler-rt
touch newfile
git add newfile
popd

clowder meow || exit 1
clowder litter || exit 1
clowder meow || exit 1
clowder herd -v v0.1 || exit 1
clowder meow || exit 1
