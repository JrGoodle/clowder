#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh || exit 1
$COMMAND herd $PARALLEL || exit 1

print_double_separator
echo "TEST: Test clowder branch"

begin_command
$COMMAND branch || exit 1
end_command

begin_command
$COMMAND branch -r || exit 1
end_command

begin_command
$COMMAND branch -a || exit 1
end_command

begin_command
$COMMAND branch 'jrgoodle/mu' 'jrgoodle/duke' || exit 1
end_command

begin_command
$COMMAND branch -r 'jrgoodle/mu' 'jrgoodle/duke' || exit 1
end_command

begin_command
$COMMAND branch -a 'jrgoodle/mu' 'jrgoodle/duke' || exit 1
end_command

begin_command
$COMMAND branch 'black-cats' || exit 1
end_command

begin_command
$COMMAND branch -r 'black-cats' || exit 1
end_command

begin_command
$COMMAND branch -a 'black-cats' || exit 1
end_command

