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

arg='parallel'
"$TEST_SCRIPT_DIR/cats/herd.sh" "$arg" || exit 1
"$TEST_SCRIPT_DIR/cats/herd_branch.sh" "$arg" || exit 1
"$TEST_SCRIPT_DIR/cats/herd_tag.sh" "$arg" || exit 1
"$TEST_SCRIPT_DIR/cats/forall.sh" "$arg" || exit 1
"$TEST_SCRIPT_DIR/cats/reset.sh" "$arg" || exit 1
"$TEST_SCRIPT_DIR/cocos2d/herd.sh" "$arg" || exit 1
"$TEST_SCRIPT_DIR/cocos2d/skip.sh" "$arg" || exit 1
"$TEST_SCRIPT_DIR/test_example_llvm.sh" "$arg" || exit 1
"$TEST_SCRIPT_DIR/swift/reset.sh" "$arg" || exit 1
