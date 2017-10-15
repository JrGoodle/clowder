#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

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

prepare_cats_example
cd "$CATS_EXAMPLE_DIR" || exit 1

print_double_separator
echo "TEST: Test clowder herd"

test_herd_missing_clowder() {
    print_single_separator
    "$CATS_EXAMPLE_DIR/clean.sh" || exit 1
    echo "TEST: Fail herd with missing clowder.yaml"
    clowder herd && exit 1
    "$CATS_EXAMPLE_DIR/init.sh" || exit 1
}
test_herd_missing_clowder

test_herd() {
    print_single_separator
    echo "TEST: Check projects are on correct branches"
    clowder herd || exit 1
    test_cats_default_herd_branches
}
test_herd

test_herd_dirty_repos() {
    print_single_separator
    make_dirty_repos "$@"
    echo "TEST: Fail herd with dirty repos"
    clowder herd && exit 1
    echo "TEST: Discard changes with clean"
    clowder clean || exit 1
    clowder status || exit 1
    echo "TEST: Successfully herd after clean"
    clowder herd || exit 1
    test_cats_default_herd_branches
    echo "TEST: Successfully herd twice"
    clowder herd || exit 1
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
    clowder status || exit 1
    echo "TEST: Successfully herd with detached HEADs"
    clowder herd || exit 1
    test_cats_default_herd_branches
}
test_herd_detached_heads "${black_cats_projects[@]}"

test_herd_version() {
    print_single_separator
    echo "TEST: Successfully herd a previously saved version"
    clowder link -v v0.1 || exit 1
    clowder herd || exit 1
    echo "TEST: Successfully herd after herding a previously saved version"
    clowder link || exit 1
    clowder herd || exit 1
    echo "TEST: Remove directories"
    rm -rf "$@"
    for project in "${cats_projects[@]}"; do
        if [ -d "$project" ]; then
            exit 1
        fi
    done
    echo "TEST: Successfully herd with missing directories"
    clowder herd || exit 1
    test_cats_default_herd_branches
}
test_herd_version 'duke' 'mu'

test_herd_groups() {
    print_single_separator
    echo "TEST: Herd saved version to test herding select groups"
    clowder link -v v0.1 || exit 1
    clowder herd || exit 1

    echo "TEST: Herd only specific groups"
    clowder herd -g "$@" || exit 1
    clowder status || exit 1
}
test_herd_groups 'cats'

test_herd_missing_branches() {
    print_single_separator
    echo "TEST: Herd v0.1 to test missing default branches"
    clowder link -v v0.1 || exit 1
    clowder herd || exit 1
    echo "TEST: Delete default branches locally"
    pushd mu || exit 1
    git branch -D knead || exit 1
    popd || exit 1
    pushd duke || exit 1
    git branch -D purr || exit 1
    popd || exit 1
    echo "TEST: Herd existing repo's with no default branch locally"
    clowder link || exit 1
    clowder herd || exit 1
    test_cats_default_herd_branches
}
test_herd_missing_branches

test_herd_sha() {
    print_single_separator
    echo "TEST: Test herd of static commit hash refs"
    clowder repo checkout static-refs || exit 1
    clowder herd || exit 1
    clowder status || exit 1
    clowder repo checkout master || exit 1
}
test_herd_sha

test_herd_tag() {
    print_single_separator
    echo "TEST: Test herd of tag refs"
    clowder repo checkout tags || exit 1
    clowder herd || exit 1
    clowder status || exit 1
    clowder repo checkout master || exit 1
}
test_herd_tag

test_herd_projects() {
    print_single_separator
    echo "TEST: Successfully herd specific projects"
    clowder herd -p "$@" || exit 1
}
test_herd_projects 'jrgoodle/kit' 'jrgoodle/kishka'

clowder repo checkout master || exit 1

test_herd_override_groups() {
    print_single_separator
    echo "TEST: Override values at group level"
    clowder link || exit 1
    clowder herd -b alt-branch || exit 1
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_branch 'alt-branch'
        popd || exit 1
    done
    clowder link -v override-group-ref || exit 1
    clowder herd || exit 1
    test_cats_default_herd_branches
}
test_herd_override_groups

EXISTING_REMOTE_BRANCH='test-herd-existing-remote-branch'
NO_REMOTE_BRANCH='test-herd-no-remote-branch'

test_herd_no_repo_existing_remote() {
    print_single_separator
    echo "TEST: Herd - No repo, existing remote branch"
    for project in "${all_projects[@]}"; do
        rm -rf $project
    done
    clowder link -v 'herd-existing-remote-branch' || exit 1
    for project in "${all_projects[@]}"; do
        if [ -d "$project" ]; then
            exit 1
        fi
    done
    clowder herd || exit 1
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
    clowder link -v 'herd-no-remote-branch' || exit 1
    for project in "${all_projects[@]}"; do
        if [ -d "$project" ]; then
            exit 1
        fi
    done
    clowder herd && exit 1
    for project in "${all_projects[@]}"; do
        if [ -d "$project" ]; then
            exit 1
        fi
    done
}
test_herd_no_repo_no_remote

test_herd_no_local_existing_remote() {
    print_single_separator
    echo "TEST: Herd - No local branch, existing remote branch"
    clowder link || exit 1
    clowder herd || exit 1
    clowder prune $EXISTING_REMOTE_BRANCH || exit 1
    clowder link -v 'herd-existing-remote-branch' || exit 1
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_no_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done
    clowder herd || exit 1
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
    clowder link -v 'herd-no-remote-branch' || exit 1
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_no_local_branch_exists $NO_REMOTE_BRANCH
        test_no_remote_branch_exists $NO_REMOTE_BRANCH
        popd || exit 1
    done
    clowder herd && exit 1
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
    clowder link || exit 1
    clowder start $NO_REMOTE_BRANCH || exit 1
    clowder herd || exit 1
    test_cats_default_herd_branches
    clowder link -v 'herd-no-remote-branch' || exit 1
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_local_branch_exists $NO_REMOTE_BRANCH
        test_no_remote_branch_exists $NO_REMOTE_BRANCH
        popd || exit 1
    done
    clowder herd || exit 1
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
    clowder link -v 'herd-existing-remote-branch' || exit 1
    clowder prune $EXISTING_REMOTE_BRANCH || exit 1
    clowder herd || exit 1
    clowder forall -c 'git branch --unset-upstream' || exit 1
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_no_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done
    clowder herd || exit 1
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_branch $EXISTING_REMOTE_BRANCH
        test_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done

    echo "TEST: Herd - Existing local branch, existing remote branch, no tracking, different commits"
    clowder link || exit 1
    clowder herd || exit 1
    clowder prune $EXISTING_REMOTE_BRANCH || exit 1
    clowder forall -c 'git reset --hard HEAD~1' || exit 1
    clowder forall -c "git branch $EXISTING_REMOTE_BRANCH" || exit 1
    clowder link -v 'herd-existing-remote-branch' || exit 1
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_no_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done
    clowder herd && exit 1
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_no_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done
}
test_herd_existing_local_existing_remote_no_tracking

test_herd_existing_local_existing_remote_tracking() {
    print_single_separator
    echo "TEST: Herd - Existing local branch, existing remote branch, tracking"
    clowder link || exit 1
    clowder prune $EXISTING_REMOTE_BRANCH || exit 1
    clowder link -v 'herd-existing-remote-branch' || exit 1
    clowder forall -c "git checkout $EXISTING_REMOTE_BRANCH" || exit 1
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done
    clowder herd || exit 1
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
    clowder link || exit 1
    clowder herd || exit 1

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

    clowder herd -r || exit 1

    pushd mu || exit 1
    test_commit_messages "$(git log --format=%B -n 1 HEAD)" "$REBASE_MESSAGE"
    test_commit_messages "$(git log --format=%B -n 1 HEAD~1)" "$COMMIT_MESSAGE_1"
    test_commit_messages "$(git log --format=%B -n 1 HEAD~2)" "$COMMIT_MESSAGE_2"
    git reset --hard HEAD~1 || exit 1
    popd || exit 1
}
test_herd_rebase

if [ "$ACCESS_LEVEL" == "write" ]; then
    test_herd_rebase_conflict() {
        print_single_separator
        echo "TEST: clowder herd rebase conflict"
        clowder link || exit 1
        clowder herd || exit 1

        pushd mu || exit 1
        touch rebasefile || exit 1
        echo 'something' >> rebasefile
        git add rebasefile || exit 1
        git commit -m 'Add rebase file' || exit 1
        git push || exit 1
        git reset --hard HEAD~1 || exit 1
        touch rebasefile || exit 1
        echo 'something else' >> rebasefile
        git add rebasefile || exit 1
        git commit -m 'Add another rebase file' || exit 1
        test_no_rebase_in_progress
        popd || exit 1

        clowder herd -r && exit 1

        pushd mu || exit 1
        test_rebase_in_progress
        popd || exit 1

        clowder clean -a || exit 1

        pushd mu || exit 1
        test_no_rebase_in_progress
        git reset --hard HEAD~1 || exit 1
        git push --force || exit 1
        popd || exit 1
    }
    test_herd_rebase_conflict
fi
