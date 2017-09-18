#!/usr/bin/env bash

pushd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

test_save()
{
    print_separator
    echo "TEST: Fail linking a previously saved version that doesn't exist"
    clowder link -v v100 && exit 1
    echo "TEST: Fail saving a previously saved version"
    clowder save v0.1 && exit 1
    echo "TEST: Successfully save a new version"
    clowder save v0.11 || exit 1
    echo "TEST: Successfully save version with path separator in input name"
    clowder save path/separator
    clowder link -v path-separator || exit 1
    clowder herd || exit 1
    clowder status || exit 1
}
test_save

test_save_missing_directories()
{
    print_separator
    echo "TEST: Remove directories"
    rm -rf "$@"
    echo "TEST: Fail saving version with missing directories"
    clowder save missing-directories && exit 1
}
test_save_missing_directories 'duke' 'mu'

popd
