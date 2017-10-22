#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

export black_cats_projects=( 'black-cats/kit' \
                             'black-cats/kishka' \
                             'black-cats/sasha' \
                             'black-cats/jules' )

export all_projects=( 'mu' 'duke' \
                      'black-cats/kit' \
                      'black-cats/kishka' \
                      'black-cats/sasha' \
                      'black-cats/jules' )

prepare_cats_example
cd "$CATS_EXAMPLE_DIR" || exit 1
./init.sh

print_double_separator
echo "TEST: Test clowder start"

test_start() {
    print_single_separator
    echo "TEST: Start new branch"

    clowder herd || exit 1
    clowder start start_branch -g cats || exit 1

    pushd mu || exit 1
    test_branch start_branch
    test_no_remote_branch_exists start_branch
    popd || exit 1
    pushd duke || exit 1
    test_branch start_branch
    test_no_remote_branch_exists start_branch
    popd || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_branch master
        test_no_remote_branch_exists start_branch
        test_no_local_branch_exists start_branch
        popd || exit 1
    done

    clowder start start_branch || exit 1

    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_branch start_branch
        test_no_remote_branch_exists start_branch
        popd || exit 1
    done
}
test_start

if [ "$ACCESS_LEVEL" == "write" ]; then
    "$TEST_SCRIPT_DIR/cats/write_start.sh"
fi
