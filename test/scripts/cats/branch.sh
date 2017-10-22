#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

prepare_cats_example
cd "$CATS_EXAMPLE_DIR" || exit 1
./init.sh

print_double_separator
echo "TEST: Test clowder branch"

clowder link || exit 1
clowder herd || exit 1

clowder branch || exit 1
clowder branch -r || exit 1
clowder branch -a || exit 1
clowder branch -p 'jrgoodle/mu' 'jrgoodle/duke' || exit 1
clowder branch -rp 'jrgoodle/mu' 'jrgoodle/duke' || exit 1
clowder branch -ap 'jrgoodle/mu' 'jrgoodle/duke' || exit 1
clowder branch -g 'black-cats' || exit 1
clowder branch -rg 'black-cats' || exit 1
clowder branch -ag 'black-cats' || exit 1
