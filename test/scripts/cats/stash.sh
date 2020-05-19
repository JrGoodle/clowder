#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh || exit 1
begin_command
$COMMAND herd $PARALLEL || exit 1
end_command

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
echo "TEST: Test clowder stash"

test_stash() {
    print_single_separator
    make_dirty_repos "${all_projects[@]}"
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_git_dirty
        popd || exit 1
    done
    echo "TEST: Fail herd with dirty repos"
    begin_command
    $COMMAND herd && exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_git_dirty
        popd || exit 1
    done
    echo "TEST: Stash specific groups when dirty"
    begin_command
    $COMMAND stash "$@" || exit 1
    end_command
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_git_clean
        popd || exit 1
    done
    for project in "${cats_projects[@]}"; do
        pushd $project || exit 1
        test_git_dirty
        popd || exit 1
    done
    echo "TEST: Stash all changes when dirty"
    begin_command
    $COMMAND stash || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_git_clean
        popd || exit 1
    done
    echo "TEST: Stash changes when clean"
    begin_command
    $COMMAND stash || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_git_clean
        popd || exit 1
    done
}
test_stash 'black-cats'

test_stash_projects() {
    print_single_separator
    make_dirty_repos "${all_projects[@]}"
    echo "TEST: Stash specific projects when dirty"
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_git_dirty
        popd || exit 1
    done
    begin_command
    $COMMAND stash "$@" || exit 1
    end_command
    for project in "${cats_projects[@]}"; do
        pushd $project || exit 1
        test_git_clean
        popd || exit 1
    done
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_git_dirty
        popd || exit 1
    done
    echo "TEST: Stash all changes when dirty"
    begin_command
    $COMMAND stash || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_git_clean
        popd || exit 1
    done
}
test_stash_projects 'jrgoodle/duke' 'jrgoodle/mu'

test_stash_missing_directories() {
    print_single_separator
    echo "TEST: Stash all changes when directories are missing"
    make_dirty_repos "${all_projects[@]}"
    rm -rf "$@"
    test_no_directory_exists 'duke'
    test_no_directory_exists 'mu'
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_git_dirty
        popd || exit 1
    done
    begin_command
    $COMMAND stash || exit 1
    end_command
    test_no_directory_exists 'duke'
    test_no_directory_exists 'mu'
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_git_clean
        popd || exit 1
    done
    begin_command
    $COMMAND status || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_git_clean
        popd || exit 1
    done
}
test_stash_missing_directories 'mu' 'duke'
