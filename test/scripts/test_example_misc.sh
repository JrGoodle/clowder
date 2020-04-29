#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

print_double_separator
echo 'TEST: misc examples test script'
print_double_separator

"$TEST_SCRIPT_DIR/misc/sources.sh" || exit 1
# "$TEST_SCRIPT_DIR/misc/forks.sh" || exit 1
