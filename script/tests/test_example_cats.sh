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
"$TEST_SCRIPT_DIR/tests/test_command.sh"

"$CATS_EXAMPLE_DIR/clean.sh" || exit 1
echo "TEST: Fail herd with missing clowder.yaml"
clowder herd && exit 1

print_separator
clowder init https://github.com/jrgoodle/cats.git
clowder herd

"$TEST_SCRIPT_DIR/tests/test_cats_status.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_clean.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_herd.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_forall.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_save.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_stash.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_link.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_yaml_validation.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_start.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_prune.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_repo.sh"
"$TEST_SCRIPT_DIR/tests/test_cats_import.sh"

test_help()
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
test_help

popd
