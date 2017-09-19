#!/usr/bin/env bash

# set -xv

print_double_separator
echo 'TEST: cats example test script'
print_double_separator

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

if [ -n "$TRAVIS_OS_NAME" ]; then
    if [ "$TRAVIS_OS_NAME" = "osx" ]; then
        "$TEST_SCRIPT_DIR/unittests.sh" || exit 1
    fi
else
    setup_local_test_directory
    "$TEST_SCRIPT_DIR/unittests.sh" || exit 1
fi

cd "$CATS_EXAMPLE_DIR" || exit 1

export projects=( 'black-cats/kit' \
                  'black-cats/kishka' \
                  'black-cats/sasha' \
                  'black-cats/jules' )

test_clowder_version

"$TEST_SCRIPT_DIR/tests/test_cats_init.sh"
"$TEST_SCRIPT_DIR/tests/test_command.sh"
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

test_help() {
    print_double_separator
    echo "TEST: Print help with invalid clowder.yaml"
    clowder repo checkout master || exit 1
    clowder link -v 'missing-defaults' >/dev/null
    clowder herd >/dev/null
    clowder status || exit 1
    "$TEST_SCRIPT_DIR/tests/test_help.sh" "$CATS_EXAMPLE_DIR"

    print_double_separator
    echo "TEST: Print help with valid clowder.yaml"
    clowder link >/dev/null
    clowder herd >/dev/null
    clowder status || exit 1
    "$TEST_SCRIPT_DIR/tests/test_help.sh" "$CATS_EXAMPLE_DIR"
}
test_help
