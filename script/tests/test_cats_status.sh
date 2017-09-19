#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh
prepare_cats_example
cd "$CATS_EXAMPLE_DIR" || exit 1

test_status_groups()
{
    print_separator
    echo "TEST: Test status for specific groups"
    clowder status -g "$@" || exit 1
    echo "TEST: Test status for specific groups with fetching"
    clowder status -f -g "$@" || exit 1
}
test_status_groups 'black-cats'

test_status_projects()
{
    print_separator
    echo "TEST: Test status for specific projects"
    clowder status -p "$@" || exit 1
    echo "TEST: Test status for specific projects with fetching"
    clowder status -f -p "$@" || exit 1
}
test_status_projects 'jrgoodle/mu' 'jrgoodle/duke'
