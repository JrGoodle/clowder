#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

print_double_separator
echo 'TEST: swift projects example test script'
print_double_separator

test_clowder_version

"$TEST_SCRIPT_DIR/swift/configure_remotes.sh" || exit 1
"$TEST_SCRIPT_DIR/swift/config_versions.sh" || exit 1
"$TEST_SCRIPT_DIR/swift/reset.sh" $1 || exit 1

test_help() {
    print_double_separator
    cd "$SWIFT_EXAMPLE_DIR" || exit 1
    ./init.sh
    clowder link -v jrgoodle-fork-travis-ci || exit 1
    "$TEST_SCRIPT_DIR/test_help.sh" "$SWIFT_EXAMPLE_DIR" || exit 1
}
test_help
