#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

export black_cats_projects=( 'black-cats/kit' \
                             'black-cats/kishka' \
                             'black-cats/sasha' \
                             'black-cats/june' )

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh || exit 1

print_double_separator
echo "TEST: Test clowder link"

test_no_versions() {
    print_single_separator
    echo "TEST: Test clowder repo with no versions saved"
    begin_command
    $COMMAND repo checkout no-versions || exit 1
    end_command
    begin_command
    $COMMAND link saved-version && exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    begin_command
    $COMMAND status || exit 1
    end_command
}
test_no_versions

test_link_versions() {
    print_single_separator
    echo "TEST: Test clowder repo link versions"
    begin_command
    $COMMAND repo checkout master || exit 1
    end_command
    begin_command
    $COMMAND link || exit 1
    end_command
    echo "TEST: Check default symlink path"
    test_symlink_path 'clowder.yaml' "$(pwd)/.clowder/clowder.yaml"
    begin_command
    $COMMAND link unknown-version && exit 1
    end_command
    test_symlink_path 'clowder.yaml' "$(pwd)/.clowder/clowder.yaml"
    begin_command
    $COMMAND link tags || exit 1
    end_command
    echo "TEST: Check tags version symlink path"
    test_symlink_path 'clowder.yaml' "$(pwd)/.clowder/versions/tags.clowder.yaml"
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    echo 'TEST: Check actual tag commit refs are correct'
    pushd mu || exit 1
    test_head_detached
    test_tag_commit 'test-clowder-yaml-tag'
    popd || exit 1
    pushd duke || exit 1
    test_head_detached
    test_tag_commit 'purr'
    popd || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_head_detached
        test_tag_commit 'v0.01'
        popd || exit 1
    done
    begin_command
    $COMMAND status || exit 1
    end_command
}
test_link_versions

./clean.sh
./init.sh || exit 1

test_link_source_missing() {
    print_single_separator
    echo "TEST: Test clowder source missing"
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_symlink_path 'clowder.yaml' "$(pwd)/.clowder/clowder.yaml"
    begin_command
    $COMMAND link 'v0.1' || exit 1
    end_command
    test_symlink_path 'clowder.yaml' "$(pwd)/.clowder/versions/v0.1.clowder.yaml"
    begin_command
    $COMMAND repo checkout no-versions || exit 1
    end_command
    test_symlink_path 'clowder.yaml' "$(pwd)/.clowder/versions/v0.1.clowder.yaml"
    begin_command
    $COMMAND status && exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL && exit 1
    end_command
    test_symlink_path 'clowder.yaml' "$(pwd)/.clowder/versions/v0.1.clowder.yaml"
    begin_command
    $COMMAND link || exit 1
    end_command
    test_symlink_path 'clowder.yaml' "$(pwd)/.clowder/clowder.yaml"
    begin_command
    $COMMAND status || exit 1
    end_command
}
test_link_source_missing
