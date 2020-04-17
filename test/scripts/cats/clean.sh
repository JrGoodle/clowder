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

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh
$COMMAND herd $PARALLEL || exit 1

print_double_separator
echo "TEST: Test clowder clean"

test_clean_groups() {
    print_single_separator
    make_dirty_repos "${all_projects[@]}"
    echo "TEST: Clean specific group when dirty"

    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_git_dirty
        popd || exit 1
    done

    $COMMAND clean -g 'black-cats' || exit 1

    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_git_clean
        popd || exit 1
    done
    pushd mu || exit 1
    test_git_dirty
    popd || exit 1
    pushd duke || exit 1
    test_git_dirty
    popd || exit 1

    make_dirty_repos "${black_cats_projects[@]}"

    echo "TEST: Clean all when dirty"

    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_git_dirty
        popd || exit 1
    done

    $COMMAND clean || exit 1

    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_git_clean
        popd || exit 1
    done
}

test_clean_projects() {
    print_single_separator
    echo "TEST: Clean projects"
    make_dirty_repos "${all_projects[@]}"
    echo "TEST: Clean specific project when dirty"

    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_git_dirty
        popd || exit 1
    done

    $COMMAND clean -p "$@" || exit 1

    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_git_dirty
        popd || exit 1
    done
    pushd mu || exit 1
    test_git_clean
    popd || exit 1
    pushd duke || exit 1
    test_git_clean
    popd || exit 1

    echo "TEST: Clean all when dirty"
    $COMMAND clean || exit 1

    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_git_clean
        popd || exit 1
    done
}

test_clean_all() {
    print_single_separator
    make_dirty_repos "${all_projects[@]}"
    echo "TEST: Clean all when dirty"

    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_git_dirty
        popd || exit 1
    done

    $COMMAND clean || exit 1

    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_git_clean
        popd || exit 1
    done

    echo "TEST: Clean when clean"
    $COMMAND clean || exit 1

    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_git_clean
        popd || exit 1
    done
}

test_clean_missing_directories() {
    print_single_separator
    make_dirty_repos "${all_projects[@]}"
    rm -rf "$@"

    for project in "${cats_projects[@]}"; do
        test_no_directory_exists "$project"
    done

    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_git_dirty
        popd || exit 1
    done

    echo "TEST: Clean when directories are missing"
    $COMMAND clean || exit 1

    for project in "${cats_projects[@]}"; do
        test_no_directory_exists "$project"
    done

    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_git_clean
        test_no_untracked_files
        popd || exit 1
    done

    $COMMAND herd $PARALLEL || exit 1
}

test_clean_abort_rebase() {
    print_single_separator
    echo "TEST: Clean when in the middle of a rebase"

    $COMMAND link || exit 1
    $COMMAND herd $PARALLEL || exit 1

    pushd mu || exit 1
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
    popd || exit 1

    $COMMAND clean || exit 1

    pushd mu || exit 1
        test_no_rebase_in_progress
        test_git_clean
        git reset --hard HEAD~1 || exit 1
    popd || exit 1
}

test_clean_d() {
    print_single_separator
    echo "TEST: Clean untracked files and directories"

    $COMMAND link || exit 1
    $COMMAND herd $PARALLEL || exit 1

    pushd mu || exit 1
    touch newfile
    mkdir something
    touch something/something
    mkdir something_else
    test_directory_exists 'something'
    test_file_exists 'something/something'
    test_file_exists 'newfile'
    test_directory_exists 'something_else'
    test_untracked_files
    popd || exit 1

    $COMMAND herd && exit 1
    $COMMAND clean || exit 1

    pushd mu || exit 1
    test_directory_exists 'something'
    test_file_exists 'something/something'
    test_no_file_exists 'newfile'
    test_directory_exists 'something_else'
    test_untracked_files
    popd || exit 1

    $COMMAND clean -d || exit 1

    pushd mu || exit 1
    test_no_directory_exists 'something'
    test_no_file_exists 'something/something'
    test_no_file_exists 'something_else'
    test_no_directory_exists 'something_else'
    test_no_untracked_files
    popd || exit 1
}

test_clean_f() {
    print_single_separator
    echo "TEST: Clean git directories"

    $COMMAND link || exit 1
    $COMMAND herd $PARALLEL || exit 1

    pushd mu || exit 1
    git clone https://github.com/JrGoodle/cats.git
    test_directory_exists 'cats'
    popd || exit 1

    $COMMAND clean || exit 1

    pushd mu || exit 1
    test_directory_exists 'cats'
    popd || exit 1

    $COMMAND clean -fd || exit 1

    pushd mu || exit 1
    test_no_directory_exists 'cats'
    popd || exit 1
}

test_clean_X() {
    print_single_separator
    echo "TEST: Clean only files ignored by git"
    $COMMAND herd $PARALLEL || exit 1

    pushd mu || exit 1
    touch ignored_file
    touch something
    test_file_exists 'ignored_file'
    test_file_exists 'something'
    popd || exit 1

    $COMMAND clean -X || exit 1

    pushd mu || exit 1
    test_no_file_exists 'ignored_file'
    test_file_exists 'something'
    popd || exit 1

    pushd mu || exit 1
    rm -f something
    test_no_file_exists 'ignored_file'
    test_no_file_exists 'something'
    popd || exit 1
}

test_clean_x() {
    print_single_separator
    echo "TEST: Clean all untracked files"
    $COMMAND herd $PARALLEL || exit 1

    pushd mu || exit 1
    touch xcuserdata
    touch something
    test_file_exists 'xcuserdata'
    test_file_exists 'something'
    popd || exit 1

    $COMMAND clean -x || exit 1

    pushd mu || exit 1
    test_no_file_exists 'xcuserdata'
    test_no_file_exists 'something'
    popd || exit 1
}

test_clean_groups
test_clean_projects 'jrgoodle/duke' 'jrgoodle/mu'
test_clean_all 'black-cats'
test_clean_missing_directories 'mu' 'duke'
test_clean_abort_rebase
test_clean_d
test_clean_f
test_clean_X
test_clean_x
