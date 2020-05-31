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
echo "TEST: Test clowder commands with various states of clowder repo dir and clowder yaml file"

cd "$CATS_EXAMPLE_DIR" || exit 1

test_commands_with_yaml_file_no_clowder_repo() {
    print_single_separator
    echo "TEST: Run commands with clowder.yaml file that is not a symlink and no existing .clowder directory"
    ./clean.sh
    ./init.sh || exit 1
    rm -f clowder.yaml || exit 1
    cp .clowder/clowder.yaml clowder.yaml || exit 1
    rm -rf .clowder || exit
    test_file_exists 'clowder.yaml'
    test_file_not_symlink 'clowder.yaml'
    test_no_directory_exists '.clowder'

    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_cats_default_herd_branches
    begin_command
    $COMMAND status || exit 1
    end_command
    begin_command
    $COMMAND branch || exit 1
    end_command
    begin_command
    $COMMAND checkout master || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_cats_default_herd_branches
    pushd 'mu' || exit 1
    touch 'new-file' || exit 1
    git add . || exit 1
    popd || exit 1
    pushd 'duke' || exit 1
    touch 'new-file' || exit 1
    git add . || exit 1
    popd || exit 1
    begin_command
    $COMMAND herd $PARALLEL && exit 1
    end_command
    begin_command
    $COMMAND clean || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_cats_default_herd_branches
    begin_command
    $COMMAND diff || exit 1
    end_command
    begin_command
    $COMMAND forall -c 'git checkout -b new-branch' || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_branch 'new-branch'
        popd || exit 1
    done
    begin_command
    $COMMAND prune 'new-branch' || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_no_local_branch_exists 'new-branch'
        popd || exit 1
    done
    test_cats_default_herd_branches
    begin_command
    $COMMAND start 'new-branch' || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_branch 'new-branch'
        popd || exit 1
    done
    begin_command
    $COMMAND reset || exit 1
    end_command
    test_cats_default_herd_branches
    begin_command
    $COMMAND repo add 'file' && exit 1
    end_command
    begin_command
    $COMMAND repo checkout 'new-branch' && exit 1
    end_command
    begin_command
    $COMMAND repo clean && exit 1
    end_command
    begin_command
    $COMMAND repo commit 'message' && exit 1
    end_command
    begin_command
    $COMMAND repo pull && exit 1
    end_command
    begin_command
    $COMMAND repo push && exit 1
    end_command
    begin_command
    $COMMAND repo run && exit 1
    end_command
    begin_command
    $COMMAND repo status && exit 1
    end_command
    pushd 'mu' || exit 1
    touch 'new-file' || exit 1
    git add . || exit 1
    popd || exit 1
    pushd 'duke' || exit 1
    touch 'new-file' || exit 1
    git add . || exit 1
    popd || exit 1
    begin_command
    $COMMAND herd $PARALLEL && exit 1
    end_command
    begin_command
    $COMMAND stash || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    begin_command
    $COMMAND status || exit 1
    end_command
    begin_command
    $COMMAND yaml || exit 1
    end_command
    begin_command
    $COMMAND yaml -r || exit 1
    end_command

    # TODO: Test more commands in subdirectory
    pushd 'mu' || exit 1
    begin_command
    $COMMAND status || exit 1
    end_command
    # !! Move coverage files to root and clean so further commands work
    cp -a .coverage* ../
    rm -rf .coverage*
    # !!
    popd || exit 1

    begin_command
    $COMMAND link && exit 1
    end_command
    begin_command
    $COMMAND save 'new-version' && exit 1
    end_command
}
test_commands_with_yaml_file_no_clowder_repo

test_commands_with_yaml_file_clowder_repo_missing_git_dir() {
    print_single_separator
    echo "TEST: Run commands with clowder.yaml file that is not a symlink and existing .clowder directory which is not a git repository"
    ./clean.sh
    ./init.sh || exit 1
    rm -f clowder.yaml || exit 1
    cp .clowder/clowder.yaml clowder.yaml || exit 1
    rm -rf .clowder/.git || exit 1
    test_file_not_symlink 'clowder.yaml'
    test_directory_exists '.clowder'
    test_no_directory_exists '.clowder/.git'

    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_cats_default_herd_branches
    begin_command
    $COMMAND status || exit 1
    end_command
    begin_command
    $COMMAND branch || exit 1
    end_command
    begin_command
    $COMMAND checkout master || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_cats_default_herd_branches
    pushd 'mu' || exit 1
    touch 'new-file' || exit 1
    git add . || exit 1
    popd || exit 1
    pushd 'duke' || exit 1
    touch 'new-file' || exit 1
    git add . || exit 1
    popd || exit 1
    begin_command
    $COMMAND herd $PARALLEL && exit 1
    end_command
    begin_command
    $COMMAND clean || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_cats_default_herd_branches
    begin_command
    $COMMAND diff || exit 1
    end_command
    begin_command
    $COMMAND forall -c 'git checkout -b new-branch' || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_branch 'new-branch'
        popd || exit 1
    done
    begin_command
    $COMMAND prune 'new-branch' || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_no_local_branch_exists 'new-branch'
        popd || exit 1
    done
    test_cats_default_herd_branches
    begin_command
    $COMMAND start 'new-branch' || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_branch 'new-branch'
        popd || exit 1
    done
    begin_command
    $COMMAND reset || exit 1
    end_command
    test_cats_default_herd_branches
    begin_command
    $COMMAND repo add 'file' && exit 1
    end_command
    begin_command
    $COMMAND repo checkout 'new-branch' && exit 1
    end_command
    begin_command
    $COMMAND repo clean && exit 1
    end_command
    begin_command
    $COMMAND repo commit 'message' && exit 1
    end_command
    begin_command
    $COMMAND repo pull && exit 1
    end_command
    begin_command
    $COMMAND repo push && exit 1
    end_command
    begin_command
    $COMMAND repo run 'touch newfile' || exit 1
    end_command
    pushd '.clowder' || exit 1
    test_file_exists 'newfile'
    popd || exit 1
    begin_command
    $COMMAND repo status || exit 1
    end_command
    pushd 'mu' || exit 1
    touch 'new-file' || exit 1
    git add . || exit 1
    popd || exit 1
    pushd 'duke' || exit 1
    touch 'new-file' || exit 1
    git add . || exit 1
    popd || exit 1
    begin_command
    $COMMAND herd $PARALLEL && exit 1
    end_command
    begin_command
    $COMMAND stash || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    begin_command
    $COMMAND status || exit 1
    end_command
    begin_command
    $COMMAND yaml || exit 1
    end_command
    begin_command
    $COMMAND yaml -r || exit 1
    end_command

    # TODO: Test more commands in subdirectory
    pushd 'mu' || exit 1
    begin_command
    $COMMAND status || exit 1
    end_command
    # !! Move coverage files to root and clean so further commands work
    cp -a .coverage* ../
    rm -rf .coverage*
    # !!
    popd || exit 1

    test_file_exists 'clowder.yaml'
    test_file_not_symlink 'clowder.yaml'
    test_file_exists '.clowder/clowder.yaml'
    test_no_file_exists 'clowder.yml'
    begin_command
    $COMMAND link && exit 1
    end_command
    test_file_exists 'clowder.yaml'
    test_file_not_symlink 'clowder.yaml'
    test_no_file_exists '.clowder/versions/new-version.clowder.yml'
    test_no_file_exists 'clowder.yml'
    begin_command
    $COMMAND save new-version || exit 1
    end_command
    test_file_exists '.clowder/versions/new-version.clowder.yml'
    test_file_exists 'clowder.yaml'
    test_file_not_symlink 'clowder.yaml'
    test_no_file_exists 'clowder.yml'
    begin_command
    $COMMAND link new-version && exit 1
    end_command
    test_file_exists 'clowder.yaml'
    test_file_not_symlink 'clowder.yaml'
    test_no_file_exists 'clowder.yml'
}
test_commands_with_yaml_file_clowder_repo_missing_git_dir

test_commands_with_yaml_file_clowder_repo_git_dir() {
    print_single_separator
    echo "TEST: Run commands with clowder.yaml file that is not a symlink and existing .clowder directory which is a git repository"
    ./clean.sh
    ./init.sh || exit 1
    rm -f clowder.yaml || exit 1
    cp .clowder/clowder.yaml clowder.yaml || exit 1
    test_file_not_symlink 'clowder.yaml'
    test_directory_exists '.clowder'
    test_directory_exists '.clowder/.git'

    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_cats_default_herd_branches
    begin_command
    $COMMAND status || exit 1
    end_command
    begin_command
    $COMMAND branch || exit 1
    end_command
    begin_command
    $COMMAND checkout master || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_cats_default_herd_branches
    pushd 'mu' || exit 1
    touch 'new-file' || exit 1
    git add . || exit 1
    popd || exit 1
    pushd 'duke' || exit 1
    touch 'new-file' || exit 1
    git add . || exit 1
    popd || exit 1
    begin_command
    $COMMAND herd $PARALLEL && exit 1
    end_command
    begin_command
    $COMMAND clean || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_cats_default_herd_branches
    begin_command
    $COMMAND diff || exit 1
    end_command
    begin_command
    $COMMAND forall -c 'git checkout -b new-branch' || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_branch 'new-branch'
        popd || exit 1
    done
    begin_command
    $COMMAND prune 'new-branch' || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_no_local_branch_exists 'new-branch'
        popd || exit 1
    done
    test_cats_default_herd_branches
    begin_command
    $COMMAND start 'new-branch' || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_branch 'new-branch'
        popd || exit 1
    done
    begin_command
    $COMMAND reset || exit 1
    end_command
    test_cats_default_herd_branches
    pushd '.clowder' || exit 1
    test_git_clean
    touch 'new-file' || exit 1
    test_file_exists 'new-file'
    popd || exit 1
    begin_command
    $COMMAND repo add 'new-file' || exit 1
    end_command
    pushd '.clowder' || exit 1
    test_git_dirty
    popd || exit 1
    begin_command
    $COMMAND repo clean || exit 1
    end_command
    pushd '.clowder' || exit 1
    test_git_clean
    test_no_file_exists 'new-file'
    popd || exit 1
    begin_command
    $COMMAND repo run 'git branch new-branch' || exit 1
    end_command
    pushd '.clowder' || exit 1
    test_branch 'master'
    test_local_branch_exists 'new-branch'
    popd || exit 1
    begin_command
    $COMMAND repo checkout 'new-branch' || exit 1
    end_command
    pushd '.clowder' || exit 1
    test_branch 'new-branch'
    popd || exit 1
    pushd '.clowder' || exit 1
    test_git_clean
    touch 'new-file' || exit 1
    test_file_exists 'new-file'
    popd || exit 1
    begin_command
    $COMMAND repo add 'new-file' || exit 1
    end_command
    pushd '.clowder' || exit 1
    test_git_dirty
    popd || exit 1
    begin_command
    $COMMAND repo commit 'new-message' || exit 1
    end_command
    pushd '.clowder' || exit 1
    test_commit_messages "$(git log --format=%B -n 1 HEAD)" 'new-message'
    test_git_clean
    popd || exit 1
    #TODO: Set back commit and check after pull that it was updated
    begin_command
    $COMMAND repo checkout master || exit 1
    end_command
    begin_command
    $COMMAND repo pull || exit 1
    end_command
    # TODO: Add this to write tests
    # begin_command
    # $COMMAND repo push && exit 1
    # end_command
    begin_command
    $COMMAND repo run 'touch newfile' || exit 1
    end_command
    test_file_exists '.clowder/newfile'
    begin_command
    $COMMAND repo status || exit 1
    end_command
    pushd 'mu' || exit 1
    touch 'new-file' || exit 1
    git add . || exit 1
    popd || exit 1
    pushd 'duke' || exit 1
    touch 'new-file' || exit 1
    git add . || exit 1
    popd || exit 1
    begin_command
    $COMMAND herd $PARALLEL && exit 1
    end_command
    begin_command
    $COMMAND stash || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    begin_command
    $COMMAND status || exit 1
    end_command
    begin_command
    $COMMAND yaml || exit 1
    end_command
    begin_command
    $COMMAND yaml -r || exit 1
    end_command

    # TODO: Test more commands in subdirectory
    pushd 'mu' || exit 1
    begin_command
    $COMMAND status || exit 1
    end_command
    # !! Move coverage files to root and clean so further commands work
    cp -a .coverage* ../
    rm -rf .coverage*
    # !!
    popd || exit 1

    test_file_exists 'clowder.yaml'
    test_file_not_symlink 'clowder.yaml'
    test_file_exists '.clowder/clowder.yaml'
    begin_command
    $COMMAND link && exit 1
    end_command
    test_file_exists 'clowder.yaml'
    test_file_not_symlink 'clowder.yaml'
    test_no_file_exists '.clowder/versions/new-version.clowder.yml'
    test_no_file_exists 'clowder.yml'
    begin_command
    $COMMAND save new-version || exit 1
    end_command
    test_file_exists '.clowder/versions/new-version.clowder.yml'
    test_file_exists 'clowder.yaml'
    test_file_not_symlink 'clowder.yaml'
    test_no_file_exists 'clowder.yml'
    begin_command
    $COMMAND link new-version && exit 1
    end_command
    test_file_exists 'clowder.yaml'
    test_file_not_symlink 'clowder.yaml'
    test_no_file_exists 'clowder.yml'
}
test_commands_with_yaml_file_clowder_repo_git_dir

test_commands_with_yaml_symlink_clowder_repo_missing_git_dir() {
    print_single_separator
    echo "TEST: Run commands with clowder.yaml symlink and existing .clowder directory which is not a git repository"
    ./clean.sh
    ./init.sh || exit 1
    rm -rf .clowder/.git || exit 1
    test_file_is_symlink 'clowder.yaml'
    test_symlink_path 'clowder.yaml' "$(pwd)/.clowder/clowder.yaml"
    test_directory_exists '.clowder'
    test_no_directory_exists '.clowder/.git'

    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_cats_default_herd_branches
    begin_command
    $COMMAND status || exit 1
    end_command
    begin_command
    $COMMAND branch || exit 1
    end_command
    begin_command
    $COMMAND checkout master || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_cats_default_herd_branches
    pushd 'mu' || exit 1
    touch 'new-file' || exit 1
    git add . || exit 1
    popd || exit 1
    pushd 'duke' || exit 1
    touch 'new-file' || exit 1
    git add . || exit 1
    popd || exit 1
    begin_command
    $COMMAND herd $PARALLEL && exit 1
    end_command
    begin_command
    $COMMAND clean || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_cats_default_herd_branches
    begin_command
    $COMMAND diff || exit 1
    end_command
    begin_command
    $COMMAND forall -c 'git checkout -b new-branch' || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_branch 'new-branch'
        popd || exit 1
    done
    begin_command
    $COMMAND prune 'new-branch' || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_no_local_branch_exists 'new-branch'
        popd || exit 1
    done
    test_cats_default_herd_branches
    begin_command
    $COMMAND start 'new-branch' || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_branch 'new-branch'
        popd || exit 1
    done
    begin_command
    $COMMAND reset || exit 1
    end_command
    test_cats_default_herd_branches
    begin_command
    $COMMAND repo add 'file' && exit 1
    end_command
    begin_command
    $COMMAND repo checkout 'new-branch' && exit 1
    end_command
    begin_command
    $COMMAND repo clean && exit 1
    end_command
    begin_command
    $COMMAND repo commit 'message' && exit 1
    end_command
    begin_command
    $COMMAND repo pull && exit 1
    end_command
    begin_command
    $COMMAND repo push && exit 1
    end_command
    begin_command
    $COMMAND repo run 'touch newfile' || exit 1
    end_command
    pushd '.clowder' || exit 1
    test_file_exists 'newfile'
    popd || exit 1
    begin_command
    $COMMAND repo status || exit 1
    end_command

    pushd 'mu' || exit 1
    touch 'new-file' || exit 1
    git add . || exit 1
    popd || exit 1
    pushd 'duke' || exit 1
    touch 'new-file' || exit 1
    git add . || exit 1
    popd || exit 1
    begin_command
    $COMMAND herd $PARALLEL && exit 1
    end_command

    begin_command
    $COMMAND stash || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    begin_command
    $COMMAND status || exit 1
    end_command
    begin_command
    $COMMAND yaml || exit 1
    end_command
    begin_command
    $COMMAND yaml -r || exit 1
    end_command

    # TODO: Test more commands in subdirectory
    pushd 'mu' || exit 1
    begin_command
    $COMMAND status || exit 1
    end_command
    # !! Move coverage files to root and clean so further commands work
    cp -a .coverage* ../
    rm -rf .coverage*
    # !!
    popd || exit 1

    test_file_exists 'clowder.yaml'
    test_file_is_symlink 'clowder.yaml'
    test_symlink_path 'clowder.yaml' "$(pwd)/.clowder/clowder.yaml"
    test_no_file_exists 'clowder.yml'
    test_no_file_exists '.clowder/versions/new-version.clowder.yml'
    begin_command
    $COMMAND save new-version || exit 1
    end_command
    test_file_exists '.clowder/versions/new-version.clowder.yml'
    test_file_exists 'clowder.yaml'
    test_file_is_symlink 'clowder.yaml'
    test_symlink_path 'clowder.yaml' "$(pwd)/.clowder/clowder.yaml"
    test_no_file_exists 'clowder.yml'
    begin_command
    $COMMAND link new-version || exit 1
    end_command
    test_file_exists 'clowder.yml'
    test_file_is_symlink 'clowder.yml'
    test_symlink_path 'clowder.yml' "$(pwd)/.clowder/versions/new-version.clowder.yml"
    test_no_file_exists 'clowder.yaml'
}
test_commands_with_yaml_symlink_clowder_repo_missing_git_dir

# TODO: Add test for non-symlink clowder.yaml file and empty .clowder dir
