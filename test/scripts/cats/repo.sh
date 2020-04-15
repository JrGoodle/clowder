#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh

print_double_separator
echo "TEST: Test clowder repo"

test_clowder_repo_add() {
    print_single_separator
    echo "TEST: Test clowder repo add command"
    $COMMAND repo add file_that_doesnt_exist && exit 1
}
test_clowder_repo_add

if [ "$ACCESS_LEVEL" == "write" ]; then
    "$TEST_SCRIPT_DIR/cats/write_repo.sh"
fi

test_clowder_repo_run() {
    print_single_separator
    echo "TEST: Test clowder repo run command"
    test_no_file_exists '.clowder/newfile'
    $COMMAND repo run 'touch newfile'
    test_file_exists '.clowder/newfile'
    $COMMAND repo run 'rm newfile'
    test_no_file_exists '.clowder/newfile'
}
test_clowder_repo_run

test_clowder_repo_checkout() {
    print_single_separator
    echo "TEST: Test clowder repo checkout command"
    $COMMAND repo checkout repo-test || exit 1
    pushd .clowder || exit 1
    test_branch repo-test
    popd || exit 1
    $COMMAND repo checkout ref_that_doesnt_exist && exit 1
    pushd .clowder || exit 1
    test_branch repo-test
    popd || exit 1
    $COMMAND repo checkout master || exit 1
    pushd .clowder || exit 1
    test_branch master
    popd || exit 1
}
test_clowder_repo_checkout

test_clowder_repo_clean() {
    print_single_separator
    echo "TEST: Test clowder repo clean command"
    pushd .clowder || exit 1
    test_git_clean
    popd || exit 1
    $COMMAND repo run 'touch newfile' || exit 1
    $COMMAND repo add 'newfile' || exit 1
    pushd .clowder || exit 1
    test_git_dirty
    popd || exit 1
    $COMMAND repo clean || exit 1
    pushd .clowder || exit 1
    test_git_clean
    popd || exit 1
}
test_clowder_repo_clean

test_clowder_repo_status() {
    print_single_separator
    echo "TEST: Test clowder repo status command"
    $COMMAND repo status || exit 1
}
test_clowder_repo_status
