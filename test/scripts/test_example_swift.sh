#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

print_double_separator
echo 'TEST: swift projects example test script'
print_double_separator

"$TEST_SCRIPT_DIR/swift/configure_remotes.sh" || exit 1
"$TEST_SCRIPT_DIR/swift/config_versions.sh" || exit 1
"$TEST_SCRIPT_DIR/swift/reset.sh" || exit 1
