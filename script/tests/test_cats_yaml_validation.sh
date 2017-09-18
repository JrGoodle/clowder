#!/usr/bin/env bash

pushd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

test_invalid_yaml()
{
    print_separator
    echo "TEST: Fail herd with invalid yaml"

    pushd .clowder/versions
    test_cases=( $(ls -d test-*) )
    popd

    for test in "${test_cases[@]}"
    do
        clowder link -v $test || exit 1
        print_separator
        clowder herd && exit 1
        print_separator
        rm clowder.yaml
    done
}
test_invalid_yaml

popd
