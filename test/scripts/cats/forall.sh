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
./init.sh || exit 1
begin_command
$COMMAND herd $PARALLEL || exit 1
end_command

test_forall_branches() {
    print_single_separator
    begin_command
    $COMMAND forall $PARALLEL -c 'git checkout -b v0.1' || exit 1
    end_command
    echo "TEST: Check current branches"
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_branch v0.1
        popd || exit 1
    done
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
}
test_forall_branches

test_forall_command() {
    print_single_separator
    echo "TEST: Run forall command"
    begin_command
    $COMMAND forall $PARALLEL -c 'git status' || exit 1
    end_command
    # echo "TEST: Run forall command with multiple arguments"
    # begin_command
    # $COMMAND forall $PARALLEL -c 'git status' 'echo "hi"'|| exit 1
    # end_command
    echo "TEST: Run forall command for specific groups"
    begin_command
    $COMMAND forall $PARALLEL "$@" -c 'git status' || exit 1
    end_command
    echo "TEST: Run forall command with error"
    begin_command
    $COMMAND forall $PARALLEL -c 'exit 1' && exit 1
    end_command
    echo "TEST: Run forall command with --ignore-error"
    begin_command
    $COMMAND forall $PARALLEL -ic 'exit 1' || exit 1
    end_command
    echo "TEST: Check exit code from forall command"
    begin_command
    $COMMAND forall $PARALLEL -c 'exit 150'
    local exit_code="$?"
    end_command
    if [ "$exit_code" != '150' ]; then
        exit 1
    fi
}
test_forall_command 'cats'

test_forall_script() {
    print_single_separator
    echo "TEST: Run forall script"
    begin_command
    $COMMAND forall $PARALLEL -c "$TEST_SCRIPT_DIR/test_forall_script.sh" || exit 1
    end_command
    echo "TEST: Run forall script with arguments"
    begin_command
    $COMMAND forall $PARALLEL -c "$TEST_SCRIPT_DIR/test_forall_script_args.sh" "one" "two" || exit 1
    end_command
    echo "TEST: Fail running forall script with arguments"
    begin_command
    $COMMAND forall $PARALLEL -c "$TEST_SCRIPT_DIR/test_forall_script_args.sh" "one" && exit 1
    end_command
    echo "TEST: Ignore failures running forall script with arguments"
    begin_command
    $COMMAND forall $PARALLEL -ic "$TEST_SCRIPT_DIR/test_forall_script_args.sh" "one" || exit 1
    end_command
    echo "TEST: Run forall script for specific groups"
    begin_command
    $COMMAND forall $PARALLEL "$@" -c "$TEST_SCRIPT_DIR/test_forall_script.sh" || exit 1
    end_command
    echo "TEST: Run forall script with error"
    begin_command
    $COMMAND forall $PARALLEL -c "$TEST_SCRIPT_DIR/test_forall_script_error.sh" && exit 1
    end_command
    echo "TEST: Run forall script with --ignore-error"
    begin_command
    $COMMAND forall $PARALLEL -ic "$TEST_SCRIPT_DIR/test_forall_script_error.sh" || exit 1
    end_command
}
test_forall_script 'cats'

test_forall_projects() {
    print_single_separator
    echo "TEST: Run forall command for specific projects"
    begin_command
    $COMMAND forall $PARALLEL "$@" -c 'git status' || exit 1
    end_command
    echo "TEST: Run forall script for specific projects"
    begin_command
    $COMMAND forall $PARALLEL "$@" -c "$TEST_SCRIPT_DIR/test_forall_script.sh" || exit 1
    end_command
}
test_forall_projects 'jrgoodle/kit' 'jrgoodle/kishka'

test_forall_environment_variables() {
    print_single_separator
    echo "TEST: Test forall environment variables in script"
    begin_command
    $COMMAND link || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    begin_command
    $COMMAND forall $PARALLEL "jrgoodle/kit" -c "$TEST_SCRIPT_DIR/test_forall_script_env_kit.sh" || exit 1
    end_command
    begin_command
    $COMMAND forall $PARALLEL "jrgoodle/duke" -c "$TEST_SCRIPT_DIR/test_forall_script_env_duke.sh" || exit 1
    end_command
    begin_command
    $COMMAND forall $PARALLEL -c "$TEST_SCRIPT_DIR/test_forall_script_env_duke.sh" && exit 1
    end_command
    begin_command
    $COMMAND forall $PARALLEL -ic "$TEST_SCRIPT_DIR/test_forall_script_env_duke.sh" || exit 1
    end_command
    echo "TEST: Test forall environment variables in command"
    begin_command
    $COMMAND forall $PARALLEL 'jrgoodle/kit' -c 'if [ $PROJECT_NAME != jrgoodle/kit ]; then exit 1; fi' || exit 1
    end_command
    begin_command
    $COMMAND forall $PARALLEL 'jrgoodle/kit' -c 'if [ $PROJECT_REMOTE != origin ]; then exit 1; fi' || exit 1
    end_command
    begin_command
    $COMMAND forall $PARALLEL 'jrgoodle/kit' -c 'if [ $PROJECT_REF != refs/heads/master ]; then exit 1; fi' || exit 1
    end_command
    begin_command
    $COMMAND forall $PARALLEL 'jrgoodle/duke' -c 'if [ $PROJECT_NAME != jrgoodle/duke ]; then exit 1; fi' || exit 1
    end_command
    begin_command
    $COMMAND forall $PARALLEL 'jrgoodle/duke' -c 'if [ $PROJECT_REMOTE != origin ]; then exit 1; fi' || exit 1
    end_command
    begin_command
    $COMMAND forall $PARALLEL 'jrgoodle/duke' -c 'if [ $PROJECT_REF != refs/heads/purr ]; then exit 1; fi' || exit 1
    end_command
}
test_forall_environment_variables
