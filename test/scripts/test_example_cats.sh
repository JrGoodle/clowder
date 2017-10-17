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

"$TEST_SCRIPT_DIR/cats/init.sh" || exit 1
"$TEST_SCRIPT_DIR/test_command.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/branch.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/status.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/clean.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/herd.sh" $ACCESS_LEVEL || exit 1
"$TEST_SCRIPT_DIR/cats/herd_parallel.sh" $ACCESS_LEVEL || exit 1
"$TEST_SCRIPT_DIR/cats/herd_branch.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/herd_branch_parallel.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/herd_tag.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/herd_tag_parallel.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/forall.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/save.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/stash.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/link.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/yaml_validation.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/start.sh" $ACCESS_LEVEL || exit 1
"$TEST_SCRIPT_DIR/cats/prune.sh" $ACCESS_LEVEL || exit 1
"$TEST_SCRIPT_DIR/cats/repo.sh" $ACCESS_LEVEL || exit 1
"$TEST_SCRIPT_DIR/cats/reset.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/reset_parallel.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/yaml.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/import.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/help.sh" || exit 1
