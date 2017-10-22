#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

print_double_separator
echo "TEST: Test clowder sync"
cd "$LLVM_EXAMPLE_DIR" || exit 1
./init.sh

"$TEST_SCRIPT_DIR/llvm/write_sync.sh" $1 || exit 1
