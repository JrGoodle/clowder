#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

ACCESS_LEVEL=${1:-read}

print_double_separator
echo 'TEST: llvm projects example test script'
print_double_separator

if [ -z "$TRAVIS_OS_NAME" ]; then
    setup_local_test_directory
fi

cd "$LLVM_EXAMPLE_DIR" || exit 1

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
#     # pushd $CLANG_DIR
#     # git clone https://github.com/JrGoodle/clang.git .
#     # git remote remove origin
#     # git remote add origin https://github.com/llvm-mirror/clang.git
#     # git fetch
#     # git branch -u origin/master
#     # popd
#
#     local CLANG_TOOLS_EXTRA_DIR="llvm/tools/clang/tools/extra"
#     rm -rf $CLANG_TOOLS_EXTRA_DIR
#     mkdir -p $CLANG_TOOLS_EXTRA_DIR
#     pushd $CLANG_TOOLS_EXTRA_DIR
#     git clone https://github.com/JrGoodle/clang-tools-extra.git .
#     git remote remove origin
#     git remote add origin https://github.com/llvm-mirror/clang-tools-extra.git
#     git fetch
#     git branch -u origin/master
#     popd
#
#     local COMPILER_RT_DIR="llvm/projects/compiler-rt"
#     rm -rf $COMPILER_RT_DIR
#     mkdir -p $COMPILER_RT_DIR
#     pushd $COMPILER_RT_DIR
#     git clone https://github.com/JrGoodle/compiler-rt.git .
#     git remote remove origin
#     git remote add origin https://github.com/llvm-mirror/compiler-rt.git
#     git fetch
#     git branch -u origin/master
#     popd
# }

test_init_herd() {
    print_double_separator
    echo "TEST: Normal herd after init"
    "$LLVM_EXAMPLE_DIR/clean.sh"
    "$LLVM_EXAMPLE_DIR/init.sh"  || exit 1
    clowder herd  || exit 1
    echo "TEST: Check current branches are on master"
    for project in "${project_paths[@]}"; do
    	pushd $project
        test_branch master
        test_tracking_branch_exists master
        popd
    done
    for project in "${fork_paths[@]}"; do
        pushd $project
        test_branch master
        test_tracking_branch_exists master
        popd
    done
}
test_init_herd

clowder status || exit 1

# test_herd_old_repos() {
#     print_double_separator
#     echo "TEST: Normal herd with out of date repos"
#     setup_old_repos
#     clowder herd || exit 1
#     clowder status || exit 1
# }
# test_herd_old_repos

# print_double_separator
# clowder forall -c 'git checkout -b v0.1'
# echo "TEST: Check current branches"
# for project in "${projects[@]}"; do
# 	pushd $project
#     test_branch v0.1
#     popd
# done

if [ "$ACCESS_LEVEL" == "write" ]; then
    test_forks() {
        print_double_separator
        echo "TEST: Forks"
        clowder link || exit 1
        clowder herd || exit 1
        clowder start -t fail_start && exit 1
        clowder prune -a fail_start || exit 1

        for project in "${project_paths[@]}"; do
            pushd $project
            test_branch master
            test_tracking_branch_exists master
            popd
        done
        for project in "${fork_paths[@]}"; do
            pushd $project
            test_branch master
            test_tracking_branch_exists master
            popd
        done

        clowder prune -af start_tracking || exit 1
        
        for project in "${fork_projects[@]}"; do
            clowder start -t start_tracking -p $project || exit 1
        done

        clowder status || exit 1

        for project in "${project_paths[@]}"; do
            pushd $project
            test_branch master
            popd
        done
        for project in "${fork_paths[@]}"; do
            pushd $project
            test_branch start_tracking
            test_tracking_branch_exists start_tracking
            popd
        done

        clowder herd || exit 1
        clowder status || exit 1

        for project in "${project_paths[@]}"; do
            pushd $project
            test_branch master
            popd
        done
        for project in "${fork_paths[@]}"; do
            pushd $project
            test_branch master
            popd
        done

        for project in "${fork_projects[@]}"; do
            clowder prune start_tracking -p $project || exit 1
        done

        for project in "${fork_paths[@]}"; do
            pushd $project
            test_no_local_branch_exists start_tracking
            test_remote_branch_exists start_tracking
            popd
        done

        clowder herd -b start_tracking || exit 1
        clowder status || exit 1

        for project in "${project_paths[@]}"; do
            pushd $project
            test_branch master
            popd
        done
        for project in "${fork_paths[@]}"; do
            pushd $project
            test_branch start_tracking
            test_tracking_branch_exists start_tracking
            popd
        done

        for project in "${fork_projects[@]}"; do
            clowder prune -a start_tracking -p $project || exit 1
        done

        for project in "${fork_paths[@]}"; do
            pushd $project
            test_branch master
            test_no_local_branch_exists start_tracking
            test_no_remote_branch_exists start_tracking
            popd
        done
    }
    test_forks

    test_sync() {
        print_double_separator
        echo "TEST: clowder sync"
        clowder link || exit 1
        clowder herd || exit 1

        pushd 'llvm/tools/clang'
        git pull upstream master || exit 1
        UPSTREAM_COMMIT="$(git rev-parse HEAD)"
        git reset --hard HEAD~1 || exit 1
        git push origin master --force || exit 1
        git pull origin master || exit 1
        if [ "$UPSTREAM_COMMIT" == "$(git rev-parse HEAD)" ]; then
            exit 1
        fi
        popd

        clowder sync || exit 1

        pushd 'llvm/tools/clang'
        if [ "$UPSTREAM_COMMIT" != "$(git rev-parse HEAD)" ]; then
            exit 1
        fi
        git reset --hard HEAD~1 || exit 1
        if [ "$UPSTREAM_COMMIT" == "$(git rev-parse HEAD)" ]; then
            exit 1
        fi
        git pull origin master
        if [ "$UPSTREAM_COMMIT" != "$(git rev-parse HEAD)" ]; then
            exit 1
        fi
        popd
    }
    test_sync
fi

test_forks_env() {
    echo "TEST: Fork remote environment variable in script"
    clowder forall -c "$TEST_SCRIPT_DIR/tests/test_forall_script_env_fork.sh" -p "llvm-mirror/clang" || exit 1
    clowder forall -c "$TEST_SCRIPT_DIR/tests/test_forall_script_env_fork.sh" -p "llvm-mirror/llvm" && exit 1
    echo "TEST: Fork remote environment variable in command"
    clowder forall -c 'if [ $PROJECT_REMOTE != upstream ]; then exit 1; fi' -p 'llvm-mirror/clang' || exit 1
    clowder forall -c 'if [ $FORK_REMOTE != origin ]; then exit 1; fi' -p 'llvm-mirror/clang' || exit 1
}

test_branch() {
    echo "TEST: clowder branch"
    clowder link || exit 1
    clowder herd || exit 1
    clowder branch || exit 1
    clowder branch -r || exit 1
    clowder branch -a || exit 1
    clowder branch -p 'llvm-mirror/llvm' || exit 1
    clowder branch -rp 'llvm-mirror/llvm' || exit 1
    clowder branch -ap 'llvm-mirror/llvm' || exit 1
    clowder branch -g 'clang' || exit 1
    clowder branch -rg 'clang' || exit 1
    clowder branch -ag 'clang' || exit 1
}
test_branch

test_help() {
    print_double_separator
    clowder link || exit 1
    clowder herd || exit 1
    "$TEST_SCRIPT_DIR/tests/test_help.sh" "$LLVM_EXAMPLE_DIR" || exit 1
}
test_help
