#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

export cats_projects=( 'duke' 'mu' )

export black_cats_projects=( 'black-cats/kit' \
                             'black-cats/kishka' \
                             'black-cats/sasha' \
                             'black-cats/june' )

export all_projects=( 'mu' 'duke' \
                      'black-cats/kit' \
                      'black-cats/kishka' \
                      'black-cats/sasha' \
                      'black-cats/june' )

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./copy-cache.sh

print_double_separator
echo "TEST: Test clowder reset"

test_reset() {
    print_single_separator
    echo "TEST: clowder reset"

    COMMIT_MESSAGE='Add new commits'
    pushd 'mu' || exit 1
    test_number_commits 'HEAD' 'origin/knead' '0'
    UPSTREAM_COMMIT=$(git rev-parse HEAD)
    git reset --hard HEAD~3 || exit 1
    test_number_commits 'HEAD' 'origin/knead' '3'
    test_not_commit "$UPSTREAM_COMMIT"
    popd || exit 1

    $COMMAND reset $PARALLEL -p jrgoodle/mu || exit 1

    pushd 'mu' || exit 1
    test_number_commits 'HEAD' 'origin/knead' '0'
    test_commit  $UPSTREAM_COMMIT
    touch file1 || exit 1
    git add file1 || exit 1
    git commit -m "$COMMIT_MESSAGE" || exit 1
    touch file2 || exit 1
    git add file2 || exit 1
    git commit -m "$COMMIT_MESSAGE" || exit 1
    test_number_commits 'origin/knead' 'HEAD' '2'
    test_not_commit "$UPSTREAM_COMMIT"
    popd || exit 1

    $COMMAND reset $PARALLEL || exit 1

    pushd 'mu' || exit 1
    test_number_commits 'HEAD' 'origin/knead' '0'
    test_commit  $UPSTREAM_COMMIT
    git reset --hard HEAD~3 || exit 1
    test_number_commits 'HEAD' 'origin/knead' '3'
    touch file1 || exit 1
    git add file1 || exit 1
    git commit -m "$COMMIT_MESSAGE" || exit 1
    touch file2 || exit 1
    git add file2 || exit 1
    git commit -m "$COMMIT_MESSAGE" || exit 1
    test_number_commits 'origin/knead' 'HEAD' '2'
    test_number_commits 'HEAD' 'origin/knead' '3'
    test_not_commit "$UPSTREAM_COMMIT"
    popd || exit 1

    $COMMAND reset $PARALLEL || exit 1

    pushd 'mu' || exit 1
    test_number_commits 'HEAD' 'origin/knead' '0'
    test_number_commits 'origin/knead' 'HEAD' '0'
    test_commit  $UPSTREAM_COMMIT
    popd || exit 1
}
test_reset
