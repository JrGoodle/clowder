#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh

export all_projects=( 'mu' 'duke' \
                      'black-cats/kit' \
                      'black-cats/kishka' \
                      'black-cats/sasha' \
                      'black-cats/june' )

export black_cats_projects=( 'black-cats/kit' \
                             'black-cats/kishka' \
                             'black-cats/sasha' \
                             'black-cats/june' )

test_cats_default_herd_branches() {
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_branch master
        popd || exit 1
    done
    pushd mu || exit 1
    test_branch knead
    popd || exit 1
    pushd duke || exit 1
    test_branch purr
    popd || exit 1
}

print_double_separator
echo "TEST: Test clowder file with import"

test_clowder_import_default() {
    print_single_separator
    echo "TEST: Test clowder file with default import"

    $COMMAND link || exit 1
    $COMMAND herd $PARALLEL || exit 1
    $COMMAND link -v import-default || exit 1
    $COMMAND herd $PARALLEL || exit 1
    $COMMAND status || exit 1

    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_branch import-default
        popd || exit 1
    done
}
test_clowder_import_default

test_clowder_import_version() {
    print_single_separator
    echo "TEST: Test clowder file with version import"
    $COMMAND link || exit 1
    $COMMAND herd $PARALLEL || exit 1
    $COMMAND link -v import-version || exit 1
    $COMMAND herd $PARALLEL || exit 1
    $COMMAND status || exit 1

    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_branch import-version
        popd || exit 1
    done
}
test_clowder_import_version

test_clowder_import_override_group_ref() {
    print_single_separator
    echo "TEST: Test clowder file import overriding group ref"
    $COMMAND link || exit 1
    $COMMAND herd $PARALLEL || exit 1
    test_cats_default_herd_branches
    $COMMAND link -v import-override-group-ref || exit 1
    $COMMAND herd $PARALLEL || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_branch import-group-branch
        popd || exit 1
    done
    pushd mu || exit 1
    test_branch knead
    popd || exit 1
    pushd duke || exit 1
    test_branch purr
    popd || exit 1
}
test_clowder_import_override_group_ref

test_clowder_import_override_project_ref() {
    print_single_separator
    echo "TEST: Test clowder file import overriding project ref"
    $COMMAND link || exit 1
    $COMMAND herd $PARALLEL || exit 1
    test_cats_default_herd_branches
    $COMMAND link -v import-project-ref || exit 1
    $COMMAND herd $PARALLEL || exit 1
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_branch master
        popd || exit 1
    done
}
test_clowder_import_override_project_ref

test_clowder_import_add_project_to_group() {
    print_single_separator
    echo "TEST: Test clowder file import adding new project to existing group"
    $COMMAND link || exit 1
    $COMMAND herd $PARALLEL || exit 1
    test_cats_default_herd_branches
    $COMMAND link -v import-add-project-to-group || exit 1
    $COMMAND herd $PARALLEL -g cats || exit 1
    test_cats_default_herd_branches
    pushd ash || exit 1
    test_branch master
    popd || exit 1
    rm -rf ash || exit 1
}
test_clowder_import_add_project_to_group

test_clowder_import_add_new_group() {
    print_single_separator
    echo "TEST: Test clowder file import adding new group"
    $COMMAND link || exit 1
    $COMMAND herd $PARALLEL || exit 1
    test_cats_default_herd_branches
    $COMMAND link -v import-add-group || exit 1
    $COMMAND herd $PARALLEL -g rip || exit 1
    test_cats_default_herd_branches
    pushd ash || exit 1
    test_branch master
    popd || exit 1
    rm -rf ash || exit 1
}
test_clowder_import_add_new_group

test_clowder_import_recursive_override_project_ref() {
    print_single_separator
    echo "TEST: Test clowder file recursive import overriding project ref"
    $COMMAND link || exit 1
    $COMMAND herd $PARALLEL || exit 1
    test_cats_default_herd_branches
    $COMMAND link -v import-recursive-project-ref || exit 1
    $COMMAND herd $PARALLEL || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_branch master
        popd || exit 1
    done
    pushd mu || exit 1
    test_branch recursive-import
    popd || exit 1
    pushd duke || exit 1
    test_branch purr
    popd || exit 1
}
test_clowder_import_recursive_override_project_ref

test_clowder_import_recursive_add_project_to_group() {
    print_single_separator
    echo "TEST: Test clowder file recursive import adding new project to existing group"
    $COMMAND link || exit 1
    $COMMAND herd $PARALLEL || exit 1
    test_cats_default_herd_branches
    $COMMAND link -v import-recursive-add-project-to-group || exit 1
    $COMMAND herd $PARALLEL -g cats || exit 1
    test_cats_default_herd_branches
    pushd ash || exit 1
    test_branch recursive-import
    popd || exit 1
    rm -rf ash || exit 1
}
test_clowder_import_recursive_add_project_to_group

test_clowder_import_recursive_add_new_group() {
    print_single_separator
    echo "TEST: Test clowder file recursive import adding new group"
    $COMMAND link || exit 1
    $COMMAND herd $PARALLEL || exit 1
    test_cats_default_herd_branches
    $COMMAND link -v import-recursive-add-group || exit 1
    $COMMAND herd $PARALLEL -g rip || exit 1
    test_cats_default_herd_branches
    pushd ash || exit 1
    test_branch recursive-import
    popd || exit 1
    rm -rf ash || exit 1
}
test_clowder_import_recursive_add_new_group

test_clowder_import_recursive_override_default() {
    print_single_separator
    echo "TEST: Test clowder file recursive import overriding default"
    $COMMAND link || exit 1
    $COMMAND herd $PARALLEL || exit 1
    test_cats_default_herd_branches
    $COMMAND link -v import-recursive-default || exit 1
    $COMMAND herd $PARALLEL || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_branch recursive-import
        popd || exit 1
    done
    pushd mu || exit 1
    test_branch knead
    popd || exit 1
    pushd duke || exit 1
    test_branch purr
    popd || exit 1
}
test_clowder_import_recursive_override_default
