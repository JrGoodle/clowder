#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

cd "$CATS_EXAMPLE_DIR" || exit 1

test_command() {
    print_double_separator
    echo "TEST: Clowder command"
    print_single_separator
    echo "TEST: Fail with unrecognized command"
    begin_command
    $COMMAND cat && exit 1
    end_command
    echo "TEST: Fail with no arguments"
    begin_command
    $COMMAND && exit 1
    end_command
    echo ''
}
test_command
