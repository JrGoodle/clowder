#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh
prepare_cats_example
cd "$CATS_EXAMPLE_DIR" || exit 1

export black_cats_projects=( 'black-cats/kit' \
                             'black-cats/kishka' \
                             'black-cats/sasha' \
                             'black-cats/jules' )

print_double_separator
echo "TEST: Test clowder forall"

test_forall_branches() {
    print_single_separator
    clowder forall -c 'git checkout -b v0.1' || exit 1
    echo "TEST: Check current branches"
    for project in "${black_cats_projects[@]}"; do
    	pushd $project
        test_branch v0.1
        popd
    done
}
test_forall_branches

test_forall_command() {
    print_single_separator
    echo "TEST: Run forall command"
    clowder forall -c 'git status' || exit 1
    echo "TEST: Run forall command for specific groups"
    clowder forall -c 'git status' -g "$@" || exit 1
    echo "TEST: Run forall command with error"
    clowder forall -c 'exit 1' && exit 1
    echo "TEST: Run forall command with --ignore-error"
    clowder forall -ic 'exit 1' || exit 1
}
test_forall_command 'cats'

test_forall_script() {
    print_single_separator
    echo "TEST: Run forall script"
    clowder forall -c "$TEST_SCRIPT_DIR/test_forall_script.sh" || exit 1
    echo "TEST: Run forall script for specific groups"
    clowder forall -c "$TEST_SCRIPT_DIR/test_forall_script.sh" -g "$@" || exit 1
    echo "TEST: Run forall script with error"
    clowder forall -c "$TEST_SCRIPT_DIR/test_forall_script_error.sh" && exit 1
    echo "TEST: Run forall script with --ignore-error"
    clowder forall -ic "$TEST_SCRIPT_DIR/test_forall_script_error.sh" || exit 1
}
test_forall_script 'cats'

test_forall_projects() {
    print_single_separator
    echo "TEST: Run forall command for specific projects"
    clowder forall -c 'git status' -p "$@" || exit 1
    echo "TEST: Run forall script for specific projects"
    clowder forall -c "$TEST_SCRIPT_DIR/test_forall_script.sh" -p "$@" || exit 1
}
test_forall_projects 'jrgoodle/kit' 'jrgoodle/kishka'

test_forall_environment_variables() {
    print_single_separator
    echo "TEST: Test forall environment variables in script"
    clowder link
    clowder herd || exit 1
    clowder forall -c "$TEST_SCRIPT_DIR/test_forall_script_env_kit.sh" -p "jrgoodle/kit" || exit 1
    clowder forall -c "$TEST_SCRIPT_DIR/test_forall_script_env_duke.sh" -p "jrgoodle/duke" || exit 1
    clowder forall -c "$TEST_SCRIPT_DIR/test_forall_script_env_duke.sh" && exit 1
    clowder forall -ic "$TEST_SCRIPT_DIR/test_forall_script_env_duke.sh" || exit 1
    echo "TEST: Test forall environment variables in command"
    clowder forall -c 'if [ $PROJECT_NAME != jrgoodle/kit ]; then exit 1; fi' -p 'jrgoodle/kit' || exit 1
    clowder forall -c 'if [ $PROJECT_REMOTE != origin ]; then exit 1; fi' -p 'jrgoodle/kit' || exit 1
    clowder forall -c 'if [ $PROJECT_REF != refs/heads/master ]; then exit 1; fi' -p 'jrgoodle/kit' || exit 1
    clowder forall -c 'if [ $PROJECT_NAME != jrgoodle/duke ]; then exit 1; fi' -p 'jrgoodle/duke' || exit 1
    clowder forall -c 'if [ $PROJECT_REMOTE != origin ]; then exit 1; fi' -p 'jrgoodle/duke' || exit 1
    clowder forall -c 'if [ $PROJECT_REF != refs/heads/purr ]; then exit 1; fi' -p 'jrgoodle/duke' || exit 1

}
test_forall_environment_variables
