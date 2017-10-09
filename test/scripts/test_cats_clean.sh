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

    for project in "${black_cats_projects[@]}"; do
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
        test_no_untracked_files
        popd
    done

    clowder herd || exit 1
}
test_clean_missing_directories 'mu' 'duke'

test_clean_abort_rebase() {
    print_single_separator
    echo "TEST: Clean when in the middle of a rebase"

    clowder link || exit 1
    clowder herd || exit 1

    pushd mu
        touch newfile
        echo 'something' > newfile
        git checkout -b something
        git add newfile || exit 1
        git commit -m 'Add newfile with something' || exit 1
        git checkout knead || exit 1
        touch newfile
        echo 'something else' > newfile || exit 1
        git add newfile || exit 1
        git commit -m 'Add newfile with something else' || exit 1
        test_no_rebase_in_progress
        git rebase something && exit 1
        test_rebase_in_progress
        git reset --hard || exit 1
        test_rebase_in_progress
    popd

    clowder clean || exit 1

    pushd mu
        test_no_rebase_in_progress
        test_git_clean
        git reset --hard HEAD~1 || exit 1
    popd
}
test_clean_abort_rebase

test_clean_untracked_files() {
    print_single_separator
    echo "TEST: Clean untracked files"

    clowder link || exit 1
    clowder herd || exit 1

    pushd mu
        touch newfile
        mkdir something
        touch something/something
        mkdir something_else
        test_untracked_files
    popd

    clowder herd && exit 1
    clowder clean -d || exit 1

    pushd mu
        if [ -d 'something' ]; then
            exit 1
        fi
        if [ -f 'something/something' ]; then
            exit 1
        fi
        if [ -d 'something_else' ]; then
            exit 1
        fi
        if [ -f 'newfile' ]; then
            exit 1
        fi
    popd
}
test_clean_untracked_files
