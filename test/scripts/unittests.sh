#!/usr/bin/env bash

# set -xv

echo 'TEST: python unittests test script'

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

cd "$TEST_SCRIPT_DIR/../.." || exit 1

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
    pushd black-cats/kishka || exit 1
    touch newfile
    git add .
    popd || exit 1
    # Set sasha repo to detached HEAD state
    pushd black-cats/sasha || exit 1
    git checkout '6ce5538d2c09fda2f56a9ca3859f5e8cfe706bf0'
    popd || exit 1
    popd || exit 1
}
prepare_unittest_repos

echo ''
print_double_separator
echo 'TEST: Run unittests'
echo ''

if [ -n "$TRAVIS_OS_NAME" ]; then
    $PYTHON_VERSION test/unittests/test_clowder_repo.py -v "$CATS_EXAMPLE_DIR" || exit 1
    $PYTHON_VERSION test/unittests/test_fork.py -v "$CATS_EXAMPLE_DIR" || exit 1
    $PYTHON_VERSION test/unittests/test_git_utilities.py -v "$CATS_EXAMPLE_DIR" || exit 1
    $PYTHON_VERSION test/unittests/test_group.py -v "$CATS_EXAMPLE_DIR" || exit 1
    $PYTHON_VERSION test/unittests/test_project.py -v "$CATS_EXAMPLE_DIR" || exit 1
    $PYTHON_VERSION test/unittests/test_source.py -v "$CATS_EXAMPLE_DIR" || exit 1
else
    $PYTHON_VERSION test/unittests/test_clowder_repo.py -v "$CATS_EXAMPLE_DIR" || exit 1
    $PYTHON_VERSION test/unittests/test_fork.py -v "$CATS_EXAMPLE_DIR" || exit 1
    $PYTHON_VERSION test/unittests/test_git_utilities.py -v "$CATS_EXAMPLE_DIR" || exit 1
    $PYTHON_VERSION test/unittests/test_group.py -v "$CATS_EXAMPLE_DIR" || exit 1
    $PYTHON_VERSION test/unittests/test_project.py -v "$CATS_EXAMPLE_DIR" || exit 1
    $PYTHON_VERSION test/unittests/test_source.py -v "$CATS_EXAMPLE_DIR" || exit 1
fi
