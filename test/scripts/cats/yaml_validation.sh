#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh

print_double_separator
echo "TEST: Test yaml validation"

test_missing_repo() {
    print_single_separator
    begin_command
    $COMMAND herd # Get exit code after completions
    local exit_code=$?
    end_command
    echo "Expected exit code: $1"
    echo "Actual exit code: $exit_code"
    if [ "$exit_code" != "$1" ]; then
        exit 1
    fi
    print_single_separator
}
test_missing_repo '42'

./init.sh || exit 1

test_missing_yaml() {
    print_single_separator
    rm -f clowder.yaml || exit 1
    begin_command
    $COMMAND herd # Get exit code after completions
    local exit_code=$?
    end_command
    echo "Expected exit code: $1"
    echo "Actual exit code: $exit_code"
    if [ "$exit_code" != "$1" ]; then
        exit 1
    fi
    print_single_separator
}
test_missing_yaml '43'

_test_invalid_yaml() {
    pushd "$CATS_EXAMPLE_DIR/.clowder/versions" || exit 1
    local test_cases=( $($1 || exit 1) )
    popd || exit 1
    for test in "${test_cases[@]}"
    do
        echo "TEST: Validate $test"
        local version=${test%'.clowder.yaml'}
        begin_command
        $COMMAND link $version || exit 1
        end_command
        print_single_separator
        begin_command
        $COMMAND herd # Get exit code after completions
        local exit_code=$?
        end_command
        echo "Expected exit code: $2"
        echo "Actual exit code: $exit_code"
        if [ "$exit_code" != "$2" ]; then
            exit 1
        fi
        print_single_separator
        rm -f clowder.yaml || exit 1
        rm -f clowder.yml || exit 1
    done
}

test_invalid_yaml() {
    begin_command
    $COMMAND repo checkout yaml-validation || exit 1
    end_command
    pushd .clowder || exit 1
    test_branch yaml-validation
    popd || exit 1

    _test_invalid_yaml 'ls -d test-empty.clowder.yaml' '44'
    # _test_open_file '45'
    _test_invalid_yaml 'ls -d test-arg-type*' '46'
    _test_invalid_yaml 'ls -d test-arg-value*' '46'
    _test_invalid_yaml 'ls -d test-empty-*' '46'
    _test_invalid_yaml 'ls -d test-missing*' '46'
    _test_invalid_yaml 'ls -d test-multiple-refs*' '46'
    _test_invalid_yaml 'ls -d test-unknown-arg*' '46'
    _test_invalid_yaml 'ls -d test-duplicate-fork-project-remote*' '47'
    _test_invalid_yaml 'ls -d test-source-not-found*' '48'
    _test_invalid_yaml 'ls -d test-duplicate-project-directories*' '49'

    begin_command
    $COMMAND repo checkout master || exit 1
    end_command
    pushd .clowder || exit 1
    test_branch master
    popd || exit 1
}
test_invalid_yaml

# TODO: Test all commands requiring @valid_clowder_yaml_required
