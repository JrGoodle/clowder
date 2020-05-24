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
./clean.sh
./init.sh || exit 1

print_double_separator
echo "TEST: Test clowder config"

CONFIG_DIR="$HOME/.config/clowder"
CONFIG_FILE="$CONFIG_DIR/clowder.config.yml"
CONFIG_FILE_BACKUP="$CONFIG_FILE.backup"
TEST_CONFIG_FILE="$CLOWDER_PROJECT_DIR/test/config/v0.1/clowder.config.yml"

# If config file already exists, move to backup
if [ -f "$CONFIG_FILE" ]; then
    mv -fv "$CONFIG_FILE" "$CONFIG_FILE_BACKUP" || exit 1
fi

copy_config_file() {
    echo 'Replace placeholder text in test file with current cats example directory'
    perl -pi -e "s:DIRECTORY_PLACEHOLDER:$CATS_EXAMPLE_DIR:g" "$TEST_CONFIG_FILE" || exit 1
    echo 'Config file contents:'
    cat "$TEST_CONFIG_FILE"
    echo "Make config directory if it doesn't exist"
    mkdir -p "$CONFIG_DIR" || exit 1
    echo 'Copy test config file to config directory'
    cp "$TEST_CONFIG_FILE" "$CONFIG_DIR/clowder.config.yml" || exit 1
    echo 'Discard changes to test config file'
    pushd "$CLOWDER_PROJECT_DIR" || exit 1
    git checkout -- "$TEST_CONFIG_FILE" || exit 1
    popd || exit 1
}

restore_config_file() {
    echo 'Restore config backup'
    if [ -f "$CONFIG_FILE_BACKUP" ]; then
        mv -fv "$CONFIG_FILE_BACKUP" "$CONFIG_FILE"
    fi
}

test_config_projects() {
    echo 'TEST: cats config projects'
    print_single_separator

    copy_config_file
    ls -al $HOME/.config
    ls -al $HOME/.config/clowder

    begin_command
    $COMMAND config get parallel || exit 1
    end_command
    begin_command
    $COMMAND config get projects || exit 1
    end_command
    begin_command
    $COMMAND config get protocol || exit 1
    end_command
    begin_command
    $COMMAND config get rebase || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command

    pushd black-cats/kishka || exit 1
    test_branch master
    popd || exit 1
    pushd black-cats/kit || exit 1
    test_branch master
    popd || exit 1
    test_no_directory_exists 'duke'
    test_no_directory_exists 'mu'
    test_no_directory_exists 'black-cats/sasha'
    test_no_directory_exists 'black-cats/june'

    ./clean.sh
    ./init.sh || exit 1

    begin_command
    $COMMAND config clear projects || exit 1
    end_command
    begin_command
    $COMMAND config get || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command

    test_cats_default_herd_branches

    ./clean.sh
    ./init.sh || exit 1

    begin_command
    $COMMAND config set projects mu duke || exit 1
    end_command
    begin_command
    $COMMAND config get || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command

    pushd mu || exit 1
    test_branch knead
    popd || exit 1
    pushd duke || exit 1
    test_branch heads/purr
    popd || exit 1
    test_no_directory_exists 'black-cats'

    ./clean.sh
    ./init.sh || exit 1

    begin_command
    $COMMAND config clear || exit 1
    end_command
    begin_command
    $COMMAND config get || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command

    test_cats_default_herd_branches
}
test_config_projects

# TODO: Add test for linking ssh version but using https protocol config
# test_remote
