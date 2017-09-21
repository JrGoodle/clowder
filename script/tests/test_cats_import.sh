#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh
prepare_cats_example
cd "$CATS_EXAMPLE_DIR" || exit 1

export black_cats_projects=( 'black-cats/kit' \
                             'black-cats/kishka' \
                             'black-cats/sasha' \
                             'black-cats/jules' )

print_double_separator
echo "TEST: Test clowder file with import"

test_clowder_import_default() {
    print_single_separator
    echo "TEST: Test clowder file with default import"

    clowder link >/dev/null
    clowder herd >/dev/null
    clowder link -v import-default
    clowder herd >/dev/null
    clowder status || exit 1

    for project in "${black_cats_projects[@]}"; do
        pushd $project
        test_branch import-default
        popd
    done
}
test_clowder_import_default

test_clowder_import_version() {
    print_single_separator
    echo "TEST: Test clowder file with version import"
    clowder link >/dev/null
    clowder herd >/dev/null
    clowder link -v import-version
    clowder herd >/dev/null
    clowder status || exit 1

    for project in "${black_cats_projects[@]}"; do
        pushd $project
        test_branch import-version
        popd
    done
}
test_clowder_import_version
