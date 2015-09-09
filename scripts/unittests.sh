#! /bin/bash

# set -xv

cd "$( dirname "${BASH_SOURCE[0]}" )"
cd ../examples/cats

prepare_unittest_repos()
{
    # Groom and herd repo's to clean state
    ./breed.sh
    clowder groom
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
cd ../..
python3 -m unittest discover -v
