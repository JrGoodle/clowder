#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh
prepare_cats_example
cd "$CATS_EXAMPLE_DIR" || exit 1

export projects=( 'black-cats/kit' \
                  'black-cats/kishka' \
                  'black-cats/sasha' \
                  'black-cats/jules' )

print_double_separator
echo "TEST: Test clowder clean"

test_clean_groups() {
    print_single_separator
    echo "TEST: Make dirty repos"
    make_dirty_repos "${projects[@]}"
    echo "TEST: Clean specific group when dirty"
    clowder clean -g "$@" || exit 1
    clowder status || exit 1
    echo "TEST: Clean all when dirty"
    clowder clean || exit 1
    clowder status || exit 1
}
test_clean_groups 'black-cats'

test_clean_projects() {
    print_single_separator
    echo "TEST: Clean projects"
    make_dirty_repos "${projects[@]}"
    echo "TEST: Clean specific project when dirty"
    clowder clean -p "$@" || exit 1
    clowder status || exit 1
    echo "TEST: Clean all when dirty"
    clowder clean || exit 1
    clowder status || exit 1
}
test_clean_projects 'jrgoodle/kit'

test_clean_all() {
    print_single_separator
    echo "TEST: Make dirty repos"
    make_dirty_repos "${projects[@]}"
    echo "TEST: Clean all when dirty"
    clowder clean || exit 1
    clowder status || exit 1
    echo "TEST: Clean when clean"
    clowder clean || exit 1
}
test_clean_all 'black-cats'

test_clean_missing_directories() {
    print_single_separator
    echo "TEST: Make dirty repos"
    make_dirty_repos "${projects[@]}"
    rm -rf "$@"
    echo "TEST: Clean when directories are missing"
    clowder clean || exit 1
    clowder status || exit 1
    clowder herd >/dev/null
}
test_clean_missing_directories 'mu' 'duke'
