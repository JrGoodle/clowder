#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

_create_json_test_files() {
    test_cases=( $($1) )
    for test in "${test_cases[@]}"
    do
        echo "TEST: Generate json from $test"
        modified_test=${test%'.yaml'}
        yaml2json -i "$test" -o "${modified_test}.json" || exit 1
    done
}

_test_invalid_yaml() {
    test_cases=( $($1) )
    for test in "${test_cases[@]}"
    do
        print_single_separator
        echo "TEST: Validate $test"
        jsonschema -i "$test" src/clowder/util/clowder.config.schema.json && exit 1
        print_single_separator
    done
}

_test_valid_yaml() {
    test_cases=( $($1) )
    for test in "${test_cases[@]}"
    do
        print_single_separator
        echo "TEST: Validate $test"
        jsonschema -i "$test" src/clowder/util/clowder.config.schema.json || exit 1
        print_single_separator
    done
}

print_double_separator
echo 'TEST: validate config yaml files'
print_double_separator

pushd '../..' || exit 1

rm -f test/config/*/invalid/*.json

print_single_separator
_create_json_test_files 'ls -d test/config/v0.1/invalid/test-arg-*.yaml'
print_single_separator

_test_invalid_yaml 'ls -d test/config/v0.1/invalid/test-arg-*.json'

print_double_separator

print_single_separator
_create_json_test_files 'ls -d test/config/v0.1/*.yaml'
print_single_separator

_test_valid_yaml 'ls -d test/config/v0.1/*.json'
