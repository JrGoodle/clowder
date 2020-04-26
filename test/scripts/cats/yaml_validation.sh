#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh

print_double_separator
echo "TEST: Test yaml validation"

_test_invalid_yaml() {
    pushd .clowder/versions || exit 1
    test_cases=( $($1) )
    popd || exit 1

    for test in "${test_cases[@]}"
    do
        $COMMAND link -v $test || exit 1
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

    _test_invalid_yaml 'ls -d test-import-loop*' '100'
    _test_invalid_yaml 'ls -d test-duplicate-fork-project-remote*' '101'
    _test_invalid_yaml 'ls -d test-import-missing-group*' '102'
    _test_invalid_yaml 'ls -d test-import-missing-source*' '102'
    _test_invalid_yaml 'ls -d test-missing-default*' '102'
    _test_invalid_yaml 'ls -d test-missing-fork*' '102'
    _test_invalid_yaml 'ls -d test-missing-group*' '102'
    _test_invalid_yaml 'ls -d test-missing-project*' '102'
    _test_invalid_yaml 'ls -d test-missing-source*' '102'
    _test_invalid_yaml 'ls -d test-empty-defaults*' '102'
    _test_invalid_yaml 'ls -d test-empty-fork*' '102'
    _test_invalid_yaml 'ls -d test-empty-group*' '102'
    _test_invalid_yaml 'ls -d test-empty-project*' '102'
    _test_invalid_yaml 'ls -d test-empty-source*' '102'
    _test_invalid_yaml 'ls -d test-import-unknown*' '103'
    _test_invalid_yaml 'ls -d test-unknown*' '103'
    _test_invalid_yaml 'ls -d test-missing-import*' '105'
    _test_invalid_yaml 'ls -d test-import-missing-clowder*' '105'
    _test_invalid_yaml 'ls -d test-empty-import*' '106'
    _test_invalid_yaml 'ls -d test-empty-yaml*' '106'
    _test_invalid_yaml 'ls -d test-arg-value-ref*' '109'
    _test_invalid_yaml 'ls -d test-arg-type-depth*' '111'
    _test_invalid_yaml 'ls -d test-arg-type-defaults*' '112'
    _test_invalid_yaml 'ls -d test-arg-type-fork*' '112'
    _test_invalid_yaml 'ls -d test-arg-type-group*' '112'
    _test_invalid_yaml 'ls -d test-arg-type-import*' '112'
    _test_invalid_yaml 'ls -d test-arg-type-project*' '112'
    _test_invalid_yaml 'ls -d test-arg-type-recursive*' '112'
    _test_invalid_yaml 'ls -d test-arg-type-root*' '112'
    _test_invalid_yaml 'ls -d test-arg-type-source*' '112'
    _test_invalid_yaml 'ls -d test-arg-type-timestamp*' '112'

    $COMMAND repo checkout master || exit 1
    pushd .clowder || exit 1
    test_branch master
    popd || exit 1
}
test_invalid_yaml
