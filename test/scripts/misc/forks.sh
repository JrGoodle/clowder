#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

export project_paths=( 'djinni' \
                       'gyp' \
                       'sox' )

export projects=( 'dropbox/djinni' \
                  'gyp' \
                  'p/sox/code' )

print_double_separator
echo "TEST: Test clowder sources"
cd "$MISC_EXAMPLE_DIR" || exit 1
./clean.sh
./copy-cache.sh

test_forks_env() {
    # echo "TEST: Fork remote environment variable in script"
    $COMMAND forall $PARALLEL -c "$TEST_SCRIPT_DIR/test_forall_script_env_fork.sh" -p "gyp" || exit 1
    $COMMAND forall $PARALLEL -c "$TEST_SCRIPT_DIR/test_forall_script_env_fork.sh" -p "dropbox/djinni" && exit 1
    # echo "TEST: Fork remote environment variable in command"
    $COMMAND forall $PARALLEL -c 'if [ $PROJECT_REMOTE != upstream ]; then exit 1; fi' -p 'gyp' || exit 1
    $COMMAND forall $PARALLEL -c 'if [ $FORK_REMOTE != origin ]; then exit 1; fi' -p 'gyp' || exit 1
}
test_forks_env

./clean.sh
./copy-cache.sh

test_fork_herd() {
    $COMMAND herd $PARALLEL || exit 1
    pushd 'gyp' || exit 1
    test_tracking_branch_exists 'fork-branch'
    fork_branch_commit=''bd11dd1c51ef17592384df927c47023071639f96''
    test_commit $fork_branch_commit
    git pull upstream master
    test_not_commit $fork_branch_commit
    popd || exit 1
}
test_fork_gyp

if [ "$ACCESS_LEVEL" == "write" ]; then
    "$TEST_SCRIPT_DIR/misc/write_forks.sh" $1
fi
