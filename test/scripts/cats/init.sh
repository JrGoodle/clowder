#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh

print_double_separator
echo "TEST: Test clowder init"

test_init_herd() {
    print_single_separator
    echo "TEST: Normal herd after init"
    "$CATS_EXAMPLE_DIR/clean.sh"
    "$CATS_EXAMPLE_DIR/init.sh"  || exit 1
    clowder herd $PARALLEL || exit 1
    clowder status -f || exit 1
}
test_init_herd

test_init_branch() {
    print_single_separator
    echo "TEST: Test clowder init branch"

    "$CATS_EXAMPLE_DIR/clean.sh"
    clowder init https://github.com/jrgoodle/cats.git -b no-versions || exit 1

    pushd .clowder || exit 1
    test_branch no-versions
    popd || exit 1

    rm -rf .clowder clowder.yaml
}
test_init_branch

test_init_herd_version() {
    print_single_separator
    echo "TEST: Herd version after init"
    "$CATS_EXAMPLE_DIR/clean.sh" || exit 1
    "$CATS_EXAMPLE_DIR/init.sh" || exit 1
    clowder link -v v0.1 || exit 1
    clowder herd $PARALLEL || exit 1
}
test_init_herd_version
