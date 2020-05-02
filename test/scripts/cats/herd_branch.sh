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
echo "TEST: Test clowder herd branch"
cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./copy-cache.sh

EXISTING_REMOTE_BRANCH='test-herd-branch'
NO_REMOTE_BRANCH='test-herd-branch-no-remote-branch'

test_herd_branch_no_repo_existing_remote() {
    print_single_separator
    echo "TEST: Herd branch - No repo, existing remote branch"
    $COMMAND link || exit 1
    $COMMAND herd $PARALLEL || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done
    for project in "${all_projects[@]}"; do
        rm -rf $project
    done
    for project in "${all_projects[@]}"; do
        test_no_directory_exists "$project"
    done
    $COMMAND herd $PARALLEL -b $EXISTING_REMOTE_BRANCH || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_branch $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        test_no_local_branch_exists 'master'
        popd || exit 1
    done
    pushd mu || exit 1
    test_branch knead
    test_no_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd || exit 1
    pushd duke || exit 1
    test_branch purr
    test_no_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd || exit 1
}
test_herd_branch_no_repo_existing_remote

test_herd_branch_no_repo_no_remote() {
    print_single_separator
    echo "TEST: Herd branch - No repo, no remote branch"
    $COMMAND link || exit 1
    $COMMAND herd $PARALLEL || exit 1
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_no_remote_branch_exists $NO_REMOTE_BRANCH
        popd || exit 1
    done
    for project in "${all_projects[@]}"; do
        rm -rf $project
    done
    for project in "${all_projects[@]}"; do
        test_no_directory_exists "$project"
    done
    $COMMAND herd $PARALLEL -b $NO_REMOTE_BRANCH || exit 1
    test_cats_default_herd_branches
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_no_local_branch_exists $NO_REMOTE_BRANCH
        test_no_remote_branch_exists $NO_REMOTE_BRANCH
        popd || exit 1
    done
}
test_herd_branch_no_repo_no_remote

test_herd_branch_no_local_existing_remote() {
    print_single_separator
    echo "TEST: Herd branch - No local branch, existing remote branch"
    $COMMAND link || exit 1
    $COMMAND herd $PARALLEL || exit 1
    $COMMAND prune $EXISTING_REMOTE_BRANCH || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_no_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done
    pushd mu || exit 1
    test_no_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd || exit 1
    pushd duke || exit 1
    test_no_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd || exit 1
    $COMMAND herd $PARALLEL -b $EXISTING_REMOTE_BRANCH || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_branch $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done
    pushd mu || exit 1
    test_branch knead
    test_no_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd || exit 1
    pushd duke || exit 1
    test_branch purr
    test_no_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd || exit 1
}
test_herd_branch_no_local_existing_remote

test_herd_branch_no_local_no_remote() {
    print_single_separator
    echo "TEST: Herd branch - No local branch, no remote branch"
    $COMMAND link || exit 1
    $COMMAND herd $PARALLEL || exit 1
    $COMMAND prune $NO_REMOTE_BRANCH || exit 1
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_no_local_branch_exists $NO_REMOTE_BRANCH
        test_no_remote_branch_exists $NO_REMOTE_BRANCH
        popd || exit 1
    done
    $COMMAND herd $PARALLEL -b $NO_REMOTE_BRANCH || exit 1
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_no_local_branch_exists $NO_REMOTE_BRANCH
        test_no_remote_branch_exists $NO_REMOTE_BRANCH
        popd || exit 1
    done
    test_cats_default_herd_branches
}
test_herd_branch_no_local_no_remote

test_herd_branch_existing_local_no_remote() {
    print_single_separator
    echo "TEST: Herd branch - Existing local branch, no remote branch"
    $COMMAND link || exit 1
    $COMMAND start $NO_REMOTE_BRANCH || exit 1
    $COMMAND herd $PARALLEL || exit 1
    test_cats_default_herd_branches
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_local_branch_exists $NO_REMOTE_BRANCH
        test_no_remote_branch_exists $NO_REMOTE_BRANCH
        popd || exit 1
    done
    $COMMAND herd $PARALLEL -b $NO_REMOTE_BRANCH || exit 1
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_local_branch_exists $NO_REMOTE_BRANCH
        test_no_remote_branch_exists $NO_REMOTE_BRANCH
        test_branch $NO_REMOTE_BRANCH
        popd || exit 1
    done
}
test_herd_branch_existing_local_no_remote

test_herd_branch_existing_local_existing_remote_no_tracking() {
    print_single_separator
    echo "TEST: Herd branch - Existing local branch, existing remote branch, no tracking, same commit"
    $COMMAND link || exit 1
    $COMMAND prune $EXISTING_REMOTE_BRANCH || exit 1
    $COMMAND forall $PARALLEL -c "git checkout -b $EXISTING_REMOTE_BRANCH" -p cats || exit 1
    $COMMAND forall $PARALLEL -ic "git checkout $EXISTING_REMOTE_BRANCH" || exit 1
    $COMMAND forall $PARALLEL -ic 'git branch --unset-upstream' || exit 1
    pushd mu || exit 1
    test_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd || exit 1
    pushd duke || exit 1
    test_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_no_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done
    $COMMAND herd $PARALLEL || exit 1
    test_cats_default_herd_branches
    $COMMAND herd $PARALLEL -b $EXISTING_REMOTE_BRANCH || exit 1
    pushd mu || exit 1
    test_branch $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd || exit 1
    pushd duke || exit 1
    test_branch $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_branch $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done
    echo "TEST: Herd branch - Existing local branch, existing remote branch, no tracking, different commits"
    $COMMAND herd $PARALLEL || exit 1
    $COMMAND prune $EXISTING_REMOTE_BRANCH || exit 1
    $COMMAND forall $PARALLEL -c 'git reset --hard HEAD~1' || exit 1
    $COMMAND forall $PARALLEL -c "git branch $EXISTING_REMOTE_BRANCH" || exit 1
    pushd mu || exit 1
    test_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd || exit 1
    pushd duke || exit 1
    test_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_no_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done
    $COMMAND herd $PARALLEL -b $EXISTING_REMOTE_BRANCH && exit 1
    pushd mu || exit 1
    test_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd || exit 1
    pushd duke || exit 1
    test_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_no_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done
}
test_herd_branch_existing_local_existing_remote_no_tracking

test_herd_branch_existing_local_existing_remote_tracking() {
    print_single_separator
    echo "TEST: Herd branch - Existing local branch, existing remote branch, tracking"
    $COMMAND link || exit 1
    $COMMAND prune $EXISTING_REMOTE_BRANCH || exit 1
    $COMMAND forall -p black-cats -c "git checkout $EXISTING_REMOTE_BRANCH" || exit 1
    $COMMAND herd $PARALLEL || exit 1
    test_cats_default_herd_branches
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_local_branch_exists $EXISTING_REMOTE_BRANCH
        test_remote_branch_exists $EXISTING_REMOTE_BRANCH
        test_tracking_branch_exists $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done
    $COMMAND herd $PARALLEL -b $EXISTING_REMOTE_BRANCH || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_branch $EXISTING_REMOTE_BRANCH
        popd || exit 1
    done
    pushd mu || exit 1
    test_branch knead
    test_no_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd || exit 1
    pushd duke || exit 1
    test_branch purr
    test_no_local_branch_exists $EXISTING_REMOTE_BRANCH
    test_no_remote_branch_exists $EXISTING_REMOTE_BRANCH
    popd || exit 1
}
test_herd_branch_existing_local_existing_remote_tracking
