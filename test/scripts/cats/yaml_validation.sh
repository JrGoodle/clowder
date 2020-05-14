#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh

print_double_separator
echo "TEST: Test yaml validation"

test_missing_repo() {
    print_single_separator
    $COMMAND herd
    exit_code=$?
    echo "Expected exit code: $1"
    echo "Actual exit code: $exit_code"
    if [ "$exit_code" != "$1" ]; then
        exit 1
    fi
    print_single_separator
}
test_missing_repo '10'

./init.sh || exit 1

test_missing_yaml() {
    print_single_separator
    rm -f clowder.yaml || exit 1
    $COMMAND herd
    exit_code=$?
    echo "Expected exit code: $1"
    echo "Actual exit code: $exit_code"
    if [ "$exit_code" != "$1" ]; then
        exit 1
    fi
    print_single_separator
}
test_missing_yaml '11'

_test_invalid_yaml() {
    pushd .clowder/versions || exit 1
    test_cases=( $($1) )
    popd || exit 1

    for test in "${test_cases[@]}"
    do
        version=${test%'.clowder.yaml'}
        $COMMAND link -v $version || exit 1
        print_single_separator
        $COMMAND herd
        exit_code=$?
        echo "Expected exit code: $2"
        echo "Actual exit code: $exit_code"
        if [ "$exit_code" != "$2" ]; then
            exit 1
        fi
        print_single_separator
        rm clowder.yaml || exit 1
    done
}

test_invalid_yaml() {
    $COMMAND repo checkout yaml-validation || exit 1
    pushd .clowder || exit 1
    test_branch yaml-validation
    popd || exit 1

    _test_invalid_yaml 'ls -d test-empty.clowder.yaml' '12'
    # _test_open_file '13'
    _test_invalid_yaml 'ls -d test-arg-type*' '14'
    _test_invalid_yaml 'ls -d test-arg-value*' '14'
    _test_invalid_yaml 'ls -d test-empty-*' '14'
    _test_invalid_yaml 'ls -d test-missing*' '14'
    _test_invalid_yaml 'ls -d test-multiple-refs*' '14'
    _test_invalid_yaml 'ls -d test-unknown-arg*' '14'
    _test_invalid_yaml 'ls -d test-duplicate-fork-project-remote*' '15'
    _test_invalid_yaml 'ls -d test-source-not-found*' '16'
    _test_invalid_yaml 'ls -d test-duplicate-project-directories*' '17'

    $COMMAND repo checkout master || exit 1
    pushd .clowder || exit 1
    test_branch master
    popd || exit 1
}
test_invalid_yaml

# TODO: Test all commands requiring @valid_clowder_yaml_required
