#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

export external_projects=( 'cocos2d-objc/external/Chipmunk' \
                           'cocos2d-objc/external/ObjectAL' \
                           'cocos2d-objc/external/SSZipArchive' )

print_double_separator
echo 'TEST: cocos2d clean'
print_double_separator
cd "$COCOS2D_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh

herd() {
    clowder herd $PARALLEL || exit 1
    pushd 'cocos2d-objc' || exit 1
    git checkout HEAD~5 || exit 1
    test_head_detached
    popd || exit 1
    pushd 'cocos2d-x' || exit 1
    git checkout HEAD~5 || exit 1
    test_head_detached
    popd || exit 1
    clowder herd $PARALLEL -s cocos2d/cocos2d-x || exit 1
    pushd 'cocos2d-objc' || exit 1
    test_branch 'heads/v3.5.0'
    popd || exit 1
    pushd 'cocos2d-x' || exit 1
    test_head_detached
    popd || exit 1
}
herd

branch() {
    clowder herd $PARALLEL || exit 1
    clowder branch -s cocos2d/cocos2d-x || exit 1
}
branch

clean() {
    local filename='clean_file'
    clowder herd $PARALLEL || exit 1
    pushd 'cocos2d-objc' || exit 1
    touch $filename || exit 1
    git add $filename || exit 1
    test_git_dirty
    popd || exit 1
    pushd 'cocos2d-x' || exit 1
    touch $filename || exit 1
    git add $filename || exit 1
    test_git_dirty
    popd || exit 1
    clowder clean -a -s cocos2d/cocos2d-x || exit 1
    pushd 'cocos2d-objc' || exit 1
    test_git_clean
    test_no_file_exists $filename
    popd || exit 1
    pushd 'cocos2d-x' || exit 1
    test_git_dirty
    test_file_exists $filename
    popd || exit 1
    clowder clean -a || exit 1
}
clean

forall() {
    local filename='forall_file'
    clowder herd $PARALLEL || exit 1
    pushd 'cocos2d-objc' || exit 1
    test_git_clean
    popd || exit 1
    pushd 'cocos2d-x' || exit 1
    test_git_clean
    popd || exit 1
    clowder forall $PARALLEL -s cocos2d/cocos2d-x -c "touch $filename; git add $filename" || exit 1
    pushd 'cocos2d-objc' || exit 1
    test_git_dirty
    test_file_exists $filename
    popd || exit 1
    pushd 'cocos2d-x' || exit 1
    test_git_clean
    test_no_file_exists $filename
    popd || exit 1
    clowder clean -a || exit 1
}
forall

prune() {
    local branch='prune_branch'
    clowder herd $PARALLEL || exit 1
    pushd 'cocos2d-objc' || exit 1
    git checkout -b $branch
    test_local_branch_exists $branch
    popd || exit 1
    pushd 'cocos2d-x' || exit 1
    git checkout -b $branch
    test_local_branch_exists $branch
    popd || exit 1
    clowder prune $branch -s cocos2d/cocos2d-x
    pushd 'cocos2d-objc' || exit 1
    test_no_local_branch_exists $branch
    popd || exit 1
    pushd 'cocos2d-x' || exit 1
    test_local_branch_exists $branch
    popd || exit 1
    clowder prune $branch || exit 1
}
prune

reset() {
    local cocos2d_objc_commit
    local cocos2d_x_commit
    local cocos2d_x_new_commit
    local filename='reset_file'
    local message='reset commit message'
    pushd 'cocos2d-objc' || exit 1
    cocos2d_objc_commit="$(git rev-parse HEAD)"
    touch $filename || exit 1
    git add $filename || exit 1
    git commit -m "$message" || exit 1
    test_not_commit $cocos2d_objc_commit
    popd || exit 1
    pushd 'cocos2d-x' || exit 1
    cocos2d_x_commit="$(git rev-parse HEAD)"
    touch $filename || exit 1
    git add $filename || exit 1
    git commit -m "$message" || exit 1
    test_not_commit $cocos2d_x_commit
    cocos2d_x_new_commit="$(git rev-parse HEAD)"
    popd || exit 1
    clowder reset $PARALLEL -s cocos2d/cocos2d-x
    pushd 'cocos2d-objc' || exit 1
    test_commit $cocos2d_objc_commit
    popd || exit 1
    pushd 'cocos2d-x' || exit 1
    test_not_commit $cocos2d_x_commit
    test_commit $cocos2d_x_new_commit
    popd || exit 1
    clowder reset $PARALLEL || exit 1
}
reset

start() {
    local branch='start_branch'
    clowder herd $PARALLEL || exit 1
    pushd 'cocos2d-objc' || exit 1
    test_no_local_branch_exists $branch
    popd || exit 1
    pushd 'cocos2d-x' || exit 1
    test_no_local_branch_exists $branch
    popd || exit 1
    clowder start $branch -s cocos2d/cocos2d-x
    pushd 'cocos2d-objc' || exit 1
    test_local_branch_exists $branch
    popd || exit 1
    pushd 'cocos2d-x' || exit 1
    test_no_local_branch_exists $branch
    popd || exit 1
    clowder prune $branch || exit 1
}
start

stash() {
    local filename='stash_file'
    clowder herd $PARALLEL || exit 1
    pushd 'cocos2d-objc' || exit 1
    touch $filename || exit 1
    git add $filename || exit 1
    test_git_dirty
    popd || exit 1
    pushd 'cocos2d-x' || exit 1
    touch $filename || exit 1
    git add $filename || exit 1
    test_git_dirty
    popd || exit 1
    clowder stash -s cocos2d/cocos2d-x || exit 1
    pushd 'cocos2d-objc' || exit 1
    test_git_clean
    test_no_file_exists $filename
    popd || exit 1
    pushd 'cocos2d-x' || exit 1
    test_git_dirty
    test_file_exists $filename
    popd || exit 1
    clowder stash || exit 1
}
stash
