#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh


if [ "$ACCESS_LEVEL" == "write" ]; then
    print_double_separator
    echo "TEST: Test clowder repo write"

    cd "$CATS_EXAMPLE_DIR" || exit 1
    ./clean.sh
    ./init.sh
    $COMMAND herd $PARALLEL || exit 1
    pushd '.clowder' || exit 1
    git remote rm origin
    git remote add origin https://${GITHUB_TOKEN}@github.com/JrGoodle/cats.git > /dev/null 2>&1
    test_remote_url 'origin' "https://${GITHUB_TOKEN}@github.com/JrGoodle/cats.git"
    popd || exit 1

    test_clowder_repo_commit_pull_push() {
        print_single_separator
        echo "TEST: Test clowder repo commit, clowder repo pull, clowder repo push commands"
        # $COMMAND repo checkout repo-test || exit 1
        pushd .clowder || exit 1
        git checkout repo-test || exit 1
        ORIGINAL_COMMIT="$(git rev-parse HEAD)"
        test_branch repo-test
        popd || exit 1
        $COMMAND repo run 'touch newfile' || exit 1
        $COMMAND repo add 'newfile' || exit 1
        $COMMAND repo commit 'Add newfile for $COMMAND repo test' || exit 1
        pushd .clowder || exit 1
        NEW_COMMIT="$(git rev-parse HEAD)"
        popd || exit 1
        if [ "$ORIGINAL_COMMIT" == "$NEW_COMMIT" ]; then
            exit 1
        fi
        $COMMAND repo push || exit 1
        $COMMAND repo run 'git reset --hard HEAD~1' || exit 1
        pushd .clowder || exit 1
        test_commit "$ORIGINAL_COMMIT"
        popd || exit 1
        $COMMAND repo pull || exit 1
        pushd .clowder || exit 1
        test_commit "$NEW_COMMIT"
        popd || exit 1
        $COMMAND repo run 'git reset --hard HEAD~1' || exit 1
        $COMMAND repo run 'git push origin repo-test --force' || exit 1
        # $COMMAND repo checkout master || exit 1
        pushd .clowder || exit 1
        git checkout master || exit 1
        popd || exit 1
    }
    test_clowder_repo_commit_pull_push
fi
