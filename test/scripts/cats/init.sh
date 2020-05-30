#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

export black_cats_projects=( 'black-cats/kit' \
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

cd "$CATS_EXAMPLE_DIR" || exit 1

print_double_separator
echo "TEST: Test clowder init"

test_init_herd() {
    print_single_separator
    echo "TEST: Normal herd after init"
    ./clean.sh
    $COMMAND init https://github.com/jrgoodle/cats.git || exit 1
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_cats_default_herd_branches
}
test_init_herd

test_init_branch() {
    print_single_separator
    echo "TEST: Test clowder init branch"
    ./clean.sh
    begin_command
    $COMMAND init https://github.com/jrgoodle/cats.git -b no-versions || exit 1
    end_command
    pushd .clowder || exit 1
    test_branch no-versions
    popd || exit 1
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_cats_default_herd_branches
}
test_init_branch

test_init_herd_version() {
    print_single_separator
    echo "TEST: Herd version after init"
    ./clean.sh || exit 1
    begin_command
    $COMMAND init https://github.com/jrgoodle/cats.git || exit 1
    end_command
    begin_command
    $COMMAND link v0.1 || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    # FIXME: Test the state of repos after herd
}
test_init_herd_version

test_init_existing_empty_clowder_repo_dir() {
    print_single_separator
    echo "TEST: Clowder init successfully with empty .clowder directory present"
    ./clean.sh || exit 1
    mkdir '.clowder' || exit 1
    begin_command
    $COMMAND init https://github.com/jrgoodle/cats.git || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_cats_default_herd_branches
}
test_init_existing_empty_clowder_repo_dir

test_init_existing_non_empty_clowder_repo_dir() {
    print_single_separator
    echo "TEST: Fail init with existing non-empty .clowder directorp present"
    ./clean.sh || exit 1
    mkdir '.clowder' || exit 1
    begin_command
    $COMMAND init https://github.com/jrgoodle/cats.git && exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL && exit 1
    end_command
}
test_init_existing_non_empty_clowder_repo_dir
