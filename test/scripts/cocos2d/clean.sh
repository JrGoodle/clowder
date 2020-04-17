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

test_clean_a() {
    print_single_separator
    echo "TEST: Clean all"
    $COMMAND herd $PARALLEL || exit 1
    for project in "${external_projects[@]}"; do
        pushd $project || exit 1
        touch newfile
        mkdir something
        touch something/something
        git checkout -b something || exit 1
        git add newfile something || exit 1
        test_git_dirty
        test_branch something
        test_directory_exists 'something'
        test_file_exists 'something/something'
        test_file_exists 'newfile'
        popd || exit 1
    done
    for project in "${external_projects[@]}"; do
        pushd $project || exit 1
        touch newfile
        mkdir something
        touch something/something
        test_directory_exists 'something'
        test_file_exists 'something/something'
        test_file_exists 'newfile'
        popd || exit 1
    done

    $COMMAND clean -a || exit 1

    for project in "${external_projects[@]}"; do
        pushd $project || exit 1
        test_head_detached
        test_no_directory_exists 'something'
        test_no_file_exists 'something/something'
        test_no_file_exists 'newfile'
        popd || exit 1
    done
    for project in "${external_projects[@]}"; do
        pushd $project || exit 1
        test_no_directory_exists 'something'
        test_no_file_exists 'something/something'
        test_no_file_exists 'newfile'
        git branch -D something
        popd || exit 1
    done
}
test_clean_a

test_clean_submodules_untracked() {
    print_single_separator
    echo "TEST: Clean untracked files in submodules"
    $COMMAND herd $PARALLEL || exit 1
    for project in "${external_projects[@]}"; do
        pushd $project || exit 1
        touch newfile
        mkdir something
        touch something/something
        test_directory_exists 'something'
        test_file_exists 'something/something'
        test_file_exists 'newfile'
        popd || exit 1
    done

    $COMMAND clean -r || exit 1

    for project in "${external_projects[@]}"; do
        pushd $project || exit 1
        test_no_directory_exists 'something'
        test_no_file_exists 'something/something'
        test_no_file_exists 'newfile'
        popd || exit 1
    done
}
test_clean_submodules_untracked

test_clean_submodules_dirty() {
    print_single_separator
    echo "TEST: Clean dirty submodules"
    $COMMAND herd $PARALLEL || exit 1
    for project in "${external_projects[@]}"; do
        pushd $project || exit 1
        touch newfile
        mkdir something
        touch something/something
        git checkout -b something || exit 1
        git add newfile something || exit 1
        test_git_dirty
        test_branch something
        test_directory_exists 'something'
        test_file_exists 'something/something'
        test_file_exists 'newfile'
        popd || exit 1
    done

    $COMMAND clean -r || exit 1

    for project in "${external_projects[@]}"; do
        pushd $project || exit 1
        test_head_detached
        test_no_directory_exists 'something'
        test_no_file_exists 'something/something'
        test_no_file_exists 'newfile'
        git branch -D something
        popd || exit 1
    done
}
test_clean_submodules_dirty
