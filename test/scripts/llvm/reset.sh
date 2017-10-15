#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

print_double_separator
echo 'TEST: llvm projects example test script'
print_double_separator

if [ -z "$TRAVIS_OS_NAME" ]; then
    setup_local_test_directory
fi

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

cd "$LLVM_EXAMPLE_DIR" || exit 1

print_double_separator
echo "TEST: Test clowder reset"
./clean.sh || exit 1
./init.sh || exit 1

test_reset() {
   print_single_separator
   echo "TEST: clowder reset"
   clowder link || exit 1
   clowder herd || exit 1

   COMMIT_MESSAGE='Add new commits'
   pushd 'llvm/tools/clang' || exit 1
   git pull upstream master || exit 1
   test_number_commits 'HEAD' 'upstream/master' '0'
   UPSTREAM_COMMIT=$(git rev-parse HEAD)
   git reset --hard HEAD~3 || exit 1
   test_number_commits 'HEAD' 'upstream/master' '3'
   test_not_commit "$UPSTREAM_COMMIT"
   popd || exit 1

   clowder reset || exit 1

   pushd 'llvm/tools/clang' || exit 1
   test_number_commits 'HEAD' 'upstream/master' '0'
   test_commit  $UPSTREAM_COMMIT
   touch file1 || exit 1
   git add file1 || exit 1
   git commit -m "$COMMIT_MESSAGE" || exit 1
   touch file2 || exit 1
   git add file2 || exit 1
   git commit -m "$COMMIT_MESSAGE" || exit 1
   test_number_commits 'upstream/master' 'HEAD' '2'
   test_not_commit "$UPSTREAM_COMMIT"
   popd || exit 1

   clowder reset || exit 1

   pushd 'llvm/tools/clang' || exit 1
   test_number_commits 'HEAD' 'upstream/master' '0'
   test_commit  $UPSTREAM_COMMIT
   git reset --hard HEAD~3 || exit 1
   test_number_commits 'HEAD' 'upstream/master' '3'
   touch file1 || exit 1
   git add file1 || exit 1
   git commit -m "$COMMIT_MESSAGE" || exit 1
   touch file2 || exit 1
   git add file2 || exit 1
   git commit -m "$COMMIT_MESSAGE" || exit 1
   test_number_commits 'upstream/master' 'HEAD' '2'
   test_number_commits 'HEAD' 'upstream/master' '3'
   test_not_commit "$UPSTREAM_COMMIT"
   popd || exit 1

   clowder reset || exit 1

   pushd 'llvm/tools/clang' || exit 1
   test_number_commits 'HEAD' 'upstream/master' '0'
   test_number_commits 'upstream/master' 'HEAD' '0'
   test_commit  $UPSTREAM_COMMIT
   popd || exit 1
}
test_reset
