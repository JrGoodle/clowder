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

print_double_separator
echo "TEST: Test clowder groups"

# TODO: Add more tests for other commands besides just herd

cd "$CATS_EXAMPLE_DIR" || exit 1

./clean.sh
./init.sh || exit 1

test_groups_1() {
    print_single_separator
    echo "TEST: Check jrgoodle/mu group"
    begin_command
    $COMMAND link groups || exit 1
    end_command
    begin_command
    $COMMAND herd jrgoodle/mu $PARALLEL || exit 1
    end_command
    pushd mu || exit 1
    test_branch knead
    popd || exit 1
    pushd mu-cat || exit 1
    test_branch knead
    popd || exit 1
    test_no_directory_exists 'duke'
    test_no_directory_exists 'black-cats'
}
test_groups_1

./clean.sh
./init.sh || exit 1

test_groups_2() {
    print_single_separator
    echo "TEST: Check mu group"
    begin_command
    $COMMAND link groups || exit 1
    end_command
    begin_command
    $COMMAND herd mu $PARALLEL || exit 1
    end_command
    pushd mu || exit 1
    test_branch knead
    popd || exit 1
    pushd mu-cat || exit 1
    test_branch knead
    popd || exit 1
    test_no_directory_exists 'duke'
    test_no_directory_exists 'black-cats'
}
test_groups_2

./clean.sh
./init.sh || exit 1

test_groups_3() {
    print_single_separator
    echo "TEST: Check default group"
    begin_command
    $COMMAND link groups || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    pushd mu-cat || exit 1
    test_branch knead
    popd || exit 1
    test_no_directory_exists 'duke'
    test_no_directory_exists 'mu'
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_branch master
        popd || exit 1
    done
}
test_groups_3

./clean.sh
./init.sh || exit 1

test_groups_4() {
    print_single_separator
    echo "TEST: Check cats group"
    begin_command
    $COMMAND link groups || exit 1
    end_command
    begin_command
    $COMMAND herd cats $PARALLEL || exit 1
    end_command
    pushd mu-cat || exit 1
    test_branch knead
    popd || exit 1
    pushd mu || exit 1
    test_branch knead
    popd || exit 1
    pushd duke || exit 1
    test_branch heads/purr
    popd || exit 1
    test_no_directory_exists 'black-cats'
}
test_groups_4

./clean.sh
./init.sh || exit 1

test_groups_5() {
    print_single_separator
    echo "TEST: Check all, notdefault groups"
    begin_command
    $COMMAND link groups || exit 1
    end_command
    begin_command
    $COMMAND herd all notdefault $PARALLEL || exit 1
    end_command
    pushd mu-cat || exit 1
    test_branch knead
    popd || exit 1
    pushd mu || exit 1
    test_branch knead
    popd || exit 1
    pushd duke || exit 1
    test_branch heads/purr
    popd || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_branch master
        popd || exit 1
    done
}
test_groups_5

./clean.sh
./init.sh || exit 1

test_groups_6() {
    print_single_separator
    echo "TEST: Check notdefault group"
    begin_command
    $COMMAND link groups || exit 1
    end_command
    begin_command
    $COMMAND herd notdefault $PARALLEL || exit 1
    end_command
    pushd mu || exit 1
    test_branch knead
    popd || exit 1
    pushd duke || exit 1
    test_branch heads/purr
    popd || exit 1
    test_no_directory_exists 'mu-cat'
    test_no_directory_exists 'black-cats'
}
test_groups_6

./clean.sh
./init.sh || exit 1

test_groups_7() {
    print_single_separator
    echo "TEST: Check cats, black-cats groups"
    begin_command
    $COMMAND link groups || exit 1
    end_command
    begin_command
    $COMMAND herd cats black-cats $PARALLEL || exit 1
    end_command
    pushd mu-cat || exit 1
    test_branch knead
    popd || exit 1
    pushd mu || exit 1
    test_branch knead
    popd || exit 1
    pushd duke || exit 1
    test_branch heads/purr
    popd || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_branch master
        popd || exit 1
    done
}
test_groups_7
