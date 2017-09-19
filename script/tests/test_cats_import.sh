#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh
prepare_cats_example
cd "$CATS_EXAMPLE_DIR" || exit 1

print_separator
echo "TEST: Test clowder file with import"

test_clowder_import_default() {
    echo "TEST: Test clowder file with default import"

    clowder link >/dev/null
    clowder herd >/dev/null
    clowder link -v import-default
    clowder herd >/dev/null
    clowder status || exit 1
    pushd black-cats/jules
    test_branch import-default
    popd
    pushd black-cats/kishka
    test_branch import-default
    popd
    pushd black-cats/kit
    test_branch import-default
    popd
    pushd black-cats/sasha
    test_branch import-default
    popd
}
test_clowder_import_default

test_clowder_import_version() {
    echo "TEST: Test clowder file with version import"
    clowder link >/dev/null
    clowder herd >/dev/null
    clowder link -v import-version
    clowder herd >/dev/null
    clowder status || exit 1
    pushd black-cats/jules
    test_branch import-version
    popd
    pushd black-cats/kishka
    test_branch import-version
    popd
    pushd black-cats/kit
    test_branch import-version
    popd
    pushd black-cats/sasha
    test_branch import-version
    popd
}
test_clowder_import_version
