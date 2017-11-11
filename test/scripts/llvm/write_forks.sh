#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

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

if [ "$ACCESS_LEVEL" == "write" ]; then
    print_double_separator
    echo "TEST: Test clowder forks"
    cd "$LLVM_EXAMPLE_DIR" || exit 1
    ./init.sh

    test_forks() {
        print_double_separator
        echo "TEST: Forks"
        $COMMAND link || exit 1
        $COMMAND herd $PARALLEL || exit 1
        $COMMAND start -t fail_start && exit 1
        $COMMAND prune -a fail_start || exit 1

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

        $COMMAND prune -af start_tracking || exit 1

        for project in "${fork_projects[@]}"; do
            $COMMAND start -t start_tracking -p $project || exit 1
        done

        $COMMAND status || exit 1

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

        $COMMAND herd $PARALLEL || exit 1
        $COMMAND status || exit 1

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
            $COMMAND prune start_tracking -p $project || exit 1
        done

        for project in "${fork_paths[@]}"; do
            pushd $project || exit 1
            test_no_local_branch_exists start_tracking
            test_remote_branch_exists start_tracking
            popd || exit 1
        done

        $COMMAND herd $PARALLEL -b start_tracking || exit 1
        $COMMAND status || exit 1

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
            $COMMAND prune -a start_tracking -p $project || exit 1
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
