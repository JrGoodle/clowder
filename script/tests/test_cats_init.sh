#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh
prepare_cats_example
cd "$CATS_EXAMPLE_DIR" || exit 1

print_separator
echo "TEST: Test clowder init"

test_init_herd() {
    echo "TEST: Normal herd after init"
    "$CATS_EXAMPLE_DIR/clean.sh"
    "$CATS_EXAMPLE_DIR/init.sh"  || exit 1
    clowder herd  || exit 1
    clowder status -f || exit 1
}
test_init_herd

test_init_branch() {
    echo "TEST: Test clowder init branch"

    "$CATS_EXAMPLE_DIR/clean.sh"
    clowder init https://github.com/jrgoodle/cats.git -b tags || exit 1

    pushd .clowder
    test_branch tags
    popd

    rm -rf .clowder clowder.yaml
}
test_init_branch

test_init_herd_version() {
    echo "TEST: Herd version after init"
    "$CATS_EXAMPLE_DIR/clean.sh" || exit 1
    "$CATS_EXAMPLE_DIR/init.sh" || exit 1
    clowder link -v v0.1 || exit 1
    clowder herd || exit 1
}
test_init_herd_version
