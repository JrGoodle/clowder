#!/usr/bin/env bash

pushd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

test_prune()
{
    print_separator
    echo "TEST: Test clowder prune branch"
    clowder herd

    clowder start prune_branch
    clowder prune -f prune_branch || exit 1

    pushd duke
    test_branch purr
    test_no_local_branch_exists prune_branch
    popd
    pushd mu
    test_branch knead
    test_no_local_branch_exists prune_branch
    popd
    pushd black-cats/jules
    test_branch master
    test_no_local_branch_exists prune_branch
    popd
    pushd black-cats/kishka
    test_branch master
    test_no_local_branch_exists prune_branch
    popd

    clowder start prune_branch
    clowder prune -f prune_branch -g black-cats || exit 1

    pushd duke
    test_branch prune_branch
    popd
    pushd mu
    test_branch prune_branch
    popd
    pushd black-cats/jules
    test_branch master
    test_no_local_branch_exists prune_branch
    popd
    pushd black-cats/kishka
    test_branch master
    test_no_local_branch_exists prune_branch
    popd

    echo "TEST: Test clowder force prune branch"

    clowder start prune_branch
    pushd duke
    touch something
    git add something
    git commit -m 'something'
    popd
    pushd mu
    touch something
    git add something
    git commit -m 'something'
    popd

    clowder prune prune_branch && exit 1
    clowder prune -f prune_branch || exit 1

    pushd duke
    test_branch purr
    popd
    pushd mu
    test_branch knead
    popd

    if [ -z "$TRAVIS_OS_NAME" ]; then
        echo "TEST: Test clowder prune remote branch"

        clowder prune -af prune_branch || exit 1
        clowder start -t prune_branch -p jrgoodle/duke || exit 1
        clowder prune -f prune_branch || exit 1

        pushd duke
        test_no_local_branch_exists prune_branch
        test_remote_branch_exists prune_branch
        popd

        clowder prune -r prune_branch || exit 1

        pushd duke
        test_no_local_branch_exists prune_branch
        test_no_remote_branch_exists prune_branch
        popd

        echo "TEST: Test clowder prune all - delete local and remote branch"
        clowder start -t prune_branch -p jrgoodle/duke || exit 1

        pushd duke
        test_local_branch_exists prune_branch
        test_remote_branch_exists prune_branch
        popd

        clowder prune -af prune_branch || exit 1

        pushd duke
        test_no_local_branch_exists prune_branch
        test_no_remote_branch_exists prune_branch
        popd
    fi
}
test_prune

popd
