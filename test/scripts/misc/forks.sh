#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

export project_paths=( 'djinni' \
                       'gyp' \
                       'sox' )

export projects=( 'dropbox/djinni' \
                  'external/gyp' \
                  'p/sox/code' )

export fork_paths=( 'djinni' \
                    'gyp' \
                    'sox' )

export fork_projects=( 'dropbox/djinni' \
                       'external/gyp' \
                       'p/sox/code' )

print_double_separator
echo "TEST: Test clowder sources"
cd "$MISC_EXAMPLE_DIR" || exit 1
./clean.sh
./copy-cache.sh

test_forks_env() {
    echo 'TODO'
    # echo "TEST: Fork remote environment variable in script"
    # $COMMAND forall $PARALLEL -c "$TEST_SCRIPT_DIR/test_forall_script_env_fork.sh" -p "llvm-mirror/clang" || exit 1
    # $COMMAND forall $PARALLEL -c "$TEST_SCRIPT_DIR/test_forall_script_env_fork.sh" -p "llvm-mirror/llvm" && exit 1
    # echo "TEST: Fork remote environment variable in command"
    # $COMMAND forall $PARALLEL -c 'if [ $PROJECT_REMOTE != upstream ]; then exit 1; fi' -p 'llvm-mirror/clang' || exit 1
    # $COMMAND forall $PARALLEL -c 'if [ $FORK_REMOTE != origin ]; then exit 1; fi' -p 'llvm-mirror/clang' || exit 1
}
