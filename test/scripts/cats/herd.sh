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
echo "TEST: Test clowder herd"

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh

test_herd_missing_clowder() {
    print_single_separator
    echo "TEST: Fail herd with missing clowder.yaml"
    begin_command
    $COMMAND herd $PARALLEL && exit 1
    end_command
}
test_herd_missing_clowder

./clean.sh
./init.sh || exit 1

test_herd_implicit_project_paths() {
    print_single_separator
    echo "TEST: Check projects are on correct branches with implicit project paths"
    begin_command
    $COMMAND link implicit-paths || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    pushd mu || exit 1
    test_branch knead
    popd || exit 1
    pushd duke || exit 1
    test_branch heads/purr
    popd || exit 1
    pushd kit || exit 1
    test_branch master
    popd || exit 1
    pushd kishka || exit 1
    test_branch master
    popd || exit 1
    pushd sasha || exit 1
    test_branch master
    popd || exit 1
    pushd june || exit 1
    test_branch master
    popd || exit 1
}
test_herd_implicit_project_paths

./clean.sh
./init.sh || exit 1

test_herd_implicit_defaults() {
    print_single_separator
    echo "TEST: Check projects are on correct branches with implicit defaults"
    begin_command
    $COMMAND link implicit-defaults || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    echo "TEST: cats projects on default branches with implicit defaults"
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_branch master
        local name=${project#"black-cats/"}
        test_remote_url 'origin' "https://github.com/jrgoodle/$name.git"
        popd || exit 1
    done
    pushd mu || exit 1
    test_branch knead
    test_remote_url 'origin' "https://github.com/jrgoodle/mu.git"
    popd || exit 1
    pushd duke || exit 1
    test_branch heads/purr
    test_remote_url 'origin' "https://github.com/jrgoodle/duke.git"
    popd || exit 1

}
test_herd_implicit_defaults

./clean.sh
./init.sh || exit 1

test_herd() {
    print_single_separator
    echo "TEST: Check projects are on correct branches"
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_cats_default_herd_branches
}
test_herd

test_herd_dirty_repos() {
    print_single_separator
    make_dirty_repos "$@"
    echo "TEST: Fail herd with dirty repos"
    begin_command
    $COMMAND herd $PARALLEL && exit 1
    end_command
    echo "TEST: Discard changes with clean"
    begin_command
    $COMMAND clean || exit 1
    end_command
    begin_command
    $COMMAND status || exit 1
    end_command
    echo "TEST: Successfully herd after clean"
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_cats_default_herd_branches
    echo "TEST: Successfully herd twice"
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_cats_default_herd_branches
}
test_herd_dirty_repos "${black_cats_projects[@]}"

test_herd_detached_heads() {
    print_single_separator
    echo "TEST: Create detached HEADs"
    for project in "$@"
    do
        pushd $project || exit 1
        git checkout master~2 || exit 1
        popd || exit 1
    done
    begin_command
    $COMMAND status || exit 1
    end_command
    echo "TEST: Successfully herd with detached HEADs"
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_cats_default_herd_branches
}
test_herd_detached_heads "${black_cats_projects[@]}"

test_herd_version() {
    print_single_separator
    echo "TEST: Successfully herd a previously saved version"
    begin_command
    $COMMAND link v0.1 || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    echo "TEST: Successfully herd after herding a previously saved version"
    begin_command
    $COMMAND link || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    echo "TEST: Remove directories"
    rm -rf "$@"
    for project in "${cats_projects[@]}"; do
        test_no_directory_exists "$project"
    done
    echo "TEST: Successfully herd with missing directories"
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_cats_default_herd_branches
}
test_herd_version 'duke' 'mu'

test_herd_groups() {
    print_single_separator
    echo "TEST: Herd saved version to test herding select groups"
    begin_command
    $COMMAND link v0.1 || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command

    echo "TEST: Herd only specific groups"
    begin_command
    $COMMAND herd "$@" $PARALLEL || exit 1
    end_command
    begin_command
    $COMMAND status || exit 1
    end_command
}
test_herd_groups 'cats'

test_herd_missing_branches() {
    print_single_separator
    echo "TEST: Herd v0.1 to test missing default branches"
    begin_command
    $COMMAND link v0.1 || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    echo "TEST: Delete default branches locally"
    pushd mu || exit 1
    git branch -D knead || exit 1
    popd || exit 1
    pushd duke || exit 1
    git branch -D purr || exit 1
    popd || exit 1
    echo "TEST: Herd existing repo's with no default branch locally"
    begin_command
    $COMMAND link || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_cats_default_herd_branches
}
test_herd_missing_branches

test_herd_sha() {
    print_single_separator
    echo 'TEST: Test herd of static commit hash refs'
    begin_command
    $COMMAND link static-refs || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    echo 'TEST: Check actual commit refs are correct'
    pushd mu || exit 1
    test_head_detached
    test_commit 'cddce39214a1ae20266d9ee36966de67438625d1'
    popd || exit 1
    pushd duke || exit 1
    test_head_detached
    test_commit '7083e8840e1bb972b7664cfa20bbd7a25f004018'
    popd || exit 1
    pushd black-cats/kit || exit 1
    test_head_detached
    test_commit 'da5c3d32ec2c00aba4a9f7d822cce2c727f7f5dd'
    popd || exit 1
    pushd black-cats/kishka || exit 1
    test_head_detached
    test_commit 'd185e3bff9eaaf6e146d4e09165276cd5c9f31c8'
    popd || exit 1
    pushd black-cats/june || exit 1
    test_head_detached
    test_commit '7b725e4953281347594585b8d1d02a3561201f72'
    popd || exit 1
    pushd black-cats/sasha || exit 1
    test_head_detached
    test_commit '775979e0b1a7f753131bf16a4794c851c67108d8'
    popd || exit 1
    begin_command
    $COMMAND status || exit 1
    end_command
    begin_command
    $COMMAND link || exit 1
    end_command
}
test_herd_sha

test_herd_tag() {
    print_single_separator
    echo 'TEST: Test herd of tag refs'
    begin_command
    $COMMAND link tags || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    echo 'TEST: Check actual tag commit refs are correct'
    pushd mu || exit 1
    test_head_detached
    test_tag_commit 'test-clowder-yaml-tag'
    popd || exit 1
    pushd duke || exit 1
    test_head_detached
    test_tag_commit 'purr'
    popd || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_head_detached
        test_tag_commit 'v0.01'
        popd || exit 1
    done
    begin_command
    $COMMAND status || exit 1
    end_command
    begin_command
    $COMMAND link || exit 1
    end_command
}
test_herd_tag

test_herd_projects() {
    print_single_separator
    echo "TEST: Successfully herd specific projects"
    begin_command
    $COMMAND herd "$@" $PARALLEL || exit 1
    end_command
}
test_herd_projects 'jrgoodle/kit' 'jrgoodle/kishka'

begin_command
$COMMAND repo checkout master || exit 1
end_command

EXISTING_REMOTE_BRANCH='test-herd-existing-remote-branch'
NO_REMOTE_BRANCH='test-herd-no-remote-branch'

test_herd_no_repo_existing_remote() {
    print_single_separator
    echo "TEST: Herd - No repo, existing remote branch"
    for project in "${all_projects[@]}"; do
        rm -rf $project
    done
    begin_command
    $COMMAND link 'herd-existing-remote-branch' || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        test_no_directory_exists "$project"
    done
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_branch $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done
}
test_herd_no_repo_existing_remote

test_herd_no_repo_no_remote() {
    print_single_separator
    echo "TEST: Herd - No repo, no remote branch"
    for project in "${all_projects[@]}"; do
        rm -rf $project
    done
    begin_command
    $COMMAND link 'herd-no-remote-branch' || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        test_no_directory_exists "$project"
    done
    begin_command
    $COMMAND herd $PARALLEL && exit 1
    end_command
    if [ -z "$PARALLEL" ]; then
        for project in "${all_projects[@]}"; do
            test_no_directory_exists "$project"
        done
    fi
}
test_herd_no_repo_no_remote

test_herd_no_local_existing_remote() {
    print_single_separator
    echo "TEST: Herd - No local branch, existing remote branch"
    begin_command
    $COMMAND link || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    begin_command
    $COMMAND prune $EXISTING_REMOTE_BRANCH || exit 1
    end_command
    begin_command
    $COMMAND link 'herd-existing-remote-branch' || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_no_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_branch $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done
}
test_herd_no_local_existing_remote

test_herd_no_local_no_remote() {
    print_single_separator
    echo "TEST: Herd - No local branch, no remote branch"
    begin_command
    $COMMAND link 'herd-no-remote-branch' || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_no_local_branch_exists $NO_REMOTE_BRANCH
        test_no_remote_branch_exists $NO_REMOTE_BRANCH
        popd || exit 1
    done
    begin_command
    $COMMAND herd $PARALLEL && exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_no_local_branch_exists $NO_REMOTE_BRANCH
        test_no_remote_branch_exists $NO_REMOTE_BRANCH
        popd || exit 1
    done
}
test_herd_no_local_no_remote

test_herd_existing_local_no_remote() {
    print_single_separator
    echo "TEST: Herd - Existing local branch, no remote branch"
    begin_command
    $COMMAND link || exit 1
    end_command
    begin_command
    $COMMAND start $NO_REMOTE_BRANCH || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_cats_default_herd_branches
    begin_command
    $COMMAND link 'herd-no-remote-branch' || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_local_branch_exists $NO_REMOTE_BRANCH
        test_no_remote_branch_exists $NO_REMOTE_BRANCH
        popd || exit 1
    done
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_local_branch_exists $NO_REMOTE_BRANCH
        test_no_remote_branch_exists $NO_REMOTE_BRANCH
        test_branch $NO_REMOTE_BRANCH
        popd || exit 1
    done
}
test_herd_existing_local_no_remote

test_herd_existing_local_existing_remote_no_tracking() {
    print_single_separator
    echo "TEST: Herd - Existing local branch, existing remote branch, no tracking, same commit"
    begin_command
    $COMMAND link 'herd-existing-remote-branch' || exit 1
    end_command
    begin_command
    $COMMAND prune $EXISTING_REMOTE_BRANCH || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    begin_command
    $COMMAND forall $PARALLEL -c 'git branch --unset-upstream' || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_no_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_branch $EXISTING_REMOTE_BRANCH
        test_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done

    # FIXME: Fix this test on CI
    # print_single_separator
    # echo "TEST: Herd - Existing local branch, existing remote branch, no tracking, different commits"
    # $COMMAND link || exit 1
    # $COMMAND herd $PARALLEL || exit 1
    # $COMMAND prune $EXISTING_REMOTE_BRANCH || exit 1
    # $COMMAND forall $PARALLEL -c 'git reset --hard HEAD~1' || exit 1
    # # $COMMAND forall $PARALLEL -c "git branch $EXISTING_REMOTE_BRANCH" || exit 1
    # $COMMAND link 'herd-existing-remote-branch' || exit 1
    # for project in "${all_projects[@]}"; do
    #     pushd $project || exit 1
    #     test_local_branch_exists $EXISTING_REMOTE_BRANCH
    #     test_remote_branch_exists $EXISTING_REMOTE_BRANCH
    #     test_no_tracking_branch_exists $EXISTING_REMOTE_BRANCH
    #     popd || exit 1
    # done
    # $COMMAND herd $PARALLEL && exit 1
    # for project in "${all_projects[@]}"; do
    #     pushd $project || exit 1
    #     test_local_branch_exists $EXISTING_REMOTE_BRANCH
    #     test_remote_branch_exists $EXISTING_REMOTE_BRANCH
    #     test_no_tracking_branch_exists $EXISTING_REMOTE_BRANCH
    #     popd || exit 1
    # done
}
test_herd_existing_local_existing_remote_no_tracking

test_herd_existing_local_existing_remote_tracking() {
    print_single_separator
    echo "TEST: Herd - Existing local branch, existing remote branch, tracking"
    begin_command
    $COMMAND link || exit 1
    end_command
    begin_command
    $COMMAND prune $EXISTING_REMOTE_BRANCH || exit 1
    end_command
    begin_command
    $COMMAND link 'herd-existing-remote-branch' || exit 1
    end_command
    begin_command
    $COMMAND forall $PARALLEL -c "git checkout $EXISTING_REMOTE_BRANCH" || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_branch $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done
}
test_herd_existing_local_existing_remote_tracking

test_herd_rebase() {
    print_single_separator
    echo "TEST: clowder herd rebase"
    begin_command
    $COMMAND link || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command

    local rebase_message='Add rebase file'
    pushd mu || exit 1
    local commit_message_1
    commit_message_1="$(git log --format=%B -n 1 HEAD)"
    echo "$commit_message_1"
    local commit_message_2
    commit_message_2="$(git log --format=%B -n 1 HEAD~1)"
    echo "$commit_message_2"
    git reset --hard HEAD~1 || exit 1
    touch rebasefile || exit 1
    git add rebasefile || exit 1
    git commit -m "$rebase_message" || exit 1
    test_commit_messages "$(git log --format=%B -n 1 HEAD)" "$rebase_message"
    test_commit_messages "$(git log --format=%B -n 1 HEAD~1)" "$commit_message_2"
    popd || exit 1

    begin_command
    $COMMAND herd $PARALLEL -r || exit 1
    end_command

    pushd mu || exit 1
    test_commit_messages "$(git log --format=%B -n 1 HEAD)" "$rebase_message"
    test_commit_messages "$(git log --format=%B -n 1 HEAD~1)" "$commit_message_1"
    test_commit_messages "$(git log --format=%B -n 1 HEAD~2)" "$commit_message_2"
    git reset --hard HEAD~1 || exit 1
    popd || exit 1
}
test_herd_rebase

if [ "$ACCESS_LEVEL" == "write" ]; then
    "$TEST_SCRIPT_DIR/cats/write_herd.sh" $1
fi
