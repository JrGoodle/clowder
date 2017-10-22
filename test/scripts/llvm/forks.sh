#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

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

print_double_separator
echo "TEST: Test clowder forks"
cd "$LLVM_EXAMPLE_DIR" || exit 1
./init.sh

if [ "$ACCESS_LEVEL" == "write" ]; then
    test_forks() {
        print_double_separator
        echo "TEST: Forks"
        clowder link || exit 1
        clowder herd $PARALLEL || exit 1
        clowder start -t fail_start && exit 1
        clowder prune -a fail_start || exit 1

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

        clowder prune -af start_tracking || exit 1

        for project in "${fork_projects[@]}"; do
            clowder start -t start_tracking -p $project || exit 1
        done

        clowder status || exit 1

        for project in "${project_paths[@]}"; do
            pushd $project || exit 1
            test_branch master
            popd || exit 1
        done
        for project in "${fork_paths[@]}"; do
            pushd $project || exit 1
            test_branch start_tracking
            test_tracking_branch_exists start_tracking
            popd || exit 1
        done

        clowder herd $PARALLEL || exit 1
        clowder status || exit 1

        for project in "${project_paths[@]}"; do
            pushd $project || exit 1
            test_branch master
            popd || exit 1
        done
        for project in "${fork_paths[@]}"; do
            pushd $project || exit 1
            test_branch master
            popd || exit 1
        done

        for project in "${fork_projects[@]}"; do
            clowder prune start_tracking -p $project || exit 1
        done

        for project in "${fork_paths[@]}"; do
            pushd $project || exit 1
            test_no_local_branch_exists start_tracking
            test_remote_branch_exists start_tracking
            popd || exit 1
        done

        clowder herd $PARALLEL -b start_tracking || exit 1
        clowder status || exit 1

        for project in "${project_paths[@]}"; do
            pushd $project || exit 1
            test_branch master
            popd || exit 1
        done
        for project in "${fork_paths[@]}"; do
            pushd $project || exit 1
            test_branch start_tracking
            test_tracking_branch_exists start_tracking
            popd || exit 1
        done

        for project in "${fork_projects[@]}"; do
            clowder prune -a start_tracking -p $project || exit 1
        done

        for project in "${fork_paths[@]}"; do
            pushd $project || exit 1
            test_branch master
            test_no_local_branch_exists start_tracking
            test_no_remote_branch_exists start_tracking
            popd || exit 1
        done
    }
    test_forks
fi

test_forks_env() {
    echo "TEST: Fork remote environment variable in script"
    clowder forall $PARALLEL -c "$TEST_SCRIPT_DIR/test_forall_script_env_fork.sh" -p "llvm-mirror/clang" || exit 1
    clowder forall $PARALLEL -c "$TEST_SCRIPT_DIR/test_forall_script_env_fork.sh" -p "llvm-mirror/llvm" && exit 1
    echo "TEST: Fork remote environment variable in command"
    clowder forall $PARALLEL -c 'if [ $PROJECT_REMOTE != upstream ]; then exit 1; fi' -p 'llvm-mirror/clang' || exit 1
    clowder forall $PARALLEL -c 'if [ $FORK_REMOTE != origin ]; then exit 1; fi' -p 'llvm-mirror/clang' || exit 1
}
