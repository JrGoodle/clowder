#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

print_double_separator
echo 'TEST: cats help test script'
print_double_separator

cd "$CATS_EXAMPLE_DIR" || exit 1
./init.sh

test_help() {
    print_double_separator
    ./clean.sh
    ./init.sh || exit 1
    echo "TEST: Print help with invalid clowder.yaml"
    clowder link -v 'test-missing-default-ref' || exit 1
    "$TEST_SCRIPT_DIR/test_help.sh" "$CATS_EXAMPLE_DIR" || exit 1

    print_double_separator
    echo "TEST: Print help with valid clowder.yaml"
    clowder link || exit 1
    clowder herd || exit 1
    clowder status || exit 1
    "$TEST_SCRIPT_DIR/test_help.sh" "$CATS_EXAMPLE_DIR" || exit 1
}
test_help
