#!/usr/bin/env bash

pushd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

test_forall()
{
    print_separator
    echo "TEST: Run forall command"
    clowder forall -c 'git status' || exit 1
    echo "TEST: Run forall script"
    clowder forall -c "$TEST_SCRIPT_DIR/tests/test_forall_script.sh" || exit 1
    echo "TEST: Run forall command for specific groups"
    clowder forall -c 'git status' -g "$@" || exit 1
    echo "TEST: Run forall script for specific groups"
    clowder forall -c "$TEST_SCRIPT_DIR/tests/test_forall_script.sh" -g "$@" || exit 1
    echo "TEST: Run forall command with error"
    clowder forall -c 'exit 1' && exit 1
    echo "TEST: Run forall command with --ignore-error"
    clowder forall -ic 'exit 1' || exit 1
    echo "TEST: Run forall script with error"
    clowder forall -c "$TEST_SCRIPT_DIR/tests/test_forall_script_error.sh" && exit 1
    echo "TEST: Run forall script with --ignore-error"
    clowder forall -ic "$TEST_SCRIPT_DIR/tests/test_forall_script_error.sh" || exit 1
}
test_forall 'cats'

test_forall_projects()
{
    print_separator
    echo "TEST: Run forall command for specific projects"
    clowder forall -c 'git status' -p "$@" || exit 1
    echo "TEST: Run forall script for specific projects"
    clowder forall -c "$TEST_SCRIPT_DIR/tests/test_forall_script.sh" -p "$@" || exit 1
}
test_forall_projects 'jrgoodle/kit' 'jrgoodle/kishka'

popd
