#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

print_double_separator
echo 'TEST: help'
cd "$SWIFT_EXAMPLE_DIR" || exit 1
./init.sh

test_help() {
    $COMMAND link -v jrgoodle-fork-travis-ci || exit 1
    "$TEST_SCRIPT_DIR/test_help.sh" "$SWIFT_EXAMPLE_DIR" || exit 1
}
test_help
