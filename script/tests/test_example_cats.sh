#!/usr/bin/env bash

# set -xv

echo 'TEST: cats example test script'

pushd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

export EXAMPLES_DIR
export TEST_SCRIPT_DIR
export CATS_EXAMPLE_DIR
TEST_SCRIPT_DIR="$(pwd)/.."
EXAMPLES_DIR="$(pwd)/../../examples"

if [ -n "$TRAVIS_OS_NAME" ]; then
    CATS_EXAMPLE_DIR="$(pwd)/../../examples/cats"
    if [ "$TRAVIS_OS_NAME" = "osx" ]; then
        "$TEST_SCRIPT_DIR/unittests.sh" || exit 1
    fi
    cd "$CATS_EXAMPLE_DIR" || exit 1
else
    CATS_EXAMPLE_DIR="$HOME/.clowder_tests/cats"
    rm -rf "$HOME/.clowder_tests"
    mkdir -p "$HOME/.clowder_tests" && cp -r "$EXAMPLES_DIR/cats" "$CATS_EXAMPLE_DIR"
    cd "$CATS_EXAMPLE_DIR" || exit 1
fi

export projects=( 'black-cats/kit' \
                  'black-cats/kishka' \
                  'black-cats/sasha' \
                  'black-cats/jules' )

test_clowder_version

"$TEST_SCRIPT_DIR/tests/test_cats_init.sh"

test_command()
{
    print_separator
    echo "TEST: Fail with unrecognized command"
    clowder cat && exit 1
    echo "TEST: Fail with no arguments"
    clowder && exit 1
    "$CATS_EXAMPLE_DIR/clean.sh" || exit 1
    echo "TEST: Fail herd with missing clowder.yaml"
    clowder herd && exit 1
}
test_command

print_separator
clowder init https://github.com/jrgoodle/cats.git
clowder herd
clowder forall -c 'git checkout -b v0.1'
echo "TEST: Check current branches"
for project in "${projects[@]}"; do
	pushd $project
    test_branch v0.1
    popd
done

test_branches()
{
    print_separator
    echo "TEST: Check current branches are on master"
    clowder herd
    for project in "${projects[@]}"; do
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
test_branches

"$TEST_SCRIPT_DIR/tests/test_cats_status.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_clean.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_herd.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_forall.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_save.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_stash.sh"

test_no_versions()
{
    print_separator
    echo "TEST: Test clowder repo with no versions saved"
    clowder repo checkout no-versions || exit 1
    clowder link -v saved-version && exit 1
    clowder herd || exit 1
    clowder status || exit 1
    clowder repo checkout master || exit 1
}
test_no_versions

"$TEST_SCRIPT_DIR/tests/test_cats_yaml_validation.sh"

test_start()
{
    print_separator
    echo "TEST: Start new branch"
    clowder herd

    clowder start start_branch || exit 1
    # TODO: clowder herd -b
    # clowder herd -b master -g black-cats
    clowder forall -g black-cats -c 'git fetch origin master'
    clowder forall -g black-cats -c 'git checkout master'

    pushd mu
    test_branch start_branch
    popd
    pushd duke
    test_branch start_branch
    popd
    pushd black-cats/jules
    test_branch master
    popd
    pushd black-cats/kishka
    test_branch master
    popd

    clowder start start_branch || exit 1

    pushd black-cats/jules
    test_branch start_branch
    popd
    pushd black-cats/kishka
    test_branch start_branch
    popd
}
test_start

if [ -z "$TRAVIS_OS_NAME" ]; then
    test_start_tracking()
    {
        print_separator
        echo "TEST: Test start tracking branch"
        clowder herd

        echo "TEST: No local or remote branches"
        clowder prune -af tracking_branch || exit 1
        clowder start -t tracking_branch || exit 1

        pushd duke
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd mu
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd black-cats/jules
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd black-cats/kishka
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd

        echo "TEST: Existing local branch checked out, remote tracking branch exists"
        clowder prune -af tracking_branch || exit 1
        clowder start -t tracking_branch || exit 1
        clowder start -t tracking_branch || exit 1

        echo "TEST: Existing local branch not checked out, remote tracking branch exists"
        clowder prune -af tracking_branch || exit 1
        clowder start -t tracking_branch || exit 1
        clowder forall -c 'git checkout master' || exit 1
        clowder start -t tracking_branch || exit 1

        echo "TEST: No local branch, existing remote branch"
        clowder prune -af tracking_branch || exit 1
        clowder start -t tracking_branch || exit 1
        clowder prune -f tracking_branch || exit 1
        clowder start -t tracking_branch && exit 1

        pushd duke
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_no_tracking_branch_exists tracking_branch
        popd
        pushd mu
        test_branch knead
        test_remote_branch_exists tracking_branch
        test_no_tracking_branch_exists tracking_branch
        popd
        pushd black-cats/jules
        test_branch master
        test_remote_branch_exists tracking_branch
        test_no_tracking_branch_exists tracking_branch
        popd
        pushd black-cats/kishka
        test_branch master
        test_remote_branch_exists tracking_branch
        test_no_tracking_branch_exists tracking_branch
        popd

        echo "TEST: Existing local branch checked out, existing remote branch, no tracking relationship"
        clowder prune -af tracking_branch || exit 1
        clowder start -t tracking_branch || exit 1
        clowder prune -f tracking_branch || exit 1
        clowder forall -c 'git checkout -b tracking_branch' || exit 1
        clowder start -t tracking_branch && exit 1

        echo "TEST: Existing local branch not checked out, existing remote branch, no tracking relationship"
        clowder prune -af tracking_branch || exit 1
        clowder start -t tracking_branch || exit 1
        clowder prune -f tracking_branch || exit 1
        clowder forall -c 'git checkout -b tracking_branch' || exit 1
        clowder forall -c 'git checkout master' || exit 1
        clowder start -t tracking_branch && exit 1

        echo "TEST: Existing local branch checked out, no remote branch"
        clowder prune -af tracking_branch
        clowder start tracking_branch || exit 1
        clowder start -t tracking_branch || exit 1

        pushd duke
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd mu
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd black-cats/jules
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd black-cats/kishka
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd

        echo "TEST: Existing local branch not checked out, no remote branch"
        clowder prune -r tracking_branch
        clowder start tracking_branch || exit 1
        clowder forall -c 'git checkout master'
        clowder start -t tracking_branch || exit 1

        pushd duke
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd mu
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd black-cats/jules
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd black-cats/kishka
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
    }
    test_start_tracking
fi

"$TEST_SCRIPT_DIR/tests/test_cats_prune.sh"

test_clowder_repo()
{
    print_separator
    echo "TEST: Test clowder repo command"
    clowder repo checkout ref_that_doesnt_exist && exit 1
    clowder repo add file_that_doesnt_exist && exit 1
}
test_clowder_repo

test_clowder_import()
{
    print_separator
    echo "TEST: Test clowder file with default import"

    clowder link
    clowder herd
    clowder link -v import-default
    clowder herd
    pushd black-cats/jules
    test_branch import-default
    popd
    pushd black-cats/kishka
    test_branch import-default
    popd
    pushd black-cats/kit
    test_branch import-default
    popd
    pushd black-cats/sasha
    test_branch import-default
    popd

    echo "TEST: Test clowder file with version import"
    clowder link
    clowder herd
    clowder link -v import-version
    clowder herd
    pushd black-cats/jules
    test_branch import-version
    popd
    pushd black-cats/kishka
    test_branch import-version
    popd
    pushd black-cats/kit
    test_branch import-version
    popd
    pushd black-cats/sasha
    test_branch import-version
    popd
}
test_clowder_import

test_print()
{
    print_separator

    clowder repo checkout master || exit 1

    clowder link -v 'missing-defaults'
    clowder herd
    "$TEST_SCRIPT_DIR/tests/test_help.sh" "$CATS_EXAMPLE_DIR"

    clowder link
    clowder herd
    "$TEST_SCRIPT_DIR/tests/test_help.sh" "$CATS_EXAMPLE_DIR"
}
test_print

popd
