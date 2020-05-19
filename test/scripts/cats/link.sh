#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh || exit 1

print_double_separator
echo "TEST: Test clowder link"

test_no_versions() {
    print_single_separator
    echo "TEST: Test clowder repo with no versions saved"
    begin_command
    $COMMAND repo checkout no-versions || exit 1
    end_command
    begin_command
    $COMMAND link saved-version && exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    begin_command
    $COMMAND status || exit 1
    end_command
    begin_command
    $COMMAND repo checkout master || exit 1
    end_command
}
test_no_versions

# TODO: Add test where linking version succeeds and check symlink
