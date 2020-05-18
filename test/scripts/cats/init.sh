#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

cd "$CATS_EXAMPLE_DIR" || exit 1

print_double_separator
echo "TEST: Test clowder init"

test_init_herd() {
    print_single_separator
    echo "TEST: Normal herd after init"
    ./clean.sh
    ./init.sh  || exit 1
    $COMMAND herd $PARALLEL || exit 1
    $COMMAND status -f || exit 1
}
test_init_herd

test_init_branch() {
    print_single_separator
    echo "TEST: Test clowder init branch"

    ./clean.sh
    $COMMAND init https://github.com/jrgoodle/cats.git -b no-versions || exit 1

    pushd .clowder || exit 1
    test_branch no-versions
    popd || exit 1
}
test_init_branch

test_init_herd_version() {
    print_single_separator
    echo "TEST: Herd version after init"
    ./clean.sh || exit 1
    ./init.sh || exit 1
    $COMMAND link v0.1 || exit 1
    $COMMAND herd $PARALLEL || exit 1
    # FIXME: Test the state of repos after herd
}
test_init_herd_version
