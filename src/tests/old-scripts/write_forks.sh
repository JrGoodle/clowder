#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

export all_projects=( 'djinni' \
                      'gyp' \
                      'sox' )

export master_projects=( 'djinni' \
                         'sox' )

if [ "$ACCESS_LEVEL" == "write" ]; then
    print_double_separator
    echo "TEST: Test clowder start/prune for forks"

    cd "$MISC_EXAMPLE_DIR" || exit 1
    ./clean.sh
    ./init.sh || exit 1
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command

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
