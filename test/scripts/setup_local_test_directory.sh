#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

setup_local_test_directory() {
    echo 'Set up local test directory at ~/.clowder_tests'

    echo "Removing existing test files"
    rm -rf "$HOME/.clowder_tests" || exit 1
    mkdir -p "$HOME/.clowder_tests" || exit 1

    cp -a "$EXAMPLES_DIR/cats" "$CATS_EXAMPLE_DIR" || exit 1
    cp -a "$EXAMPLES_DIR/swift-projects" "$SWIFT_EXAMPLE_DIR" || exit 1
    cp -a "$EXAMPLES_DIR/misc" "$MISC_EXAMPLE_DIR" || exit 1
}

if [ -z "$TRAVIS_OS_NAME" ] && [ -z "$CIRCLECI" ]; then
    setup_local_test_directory
fi
