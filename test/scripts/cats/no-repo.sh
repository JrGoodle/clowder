#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

export cats_projects=( 'duke' 'mu' )

export black_cats_projects=( 'black-cats/kit' \
                             'black-cats/kishka' \
                             'black-cats/sasha' \
                             'black-cats/june' )

export all_projects=( 'mu' 'duke' \
                      'black-cats/kit' \
                      'black-cats/kishka' \
                      'black-cats/sasha' \
                      'black-cats/june' )

test_cats_default_herd_branches() {
    echo "TEST: cats projects on default branches"
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_branch master
        popd || exit 1
    done
    pushd mu || exit 1
    test_branch knead
    popd || exit 1
    pushd duke || exit 1
    test_branch heads/purr
    popd || exit 1
}

print_double_separator
echo "TEST: Test clowder commands with non-symlink clowder yaml file and no clowder repo"

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh

test_herd_missing_clowder() {
    print_single_separator
    echo "TEST: Fail herd with missing clowder.yaml"
    begin_command
    $COMMAND herd $PARALLEL && exit 1
    end_command
}
test_herd_missing_clowder
