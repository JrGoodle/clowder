#!/usr/bin/env bash

pushd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

test_clowder_repo()
{
    print_separator
    echo "TEST: Test clowder repo command"
    clowder repo checkout ref_that_doesnt_exist && exit 1
    clowder repo add file_that_doesnt_exist && exit 1
}
test_clowder_repo

popd
