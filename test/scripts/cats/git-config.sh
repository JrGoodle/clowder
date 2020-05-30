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

print_double_separator
echo "TEST: Test clowder git config"

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh || exit 1

test_project_git_config() {
    print_single_separator
    echo "TEST: Custom git config in project"
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command

    echo "TEST: custom project git config alias is not installed"
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        git something && exit 1
        test_no_file_exists 'something'
        popd || exit 1
    done
    pushd mu || exit 1
    git something && exit 1
    test_no_file_exists 'something'
    popd || exit 1
    pushd duke || exit 1
    git something && exit 1
    test_no_file_exists 'something'
    popd || exit 1

    begin_command
    $COMMAND link git-config-project || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command

    echo "TEST: custom project git config alias is installed"
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        git something && exit 1
        test_no_file_exists 'something'
        popd || exit 1
    done
    pushd mu || exit 1
    git something || exit 1
    test_file_exists 'something'
    popd || exit 1
    pushd duke || exit 1
    git something && exit 1
    test_no_file_exists 'something'
    popd || exit 1

    ./clean.sh
    ./init.sh || exit 1

    begin_command
    $COMMAND link git-config-project || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command

    echo "TEST: custom git config alias is installed"
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        git something && exit 1
        test_no_file_exists 'something'
        popd || exit 1
    done
    pushd mu || exit 1
    git something || exit 1
    test_file_exists 'something'
    popd || exit 1
    pushd duke || exit 1
    git something && exit 1
    test_no_file_exists 'something'
    popd || exit 1
}
test_project_git_config

./clean.sh
./init.sh || exit 1

test_defaults_project_git_config() {
    print_single_separator
    echo "TEST: Custom git config inherited from defaults and set in projects"
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command

    echo "TEST: custom git config aliases are not installed"
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        git something && exit 1
        test_no_file_exists 'something'
        git something-else && exit 1
        test_no_file_exists 'something-else'
        popd || exit 1
    done
    pushd mu || exit 1
    git something && exit 1
    test_no_file_exists 'something'
    git something-else && exit 1
    test_no_file_exists 'something-else'
    popd || exit 1
    pushd duke || exit 1
    git something && exit 1
    test_no_file_exists 'something'
    git something-else && exit 1
    test_no_file_exists 'something-else'
    popd || exit 1

    begin_command
    $COMMAND link git-config-defaults || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command

    echo "TEST: custom git config aliases are installed"
    pushd black-cats/kit || exit 1
    git something && exit 1
    test_no_file_exists 'something'
    git something-else || exit 1
    test_file_exists 'something-else'
    popd || exit 1
    pushd black-cats/kishka || exit 1
    git something || exit 1
    test_file_exists 'something'
    git something-else && exit 1
    test_no_file_exists 'something-else'
    popd || exit 1
    pushd black-cats/june || exit 1
    git something || exit 1
    test_file_exists 'something'
    git something-else && exit 1
    test_no_file_exists 'something-else'
    popd || exit 1
    pushd black-cats/sasha || exit 1
    git something || exit 1
    test_file_exists 'something'
    git something-else && exit 1
    test_no_file_exists 'something-else'
    popd || exit 1
    pushd mu || exit 1
    git something && exit 1
    test_no_file_exists 'something'
    git something-else && exit 1
    test_no_file_exists 'something-else'
    popd || exit 1
    pushd duke || exit 1
    git something || exit 1
    test_file_exists 'something'
    git something-else || exit 1
    test_file_exists 'something-else'
    popd || exit 1

    ./clean.sh
    ./init.sh || exit 1

    begin_command
    $COMMAND link git-config-defaults || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command

    echo "TEST: custom git config aliases are installed"
    pushd black-cats/kit || exit 1
    git something && exit 1
    test_no_file_exists 'something'
    git something-else || exit 1
    test_file_exists 'something-else'
    popd || exit 1
    pushd black-cats/kishka || exit 1
    git something || exit 1
    test_file_exists 'something'
    git something-else && exit 1
    test_no_file_exists 'something-else'
    popd || exit 1
    pushd black-cats/june || exit 1
    git something || exit 1
    test_file_exists 'something'
    git something-else && exit 1
    test_no_file_exists 'something-else'
    popd || exit 1
    pushd black-cats/sasha || exit 1
    git something || exit 1
    test_file_exists 'something'
    git something-else && exit 1
    test_no_file_exists 'something-else'
    popd || exit 1
    pushd mu || exit 1
    git something && exit 1
    test_no_file_exists 'something'
    git something-else && exit 1
    test_no_file_exists 'something-else'
    popd || exit 1
    pushd duke || exit 1
    git something || exit 1
    test_file_exists 'something'
    git something-else || exit 1
    test_file_exists 'something-else'
    popd || exit 1
}
test_defaults_project_git_config

./clean.sh
./init.sh || exit 1

test_project_git_herd_alias() {
    print_single_separator
    echo "TEST: Custom git herd config alias in project"
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command

    echo "TEST: Custom git herd config alias in project is installed"
    for project in "${all_projects[@]}"; do
        pushd $project || exit 1
        begin_command
        git herd || exit 1
        end_command
        popd || exit 1
    done

    # TODO: Add test setting projects to a known older state, running 'git herd' on select projects,
    # and validating that only the correct ones have been update
}
test_project_git_herd_alias
