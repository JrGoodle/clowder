#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh
prepare_cats_example
cd "$CATS_EXAMPLE_DIR" || exit 1

export projects=( 'black-cats/kit' \
                  'black-cats/kishka' \
                  'black-cats/sasha' \
                  'black-cats/jules' )

print_separator
echo "TEST: Test clowder diff"

test_diff() {
    echo "TEST: Make dirty repos"
    make_dirty_repos "${projects[@]}"
    echo "TEST: Display diff"
    clowder diff || exit 1
}
test_diff
