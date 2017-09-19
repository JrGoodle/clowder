#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh
prepare_cats_example
cd "$CATS_EXAMPLE_DIR" || exit 1

print_separator
echo "TEST: Test clowder start"

test_start() {
    echo "TEST: Start new branch"
    clowder herd >/dev/null

    clowder start start_branch || exit 1
    # TODO: clowder herd -b
    # clowder herd -b master -g black-cats
    clowder forall -g black-cats -c 'git fetch origin master'
    clowder forall -g black-cats -c 'git checkout master'

    pushd mu
    test_branch start_branch
    popd
    pushd duke
    test_branch start_branch
    popd
    pushd black-cats/jules
    test_branch master
    popd
    pushd black-cats/kishka
    test_branch master
    popd

    clowder start start_branch || exit 1

    pushd black-cats/jules
    test_branch start_branch
    popd
    pushd black-cats/kishka
    test_branch start_branch
    popd
}
test_start

if [ -z "$TRAVIS_OS_NAME" ]; then
    test_start_tracking() {
        echo "TEST: Test start tracking branch"
        clowder herd >/dev/null

        echo "TEST: No local or remote branches"
        clowder prune -af tracking_branch || exit 1
        clowder start -t tracking_branch || exit 1

        pushd duke
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd mu
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd black-cats/jules
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd black-cats/kishka
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd

        echo "TEST: Existing local branch checked out, remote tracking branch exists"
        clowder prune -af tracking_branch || exit 1
        clowder start -t tracking_branch || exit 1
        clowder start -t tracking_branch || exit 1

        echo "TEST: Existing local branch not checked out, remote tracking branch exists"
        clowder prune -af tracking_branch || exit 1
        clowder start -t tracking_branch || exit 1
        clowder forall -c 'git checkout master' || exit 1
        clowder start -t tracking_branch || exit 1

        echo "TEST: No local branch, existing remote branch"
        clowder prune -af tracking_branch || exit 1
        clowder start -t tracking_branch || exit 1
        clowder prune -f tracking_branch || exit 1
        clowder start -t tracking_branch && exit 1

        pushd duke
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_no_tracking_branch_exists tracking_branch
        popd
        pushd mu
        test_branch knead
        test_remote_branch_exists tracking_branch
        test_no_tracking_branch_exists tracking_branch
        popd
        pushd black-cats/jules
        test_branch master
        test_remote_branch_exists tracking_branch
        test_no_tracking_branch_exists tracking_branch
        popd
        pushd black-cats/kishka
        test_branch master
        test_remote_branch_exists tracking_branch
        test_no_tracking_branch_exists tracking_branch
        popd

        echo "TEST: Existing local branch checked out, existing remote branch, no tracking relationship"
        clowder prune -af tracking_branch || exit 1
        clowder start -t tracking_branch || exit 1
        clowder prune -f tracking_branch || exit 1
        clowder forall -c 'git checkout -b tracking_branch' || exit 1
        clowder start -t tracking_branch && exit 1

        echo "TEST: Existing local branch not checked out, existing remote branch, no tracking relationship"
        clowder prune -af tracking_branch || exit 1
        clowder start -t tracking_branch || exit 1
        clowder prune -f tracking_branch || exit 1
        clowder forall -c 'git checkout -b tracking_branch' || exit 1
        clowder forall -c 'git checkout master' || exit 1
        clowder start -t tracking_branch && exit 1

        echo "TEST: Existing local branch checked out, no remote branch"
        clowder prune -af tracking_branch
        clowder start tracking_branch || exit 1
        clowder start -t tracking_branch || exit 1

        pushd duke
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd mu
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd black-cats/jules
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd black-cats/kishka
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd

        echo "TEST: Existing local branch not checked out, no remote branch"
        clowder prune -r tracking_branch >/dev/null
        clowder start tracking_branch || exit 1
        clowder forall -c 'git checkout master'
        clowder start -t tracking_branch || exit 1
        clowder status

        pushd duke
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd mu
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd black-cats/jules
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd black-cats/kishka
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
    }
    test_start_tracking
fi
