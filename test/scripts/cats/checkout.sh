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
    test_branch purr
    popd || exit 1
}

print_double_separator
echo "TEST: Test clowder checkout"

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh || exit 1

begin_command
$COMMAND herd $PARALLEL || exit 1
end_command

test_checkout() {
    print_single_separator
    echo "TEST: Check projects are on correct branches"
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    local branch='checkout_branch'

    pushd duke || exit 1
    git branch $branch || exit 1
    popd || exit 1
    pushd mu || exit 1
    git branch $branch || exit 1
    popd || exit 1

    test_cats_default_herd_branches

    begin_command
    $COMMAND checkout $branch || exit 1
    end_command

    pushd duke || exit 1
    test_branch $branch || exit 1
    popd || exit 1
    pushd mu || exit 1
    test_branch $branch || exit 1
    popd || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_branch master
        popd || exit 1
    done

    begin_command
    $COMMAND checkout knead jrgoodle/mu || exit 1
    end_command
    begin_command
    $COMMAND checkout purr jrgoodle/duke || exit 1
    end_command

    test_cats_default_herd_branches
}
test_checkout
