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
"$TEST_SCRIPT_DIR/tests/test_cats_start.sh"
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
