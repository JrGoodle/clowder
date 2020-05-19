#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh || exit 1
begin_command
$COMMAND herd $PARALLEL || exit 1
end_command

print_double_separator
echo "TEST: Test clowder status"

test_status() {
    print_single_separator
    echo "TEST: Test status"
    begin_command
    $COMMAND status || exit 1
    end_command
}
test_status

test_status_fetch() {
    print_single_separator
    echo "TEST: Test status with fetching"
    begin_command
    $COMMAND status -f || exit 1
    end_command
}
test_status_fetch

test_status_groups() {
    print_single_separator
    echo "TEST: Test status groups"
    begin_command
    $COMMAND status black-cats || exit 1
    end_command
}
test_status_groups
