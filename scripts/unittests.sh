#!/usr/bin/env bash

# set -xv

echo 'TEST: python unittests test script'

cd "$( dirname "${BASH_SOURCE[0]}" )" || exit 1
cd ../examples/cats || exit 1

prepare_unittest_repos()
{
    # Clean and herd repo's to clean state
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

echo 'TEST: Run unittests'
prepare_unittest_repos
cd ../.. || exit 1
python3 -m unittest discover -v

cd examples/cats || exit 1
./clean.sh
