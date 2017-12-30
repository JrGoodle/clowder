#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

export black_cats_projects=( 'black-cats/kit' \
                             'black-cats/kishka' \
                             'black-cats/sasha' \
                             'black-cats/june' )

print_double_separator
echo "TEST: Test clowder forall"

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh
$COMMAND herd $PARALLEL || exit 1

test_forall_branches() {
    print_single_separator
    $COMMAND forall $PARALLEL -c 'git checkout -b v0.1' || exit 1
    echo "TEST: Check current branches"
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_branch v0.1
        popd || exit 1
    done
    $COMMAND herd $PARALLEL || exit 1
}
test_forall_branches

test_forall_command() {
    print_single_separator
    echo "TEST: Run forall command"
    $COMMAND forall $PARALLEL -c 'git status' || exit 1
    # echo "TEST: Run forall command with multiple arguments"
    # $COMMAND forall $PARALLEL -c 'git status' 'echo "hi"'|| exit 1
    echo "TEST: Run forall command for specific groups"
    $COMMAND forall $PARALLEL -c 'git status' -g "$@" || exit 1
    echo "TEST: Run forall command with error"
    $COMMAND forall $PARALLEL -c 'exit 1' && exit 1
    echo "TEST: Run forall command with --ignore-error"
    $COMMAND forall $PARALLEL -ic 'exit 1' || exit 1
}
test_forall_command 'cats'

test_forall_script() {
    print_single_separator
    echo "TEST: Run forall script"
    $COMMAND forall $PARALLEL -c "$TEST_SCRIPT_DIR/test_forall_script.sh" || exit 1
    echo "TEST: Run forall script with arguments"
    $COMMAND forall $PARALLEL -c "$TEST_SCRIPT_DIR/test_forall_script_args.sh" "one" "two" || exit 1
    echo "TEST: Fail running forall script with arguments"
    $COMMAND forall $PARALLEL -c "$TEST_SCRIPT_DIR/test_forall_script_args.sh" "one" && exit 1
    echo "TEST: Ignore failures running forall script with arguments"
    $COMMAND forall $PARALLEL -ic "$TEST_SCRIPT_DIR/test_forall_script_args.sh" "one" || exit 1
    echo "TEST: Run forall script for specific groups"
    $COMMAND forall $PARALLEL -c "$TEST_SCRIPT_DIR/test_forall_script.sh" -g "$@" || exit 1
    echo "TEST: Run forall script with error"
    $COMMAND forall $PARALLEL -c "$TEST_SCRIPT_DIR/test_forall_script_error.sh" && exit 1
    echo "TEST: Run forall script with --ignore-error"
    $COMMAND forall $PARALLEL -ic "$TEST_SCRIPT_DIR/test_forall_script_error.sh" || exit 1
}
test_forall_script 'cats'

test_forall_projects() {
    print_single_separator
    echo "TEST: Run forall command for specific projects"
    $COMMAND forall $PARALLEL -c 'git status' -p "$@" || exit 1
    echo "TEST: Run forall script for specific projects"
    $COMMAND forall $PARALLEL -c "$TEST_SCRIPT_DIR/test_forall_script.sh" -p "$@" || exit 1
}
test_forall_projects 'jrgoodle/kit' 'jrgoodle/kishka'

test_forall_environment_variables() {
    print_single_separator
    echo "TEST: Test forall environment variables in script"
    $COMMAND link
    $COMMAND herd $PARALLEL || exit 1
    $COMMAND forall $PARALLEL -c "$TEST_SCRIPT_DIR/test_forall_script_env_kit.sh" -p "jrgoodle/kit" || exit 1
    $COMMAND forall $PARALLEL -c "$TEST_SCRIPT_DIR/test_forall_script_env_duke.sh" -p "jrgoodle/duke" || exit 1
    $COMMAND forall $PARALLEL -c "$TEST_SCRIPT_DIR/test_forall_script_env_duke.sh" && exit 1
    $COMMAND forall $PARALLEL -ic "$TEST_SCRIPT_DIR/test_forall_script_env_duke.sh" || exit 1
    echo "TEST: Test forall environment variables in command"
    $COMMAND forall $PARALLEL -c 'if [ $PROJECT_NAME != jrgoodle/kit ]; then exit 1; fi' -p 'jrgoodle/kit' || exit 1
    $COMMAND forall $PARALLEL -c 'if [ $PROJECT_REMOTE != origin ]; then exit 1; fi' -p 'jrgoodle/kit' || exit 1
    $COMMAND forall $PARALLEL -c 'if [ $PROJECT_REF != refs/heads/master ]; then exit 1; fi' -p 'jrgoodle/kit' || exit 1
    $COMMAND forall $PARALLEL -c 'if [ $PROJECT_NAME != jrgoodle/duke ]; then exit 1; fi' -p 'jrgoodle/duke' || exit 1
    $COMMAND forall $PARALLEL -c 'if [ $PROJECT_REMOTE != origin ]; then exit 1; fi' -p 'jrgoodle/duke' || exit 1
    $COMMAND forall $PARALLEL -c 'if [ $PROJECT_REF != refs/heads/purr ]; then exit 1; fi' -p 'jrgoodle/duke' || exit 1

}
test_forall_environment_variables

test_forall_missing_project() {
    print_single_separator
    echo "TEST: clowder forall missing project"
    $COMMAND herd $PARALLEL || exit 1

    rm -rf mu duke || exit 1

    $COMMAND forall -c 'git status' $PARALLEL || exit 1
}
test_forall_missing_project
