#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh
$COMMAND herd $PARALLEL || exit 1

print_double_separator
echo "TEST: Test clowder status"

test_status() {
    print_single_separator
    echo "TEST: Test status"
    $COMMAND status || exit 1
}
test_status

test_status_fetch() {
    print_single_separator
    echo "TEST: Test status with fetching"
    $COMMAND status -f || exit 1
}
test_status_fetch
