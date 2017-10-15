#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

print_double_separator
echo 'TEST: cats example test script'
print_double_separator

if [ -z "$TRAVIS_OS_NAME" ]; then
    setup_local_test_directory
fi

cd "$CATS_EXAMPLE_DIR" || exit 1

test_clowder_version

"$TEST_SCRIPT_DIR/test_cats_init.sh" || exit 1
"$TEST_SCRIPT_DIR/test_command.sh" || exit 1
"$TEST_SCRIPT_DIR/test_cats_branch.sh" || exit 1
"$TEST_SCRIPT_DIR/test_cats_status.sh" || exit 1
"$TEST_SCRIPT_DIR/test_cats_clean.sh" || exit 1
"$TEST_SCRIPT_DIR/test_cats_herd.sh" $ACCESS_LEVEL || exit 1
"$TEST_SCRIPT_DIR/test_cats_herd_branch.sh" || exit 1
"$TEST_SCRIPT_DIR/test_cats_herd_tag.sh" || exit 1
"$TEST_SCRIPT_DIR/test_cats_forall.sh" || exit 1
"$TEST_SCRIPT_DIR/test_cats_save.sh" || exit 1
"$TEST_SCRIPT_DIR/test_cats_stash.sh" || exit 1
"$TEST_SCRIPT_DIR/test_cats_link.sh" || exit 1
"$TEST_SCRIPT_DIR/test_cats_yaml_validation.sh" || exit 1
"$TEST_SCRIPT_DIR/test_cats_start.sh" $ACCESS_LEVEL || exit 1
"$TEST_SCRIPT_DIR/test_cats_prune.sh" $ACCESS_LEVEL || exit 1
"$TEST_SCRIPT_DIR/test_cats_repo.sh" $ACCESS_LEVEL || exit 1
"$TEST_SCRIPT_DIR/test_cats_reset.sh" || exit 1
"$TEST_SCRIPT_DIR/test_cats_yaml.sh" || exit 1
"$TEST_SCRIPT_DIR/test_cats_import.sh" || exit 1
"$TEST_SCRIPT_DIR/test_cats_help.sh" || exit 1
