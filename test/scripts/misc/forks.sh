#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

print_double_separator
echo "TEST: Test clowder forks"
cd "$MISC_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh || exit 1

test_fork_groups_1() {
    test_no_directory_exists 'sox'
    test_no_directory_exists 'djinni'
    test_no_directory_exists 'gyp'
    begin_command
    $COMMAND herd JrGoodle/sox $PARALLEL || exit 1
    end_command
    pushd sox || exit 1
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
    test_no_directory_exists 'sox'
    test_no_directory_exists 'djinni'
    test_no_directory_exists 'gyp'
    begin_command
    $COMMAND herd sox $PARALLEL || exit 1
    end_command
    pushd sox || exit 1
    test_branch 'master'
    test_remote_url 'origin' 'git@github.com:JrGoodle/sox.git'
    test_remote_url 'upstream' 'https://git.code.sf.net/p/sox/code.git'
    popd || exit 1
    test_no_directory_exists 'djinni'
    test_no_directory_exists 'gyp'
}
test_fork_groups_2

test_fork_herd() {
    echo "TEST: Herd fork"
    ./clean.sh
    ./init.sh || exit 1
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
test_fork_herd

# TODO: Add tests for logic renaming remotes

if [ "$ACCESS_LEVEL" == "write" ]; then
    "$TEST_SCRIPT_DIR/misc/write_forks.sh" $1
fi
