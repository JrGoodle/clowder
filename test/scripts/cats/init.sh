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

# test_init_existing_clowder_yaml_symlink_no_clowder_repo_dir() {
#     print_single_separator
#     echo "TEST: Clowder init with existing clowder.yaml symlink file and no existing clowder repo dir"
#     ./clean.sh
#     ./init.sh || exit 1
#     rm -rf .clowder || exit
#     mv 'clowder.yaml' 'clowder.yml' || exit 1
#     test_no_file_exists 'clowder.yaml'
#     test_file_is_symlink 'clowder.yml'
#     test_symlink_path 'clowder.yml' "$(pwd)/.clowder/clowder.yaml"
#     test_no_file_exists 'clowder.yml'
#     test_no_directory_exists '.clowder'
#     begin_command
#     $COMMAND init https://github.com/jrgoodle/cats.git || exit 1
#     end_command
#     test_no_file_exists 'clowder.yml'
#     test_file_is_symlink 'clowder.yaml'
#     test_symlink_path 'clowder.yaml' "$(pwd)/.clowder/clowder.yaml"
#     test_file_exists 'clowder.yaml'
#     test_directory_exists '.clowder'
#     test_directory_exists '.clowder/.git'
#     test_file_exists '.clowder/clowder.yaml'
#     begin_command
#     $COMMAND herd $PARALLEL || exit 1
#     end_command
# }
# test_init_existing_clowder_yaml_symlink_no_clowder_repo_dir

# test_init_existing_ambiguous_clowder_yaml_files_no_clowder_repo_dir() {
#     print_single_separator
#     echo "TEST: Clowder init with ambiguous existing non-symlink clowder.yaml file, existing non-symlink clowder.yml file, and no existing clowder repo dir"
#     ./clean.sh
#     ./init.sh || exit 1
#     rm -f clowder.yaml || exit 1
#     cp .clowder/clowder.yaml clowder.yaml || exit 1
#     cp .clowder/clowder.yaml clowder.yml || exit 1
#     rm -rf .clowder || exit
#     test_file_exists 'clowder.yml'
#     test_file_not_symlink 'clowder.yml'
#     test_file_exists 'clowder.yaml'
#     test_file_not_symlink 'clowder.yaml'
#     test_no_directory_exists '.clowder'
#     begin_command
#     $COMMAND init https://github.com/jrgoodle/cats.git && exit 1
#     end_command
#     test_file_exists 'clowder.yml'
#     test_file_not_symlink 'clowder.yml'
#     test_file_exists 'clowder.yaml'
#     test_file_not_symlink 'clowder.yaml'
#     test_directory_exists '.clowder'
#     test_directory_exists '.clowder/.git'
#     test_file_exists '.clowder/clowder.yaml'
#     begin_command
#     $COMMAND herd $PARALLEL && exit 1
#     end_command
# }
# test_init_existing_ambiguous_clowder_yaml_files_no_clowder_repo_dir

# test_init_existing_ambiguous_clowder_yaml_file_and_symlink_no_clowder_repo_dir() {
#     print_single_separator
#     echo "TEST: Clowder init with ambiguous existing non-symlink clowder.yaml file, existing symlink clowder.yml symlink, and no existing clowder repo dir"
#     ./clean.sh
#     ./init.sh || exit 1
#     $COMMAND link groups || exit 1
#     cp .clowder/clowder.yaml clowder.yml || exit 1
#     rm -rf .clowder || exit
#     test_file_is_symlink 'clowder.yaml'
#     test_symlink_path 'clowder.yaml' "$(pwd)/.clowder/versions/groups.clowder.yaml"
#     test_no_file_exists 'clowder.yaml'
#     test_file_exists 'clowder.yml'
#     test_file_not_symlink 'clowder.yml'
#     test_no_directory_exists '.clowder'
#     begin_command
#     $COMMAND init https://github.com/jrgoodle/cats.git && exit 1
#     end_command
#     test_file_is_symlink 'clowder.yaml'
#     test_symlink_path 'clowder.yaml' "$(pwd)/.clowder/clowder.yaml"
#     test_file_exists 'clowder.yaml'
#     test_file_exists 'clowder.yml'
#     test_file_not_symlink 'clowder.yml'
#     test_directory_exists '.clowder'
#     test_directory_exists '.clowder/.git'
#     test_file_exists '.clowder/clowder.yaml'
#     begin_command
#     $COMMAND herd $PARALLEL && exit 1
#     end_command
# }
# test_init_existing_ambiguous_clowder_yaml_file_and_symlink_no_clowder_repo_dir

test_init_existing_ambiguous_clowder_yaml_symlinks_no_clowder_repo_dir() {
    print_single_separator
    echo "TEST: Clowder init with ambiguous existing clowder.yaml symlinks and no existing clowder repo dir"
    ./clean.sh
    ./init.sh || exit 1
    $COMMAND link groups || exit 1
    cp clowder.yaml clowder.yml || exit 1
    rm -rf .clowder || exit
    test_file_is_symlink 'clowder.yaml'
    test_symlink_path 'clowder.yaml' "$(pwd)/.clowder/versions/groups.clowder.yaml"
    test_no_file_exists 'clowder.yaml'
    test_file_is_symlink 'clowder.yml'
    test_symlink_path 'clowder.yml' "$(pwd)/.clowder/versions/groups.clowder.yaml"
    test_no_file_exists 'clowder.yml'
    test_no_directory_exists '.clowder'
    begin_command
    $COMMAND init https://github.com/jrgoodle/cats.git && exit 1
    end_command
    test_file_is_symlink 'clowder.yaml'
    test_symlink_path 'clowder.yaml' "$(pwd)/.clowder/clowder.yaml"
    test_file_exists 'clowder.yaml'
    test_no_file_exists 'clowder.yml'
    test_no_symlink_exists 'clowder.yml'
    test_directory_exists '.clowder'
    test_directory_exists '.clowder/.git'
    test_file_exists '.clowder/clowder.yaml'
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
}
test_init_existing_ambiguous_clowder_yaml_file_and_symlink_no_clowder_repo_dir

test_init_existing_file_at_clowder_repo_path() {
    print_single_separator
    echo "TEST: Clowder init with existing file at clowder repo path"
    ./clean.sh
    touch '.clowder' || exit 1
    test_file_exists '.clowder'
    test_no_directory_exists '.clowder'
    begin_command
    $COMMAND init https://github.com/jrgoodle/cats.git && exit 1
    end_command
    test_file_exists '.clowder'
    test_no_directory_exists '.clowder'
    begin_command
    $COMMAND herd $PARALLEL && exit 1
    end_command
}
test_init_existing_file_at_clowder_repo_path

test_init_existing_symlink_at_clowder_repo_path() {
    print_single_separator
    echo "TEST: Clowder init with existing valid symlink at clowder repo path"
    ./clean.sh
    ./init.sh || exit 1
    mv '.clowder' 'clowder-symlink-source-dir'  || exit
    rm -f 'clowder.yaml' || exit 1
    ln -s "$(pwd)/clowder-symlink-source-dir" '.clowder'
    test_file_is_symlink '.clowder'
    test_symlink_path '.clowder' "$(pwd)/clowder-symlink-source-dir"
    test_directory_exists 'clowder-symlink-source-dir'
    test_no_file_exists 'clowder.yaml'
    test_file_not_symlink 'clowder.yaml'
    test_no_file_exists 'clowder.yml'
    test_file_not_symlink 'clowder.yml'
    begin_command
    $COMMAND init https://github.com/jrgoodle/cats.git && exit 1
    end_command
    test_file_is_symlink '.clowder'
    test_symlink_path '.clowder' "$(pwd)/clowder-symlink-source-dir"
    test_directory_exists 'clowder-symlink-source-dir'
    test_no_file_exists 'clowder.yaml'
    test_file_not_symlink 'clowder.yaml'
    test_no_file_exists 'clowder.yml'
    test_file_not_symlink 'clowder.yml'
    begin_command
    $COMMAND link || exit 1
    end_command
    test_file_is_symlink '.clowder'
    test_symlink_path '.clowder' "$(pwd)/clowder-symlink-source-dir"
    test_directory_exists 'clowder-symlink-source-dir'
    test_file_exists 'clowder.yaml'
    test_file_is_symlink 'clowder.yaml'
    test_symlink_path 'clowder.yaml' "$(pwd)/.clowder/clowder.yaml"
    test_no_file_exists 'clowder.yml'
    test_file_not_symlink 'clowder.yml'
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
}
test_init_existing_symlink_at_clowder_repo_path
