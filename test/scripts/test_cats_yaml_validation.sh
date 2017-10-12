#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh
prepare_cats_example
cd "$CATS_EXAMPLE_DIR" || exit 1

print_double_separator
echo "TEST: Test yaml validation"

test_invalid_yaml() {
    pushd .clowder/versions || exit 1
    test_cases=( $(ls -d test-*) )
    popd || exit 1

    for test in "${test_cases[@]}"
    do
        clowder link -v $test || exit 1
        print_single_separator
        clowder herd && exit 1
        print_single_separator
        rm clowder.yaml || exit 1
    done
}
test_invalid_yaml
