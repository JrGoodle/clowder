#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

export cats_projects=( 'duke' 'mu' )

export black_cats_projects=( 'black-cats/kit' \
                             'black-cats/kishka' \
                             'black-cats/sasha' \
                             'black-cats/june' )

export all_projects=( 'mu' 'duke' \
                      'black-cats/kit' \
                      'black-cats/kishka' \
                      'black-cats/sasha' \
                      'black-cats/june' )

test_cats_default_herd_branches() {
    echo "TEST: cats projects on default branches"
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_branch master
        popd || exit 1
    done
    pushd mu || exit 1
    test_branch knead
    popd || exit 1
    pushd duke || exit 1
    test_branch heads/purr
    popd || exit 1
}

test_cats_herd_tag() {
    echo "TEST: cats projects on default branches"
    pushd 'black-cats/kit' || exit 1
    test_head_detached
    test_commit '490f00c63551a6384b64063c210dc08f22426712'
    popd || exit 1
    pushd 'black-cats/kishka' || exit 1
    test_head_detached
    test_commit 'c489dfafe1e0adb7a070e4eedfc20f1c53ecaeb9'
    popd || exit 1
    pushd 'black-cats/sasha' || exit 1
    test_branch master
    popd || exit 1
    pushd 'black-cats/june' || exit 1
    test_branch master
    popd || exit 1
    pushd mu || exit 1
    test_head_detached
    test_commit 'cddce39214a1ae20266d9ee36966de67438625d1'
    popd || exit 1
    pushd duke || exit 1
    test_branch heads/purr
    popd || exit 1
}

print_double_separator
echo "TEST: Test clowder herd tag"
cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh || exit 1

EXISTING_TAG='test-herd-tag'
NO_TAG='test-herd-no-tag'

test_herd_tag_no_repo_existing_tag() {
    print_single_separator
    echo "TEST: Herd tag - No repo, existing remote tag"
    begin_command
    $COMMAND link || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        rm -rf $project
        test_no_directory_exists "$project"
    done
    begin_command
    $COMMAND herd $PARALLEL -t $EXISTING_TAG || exit 1
    end_command
    begin_command
    $COMMAND status || exit 1
    end_command
    test_cats_herd_tag
}
test_herd_tag_no_repo_existing_tag

test_herd_tag_no_repo_no_tag() {
    print_single_separator
    echo "TEST: Herd tag - No repo, no tag"
    begin_command
    $COMMAND link || exit 1
    end_command
    for project in "${all_projects[@]}"; do
        rm -rf $project
        test_no_directory_exists "$project"
    done
    begin_command
    $COMMAND herd $PARALLEL -t $NO_TAG || exit 1
    end_command
    test_cats_default_herd_branches
}
test_herd_tag_no_repo_no_tag

test_herd_tag_existing_tag() {
    print_single_separator
    echo "TEST: Herd tag - Existing tag"
    begin_command
    $COMMAND link || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_cats_default_herd_branches
    begin_command
    $COMMAND herd $PARALLEL -t $EXISTING_TAG || exit 1
    end_command
    begin_command
    $COMMAND status || exit 1
    end_command
    test_cats_herd_tag
}
test_herd_tag_existing_tag

test_herd_tag_no_tag() {
    print_single_separator
    echo "TEST: Herd tag - No existing tag"
    begin_command
    $COMMAND link || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_cats_default_herd_branches
    begin_command
    $COMMAND herd $PARALLEL -t $NO_TAG || exit 1
    end_command
    test_cats_default_herd_branches
}
test_herd_tag_no_tag
