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
    test_branch purr
    popd || exit 1
}

print_double_separator
echo "TEST: Test clowder herd"

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh

test_herd_missing_clowder() {
    print_single_separator
    echo "TEST: Fail herd with missing clowder.yaml"
    $COMMAND herd $PARALLEL && exit 1
}
test_herd_missing_clowder

./clean.sh
./init.sh || exit 1

test_herd_implicit_project_paths() {
    print_single_separator
    echo "TEST: Check projects are on correct branches with implicit project paths"
    $COMMAND link -v implicit-paths || exit 1
    $COMMAND herd $PARALLEL || exit 1
    pushd jrgoodle/mu || exit 1
    test_branch knead
    popd || exit 1
    pushd jrgoodle/duke || exit 1
    test_branch purr
    popd || exit 1
    pushd jrgoodle/kit || exit 1
    test_branch master
    popd || exit 1
    pushd jrgoodle/kishka || exit 1
    test_branch master
    popd || exit 1
    pushd jrgoodle/sasha || exit 1
    test_branch master
    popd || exit 1
    pushd jrgoodle/june || exit 1
    test_branch master
    popd || exit 1
}
test_herd_implicit_project_paths

./clean.sh
./init.sh || exit 1

test_herd_implicit_defaults() {
    print_single_separator
    echo "TEST: Check projects are on correct branches with implicit defaults"
    $COMMAND link -v implicit-defaults || exit 1
    $COMMAND herd $PARALLEL || exit 1
    echo "TEST: cats projects on default branches with implicit defaults"
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_branch master
        name=${project#"black-cats/"}
        test_remote_url 'origin' "https://github.com/jrgoodle/$name.git"
        popd || exit 1
    done
    pushd mu || exit 1
    test_branch knead
    test_remote_url 'origin' "https://github.com/jrgoodle/mu.git"
    popd || exit 1
    pushd duke || exit 1
    test_branch purr
    test_remote_url 'origin' "https://github.com/jrgoodle/duke.git"
    popd || exit 1

}
test_herd_implicit_defaults

./clean.sh
./init.sh || exit 1

test_herd() {
    print_single_separator
    echo "TEST: Check projects are on correct branches"
    $COMMAND herd $PARALLEL || exit 1
    test_cats_default_herd_branches
}
test_herd

test_herd_dirty_repos() {
    print_single_separator
    make_dirty_repos "$@"
    echo "TEST: Fail herd with dirty repos"
    $COMMAND herd $PARALLEL && exit 1
    echo "TEST: Discard changes with clean"
    $COMMAND clean || exit 1
    $COMMAND status || exit 1
    echo "TEST: Successfully herd after clean"
    $COMMAND herd $PARALLEL || exit 1
    test_cats_default_herd_branches
    echo "TEST: Successfully herd twice"
    $COMMAND herd $PARALLEL || exit 1
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
    $COMMAND status || exit 1
    echo "TEST: Successfully herd with detached HEADs"
    $COMMAND herd $PARALLEL || exit 1
    test_cats_default_herd_branches
}
test_herd_detached_heads "${black_cats_projects[@]}"

test_herd_version() {
    print_single_separator
    echo "TEST: Successfully herd a previously saved version"
    $COMMAND link -v v0.1 || exit 1
    $COMMAND herd $PARALLEL || exit 1
    echo "TEST: Successfully herd after herding a previously saved version"
    $COMMAND link || exit 1
    $COMMAND herd $PARALLEL || exit 1
    echo "TEST: Remove directories"
    rm -rf "$@"
    for project in "${cats_projects[@]}"; do
        test_no_directory_exists "$project"
    done
    echo "TEST: Successfully herd with missing directories"
    $COMMAND herd $PARALLEL || exit 1
    test_cats_default_herd_branches
}
test_herd_version 'duke' 'mu'

test_herd_groups() {
    print_single_separator
    echo "TEST: Herd saved version to test herding select groups"
    $COMMAND link -v v0.1 || exit 1
    $COMMAND herd $PARALLEL || exit 1

    echo "TEST: Herd only specific groups"
    $COMMAND herd $PARALLEL -p "$@" || exit 1
    $COMMAND status || exit 1
}
test_herd_groups 'cats'

test_herd_missing_branches() {
    print_single_separator
    echo "TEST: Herd v0.1 to test missing default branches"
    $COMMAND link -v v0.1 || exit 1
    $COMMAND herd $PARALLEL || exit 1
    echo "TEST: Delete default branches locally"
    pushd mu || exit 1
    git branch -D knead || exit 1
    popd || exit 1
    pushd duke || exit 1
    git branch -D purr || exit 1
    popd || exit 1
    echo "TEST: Herd existing repo's with no default branch locally"
    $COMMAND link || exit 1
    $COMMAND herd $PARALLEL || exit 1
    test_cats_default_herd_branches
}
test_herd_missing_branches

test_herd_sha() {
    print_single_separator
    echo "TEST: Test herd of static commit hash refs"
    $COMMAND link -v static-refs || exit 1
    $COMMAND herd $PARALLEL || exit 1
    $COMMAND status || exit 1
    $COMMAND link || exit 1
}
test_herd_sha

test_herd_tag() {
    print_single_separator
    echo "TEST: Test herd of tag refs"
    $COMMAND link -v tags || exit 1
    $COMMAND herd $PARALLEL || exit 1
    $COMMAND status || exit 1
    $COMMAND link || exit 1
}
test_herd_tag

test_herd_projects() {
    print_single_separator
    echo "TEST: Successfully herd specific projects"
    $COMMAND herd $PARALLEL -p "$@" || exit 1
}
test_herd_projects 'jrgoodle/kit' 'jrgoodle/kishka'

pushd .clowder || exit 1
git checkout master || exit 1
popd || exit 1

EXISTING_REMOTE_BRANCH='test-herd-existing-remote-branch'
NO_REMOTE_BRANCH='test-herd-no-remote-branch'

test_herd_no_repo_existing_remote() {
    print_single_separator
    echo "TEST: Herd - No repo, existing remote branch"
    for project in "${all_projects[@]}"; do
        rm -rf $project
    done
    $COMMAND link -v 'herd-existing-remote-branch' || exit 1
    for project in "${all_projects[@]}"; do
        test_no_directory_exists "$project"
    done
    $COMMAND herd $PARALLEL || exit 1
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
    $COMMAND link -v 'herd-no-remote-branch' || exit 1
    for project in "${all_projects[@]}"; do
        test_no_directory_exists "$project"
    done
    $COMMAND herd $PARALLEL && exit 1
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
    $COMMAND link || exit 1
    $COMMAND herd $PARALLEL || exit 1
    $COMMAND prune $EXISTING_REMOTE_BRANCH || exit 1
    $COMMAND link -v 'herd-existing-remote-branch' || exit 1
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_no_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done
    $COMMAND herd $PARALLEL || exit 1
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
    $COMMAND link -v 'herd-no-remote-branch' || exit 1
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_no_local_branch_exists $NO_REMOTE_BRANCH
        test_no_remote_branch_exists $NO_REMOTE_BRANCH
        popd || exit 1
    done
    $COMMAND herd $PARALLEL && exit 1
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
    $COMMAND link || exit 1
    $COMMAND start $NO_REMOTE_BRANCH || exit 1
    $COMMAND herd $PARALLEL || exit 1
    test_cats_default_herd_branches
    $COMMAND link -v 'herd-no-remote-branch' || exit 1
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_local_branch_exists $NO_REMOTE_BRANCH
        test_no_remote_branch_exists $NO_REMOTE_BRANCH
        popd || exit 1
    done
    $COMMAND herd $PARALLEL || exit 1
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
    $COMMAND link -v 'herd-existing-remote-branch' || exit 1
    $COMMAND prune $EXISTING_REMOTE_BRANCH || exit 1
    $COMMAND herd $PARALLEL || exit 1
    $COMMAND forall $PARALLEL -c 'git branch --unset-upstream' || exit 1
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_no_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done
    $COMMAND herd $PARALLEL || exit 1
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_branch $EXISTING_REMOTE_BRANCH
        test_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done

    # FIXME: Fix this test on Travis CI
    # print_single_separator
    # echo "TEST: Herd - Existing local branch, existing remote branch, no tracking, different commits"
    # $COMMAND link || exit 1
    # $COMMAND herd $PARALLEL || exit 1
    # $COMMAND prune $EXISTING_REMOTE_BRANCH || exit 1
    # $COMMAND forall $PARALLEL -c 'git reset --hard HEAD~1' || exit 1
    # # $COMMAND forall $PARALLEL -c "git branch $EXISTING_REMOTE_BRANCH" || exit 1
    # $COMMAND link -v 'herd-existing-remote-branch' || exit 1
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
    $COMMAND link || exit 1
    $COMMAND prune $EXISTING_REMOTE_BRANCH || exit 1
    $COMMAND link -v 'herd-existing-remote-branch' || exit 1
    $COMMAND forall $PARALLEL -c "git checkout $EXISTING_REMOTE_BRANCH" || exit 1
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done
    $COMMAND herd $PARALLEL || exit 1
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
    $COMMAND link || exit 1
    $COMMAND herd $PARALLEL || exit 1

    REBASE_MESSAGE='Add rebase file'
    pushd mu || exit 1
    COMMIT_MESSAGE_1="$(git log --format=%B -n 1 HEAD)"
    echo "$COMMIT_MESSAGE_1"
    COMMIT_MESSAGE_2="$(git log --format=%B -n 1 HEAD~1)"
    echo "$COMMIT_MESSAGE_2"
    git reset --hard HEAD~1 || exit 1
    touch rebasefile || exit 1
    git add rebasefile || exit 1
    git commit -m "$REBASE_MESSAGE" || exit 1
    test_commit_messages "$(git log --format=%B -n 1 HEAD)" "$REBASE_MESSAGE"
    test_commit_messages "$(git log --format=%B -n 1 HEAD~1)" "$COMMIT_MESSAGE_2"
    popd || exit 1

    $COMMAND herd $PARALLEL -r || exit 1

    pushd mu || exit 1
    test_commit_messages "$(git log --format=%B -n 1 HEAD)" "$REBASE_MESSAGE"
    test_commit_messages "$(git log --format=%B -n 1 HEAD~1)" "$COMMIT_MESSAGE_1"
    test_commit_messages "$(git log --format=%B -n 1 HEAD~2)" "$COMMIT_MESSAGE_2"
    git reset --hard HEAD~1 || exit 1
    popd || exit 1
}
test_herd_rebase

if [ "$ACCESS_LEVEL" == "write" ]; then
    "$TEST_SCRIPT_DIR/cats/write_herd.sh" $1
fi
