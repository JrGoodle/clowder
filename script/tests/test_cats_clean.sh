#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

export cats_projects=( 'duke' 'mu' )

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

print_double_separator
echo "TEST: Test clowder clean"

test_clean_groups() {
    print_single_separator
    make_dirty_repos "${all_projects[@]}"
    echo "TEST: Clean specific group when dirty"

    for project in "${all_projects[@]}"; do
        pushd $project
        test_git_dirty
        popd
    done

    clowder clean -g 'black-cats' || exit 1

    for project in "${all_projects[@]}"; do
        pushd $project
        test_git_clean
        popd
    done
    pushd mu
    test_git_dirty
    popd
    pushd duke
    test_git_dirty
    popd

    make_dirty_repos "${black_cats_projects[@]}"

    echo "TEST: Clean all when dirty"

    for project in "${all_projects[@]}"; do
        pushd $project
        test_git_dirty
        popd
    done

    clowder clean || exit 1

    for project in "${all_projects[@]}"; do
        pushd $project
        test_git_clean
        popd
    done
}
test_clean_groups

test_clean_projects() {
    print_single_separator
    echo "TEST: Clean projects"
    make_dirty_repos "${all_projects[@]}"
    echo "TEST: Clean specific project when dirty"

    for project in "${all_projects[@]}"; do
        pushd $project
        test_git_dirty
        popd
    done

    clowder clean -p "$@" || exit 1

    for project in "${black_cats_projects[@]}"; do
        pushd $project
        test_git_dirty
        popd
    done
    pushd mu
    test_git_clean
    popd
    pushd duke
    test_git_clean
    popd

    echo "TEST: Clean all when dirty"
    clowder clean || exit 1

    for project in "${all_projects[@]}"; do
        pushd $project
        test_git_clean
        popd
    done
}
test_clean_projects 'jrgoodle/duke' 'jrgoodle/mu'

test_clean_all() {
    print_single_separator
    make_dirty_repos "${all_projects[@]}"
    echo "TEST: Clean all when dirty"

    for project in "${all_projects[@]}"; do
        pushd $project
        test_git_dirty
        popd
    done

    clowder clean || exit 1

    for project in "${all_projects[@]}"; do
        pushd $project
        test_git_clean
        popd
    done

    echo "TEST: Clean when clean"
    clowder clean || exit 1

    for project in "${all_projects[@]}"; do
        pushd $project
        test_git_clean
        popd
    done
}
test_clean_all 'black-cats'

test_clean_missing_directories() {
    print_single_separator
    make_dirty_repos "${all_projects[@]}"
    rm -rf "$@"

    for project in "${cats_projects[@]}"; do
    	if [ -d "$project" ]; then
            exit 1
        fi
    done

    for project in "${black_cats_projects[@]}"; do
        pushd $project
        test_git_dirty
        popd
    done

    echo "TEST: Clean when directories are missing"
    clowder clean || exit 1

    for project in "${cats_projects[@]}"; do
    	if [ -d "$project" ]; then
            exit 1
        fi
    done

    for project in "${black_cats_projects[@]}"; do
        pushd $project
        test_git_clean
        popd
    done

    clowder herd || exit 1
}
test_clean_missing_directories 'mu' 'duke'
