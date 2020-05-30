#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh || exit 1
begin_command
$COMMAND herd $PARALLEL || exit 1
end_command

print_double_separator
echo "TEST: Test clowder save"

test_save() {
    print_single_separator
    echo "TEST: Fail linking a previously saved version that doesn't exist"
    begin_command
    $COMMAND link v100 && exit 1
    end_command
    echo "TEST: Fail saving a previously saved version"
    begin_command
    $COMMAND save v0.1 && exit 1
    end_command
    echo "TEST: Fail saving a saved version named 'default'"
    echo "TEST: Try to save version named 'default'"
    begin_command
    $COMMAND save default && exit 1
    end_command
    echo "TEST: Try to save version named 'DEFAULT'"
    begin_command
    $COMMAND save DEFAULT && exit 1
    end_command
    echo "TEST: Successfully save a new version"
    begin_command
    $COMMAND save v0.11 || exit 1
    end_command
    begin_command
    $COMMAND link v0.11 || exit 1
    end_command
    # TODO: Check whether symlink is correct
    echo "TEST: Successfully save version with path separator in input name"
    begin_command
    $COMMAND save path/separator || exit 1
    end_command
    begin_command
    $COMMAND link path-separator || exit 1
    end_command
    # TODO: Check whether symlink is correct
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    begin_command
    $COMMAND status || exit 1
    end_command
}
test_save

test_save_missing_directories() {
    print_single_separator
    echo "TEST: Remove directories"
    rm -rf "$@"
    test_no_directory_exists 'duke'
    test_no_directory_exists 'mu'
    echo "TEST: Fail saving version with missing directories"
    begin_command
    $COMMAND save missing-directories && exit 1
    end_command
    echo ''
}
test_save_missing_directories 'duke' 'mu'

test_save_first_version_no_existing_versions_directory() {
    print_single_separator
    echo "TEST: Test saving first version when versions directory doesn't currently exist"
    ./clean.sh
    begin_command
    $COMMAND init https://github.com/jrgoodle/cats.git -b no-versions || exit 1
    end_command
    test_symlink_path 'clowder.yaml' "$(pwd)/.clowder/clowder.yaml"
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_no_directory_exists '.clowder/versions'
    begin_command
    $COMMAND save first-version || exit 1
    end_command
    test_directory_exists '.clowder/versions'
    test_file_exists '.clowder/versions/first-version.clowder.yml'
    test_no_file_exists 'clowder.yml'
    test_file_exists 'clowder.yaml'
    test_file_is_symlink 'clowder.yaml'
    test_symlink_path 'clowder.yaml' "$(pwd)/.clowder/clowder.yaml"
    begin_command
    $COMMAND link first-version || exit 1
    end_command
    test_no_file_exists 'clowder.yaml'
    test_file_exists 'clowder.yml'
    test_file_is_symlink 'clowder.yml'
    test_symlink_path 'clowder.yml' "$(pwd)/.clowder/versions/first-version.clowder.yml"
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    begin_command
    $COMMAND status || exit 1
    end_command
}
test_save_first_version_no_existing_versions_directory


# TODO: Add tests for saving projects with forks using differnt sources
