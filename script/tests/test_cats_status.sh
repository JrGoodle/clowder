#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh
prepare_cats_example
cd "$CATS_EXAMPLE_DIR" || exit 1

print_double_separator
echo "TEST: Test clowder status"

test_status() {
    print_single_separator
    echo "TEST: Test status"
    clowder status -f || exit 1
}
test_status

test_status_fetch() {
    print_single_separator
    echo "TEST: Test status with fetching"
    clowder status -f || exit 1
}
test_status_fetch
