#! /bin/bash

# set -xv

setup_old_repos()
{
    echo 'TEST: Setting up older copies of repos'

    local CLANG_DIR="$LLVM_PROJECTS_DIR/llvm/tools/clang"
    rm -rf $CLANG_DIR
    mkdir -p $CLANG_DIR
    pushd $CLANG_DIR &>/dev/null
    git clone https://github.com/JrGoodle/clang.git . &>/dev/null
    git remote remove origin &>/dev/null
    git remote add origin https://github.com/llvm-mirror/clang.git &>/dev/null
    git fetch &>/dev/null
    git branch -u origin/master &>/dev/null
    popd &>/dev/null

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

    echo ''
}

test_branch()
{
    local git_branch
    git_branch=$(git rev-parse --abbrev-ref HEAD)
    # echo "TEST: Current branch: $git_branch"
    # echo "TEST: Test branch: $1"
    [[ "$1" = "$git_branch" ]] && echo "TEST: On correct branch: $1" || exit 1
}

export LLVM_PROJECTS_DIR="$TRAVIS_BUILD_DIR/examples/llvm-projects"
cd $LLVM_PROJECTS_DIR

# Test breed and herding
./breed.sh && clowder herd || exit 1
setup_old_repos # configure repo's for testing pulling new commits
clowder herd || exit 1
clowder meow || exit 1
clowder groom || exit 1
clowder herd -v v0.1 || exit 1
clowder meow || exit 1

projects=( 'llvm' \
            'llvm/tools/clang' \
            'llvm/tools/clang/tools/extra' \
            'llvm/projects/compiler-rt' \
            'llvm/projects/libunwind' \
            'llvm/projects/dragonegg' )

for project in "${projects[@]}"
do
	pushd $project &>/dev/null
    test_branch clowder-fix/v0.1
    popd &>/dev/null
done
echo ''

clowder herd || exit 1
clowder meow || exit 1

for project in "${projects[@]}"
do
	pushd $project &>/dev/null
    test_branch master
    popd &>/dev/null
done
echo ''

for project in "${projects[@]}"
do
	pushd $project &>/dev/null
    touch newfile
    git add newfile
    popd &>/dev/null
done
echo ''

clowder meow || exit 1
clowder herd || exit 1
clowder meow || exit 1
clowder litter || exit 1
clowder meow || exit 1

pushd clowder &>/dev/null
touch newfile
git add newfile
popd &>/dev/null

clowder meow || exit 1
clowder herd || exit 1
clowder meow || exit 1
clowder groom || exit 1
clowder meow || exit 1
clowder litter || exit 1
clowder meow || exit 1

for project in "${projects[@]}"
do
	pushd $project &>/dev/null
    git checkout master~2 &>/dev/null
    popd &>/dev/null
done

clowder meow || exit 1
clowder herd || exit 1
clowder meow || exit 1
clowder herd -v v0.1 || exit 1
clowder meow || exit 1
clowder herd || exit 1
clowder meow || exit 1
clowder forall 'git status' || exit 1
clowder fix -v v0.1 || exit 1
clowder fix -v v0.11 || exit 1
clowder herd -v v0.11 || exit 1
clowder meow || exit 1

for project in "${projects[@]}"
do
	pushd $project &>/dev/null
    touch newfile
    git add newfile
    popd &>/dev/null
done

clowder meow || exit 1
clowder herd || exit 1
clowder stash || exit 1
clowder meow || exit 1
rm -rf 'llvm/tools/clang/tools/extra'
rm -rf 'llvm/projects/dragonegg'
clowder herd || exit 1
clowder meow || exit 1
clowder herd -v v0.11 || exit 1
clowder meow || exit 1
clowder herd -g clang llvm projects || exit 1
clowder meow || exit 1
