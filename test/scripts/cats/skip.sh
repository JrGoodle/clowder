#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

print_double_separator
echo 'TEST: cats skip'
print_double_separator
cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./copy-cache.sh

test_skip_herd() {
    pushd 'mu' || exit 1
    git checkout HEAD~2 || exit 1
    test_head_detached
    popd || exit 1
    pushd 'duke' || exit 1
    git checkout HEAD~2 || exit 1
    test_head_detached
    popd || exit 1
    $COMMAND herd $PARALLEL -s jrgoodle/duke || exit 1
    pushd 'mu' || exit 1
    test_branch 'knead'
    popd || exit 1
    pushd 'duke' || exit 1
    test_head_detached
    popd || exit 1
}

test_skip_branch() {
    $COMMAND herd $PARALLEL || exit 1
    $COMMAND branch -s jrgoodle/duke || exit 1
}

test_skip_clean() {
    local filename='clean_file'
    $COMMAND herd $PARALLEL || exit 1
    pushd 'mu' || exit 1
    touch $filename || exit 1
    git add $filename || exit 1
    test_git_dirty
    popd || exit 1
    pushd 'duke' || exit 1
    touch $filename || exit 1
    git add $filename || exit 1
    test_git_dirty
    popd || exit 1
    $COMMAND clean -a -s jrgoodle/duke || exit 1
    pushd 'mu' || exit 1
    test_git_clean
    test_no_file_exists $filename
    popd || exit 1
    pushd 'duke' || exit 1
    test_git_dirty
    test_file_exists $filename
    popd || exit 1
    $COMMAND clean -a || exit 1
}

test_skip_forall() {
    local filename='forall_file'
    $COMMAND herd $PARALLEL || exit 1
    pushd 'mu' || exit 1
    test_git_clean
    popd || exit 1
    pushd 'duke' || exit 1
    test_git_clean
    popd || exit 1
    $COMMAND forall $PARALLEL -s jrgoodle/duke -c "touch $filename; git add $filename" || exit 1
    pushd 'mu' || exit 1
    test_git_dirty
    test_file_exists $filename
    popd || exit 1
    pushd 'duke' || exit 1
    test_git_clean
    test_no_file_exists $filename
    popd || exit 1
    $COMMAND clean -a || exit 1
}

test_skip_prune() {
    local branch='prune_branch'
    $COMMAND herd $PARALLEL || exit 1
    pushd 'mu' || exit 1
    git checkout -b $branch
    test_local_branch_exists $branch
    popd || exit 1
    pushd 'duke' || exit 1
    git checkout -b $branch
    test_local_branch_exists $branch
    popd || exit 1
    $COMMAND prune $branch -s jrgoodle/duke
    pushd 'mu' || exit 1
    test_no_local_branch_exists $branch
    popd || exit 1
    pushd 'duke' || exit 1
    test_local_branch_exists $branch
    popd || exit 1
    $COMMAND prune $branch || exit 1
}

test_skip_reset() {
    local mu_commit
    local duke_commit
    local duke_new_commit
    local filename='reset_file'
    local message='reset commit message'
    $COMMAND herd $PARALLEL || exit 1
    pushd 'mu' || exit 1
    mu_commit="$(git rev-parse HEAD)"
    touch $filename || exit 1
    git add $filename || exit 1
    git commit -m "$message" || exit 1
    test_not_commit $mu_commit
    popd || exit 1
    pushd 'duke' || exit 1
    duke_commit="$(git rev-parse HEAD)"
    touch $filename || exit 1
    git add $filename || exit 1
    git commit -m "$message" || exit 1
    test_not_commit $duke_commit
    duke_new_commit="$(git rev-parse HEAD)"
    popd || exit 1
    $COMMAND reset $PARALLEL -s jrgoodle/duke
    pushd 'mu' || exit 1
    test_commit $mu_commit
    popd || exit 1
    pushd 'duke' || exit 1
    test_not_commit $duke_commit
    test_commit $duke_new_commit
    popd || exit 1
    $COMMAND reset $PARALLEL || exit 1
}

test_skip_start() {
    local branch='start_branch'
    $COMMAND herd $PARALLEL || exit 1
    pushd 'mu' || exit 1
    test_no_local_branch_exists $branch
    popd || exit 1
    pushd 'duke' || exit 1
    test_no_local_branch_exists $branch
    popd || exit 1
    $COMMAND start $branch -s jrgoodle/duke
    pushd 'mu' || exit 1
    test_local_branch_exists $branch
    popd || exit 1
    pushd 'duke' || exit 1
    test_no_local_branch_exists $branch
    popd || exit 1
    $COMMAND prune $branch || exit 1
}

test_skip_stash() {
    local filename='stash_file'
    $COMMAND herd $PARALLEL || exit 1
    pushd 'mu' || exit 1
    touch $filename || exit 1
    git add $filename || exit 1
    test_git_dirty
    popd || exit 1
    pushd 'duke' || exit 1
    touch $filename || exit 1
    git add $filename || exit 1
    test_git_dirty
    popd || exit 1
    $COMMAND stash -s jrgoodle/duke || exit 1
    pushd 'mu' || exit 1
    test_git_clean
    test_no_file_exists $filename
    popd || exit 1
    pushd 'duke' || exit 1
    test_git_dirty
    test_file_exists $filename
    popd || exit 1
    $COMMAND stash || exit 1
}

test_skip_herd
test_skip_branch
test_skip_clean
test_skip_forall
test_skip_prune
test_skip_reset
test_skip_start
test_skip_stash
