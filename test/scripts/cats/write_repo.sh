#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

print_double_separator
echo "TEST: Test clowder repo write"

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh
clowder herd $PARALLEL || exit 1

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
        test_commit "$ORIGINAL_COMMIT"
        popd || exit 1
        clowder repo pull || exit 1
        pushd .clowder || exit 1
        test_commit "$NEW_COMMIT"
        popd || exit 1
        clowder repo run 'git reset --hard HEAD~1' || exit 1
        clowder repo run 'git push origin repo-test --force' || exit 1
        clowder repo checkout master || exit 1
    }
    test_clowder_repo_commit_pull_push
fi
