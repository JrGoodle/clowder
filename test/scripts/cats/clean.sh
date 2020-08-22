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

export submodule_projects=( 'mu/ash' \
                            'mu/ash/duffy')

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh || exit 1
begin_command
$COMMAND herd $PARALLEL || exit 1
end_command

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

    begin_command
    $COMMAND clean 'black-cats' || exit 1
    end_command

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

    begin_command
    $COMMAND clean || exit 1
    end_command

    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_git_clean
        popd || exit 1
    done
}
test_clean_groups

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

    begin_command
    $COMMAND clean "$@" || exit 1
    end_command

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
    begin_command
    $COMMAND clean || exit 1
    end_command

    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_git_clean
        popd || exit 1
    done
}
test_clean_projects 'jrgoodle/duke' 'jrgoodle/mu'

test_clean_all() {
    print_single_separator
    make_dirty_repos "${all_projects[@]}"
    echo "TEST: Clean all when dirty"

    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_git_dirty
        popd || exit 1
    done

    begin_command
    $COMMAND clean || exit 1
    end_command

    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_git_clean
        popd || exit 1
    done

    echo "TEST: Clean when clean"
    begin_command
    $COMMAND clean || exit 1
    end_command

    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_git_clean
        popd || exit 1
    done
}
test_clean_all 'black-cats'

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
    begin_command
    $COMMAND clean || exit 1
    end_command

    for project in "${cats_projects[@]}"; do
        test_no_directory_exists "$project"
    done

    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_git_clean
        test_no_untracked_files
        popd || exit 1
    done

    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
}
test_clean_missing_directories 'mu' 'duke'

test_clean_abort_rebase() {
    print_single_separator
    echo "TEST: Clean when in the middle of a rebase"
    begin_command
    $COMMAND link || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command

    pushd mu || exit 1
        touch newfile
        echo 'something' > newfile
        echo "TEST: Create branch"
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

    begin_command
    $COMMAND clean || exit 1
    end_command

    pushd mu || exit 1
        test_no_rebase_in_progress
        test_git_clean
        git reset --hard HEAD~1 || exit 1
    popd || exit 1
}
test_clean_abort_rebase

test_clean_d() {
    print_single_separator
    echo "TEST: Clean untracked files and directories"

    begin_command
    $COMMAND link || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command

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

    begin_command
    $COMMAND herd && exit 1
    end_command
    begin_command
    $COMMAND clean || exit 1
    end_command

    pushd mu || exit 1
    test_directory_exists 'something'
    test_file_exists 'something/something'
    test_no_file_exists 'newfile'
    test_directory_exists 'something_else'
    test_untracked_files
    popd || exit 1

    begin_command
    $COMMAND clean -d || exit 1
    end_command

    pushd mu || exit 1
    test_no_directory_exists 'something'
    test_no_file_exists 'something/something'
    test_no_file_exists 'something_else'
    test_no_directory_exists 'something_else'
    test_no_untracked_files
    popd || exit 1
}
test_clean_d

test_clean_f() {
    print_single_separator
    echo "TEST: Clean git directories"

    begin_command
    $COMMAND link || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command

    pushd mu || exit 1
    git clone https://github.com/JrGoodle/cats.git
    test_directory_exists 'cats'
    popd || exit 1

    begin_command
    $COMMAND clean || exit 1
    end_command

    pushd mu || exit 1
    test_directory_exists 'cats'
    popd || exit 1

    begin_command
    $COMMAND clean -fd || exit 1
    end_command

    pushd mu || exit 1
    test_no_directory_exists 'cats'
    popd || exit 1
}
test_clean_f

test_clean_X() {
    print_single_separator
    echo "TEST: Clean only files ignored by git"
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command

    pushd mu || exit 1
    touch ignored_file
    touch something
    test_file_exists 'ignored_file'
    test_file_exists 'something'
    popd || exit 1

    begin_command
    $COMMAND clean -X || exit 1
    end_command

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
test_clean_X

test_clean_x() {
    print_single_separator
    echo "TEST: Clean all untracked files"
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command

    pushd mu || exit 1
    touch xcuserdata
    touch something
    test_file_exists 'xcuserdata'
    test_file_exists 'something'
    popd || exit 1

    begin_command
    $COMMAND clean -x || exit 1
    end_command

    pushd mu || exit 1
    test_no_file_exists 'xcuserdata'
    test_no_file_exists 'something'
    popd || exit 1
}
test_clean_x

test_clean_a() {
    print_single_separator
    echo "TEST: Clean all"
    begin_command
    $COMMAND link submodules || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    for project in "${submodule_projects[@]}"; do
        pushd $project || exit 1
        touch newfile
        mkdir something
        touch something/something
        echo "TEST: Create branch"
        git checkout -b something || exit 1
        git add newfile something || exit 1
        test_git_dirty
        test_branch something
        test_directory_exists 'something'
        test_file_exists 'something/something'
        test_file_exists 'newfile'
        popd || exit 1
    done
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        touch newfile
        mkdir something
        touch something/something
        test_directory_exists 'something'
        test_file_exists 'something/something'
        test_file_exists 'newfile'
        popd || exit 1
    done

    begin_command
    $COMMAND clean -a || exit 1
    end_command

    for project in "${submodule_projects[@]}"; do
        pushd $project || exit 1
        test_head_detached
        test_no_directory_exists 'something'
        test_no_file_exists 'something/something'
        test_no_file_exists 'newfile'
        git checkout master || exit 1
        echo "TEST: Delete branch"
        git branch -D something || exit 1
        popd || exit 1
    done
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_no_directory_exists 'something'
        test_no_file_exists 'something/something'
        test_no_file_exists 'newfile'
        popd || exit 1
    done
    begin_command
    $COMMAND link || exit 1
    end_command
}
test_clean_a

test_clean_submodules_untracked() {
    print_single_separator
    echo "TEST: Clean untracked files in submodules"
    begin_command
    $COMMAND link submodules || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    for project in "${submodule_projects[@]}"; do
        pushd $project || exit 1
        touch newfile
        mkdir something
        touch something/something
        test_directory_exists 'something'
        test_file_exists 'something/something'
        test_file_exists 'newfile'
        popd || exit 1
    done

    begin_command
    $COMMAND clean -r || exit 1
    end_command

    for project in "${submodule_projects[@]}"; do
        pushd $project || exit 1
        test_no_directory_exists 'something'
        test_no_file_exists 'something/something'
        test_no_file_exists 'newfile'
        popd || exit 1
    done

    clowder link || exit 1
}
test_clean_submodules_untracked

test_clean_submodules_dirty() {
    print_single_separator
    echo "TEST: Clean dirty submodules"
    begin_command
    $COMMAND link submodules || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    for project in "${submodule_projects[@]}"; do
        pushd $project || exit 1
        touch newfile
        mkdir something
        touch something/something
        echo "TEST: Create branch"
        git checkout -b something || exit 1
        git add newfile something || exit 1
        test_git_dirty
        test_branch something
        test_directory_exists 'something'
        test_file_exists 'something/something'
        test_file_exists 'newfile'
        popd || exit 1
    done

    begin_command
    $COMMAND clean -r || exit 1
    end_command

    for project in "${submodule_projects[@]}"; do
        pushd $project || exit 1
        test_head_detached
        test_no_directory_exists 'something'
        test_no_file_exists 'something/something'
        test_no_file_exists 'newfile'
        git checkout master || exit 1
        echo "TEST: Delete branch"
        git branch -D something || exit 1
        popd || exit 1
    done

    begin_command
    $COMMAND link || exit 1
    end_command
}
test_clean_submodules_dirty
