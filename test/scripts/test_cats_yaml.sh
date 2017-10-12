#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh
prepare_cats_example
cd "$CATS_EXAMPLE_DIR" || exit 1

print_double_separator
echo "TEST: Test clowder yaml command"

test_clowder_yaml() {
    print_single_separator
    echo "TEST: Test clowder yaml command"
    pushd .clowder/versions >/dev/null
    test_cases=( $(ls -d import-*) )
    popd >/dev/null

    print_double_separator
    clowder link || exit 1
    clowder yaml || exit 1
    print_single_separator
    clowder yaml -r || exit 1

    for test in "${test_cases[@]}"
    do
        print_double_separator
        clowder link -v $test || exit 1
        clowder yaml || exit 1
        print_single_separator
        clowder yaml -r || exit 1
    done
}
test_clowder_yaml
