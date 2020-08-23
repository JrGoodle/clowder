#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh || exit 1

print_double_separator

test_clowder_yaml() {
    print_single_separator
    echo "TEST: Test clowder yaml command"

    print_double_separator
    begin_command
    $COMMAND link || exit 1
    end_command
    begin_command
    $COMMAND yaml || exit 1
    end_command
    begin_command
    $COMMAND yaml -r && exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    begin_command
    $COMMAND yaml -r || exit 1
    end_command
    begin_command
    $COMMAND yaml -f || exit 1
    end_command
}
test_clowder_yaml

test_clowder_yaml_contents() {
    print_single_separator
    echo "TEST: Test clowder yaml command contents"

    unset CLOWDER_DEBUG
    print_double_separator

    test_output=$(cat clowder-yaml.txt)
    command_output=$($COMMAND yaml)
    test_strings_equal "$test_output" "$command_output"

    # FIXME: Fix printing resolved yaml
    # test_output=$(cat clowder-yaml-r.txt)
    # command_output=$($COMMAND yaml -r)
    # test_strings_equal "$test_output" "$command_output"

    test_output=$(cat clowder-yaml-f.txt)
    command_output=$($COMMAND yaml -f)
    test_strings_equal "$test_output" "$command_output"

    export CLOWDER_DEBUG='true'
}
test_clowder_yaml_contents

test_clowder_yml_extension() {
    print_single_separator
    echo "TEST: clowder yaml file extension"
    ./clean.sh
    begin_command
    $COMMAND init https://github.com/jrgoodle/cats.git -b extension || exit 1
    end_command

    test_no_file_exists 'clowder.yaml'
    test_file_exists 'clowder.yml'
    test_symlink_path 'clowder.yml' "$(pwd)/.clowder/clowder.yml"

    begin_command
    $COMMAND link tags || exit 1
    end_command

    test_no_file_exists 'clowder.yml'
    test_file_exists 'clowder.yaml'
    test_symlink_path 'clowder.yaml' "$(pwd)/.clowder/versions/tags.clowder.yaml"

    begin_command
    $COMMAND link || exit 1
    end_command

    test_no_file_exists 'clowder.yaml'
    test_file_exists 'clowder.yml'
    test_symlink_path 'clowder.yml' "$(pwd)/.clowder/clowder.yml"
}
test_clowder_yml_extension

test_duplicate_versions() {
    print_single_separator
    echo "TEST: Duplicate versions"
    ./clean.sh
    begin_command
    $COMMAND init https://github.com/jrgoodle/cats.git -b duplicate-versions || exit 1
    end_command

    begin_command
    $COMMAND link duplicate-version && exit 1
    end_command
}
test_duplicate_versions

test_duplicate_symlinks() {
    print_single_separator
    echo "TEST: Duplicate symlinks"
    ./clean.sh
    begin_command
    $COMMAND init https://github.com/jrgoodle/cats.git -b extension || exit 1
    end_command

    ln -s "$(pwd)/.clowder/versions/tags.clowder.yaml" 'clowder.yaml'
    test_file_exists 'clowder.yml'
    test_symlink_path 'clowder.yml' "$(pwd)/.clowder/clowder.yml"
    test_file_exists 'clowder.yaml'
    test_symlink_path 'clowder.yaml' "$(pwd)/.clowder/versions/tags.clowder.yaml"

    begin_command
    $COMMAND status && exit 1
    end_command
}
test_duplicate_symlinks
