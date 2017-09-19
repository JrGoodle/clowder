#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh
prepare_cats_example
cd "$CATS_EXAMPLE_DIR" || exit 1

print_separator
echo "TEST: Test clowder prune"

test_prune() {
    echo "TEST: Test clowder prune branch"
    clowder herd >/dev/null

    clowder start prune_branch >/dev/null
    clowder status || exit 1
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

    clowder start prune_branch >/dev/null
    clowder prune -f prune_branch -g black-cats || exit 1
    clowder status || exit 1

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
}
test_prune

test_prune_force() {
    echo "TEST: Test clowder force prune branch"

    clowder start prune_branch >/dev/null
    clowder status || exit 1
    pushd duke
    touch something >/dev/null
    git add something >/dev/null
    git commit -m 'something' >/dev/null
    popd
    pushd mu
    touch something >/dev/null
    git add something >/dev/null
    git commit -m 'something' >/dev/null
    popd

    clowder status || exit 1
    clowder prune prune_branch && exit 1
    clowder prune -f prune_branch || exit 1

    pushd duke
    test_branch purr
    popd
    pushd mu
    test_branch knead
    popd
}
test_prune_force

if [ -z "$TRAVIS_OS_NAME" ]; then
    test_prune_remote() {
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
    }
    test_prune_remote

    test_prune_all() {
        echo "TEST: Test clowder prune all - delete local and remote branch"
        clowder start -t prune_branch -p jrgoodle/duke >/dev/null
        clowder status || exit 1

        pushd duke
        test_local_branch_exists prune_branch
        test_remote_branch_exists prune_branch
        popd

        clowder prune -af prune_branch || exit 1

        pushd duke
        test_no_local_branch_exists prune_branch
        test_no_remote_branch_exists prune_branch
        popd
    }
    test_prune_all
fi
