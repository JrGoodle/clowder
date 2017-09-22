#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh
prepare_cats_example
cd "$CATS_EXAMPLE_DIR" || exit 1

print_double_separator
echo "TEST: Test clowder repo"

test_clowder_repo_add() {
    print_single_separator
    echo "TEST: Test clowder repo add command"
    clowder repo add file_that_doesnt_exist && exit 1
}
test_clowder_repo_add

test_clowder_repo_checkout() {
    print_single_separator
    echo "TEST: Test clowder repo checkout command"
    clowder repo checkout tags || exit 1
    pushd .clowder
    test_branch tags
    popd
    clowder repo checkout ref_that_doesnt_exist && exit 1
    pushd .clowder
    test_branch tags
    popd
    clowder repo checkout master || exit 1
    pushd .clowder
    test_branch master
    popd
}
test_clowder_repo_checkout

test_clowder_repo_clean() {
    print_single_separator
    echo "TEST: Test clowder repo clean command"
    echo "TODO: Add tests"
}
test_clowder_repo_clean

test_clowder_repo_commit() {
    print_single_separator
    echo "TEST: Test clowder repo commit command"
    echo "TODO: Add tests"
}
test_clowder_commit

test_clowder_repo_pull() {
    print_single_separator
    echo "TEST: Test clowder repo pull command"
    echo "TODO: Add tests"
}
test_clowder_repo_pull

test_clowder_repo_push() {
    print_single_separator
    echo "TEST: Test clowder repo push command"
    echo "TODO: Add tests"
}
test_clowder_repo_push

test_clowder_repo_run() {
    print_single_separator
    echo "TEST: Test clowder repo run command"
    echo "TODO: Add tests"
}
test_clowder_repo_run

test_clowder_repo_status() {
    print_single_separator
    echo "TEST: Test clowder repo status command"
    echo "TODO: Add tests"
}
test_clowder_repo_status
