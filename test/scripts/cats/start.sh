#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

export black_cats_projects=( 'black-cats/kit' \
                             'black-cats/kishka' \
                             'black-cats/sasha' \
                             'black-cats/june' )

export all_projects=( 'mu' 'duke' \
                      'black-cats/kit' \
                      'black-cats/kishka' \
                      'black-cats/sasha' \
                      'black-cats/june' )

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh

print_double_separator
echo "TEST: Test clowder start"

test_start() {
    print_single_separator
    echo "TEST: Start new branch"

    $COMMAND herd $PARALLEL || exit 1
    $COMMAND start start_branch -p jrgoodle/duke jrgoodle/mu || exit 1

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

    $COMMAND start start_branch || exit 1

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
