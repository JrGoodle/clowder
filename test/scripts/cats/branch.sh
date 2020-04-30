#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./copy-cache.sh

print_double_separator
echo "TEST: Test clowder branch"

$COMMAND branch || exit 1
$COMMAND branch -r || exit 1
$COMMAND branch -a || exit 1
$COMMAND branch -p 'jrgoodle/mu' 'jrgoodle/duke' || exit 1
$COMMAND branch -rp 'jrgoodle/mu' 'jrgoodle/duke' || exit 1
$COMMAND branch -ap 'jrgoodle/mu' 'jrgoodle/duke' || exit 1
$COMMAND branch -g 'black-cats' || exit 1
$COMMAND branch -rg 'black-cats' || exit 1
$COMMAND branch -ag 'black-cats' || exit 1
