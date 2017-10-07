#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

ACCESS_LEVEL=${1:-read}

print_double_separator
echo 'TEST: cats example test script'
print_double_separator

if [ -z "$TRAVIS_OS_NAME" ]; then
    setup_local_test_directory
fi

"$TEST_SCRIPT_DIR/unittests.sh" || exit 1

cd "$CATS_EXAMPLE_DIR" || exit 1

export projects=( 'black-cats/kit' \
                  'black-cats/kishka' \
                  'black-cats/sasha' \
                  'black-cats/jules' )

test_clowder_version

"$TEST_SCRIPT_DIR/tests/test_cats_init.sh" || exit 1
"$TEST_SCRIPT_DIR/tests/test_command.sh" || exit 1
"$TEST_SCRIPT_DIR/tests/test_cats_branch.sh" || exit 1
"$TEST_SCRIPT_DIR/tests/test_cats_status.sh" || exit 1
"$TEST_SCRIPT_DIR/tests/test_cats_clean.sh" || exit 1
"$TEST_SCRIPT_DIR/tests/test_cats_herd.sh" || exit 1
"$TEST_SCRIPT_DIR/tests/test_cats_herd_branch.sh" || exit 1
"$TEST_SCRIPT_DIR/tests/test_cats_forall.sh" || exit 1
"$TEST_SCRIPT_DIR/tests/test_cats_save.sh" || exit 1
"$TEST_SCRIPT_DIR/tests/test_cats_stash.sh" || exit 1
"$TEST_SCRIPT_DIR/tests/test_cats_link.sh" || exit 1
"$TEST_SCRIPT_DIR/tests/test_cats_yaml_validation.sh" || exit 1
"$TEST_SCRIPT_DIR/tests/test_cats_start.sh" $ACCESS_LEVEL || exit 1
"$TEST_SCRIPT_DIR/tests/test_cats_prune.sh" $ACCESS_LEVEL || exit 1
"$TEST_SCRIPT_DIR/tests/test_cats_repo.sh" $ACCESS_LEVEL || exit 1
"$TEST_SCRIPT_DIR/tests/test_cats_yaml.sh" || exit 1
"$TEST_SCRIPT_DIR/tests/test_cats_import.sh" || exit 1

test_help() {
    print_double_separator
    ./clean.sh
    ./init.sh || exit 1
    echo "TEST: Print help with invalid clowder.yaml"
    clowder link -v 'test-missing-default-ref' || exit 1
    "$TEST_SCRIPT_DIR/tests/test_help.sh" "$CATS_EXAMPLE_DIR" || exit 1

    print_double_separator
    echo "TEST: Print help with valid clowder.yaml"
    clowder link || exit 1
    clowder herd || exit 1
    clowder status || exit 1
    "$TEST_SCRIPT_DIR/tests/test_help.sh" "$CATS_EXAMPLE_DIR" || exit 1
}
test_help
