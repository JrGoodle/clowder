#!/usr/bin/env bash

# set -xv

echo 'TEST: python unittests test script'

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. tests/test_utilities.sh

if [ -z "$TRAVIS_OS_NAME" ]; then
    setup_local_test_directory
fi

prepare_unittest_repos() {
    print_single_separator
    echo 'TEST: Prepare repos for unit tests'
    pushd "$CATS_EXAMPLE_DIR" || exit 1
    # Clean and herd repo's to clean state
    $CATS_EXAMPLE_DIR/clean.sh
    $CATS_EXAMPLE_DIR/init.sh
    clowder clean
    clowder herd
    # Remove jules repository
    rm -rf black-cats/jules
    # Make kishka repo dirty
    pushd black-cats/kishka &>/dev/null
    touch newfile
    git add .
    popd &>/dev/null
    # Set sasha repo to detached HEAD state
    pushd black-cats/sasha &>/dev/null
    git checkout '6ce5538d2c09fda2f56a9ca3859f5e8cfe706bf0'
    popd &>/dev/null
    popd
}
prepare_unittest_repos

cd "$TEST_SCRIPT_DIR/.." || exit 1

echo ''
print_double_separator
echo 'TEST: Run unittests'
echo ''

if [ -n "$TRAVIS_OS_NAME" ]; then
    python3 test/test_clowder_repo.py || exit 1
    python3 test/test_fork.py || exit 1
    python3 test/test_git_utilities.py || exit 1
    python3 test/test_group.py || exit 1
    python3 test/test_project.py || exit 1
    python3 test/test_source.py || exit 1
else
    python3 test/test_clowder_repo.py "$CATS_EXAMPLE_DIR" || exit 1
    python3 test/test_fork.py "$CATS_EXAMPLE_DIR" || exit 1
    python3 test/test_git_utilities.py "$CATS_EXAMPLE_DIR" || exit 1
    python3 test/test_group.py "$CATS_EXAMPLE_DIR" || exit 1
    python3 test/test_project.py "$CATS_EXAMPLE_DIR" || exit 1
    python3 test/test_source.py "$CATS_EXAMPLE_DIR" || exit 1
fi

$CATS_EXAMPLE_DIR/clean.sh
