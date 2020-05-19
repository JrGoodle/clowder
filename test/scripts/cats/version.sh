#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

cd "$CATS_EXAMPLE_DIR" || exit 1

test_clowder_version() {
    print_double_separator
    echo "TEST: Print clowder version"
    begin_command
    $COMMAND --version || exit 1
    end_command
}
test_clowder_version
