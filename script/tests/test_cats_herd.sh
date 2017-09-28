#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

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
    	pushd $project
        test_branch master
        popd
    done
    pushd mu
    test_branch knead
    popd
    pushd duke
    test_branch purr
    popd
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
    	pushd $project >/dev/null
        git checkout master~2 >/dev/null
        popd >/dev/null
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
    pushd mu >/dev/null
    git branch -D knead >/dev/null
    popd >/dev/null
    pushd duke >/dev/null
    git branch -D purr >/dev/null
    popd >/dev/null
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
    	pushd $project
        test_branch 'alt-branch'
        popd
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
    clowder link -v $EXISTING_REMOTE_BRANCH || exit 1
    for project in "${all_projects[@]}"; do
    	if [ -d "$project" ]; then
            exit 1
        fi
    done
    clowder herd || exit 1
    for project in "${all_projects[@]}"; do
    	pushd $project
        test_branch $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd
    done
}
test_herd_no_repo_existing_remote

test_herd_no_repo_no_remote() {
    print_single_separator
    echo "TEST: Herd - No repo, no remote branch"
    for project in "${all_projects[@]}"; do
        rm -rf $project
    done
    clowder link -v $NO_REMOTE_BRANCH || exit 1
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
    clowder link -v $EXISTING_REMOTE_BRANCH || exit 1
    for project in "${all_projects[@]}"; do
    	pushd $project
        test_no_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        popd
    done
    clowder herd || exit 1
    for project in "${all_projects[@]}"; do
    	pushd $project
        test_branch $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd
    done
}
test_herd_no_local_existing_remote

test_herd_no_local_no_remote() {
    print_single_separator
    echo "TEST: Herd - No local branch, no remote branch"
    clowder link -v $NO_REMOTE_BRANCH || exit 1
    for project in "${all_projects[@]}"; do
    	pushd $project
        test_no_local_branch_exists $NO_REMOTE_BRANCH
        test_no_remote_branch_exists $NO_REMOTE_BRANCH
        popd
    done
    clowder herd && exit 1
    for project in "${all_projects[@]}"; do
    	pushd $project
        test_no_local_branch_exists $NO_REMOTE_BRANCH
        test_no_remote_branch_exists $NO_REMOTE_BRANCH
        popd
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
    clowder link -v $NO_REMOTE_BRANCH || exit 1
    for project in "${all_projects[@]}"; do
    	pushd $project
        test_local_branch_exists $NO_REMOTE_BRANCH
        test_no_remote_branch_exists $NO_REMOTE_BRANCH
        popd
    done
    clowder herd || exit 1
    for project in "${all_projects[@]}"; do
    	pushd $project
        test_local_branch_exists $NO_REMOTE_BRANCH
        test_no_remote_branch_exists $NO_REMOTE_BRANCH
        test_branch $NO_REMOTE_BRANCH
        popd
    done
}
test_herd_existing_local_no_remote

test_herd_existing_local_existing_remote_no_tracking() {
    print_single_separator
    echo "TEST: Herd - Existing local branch, existing remote branch, no tracking, same commit"
    clowder link -v $EXISTING_REMOTE_BRANCH || exit 1
    clowder prune $EXISTING_REMOTE_BRANCH || exit 1
    clowder herd || exit 1
    clowder forall -c 'git branch --unset-upstream' || exit 1
    for project in "${all_projects[@]}"; do
    	pushd $project
        test_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_no_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd
    done
    clowder herd || exit 1
    for project in "${all_projects[@]}"; do
    	pushd $project
        test_branch $EXISTING_REMOTE_BRANCH
        test_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd
    done

    echo "TEST: Herd - Existing local branch, existing remote branch, no tracking, different commits"
    clowder link || exit 1
    clowder herd || exit 1
    clowder prune $EXISTING_REMOTE_BRANCH || exit 1
    clowder forall -c 'git reset --hard HEAD~1' || exit 1
    clowder forall -c "git branch $EXISTING_REMOTE_BRANCH" || exit 1
    clowder link -v $EXISTING_REMOTE_BRANCH || exit 1
    for project in "${all_projects[@]}"; do
    	pushd $project
        test_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_no_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd
    done
    clowder herd && exit 1
    for project in "${all_projects[@]}"; do
    	pushd $project
        test_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_no_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd
    done
}
test_herd_existing_local_existing_remote_no_tracking

test_herd_existing_local_existing_remote_tracking() {
    print_single_separator
    echo "TEST: Herd - Existing local branch, existing remote branch, tracking"
    clowder link || exit 1
    clowder prune $EXISTING_REMOTE_BRANCH || exit 1
    clowder link -v $EXISTING_REMOTE_BRANCH || exit 1
    clowder forall -c "git checkout $EXISTING_REMOTE_BRANCH" || exit 1
    for project in "${all_projects[@]}"; do
    	pushd $project
        test_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd
    done
    clowder herd || exit 1
    for project in "${all_projects[@]}"; do
    	pushd $project
        test_branch $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd
    done
}
test_herd_existing_local_existing_remote_tracking
