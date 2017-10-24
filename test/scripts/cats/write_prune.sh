#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

export all_projects=( 'mu' 'duke' \
                      'black-cats/kit' \
                      'black-cats/kishka' \
                      'black-cats/sasha' \
                      'black-cats/jules' )

print_double_separator
echo "TEST: Test clowder prune write"

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh
clowder herd $PARALLEL || exit 1

if [ "$ACCESS_LEVEL" == "write" ]; then
    test_prune_remote() {
        print_single_separator
        echo "TEST: Test clowder prune remote branch"

        clowder prune -af prune_branch || exit 1
        clowder start -t prune_branch || exit 1
        clowder prune prune_branch || exit 1

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_no_local_branch_exists prune_branch
            test_remote_branch_exists prune_branch
            popd || exit 1
        done

        clowder prune -r prune_branch || exit 1

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_no_local_branch_exists prune_branch
            test_no_remote_branch_exists prune_branch
            popd || exit 1
        done
    }
    test_prune_remote

    test_prune_all() {
        print_single_separator
        echo "TEST: Test clowder prune all - delete local and remote branch"
        clowder start -t prune_branch || exit 1

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_local_branch_exists prune_branch
            test_remote_branch_exists prune_branch
            popd || exit 1
        done

        clowder prune -af prune_branch || exit 1

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_no_local_branch_exists prune_branch
            test_no_remote_branch_exists prune_branch
            popd || exit 1
        done
    }
    test_prune_all
fi
