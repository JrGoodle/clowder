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
echo "TEST: Test clowder herd"

cd "$CATS_EXAMPLE_DIR" || exit 1

sudo git lfs uninstall --system --skip-repo || exit 1

./clean.sh
./init.sh

test_install_lfs_project_new_repo() {
    print_single_separator
    echo "TEST: Install lfs project new repo"
    git lfs uninstall --skip-repo || exit 1
    test_git_lfs_filters_not_installed

    begin_command
    $COMMAND link lfs-true || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_git_lfs_filters_installed
    pushd mu || exit 1
    test_git_lfs_hooks_installed
    test_file_exists 'jrgoodle.png'
    popd || exit 1
    pushd duke || exit 1
    test_git_lfs_hooks_not_installed
    popd || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_git_lfs_hooks_not_installed
        popd || exit 1
    done
}
test_install_lfs_project_new_repo

./clean.sh
./init.sh

test_install_lfs_project_existing_repo_explicit() {
    print_single_separator
    echo "TEST: Install lfs project existing repo explicit"
    git lfs uninstall --skip-repo || exit 1
    test_git_lfs_filters_not_installed

    begin_command
    $COMMAND link lfs-false || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_git_lfs_filters_not_installed
    pushd mu || exit 1
    test_git_lfs_hooks_not_installed
    test_file_exists 'jrgoodle.png'
    test_file_is_lfs_pointer 'jrgoodle.png'
    popd || exit 1
    pushd duke || exit 1
    test_git_lfs_hooks_not_installed
    popd || exit 1

    begin_command
    $COMMAND link lfs-true || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_git_lfs_filters_installed
    pushd mu || exit 1
    test_git_lfs_hooks_installed
    test_file_exists 'jrgoodle.png'
    test_file_is_not_lfs_pointer 'jrgoodle.png'
    popd || exit 1
    pushd duke || exit 1
    test_git_lfs_hooks_not_installed
    popd || exit 1
}
test_install_lfs_project_existing_repo_explicit

./clean.sh
./init.sh

test_install_lfs_project_existing_repo_implicit() {
    print_single_separator
    echo "TEST: Install lfs project existing repo implicit"
    git lfs uninstall --skip-repo || exit 1
    test_git_lfs_filters_not_installed

    begin_command
    $COMMAND link lfs-false-implicit || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_git_lfs_filters_not_installed
    pushd mu || exit 1
    test_git_lfs_hooks_not_installed
    test_file_exists 'jrgoodle.png'
    test_file_is_lfs_pointer 'jrgoodle.png'
    popd || exit 1
    pushd duke || exit 1
    test_git_lfs_hooks_not_installed
    popd || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_git_lfs_hooks_not_installed
        popd || exit 1
    done

    begin_command
    $COMMAND link lfs-true || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_git_lfs_filters_installed
    pushd mu || exit 1
    test_git_lfs_hooks_installed
    test_file_exists 'jrgoodle.png'
    test_file_is_not_lfs_pointer 'jrgoodle.png'
    popd || exit 1
    pushd duke || exit 1
    test_git_lfs_hooks_not_installed
    popd || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_git_lfs_hooks_not_installed
        popd || exit 1
    done
}
test_install_lfs_project_existing_repo_implicit

./clean.sh
./init.sh

test_install_lfs_defaults_new_repo() {
    print_single_separator
    echo "TEST: Install lfs defaults new repo"
    git lfs uninstall --skip-repo || exit 1
    test_git_lfs_filters_not_installed

    begin_command
    $COMMAND link lfs-true-defaults || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_git_lfs_filters_installed
    pushd mu || exit 1
    test_git_lfs_hooks_installed
    test_file_exists 'jrgoodle.png'
    test_file_is_not_lfs_pointer 'jrgoodle.png'
    popd || exit 1
    pushd duke || exit 1
    test_git_lfs_hooks_installed
    popd || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_git_lfs_hooks_installed
        popd || exit 1
    done
}
test_install_lfs_defaults_new_repo

./clean.sh
./init.sh

test_install_lfs_defaults_existing_repo_explicit() {
    print_single_separator
    echo "TEST: Install lfs defaults existing repo explicit"
    git lfs uninstall --skip-repo || exit 1
    test_git_lfs_filters_not_installed

    begin_command
    $COMMAND link lfs-false || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_git_lfs_filters_not_installed
    pushd mu || exit 1
    test_git_lfs_hooks_not_installed
    test_file_exists 'jrgoodle.png'
    test_file_is_lfs_pointer 'jrgoodle.png'
    popd || exit 1
    pushd duke || exit 1
    test_git_lfs_hooks_not_installed
    popd || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_git_lfs_hooks_not_installed
        popd || exit 1
    done

    begin_command
    $COMMAND link lfs-true-defaults || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_git_lfs_filters_installed
    pushd mu || exit 1
    test_git_lfs_hooks_installed
    test_file_exists 'jrgoodle.png'
    test_file_is_not_lfs_pointer 'jrgoodle.png'
    popd || exit 1
    pushd duke || exit 1
    test_git_lfs_hooks_installed
    popd || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_git_lfs_hooks_installed
        popd || exit 1
    done
}
test_install_lfs_defaults_existing_repo_explicit

./clean.sh
./init.sh

test_install_lfs_defaults_existing_repo_implicit() {
    print_single_separator
    echo "TEST: Install lfs defaults existing repo implicit"
    git lfs uninstall --skip-repo || exit 1
    test_git_lfs_filters_not_installed

    begin_command
    $COMMAND link lfs-false-implicit || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_git_lfs_filters_not_installed
    pushd mu || exit 1
    test_git_lfs_hooks_not_installed
    test_file_exists 'jrgoodle.png'
    test_file_is_lfs_pointer 'jrgoodle.png'
    popd || exit 1
    pushd duke || exit 1
    test_git_lfs_hooks_not_installed
    popd || exit 1

    begin_command
    $COMMAND link lfs-true-defaults || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_git_lfs_filters_installed
    pushd mu || exit 1
    test_git_lfs_hooks_installed
    test_file_exists 'jrgoodle.png'
    test_file_is_not_lfs_pointer 'jrgoodle.png'
    popd || exit 1
    pushd duke || exit 1
    test_git_lfs_hooks_installed
    popd || exit 1
        for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_git_lfs_hooks_installed
        popd || exit 1
    done
}
test_install_lfs_defaults_existing_repo_implicit
