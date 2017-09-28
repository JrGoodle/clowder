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
echo "TEST: Test clowder herd branch"
./init.sh || exit 1

EXISTING_REMOTE_BRANCH='test-herd-branch'
NO_REMOTE_BRANCH='test-herd-branch-no-remote-branch'

test_herd_branch_no_repo_existing_remote() {
    print_single_separator
    echo "TEST: Herd branch - No repo, existing remote branch"
    clowder link || exit 1
    clowder herd || exit 1
    for project in "${black_cats_projects[@]}"; do
    	pushd $project
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        popd
    done
    for project in "${all_projects[@]}"; do
        rm -rf $project
    done
    for project in "${all_projects[@]}"; do
    	if [ -d "$project" ]; then
            exit 1
        fi
    done
    clowder herd -b $EXISTING_REMOTE_BRANCH || exit 1
    for project in "${black_cats_projects[@]}"; do
    	pushd $project
        test_branch $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        test_no_local_branch_exists 'master'
        popd
    done
    pushd mu
    test_branch knead
    test_no_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd
    pushd duke
    test_branch purr
    test_no_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd
}
test_herd_branch_no_repo_existing_remote

test_herd_branch_no_repo_no_remote() {
    print_single_separator
    echo "TEST: Herd branch - No repo, no remote branch"
    clowder link || exit 1
    clowder herd || exit 1
    for project in "${all_projects[@]}"; do
    	pushd $project
        test_no_remote_branch_exists $NO_REMOTE_BRANCH
        popd
    done
    for project in "${all_projects[@]}"; do
        rm -rf $project
    done
    for project in "${all_projects[@]}"; do
    	if [ -d "$project" ]; then
            exit 1
        fi
    done
    clowder herd -b $NO_REMOTE_BRANCH || exit 1
    test_cats_default_herd_branches
    for project in "${all_projects[@]}"; do
    	pushd $project
        test_no_local_branch_exists $NO_REMOTE_BRANCH
        test_no_remote_branch_exists $NO_REMOTE_BRANCH
        popd
    done
}
test_herd_branch_no_repo_no_remote

test_herd_branch_no_local_existing_remote() {
    print_single_separator
    echo "TEST: Herd branch - No local branch, existing remote branch"
    clowder link || exit 1
    clowder herd || exit 1
    clowder prune $EXISTING_REMOTE_BRANCH || exit 1
    for project in "${black_cats_projects[@]}"; do
    	pushd $project
        test_no_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        popd
    done
    pushd mu
    test_no_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd
    pushd duke
    test_no_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd
    clowder herd -b $EXISTING_REMOTE_BRANCH || exit 1
    for project in "${black_cats_projects[@]}"; do
    	pushd $project
        test_branch $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd
    done
    pushd mu
    test_branch knead
    test_no_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd
    pushd duke
    test_branch purr
    test_no_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd
}
test_herd_branch_no_local_existing_remote

test_herd_branch_no_local_no_remote() {
    print_single_separator
    echo "TEST: Herd branch - No local branch, no remote branch"
    clowder link || exit 1
    clowder herd || exit 1
    clowder prune $NO_REMOTE_BRANCH || exit 1
    for project in "${all_projects[@]}"; do
    	pushd $project
        test_no_local_branch_exists $NO_REMOTE_BRANCH
        test_no_remote_branch_exists $NO_REMOTE_BRANCH
        popd
    done
    clowder herd -b $NO_REMOTE_BRANCH || exit 1
    for project in "${all_projects[@]}"; do
    	pushd $project
        test_no_local_branch_exists $NO_REMOTE_BRANCH
        test_no_remote_branch_exists $NO_REMOTE_BRANCH
        popd
    done
    test_cats_default_herd_branches
}
test_herd_branch_no_local_no_remote

test_herd_branch_existing_local_no_remote() {
    print_single_separator
    echo "TEST: Herd branch - Existing local branch, no remote branch"
    clowder link || exit 1
    clowder start $NO_REMOTE_BRANCH || exit 1
    clowder herd || exit 1
    test_cats_default_herd_branches
    for project in "${all_projects[@]}"; do
    	pushd $project
        test_local_branch_exists $NO_REMOTE_BRANCH
        test_no_remote_branch_exists $NO_REMOTE_BRANCH
        popd
    done
    clowder herd -b $NO_REMOTE_BRANCH || exit 1
    for project in "${all_projects[@]}"; do
    	pushd $project
        test_local_branch_exists $NO_REMOTE_BRANCH
        test_no_remote_branch_exists $NO_REMOTE_BRANCH
        test_branch $NO_REMOTE_BRANCH
        popd
    done
}
test_herd_branch_existing_local_no_remote

test_herd_branch_existing_local_existing_remote_no_tracking() {
    print_single_separator
    echo "TEST: Herd branch - Existing local branch, existing remote branch, no tracking, same commit"
    clowder link || exit 1
    clowder prune $EXISTING_REMOTE_BRANCH || exit 1
    clowder forall -c "git checkout -b $EXISTING_REMOTE_BRANCH" -g cats || exit 1
    clowder forall -ic "git checkout $EXISTING_REMOTE_BRANCH" || exit 1
    clowder forall -ic 'git branch --unset-upstream' || exit 1
    pushd mu
    test_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd
    pushd duke
    test_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd
    for project in "${black_cats_projects[@]}"; do
    	pushd $project
        test_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_no_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd
    done
    clowder herd || exit 1
    test_cats_default_herd_branches
    clowder herd -b $EXISTING_REMOTE_BRANCH || exit 1
    pushd mu
    test_branch $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd
    pushd duke
    test_branch $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd
    for project in "${black_cats_projects[@]}"; do
    	pushd $project
        test_branch $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd
    done
    echo "TEST: Herd branch - Existing local branch, existing remote branch, no tracking, different commits"
    clowder herd || exit 1
    clowder prune $EXISTING_REMOTE_BRANCH || exit 1
    clowder forall -c 'git reset --hard HEAD~1' || exit 1
    clowder forall -c "git branch $EXISTING_REMOTE_BRANCH" || exit 1
    pushd mu
    test_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd
    pushd duke
    test_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd
    for project in "${black_cats_projects[@]}"; do
    	pushd $project
        test_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_no_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd
    done
    clowder herd -b $EXISTING_REMOTE_BRANCH && exit 1
    pushd mu
    test_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd
    pushd duke
    test_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd
    for project in "${black_cats_projects[@]}"; do
    	pushd $project
        test_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_no_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd
    done
}
test_herd_branch_existing_local_existing_remote_no_tracking

test_herd_branch_existing_local_existing_remote_tracking() {
    print_single_separator
    echo "TEST: Herd branch - Existing local branch, existing remote branch, tracking"
    clowder link || exit 1
    clowder prune $EXISTING_REMOTE_BRANCH || exit 1
    clowder forall -g black-cats -c "git checkout $EXISTING_REMOTE_BRANCH" || exit 1
    clowder herd || exit 1
    test_cats_default_herd_branches
    for project in "${black_cats_projects[@]}"; do
    	pushd $project
        test_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd
    done
    clowder herd -b $EXISTING_REMOTE_BRANCH || exit 1
    for project in "${black_cats_projects[@]}"; do
    	pushd $project
        test_branch $EXISTING_REMOTE_BRANCH
        popd
    done
    pushd mu
    test_branch knead
    test_no_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd
    pushd duke
    test_branch purr
    test_no_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd
}
test_herd_branch_existing_local_existing_remote_tracking
