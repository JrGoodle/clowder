#!/usr/bin/env bash

# set -xv

# cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

# . test_utilities.sh

# export all_projects=( 'djinni' \
#                       'gyp' \
#                       'sox' )

# export master_projects=( 'djinni' \
#                          'sox' )

# if [ "$ACCESS_LEVEL" == "write" ]; then
#     print_double_separator
#     echo "TEST: Test clowder start/prune for forks"

#     cd "$MISC_EXAMPLE_DIR" || exit 1
#     ./clean.sh
#     ./init.sh || exit 1
#     begin_command
#     $COMMAND herd $PARALLEL || exit 1
#     end_command

    test_start_prune_forks() {
        print_single_separator
        echo "TEST: Test start prune upstream tracking branch"

        echo "TEST: No local or remote branches"
        begin_command
        $COMMAND prune -af tracking_branch || exit 1
        end_command

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_no_remote_branch_exists tracking_branch
            test_no_local_branch_exists tracking_branch
            popd || exit 1
        done

        begin_command
        $COMMAND start -t tracking_branch || exit 1
        end_command

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_branch tracking_branch
            test_remote_branch_exists tracking_branch
            test_tracking_branch_exists tracking_branch
            popd || exit 1
        done

        echo "TEST: Existing local branch checked out, remote tracking branch exists"
        begin_command
        $COMMAND prune -af tracking_branch || exit 1
        end_command

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_no_remote_branch_exists tracking_branch
            test_no_local_branch_exists tracking_branch
            popd || exit 1
        done

        begin_command
        $COMMAND start -t tracking_branch || exit 1
        end_command

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_branch tracking_branch
            test_remote_branch_exists tracking_branch
            test_tracking_branch_exists tracking_branch
            popd || exit 1
        done

        begin_command
        $COMMAND start -t tracking_branch || exit 1
        end_command

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_branch tracking_branch
            test_remote_branch_exists tracking_branch
            test_tracking_branch_exists tracking_branch
            popd || exit 1
        done

        echo "TEST: Existing local branch not checked out, remote tracking branch exists"
        begin_command
        $COMMAND prune -af tracking_branch || exit 1
        end_command
        begin_command
        $COMMAND start -t tracking_branch || exit 1
        end_command
        begin_command
        $COMMAND herd $PARALLEL || exit 1
        end_command

        pushd gyp || exit 1
        test_branch fork-branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd || exit 1
        for project in "${master_projects[@]}"; do
            pushd $project || exit 1
            test_branch 'master'
            test_remote_branch_exists tracking_branch
            test_tracking_branch_exists tracking_branch
            popd || exit 1
        done

        begin_command
        $COMMAND start -t tracking_branch || exit 1
        end_command

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_branch tracking_branch
            test_remote_branch_exists tracking_branch
            test_tracking_branch_exists tracking_branch
            popd || exit 1
        done

        echo "TEST: No local branch, existing remote branch"
        begin_command
        $COMMAND prune -af tracking_branch || exit 1
        end_command
        begin_command
        $COMMAND start -t tracking_branch || exit 1
        end_command
        begin_command
        $COMMAND prune -f tracking_branch || exit 1
        end_command

        pushd gyp || exit 1
        test_branch fork-branch
        test_remote_branch_exists tracking_branch
        test_no_local_branch_exists tracking_branch
        popd || exit 1
        for project in "${master_projects[@]}"; do
            pushd $project || exit 1
            test_branch 'master'
            test_remote_branch_exists tracking_branch
            test_no_local_branch_exists tracking_branch
            popd || exit 1
        done

        begin_command
        $COMMAND start -t tracking_branch && exit 1
        end_command

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_remote_branch_exists tracking_branch
            test_no_tracking_branch_exists tracking_branch
            popd || exit 1
        done

        echo "TEST: Existing local branch checked out, existing remote branch, no tracking relationship"
        begin_command
        $COMMAND prune -af tracking_branch || exit 1
        end_command
        begin_command
        $COMMAND start -t tracking_branch || exit 1
        end_command
        begin_command
        $COMMAND prune -f tracking_branch || exit 1
        end_command
        begin_command
        $COMMAND forall $PARALLEL -c 'git checkout -b tracking_branch' || exit 1
        end_command

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_branch tracking_branch
            test_remote_branch_exists tracking_branch
            test_no_tracking_branch_exists tracking_branch
            popd || exit 1
        done
        begin_command
        $COMMAND start -t tracking_branch && exit 1
        end_command
        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_branch tracking_branch
            test_remote_branch_exists tracking_branch
            test_no_tracking_branch_exists tracking_branch
            popd || exit 1
        done

        echo "TEST: Existing local branch not checked out, existing remote branch, no tracking relationship"
        begin_command
        $COMMAND prune -af tracking_branch || exit 1
        end_command
        begin_command
        $COMMAND start -t tracking_branch || exit 1
        end_command
        begin_command
        $COMMAND prune -f tracking_branch || exit 1
        end_command
        begin_command
        $COMMAND forall $PARALLEL -c 'git checkout -b tracking_branch' || exit 1
        end_command
        begin_command
        $COMMAND herd $PARALLEL || exit 1
        end_command

        pushd gyp || exit 1
        test_branch fork-branch
        test_local_branch_exists tracking_branch
        test_remote_branch_exists tracking_branch
        test_no_tracking_branch_exists tracking_branch
        popd || exit 1
        for project in "${master_projects[@]}"; do
            pushd $project || exit 1
            test_branch 'master'
            test_local_branch_exists tracking_branch
            test_remote_branch_exists tracking_branch
            test_no_tracking_branch_exists tracking_branch
            popd || exit 1
        done
        begin_command
        $COMMAND start -t tracking_branch && exit 1
        end_command
        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_local_branch_exists tracking_branch
            test_remote_branch_exists tracking_branch
            test_no_tracking_branch_exists tracking_branch
            popd || exit 1
        done

        echo "TEST: Existing local branch checked out, no remote branch"
        begin_command
        $COMMAND prune -af tracking_branch || exit 1
        end_command
        begin_command
        $COMMAND start tracking_branch || exit 1
        end_command

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_branch tracking_branch
            test_local_branch_exists tracking_branch
            test_no_remote_branch_exists tracking_branch
            popd || exit 1
        done

        begin_command
        $COMMAND start -t tracking_branch || exit 1
        end_command

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_branch tracking_branch
            test_remote_branch_exists tracking_branch
            test_tracking_branch_exists tracking_branch
            popd || exit 1
        done

        echo "TEST: Existing local branch not checked out, no remote branch"
        begin_command
        $COMMAND prune -r tracking_branch || exit 1
        end_command
        begin_command
        $COMMAND start tracking_branch || exit 1
        end_command
        begin_command
        $COMMAND herd $PARALLEL || exit 1
        end_command

        pushd gyp || exit 1
        test_branch fork-branch
        test_local_branch_exists tracking_branch
        test_no_remote_branch_exists tracking_branch
        popd || exit 1
        for project in "${master_projects[@]}"; do
            pushd $project || exit 1
            test_branch 'master'
            test_local_branch_exists tracking_branch
            test_no_remote_branch_exists tracking_branch
            popd || exit 1
        done

        begin_command
        $COMMAND start -t tracking_branch || exit 1
        end_command

        for project in "${all_projects[@]}"; do
            pushd $project || exit 1
            test_branch tracking_branch
            test_remote_branch_exists tracking_branch
            test_tracking_branch_exists tracking_branch
            popd || exit 1
        done
    }
    test_start_prune_forks
fi

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

#     begin_command
#     $COMMAND link || exit 1
#     end_command
# }
# test_clean_submodules_dirty
