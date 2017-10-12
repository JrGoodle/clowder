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
    pushd .clowder || exit 1
    test_branch tags
    popd || exit 1
    clowder repo checkout ref_that_doesnt_exist && exit 1
    pushd .clowder || exit 1
    test_branch tags
    popd || exit 1
    clowder repo checkout master || exit 1
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
    clowder repo run 'touch newfile' || exit 1
    clowder repo add 'newfile' || exit 1
    pushd .clowder || exit 1
    test_git_dirty
    popd || exit 1
    clowder repo clean || exit 1
    pushd .clowder || exit 1
    test_git_clean
    popd || exit 1
}
test_clowder_repo_clean

if [ "$ACCESS_LEVEL" == "write" ]; then
    test_clowder_repo_commit_pull_push() {
        print_single_separator
        echo "TEST: Test clowder repo commit, clowder repo pull, clowder repo push commands"
        clowder repo checkout repo-test || exit 1
        pushd .clowder || exit 1
        ORIGINAL_COMMIT="$(git rev-parse HEAD)"
        test_branch repo-test
        popd || exit 1
        clowder repo run 'touch newfile' || exit 1
        clowder repo add 'newfile' || exit 1
        clowder repo commit 'Add newfile for clowder repo test' || exit 1
        pushd .clowder || exit 1
        NEW_COMMIT="$(git rev-parse HEAD)"
        popd || exit 1
        if [ "$ORIGINAL_COMMIT" == "$NEW_COMMIT" ]; then
            exit 1
        fi
        clowder repo push || exit 1
        clowder repo run 'git reset --hard HEAD~1' || exit 1
        pushd .clowder || exit 1
        if [ "$ORIGINAL_COMMIT" != "$(git rev-parse HEAD)" ]; then
            exit 1
        fi
        popd || exit 1
        clowder repo pull || exit 1
        pushd .clowder || exit 1
        if [ "$NEW_COMMIT" != "$(git rev-parse HEAD)" ]; then
            exit 1
        fi
        popd || exit 1
        clowder repo run 'git reset --hard HEAD~1' || exit 1
        clowder repo run 'git push origin repo-test --force' || exit 1
        clowder repo checkout master || exit 1
    }
    test_clowder_repo_commit_pull_push
fi

test_clowder_repo_run() {
    print_single_separator
    echo "TEST: Test clowder repo run command"
    if [ -f .clowder/newfile ]; then
        exit 1
    fi
    clowder repo run 'touch newfile'
    if [ ! -f .clowder/newfile ]; then
        exit 1
    fi
    clowder repo run 'rm newfile'
    if [ -f .clowder/newfile ]; then
        exit 1
    fi
}
test_clowder_repo_run

test_clowder_repo_status() {
    print_single_separator
    echo "TEST: Test clowder repo status command"
    clowder repo status || exit 1
}
test_clowder_repo_status
