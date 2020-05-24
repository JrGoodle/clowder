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
echo "TEST: Test clowder forks"
cd "$MISC_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh || exit 1

test_fork_groups_1() {
    test_no_directory_exists 'sox-code'
    test_no_directory_exists 'djinni'
    test_no_directory_exists 'gyp'
    begin_command
    $COMMAND herd $PARALLEL JrGoodle/sox || exit 1
    end_command
    pushd sox-code || exit 1
    test_branch 'master'
    test_remote_url 'origin' 'git@github.com:JrGoodle/sox.git'
    test_remote_url 'upstream' 'https://git.code.sf.net/p/sox/code.git'
    popd || exit 1
    test_no_directory_exists 'djinni'
    test_no_directory_exists 'gyp'
}
test_fork_groups_1

./clean.sh
./init.sh || exit 1

test_fork_groups_2() {
    test_no_directory_exists 'sox-code'
    test_no_directory_exists 'djinni'
    test_no_directory_exists 'gyp'
    begin_command
    $COMMAND herd $PARALLEL sox || exit 1
    end_command
    pushd sox-code || exit 1
    test_branch 'master'
    test_remote_url 'origin' 'git@github.com:JrGoodle/sox.git'
    test_remote_url 'upstream' 'https://git.code.sf.net/p/sox/code.git'
    popd || exit 1
    test_no_directory_exists 'djinni'
    test_no_directory_exists 'gyp'
}
test_fork_groups_2

./clean.sh
./init.sh || exit 1

test_forks_env() {
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    # echo "TEST: Fork remote environment variable in script"
    begin_command
    $COMMAND forall $PARALLEL "gyp" -c "$TEST_SCRIPT_DIR/test_forall_script_env_fork.sh" || exit 1
    end_command
    begin_command
    $COMMAND forall $PARALLEL "dropbox/djinni" -c "$TEST_SCRIPT_DIR/test_forall_script_env_fork.sh" && exit 1
    end_command
    # echo "TEST: Fork remote environment variable in command"
    begin_command
    $COMMAND forall $PARALLEL 'gyp' -c 'if [ $PROJECT_REMOTE != upstream ]; then exit 1; fi' || exit 1
    end_command
    begin_command
    $COMMAND forall $PARALLEL 'gyp' -c 'if [ $FORK_REMOTE != origin ]; then exit 1; fi' || exit 1
    end_command
}
test_forks_env

./clean.sh
./init.sh || exit 1

test_fork_herd() {
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    pushd 'gyp' || exit 1
    test_tracking_branch_exists 'fork-branch'
    local fork_branch_commit='bd11dd1c51ef17592384df927c47023071639f96'
    test_commit $fork_branch_commit
    git pull upstream master
    test_not_commit $fork_branch_commit
    popd || exit 1
}
test_fork_gyp

if [ "$ACCESS_LEVEL" == "write" ]; then
    "$TEST_SCRIPT_DIR/misc/write_forks.sh" $1
fi
