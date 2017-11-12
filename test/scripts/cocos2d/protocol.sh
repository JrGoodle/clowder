#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

"$TEST_SCRIPT_DIR/cocos2d/ssh_protocol.sh" || exit 1
