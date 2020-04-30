#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh || exit 1

print_double_separator
echo "TEST: Test clowder yaml command"

test_clowder_yaml() {
    print_single_separator
    echo "TEST: Test clowder yaml command"

    print_double_separator
    $COMMAND link || exit 1
    $COMMAND yaml || exit 1
    print_single_separator
    $COMMAND yaml -r || exit 1

    # pushd .clowder/versions || exit 1
    # test_cases=( $(ls -d import-*) )
    # popd || exit 1
    # for test in "${test_cases[@]}"
    # do
    #     print_double_separator
    #     $COMMAND link -v $test || exit 1
    #     $COMMAND yaml || exit 1
    #     print_single_separator
    #     $COMMAND yaml -r || exit 1
    # done
}
test_clowder_yaml
