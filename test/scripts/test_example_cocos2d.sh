#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

print_double_separator
echo 'TEST: cocos2d example test script'
print_double_separator

"$TEST_SCRIPT_DIR/cocos2d/protocol.sh" || exit 1
