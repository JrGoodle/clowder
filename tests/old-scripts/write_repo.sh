#!/usr/bin/env bash

# cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

# . test_utilities.sh

# if [ "$ACCESS_LEVEL" == "write" ]; then
#     print_double_separator
#     echo "TEST: Test clowder repo write"

#     cd "$CATS_EXAMPLE_DIR" || exit 1
#     ./clean.sh
#     ./init.sh || exit 1
#     begin_command
#     $COMMAND link ssh || exit 1
#     end_command

    begin_command
    $COMMAND repo checkout repo-test || exit 1
    end_command
    pushd .clowder || exit 1
    test_branch repo-test
    popd || exit 1
    begin_command
    $COMMAND link ssh || exit 1
    end_command

    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command

    test_clowder_repo_commit_pull_push() {
        print_single_separator
        echo "TEST: Test clowder repo commit, clowder repo pull, clowder repo push commands"
        begin_command
        $COMMAND repo checkout repo-test || exit 1
        end_command
        pushd .clowder || exit 1
        local original_commit
        original_commit="$(git rev-parse HEAD)"
        test_branch repo-test
        popd || exit 1
        begin_command
        $COMMAND repo run 'touch newfile' || exit 1
        end_command
        begin_command
        $COMMAND repo add 'newfile' || exit 1
        end_command
        begin_command
        $COMMAND repo commit 'Add newfile for clowder repo test' || exit 1
        end_command
        pushd .clowder || exit 1
        local new_commit
        new_commit="$(git rev-parse HEAD)"
        popd || exit 1
        if [ "$original_commit" == "$new_commit" ]; then
            exit 1
        fi
        begin_command
        $COMMAND repo push || exit 1
        end_command
        begin_command
        $COMMAND repo run 'git reset --hard HEAD~1' || exit 1
        end_command
        pushd .clowder || exit 1
        test_commit "$original_commit"
        popd || exit 1
        begin_command
        $COMMAND repo pull || exit 1
        end_command
        pushd .clowder || exit 1
        test_commit "$new_commit"
        popd || exit 1
        begin_command
        $COMMAND repo run 'git reset --hard HEAD~1' || exit 1
        end_command
        begin_command
        $COMMAND repo run 'git push origin repo-test --force' || exit 1
        end_command
        begin_command
        $COMMAND repo checkout master || exit 1
        end_command
        pushd .clowder || exit 1
        test_branch master || exit 1
        popd || exit 1
    }
    test_clowder_repo_commit_pull_push
# fi

# TODO: Adapt these tests along with the write ones
# echo 'TEST: clowder repo add'
# begin_command
# $COMMAND repo add . || enable_connection_exit
# end_command
# print_single_separator
# echo 'TEST: clowder repo checkout'
# begin_command
# $COMMAND repo checkout repo-test || enable_connection_exit
# end_command
# begin_command
# $COMMAND repo checkout master || enable_connection_exit
# end_command
# print_single_separator
# echo 'TEST: clowder repo clean'
# begin_command
# $COMMAND repo clean || enable_connection_exit
# end_command
# print_single_separator
# echo 'TEST: clowder repo commit'
# pushd .clowder || exit 1
# touch newfile || enable_connection_exit
# # git add newfile || enable_connection_exit
# popd || exit 1
# begin_command
# $COMMAND repo add newfile || enable_connection_exit
# end_command
# begin_command
# $COMMAND repo commit 'Add newfile' || enable_connection_exit
# end_command
# pushd .clowder || exit 1
# git reset --hard HEAD~1 || enable_connection_exit
# popd || exit 1
# print_single_separator
# echo 'TEST: clowder repo pull'
# begin_command
# $COMMAND repo pull && enable_connection_exit
# end_command
# print_single_separator
# echo 'TEST: clowder repo push'
# begin_command
# $COMMAND repo push && enable_connection_exit
# end_command
# print_single_separator
# echo 'TEST: clowder repo run'
# begin_command
# $COMMAND repo run 'git status' || enable_connection_exit
# end_command
# print_single_separator
