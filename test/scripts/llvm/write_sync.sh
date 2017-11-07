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

print_double_separator
echo "TEST: Test clowder sync"
cd "$LLVM_EXAMPLE_DIR" || exit 1
./init.sh

if [ "$ACCESS_LEVEL" == "write" ]; then
    test_sync() {
        print_double_separator
        echo "TEST: clowder sync"
        $COMMAND link || exit 1
        $COMMAND herd $PARALLEL || exit 1

        pushd 'llvm/tools/clang' || exit 1
        git pull upstream master || exit 1
        UPSTREAM_COMMIT="$(git rev-parse HEAD)"
        git reset --hard HEAD~1 || exit 1
        git push origin master --force || exit 1
        git pull origin master || exit 1
        test_not_commit "$UPSTREAM_COMMIT"
        popd || exit 1

        $COMMAND sync $PARALLEL || exit 1

        pushd 'llvm/tools/clang' || exit 1
        test_commit "$UPSTREAM_COMMIT"
        git reset --hard HEAD~1 || exit 1
        test_not_commit "$UPSTREAM_COMMIT"
        git pull origin master
        test_commit "$UPSTREAM_COMMIT"
        popd || exit 1
    }
    test_sync

    test_sync_rebase() {
        print_single_separator
        echo "TEST: clowder sync rebase"
        $COMMAND link || exit 1
        $COMMAND herd $PARALLEL || exit 1
        $COMMAND sync $PARALLEL || exit 1

        REBASE_MESSAGE='Add rebase file'
        pushd 'llvm/tools/clang' || exit 1
        git pull upstream master || exit 1
        UPSTREAM_COMMIT="$(git rev-parse HEAD)"
        COMMIT_MESSAGE_1="$(git log --format=%B -n 1 HEAD)"
        echo "$COMMIT_MESSAGE_1"
        COMMIT_MESSAGE_2="$(git log --format=%B -n 1 HEAD~1)"
        echo "$COMMIT_MESSAGE_2"
        git reset --hard HEAD~1 || exit 1
        git push origin master --force || exit 1
        git pull origin master || exit 1
        test_not_commit "$UPSTREAM_COMMIT"
        touch rebasefile || exit 1
        git add rebasefile || exit 1
        git commit -m "$REBASE_MESSAGE" || exit 1
        test_commit_messages "$(git log --format=%B -n 1 HEAD)" "$REBASE_MESSAGE"
        test_commit_messages "$(git log --format=%B -n 1 HEAD~1)" "$COMMIT_MESSAGE_2"
        popd || exit 1

        $COMMAND sync $PARALLEL -r || exit 1

        pushd 'llvm/tools/clang' || exit 1
        test_commit_messages "$(git log --format=%B -n 1 HEAD)" "$REBASE_MESSAGE"
        test_commit_messages "$(git log --format=%B -n 1 HEAD~1)" "$COMMIT_MESSAGE_1"
        test_commit_messages "$(git log --format=%B -n 1 HEAD~2)" "$COMMIT_MESSAGE_2"
        if [ "$UPSTREAM_COMMIT" != "$(git rev-parse HEAD~1)" ]; then
            exit 1
        fi
        git reset --hard HEAD~1 || exit 1
        test_commit "$UPSTREAM_COMMIT"
        git pull origin master
        test_not_commit "$UPSTREAM_COMMIT"
        if [ "$UPSTREAM_COMMIT" != "$(git rev-parse HEAD~1)" ]; then
            exit 1
        fi
        git reset --hard HEAD~1 || exit 1
        git push origin master --force || exit 1
        popd || exit 1
    }
    test_sync_rebase
fi
