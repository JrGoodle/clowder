#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

print_double_separator
echo 'TEST: parallel tests script'
print_double_separator

"$TEST_SCRIPT_DIR/create_cache.sh" 'cats' || exit 1

"$TEST_SCRIPT_DIR/cats/herd.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/herd_branch.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/herd_tag.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/forall.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/reset.sh" || exit 1
"$TEST_SCRIPT_DIR/cats/herd_submodules.sh" || exit 1
# "$TEST_SCRIPT_DIR/swift/reset.sh" || exit 1
