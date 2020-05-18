#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh || exit 1
begin_command
$COMMAND herd $PARALLEL || exit 1
end_command

export black_cats_projects=( 'black-cats/kit' \
                             'black-cats/kishka' \
                             'black-cats/sasha' \
                             'black-cats/june' )

export all_projects=( 'mu' 'duke' \
                      'black-cats/kit' \
                      'black-cats/kishka' \
                      'black-cats/sasha' \
                      'black-cats/june' )

print_double_separator
echo "TEST: Test clowder prune"

test_prune() {
    print_single_separator
    echo "TEST: Test clowder prune branch"

    begin_command
    $COMMAND start prune_branch || exit 1
    end_command

    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_branch prune_branch
        popd || exit 1
    done

    begin_command
    $COMMAND prune -f prune_branch || exit 1
    end_command

    pushd duke || exit 1
    test_branch purr
    test_no_local_branch_exists prune_branch
    popd || exit 1
    pushd mu || exit 1
    test_branch knead
    test_no_local_branch_exists prune_branch
    popd || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_branch master
        test_no_local_branch_exists prune_branch
        popd || exit 1
    done

    begin_command
    $COMMAND start prune_branch >/dev/null
    end_command

    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_branch prune_branch
        popd || exit 1
    done

    begin_command
    $COMMAND prune -f prune_branch jrgoodle/kit jrgoodle/kishka || exit 1
    end_command

    pushd black-cats/kit || exit 1
    test_branch master
    test_no_local_branch_exists prune_branch
    popd || exit 1
    pushd black-cats/kishka || exit 1
    test_branch master
    test_no_local_branch_exists prune_branch
    popd || exit 1

    begin_command
    $COMMAND prune -f prune_branch black-cats || exit 1
    end_command

    pushd duke || exit 1
    test_branch prune_branch
    popd || exit 1
    pushd mu || exit 1
    test_branch prune_branch
    popd || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_branch master
        test_no_local_branch_exists prune_branch
        popd || exit 1
    done
}
test_prune

test_prune_force() {
    print_single_separator
    echo "TEST: Test clowder force prune branch"

    begin_command
    $COMMAND start prune_branch || exit 1
    end_command

    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_branch prune_branch
        touch something >/dev/null
        git add something >/dev/null
        git commit -m 'something' >/dev/null
        popd || exit 1
    done

    begin_command
    $COMMAND prune prune_branch && exit 1
    end_command

    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        test_local_branch_exists prune_branch
        popd || exit 1
    done

    begin_command
    $COMMAND prune -f prune_branch || exit 1
    end_command

    pushd duke || exit 1
    test_branch purr
    test_no_local_branch_exists prune_branch
    popd || exit 1
    pushd mu || exit 1
    test_branch knead
    test_no_local_branch_exists prune_branch
    popd || exit 1
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_branch master
        test_no_local_branch_exists prune_branch
        popd || exit 1
    done
}
test_prune_force

if [ "$ACCESS_LEVEL" == "write" ]; then
    "$TEST_SCRIPT_DIR/cats/write_prune.sh"
fi
