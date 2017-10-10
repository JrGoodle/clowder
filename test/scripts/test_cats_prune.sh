#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh
prepare_cats_example
cd "$CATS_EXAMPLE_DIR" || exit 1

export black_cats_projects=( 'black-cats/kit' \
                             'black-cats/kishka' \
                             'black-cats/sasha' \
                             'black-cats/jules' )

export all_projects=( 'mu' 'duke' \
                      'black-cats/kit' \
                      'black-cats/kishka' \
                      'black-cats/sasha' \
                      'black-cats/jules' )

print_double_separator
echo "TEST: Test clowder prune"

test_prune() {
    print_single_separator
    echo "TEST: Test clowder prune branch"
    clowder herd || exit 1

    clowder start prune_branch || exit 1

    for project in "${all_projects[@]}"; do
        pushd $project
        test_branch prune_branch
        popd
    done

    clowder prune -f prune_branch || exit 1

    pushd duke
    test_branch purr
    test_no_local_branch_exists prune_branch
    popd
    pushd mu
    test_branch knead
    test_no_local_branch_exists prune_branch
    popd
    for project in "${black_cats_projects[@]}"; do
        pushd $project
        test_branch master
        test_no_local_branch_exists prune_branch
        popd
    done

    clowder start prune_branch >/dev/null

    for project in "${all_projects[@]}"; do
        pushd $project
        test_branch prune_branch
        popd
    done

    clowder prune -f prune_branch -g black-cats || exit 1

    pushd duke
    test_branch prune_branch
    popd
    pushd mu
    test_branch prune_branch
    popd
    for project in "${black_cats_projects[@]}"; do
        pushd $project
        test_branch master
        test_no_local_branch_exists prune_branch
        popd
    done
}
test_prune

test_prune_force() {
    print_single_separator
    echo "TEST: Test clowder force prune branch"

    clowder start prune_branch || exit 1

    for project in "${all_projects[@]}"; do
        pushd $project
        test_branch prune_branch
        touch something >/dev/null
        git add something >/dev/null
        git commit -m 'something' >/dev/null
        popd
    done

    clowder prune prune_branch && exit 1

    for project in "${all_projects[@]}"; do
        pushd $project
        test_local_branch_exists prune_branch
        popd
    done

    clowder prune -f prune_branch || exit 1

    pushd duke
    test_branch purr
    test_no_local_branch_exists prune_branch
    popd
    pushd mu
    test_branch knead
    test_no_local_branch_exists prune_branch
    popd
    for project in "${black_cats_projects[@]}"; do
        pushd $project
        test_branch master
        test_no_local_branch_exists prune_branch
        popd
    done
}
test_prune_force

if [ "$ACCESS_LEVEL" == "write" ]; then
    test_prune_remote() {
        print_single_separator
        echo "TEST: Test clowder prune remote branch"

        clowder prune -af prune_branch || exit 1
        clowder start -t prune_branch || exit 1
        clowder prune prune_branch || exit 1

        for project in "${all_projects[@]}"; do
            pushd $project
            test_no_local_branch_exists prune_branch
            test_remote_branch_exists prune_branch
            popd
        done

        clowder prune -r prune_branch || exit 1

        for project in "${all_projects[@]}"; do
            pushd $project
            test_no_local_branch_exists prune_branch
            test_no_remote_branch_exists prune_branch
            popd
        done
    }
    test_prune_remote

    test_prune_all() {
        print_single_separator
        echo "TEST: Test clowder prune all - delete local and remote branch"
        clowder start -t prune_branch || exit 1

        for project in "${all_projects[@]}"; do
            pushd $project
            test_local_branch_exists prune_branch
            test_remote_branch_exists prune_branch
            popd
        done

        clowder prune -af prune_branch || exit 1

        for project in "${all_projects[@]}"; do
            pushd $project
            test_no_local_branch_exists prune_branch
            test_no_remote_branch_exists prune_branch
            popd
        done
    }
    test_prune_all
fi
