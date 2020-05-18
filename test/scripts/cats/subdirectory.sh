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
./init.sh || exit 1
$COMMAND herd $PARALLEL || exit 1

test_init_existing_clowder() {
    print_single_separator
    echo "TEST: Fail init with existing .clowder directory in current working directory"
    $COMMAND init https://github.com/jrgoodle/cats.git && exit 1
}
test_init_existing_clowder

test_init_existing_clowder_parent() {
    print_single_separator
    echo "TEST: Successfully init with existing .clowder directory in parent directory"
    pushd mu || exit 1
    $COMMAND init https://github.com/jrgoodle/cats.git || exit 1
    $COMMAND herd $PARALLEL || exit 1
    test_cats_default_herd_branches
    # !! Move coverage files to root and clean so further commands work
    cp -a .coverage* ../
    rm -rf .coverage*
    # !!
    popd || exit 1
}
test_init_existing_clowder_parent

./clean.sh
./init.sh || exit 1
$COMMAND herd $PARALLEL || exit 1

test_forall_environment_subdirectory() {
    print_single_separator
    echo "TEST: Check that forall environment variables are set correctly when invoked from subdirectory"
    pushd mu || exit 1
    $COMMAND forall $PARALLEL "jrgoodle/duke" -c "$TEST_SCRIPT_DIR/test_forall_script_env_duke.sh" || exit 1
    # !! Move coverage files to root and clean so further commands work
    cp -a .coverage* ../
    rm -rf .coverage*
    # !!
    popd || exit 1
    pushd black-cats/kit || exit 1
    $COMMAND forall $PARALLEL "jrgoodle/duke" -c "$TEST_SCRIPT_DIR/test_forall_script_env_duke.sh" || exit 1
    # !! Move coverage files to root and clean so further commands work
    cp -a .coverage* ../../
    rm -rf .coverage*
    # !!
    popd || exit 1
}
test_forall_environment_subdirectory

./clean.sh
./init.sh || exit 1
$COMMAND herd $PARALLEL || exit 1

test_commands_subdirectory() {
    print_single_separator
    echo "TEST: Check that various commands work when invoked from subdirectory"
    pushd mu || exit 1
    $COMMAND branch || exit 1
    $COMMAND status || exit 1
    $COMMAND link v0.1 || exit 1
    $COMMAND link || exit 1
    test_no_local_branch_exists 'subdir-branch'
    # !! Move coverage files to root and clean so further commands work
    cp -a .coverage* ../
    rm -rf .coverage*
    # !!
    $COMMAND start 'subdir-branch' 'jrgoodle/mu' || exit 1
    test_local_branch_exists 'subdir-branch'
    # !! Move coverage files to root and clean so further commands work
    cp -a .coverage* ../
    rm -rf .coverage*
    # !!
    $COMMAND prune 'subdir-branch' 'jrgoodle/mu' || exit 1
    test_no_local_branch_exists 'subdir-branch'
    # !! Move coverage files to root and clean so further commands work
    cp -a .coverage* ../
    rm -rf .coverage*
    # !!
    popd || exit 1
    pushd duke || exit 1
    test_no_local_branch_exists 'subdir-branch'
    popd || exit 1
    pushd black-cats/kit || exit 1
    $COMMAND branch || exit 1
    $COMMAND status || exit 1
    $COMMAND link v0.1 || exit 1
    $COMMAND link || exit 1
    test_no_local_branch_exists 'subdir-branch'
    # !! Move coverage files to root and clean so further commands work
    cp -a .coverage* ../../
    rm -rf .coverage*
    # !!
    $COMMAND start 'subdir-branch' || exit 1
    test_local_branch_exists 'subdir-branch'
    # !! Move coverage files to root and clean so further commands work
    cp -a .coverage* ../../
    rm -rf .coverage*
    # !!
    popd || exit 1
    pushd duke || exit 1
    test_local_branch_exists 'subdir-branch'
    popd || exit 1
}
test_commands_subdirectory

# TODO: Test reset

# TODO: Test clean

# TODO: Test checkout

# TODO: Test herd
