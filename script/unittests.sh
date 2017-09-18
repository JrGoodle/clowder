#!/usr/bin/env bash

# set -xv

echo 'TEST: python unittests test script'

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. tests/test_utilities.sh

if [ -z "$TRAVIS_OS_NAME" ]; then
    setup_local_test_directory
fi

prepare_unittest_repos()
{
    echo 'TEST: Prepare repos for unit tests'
    pushd "$CATS_EXAMPLE_DIR" || exit 1
    # Clean and herd repo's to clean state
    ./clean.sh
    ./init.sh
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
}
prepare_unittest_repos

pushd "$TEST_SCRIPT_DIR/.." || exit 1

echo ''
echo '----------------------------------------------------------------------'
echo 'TEST: Run unittests'
echo ''
python3 test/test_clowder_repo.py "$1" || exit 1
python3 test/test_fork.py "$1" || exit 1
python3 test/test_git_utilities.py "$1" || exit 1
python3 test/test_group.py "$1" || exit 1
python3 test/test_project.py "$1" || exit 1
python3 test/test_source.py "$1" || exit 1

popd

./clean.sh

popd
