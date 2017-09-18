#!/usr/bin/env bash

pushd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

export projects=( 'black-cats/kit' \
                  'black-cats/kishka' \
                  'black-cats/sasha' \
                  'black-cats/jules' )

test_clean()
{
    print_separator
    echo "TEST: Clean repos"
    make_dirty_repos "${projects[@]}"
    echo "TEST: Clean specific group when dirty"
    clowder clean -g "$@" || exit 1
    clowder status || exit 1
    echo "TEST: Clean all when dirty"
    clowder clean || exit 1
    clowder status || exit 1
    echo "TEST: Clean when clean"
    clowder clean || exit 1
}
test_clean 'black-cats'

test_clean_projects()
{
    print_separator
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

test_clean_missing_directories()
{
    rm -rf "$@"
    echo "TEST: Discard all changes when directories are missing"
    clowder clean || exit 1
    clowder status || exit 1
    clowder herd || exit 1
}
test_clean_missing_directories 'mu' 'duke'

popd
