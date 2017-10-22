#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

if [ "$1" = 'parallel' ]; then
    PARALLEL='--parallel'
fi

. test_utilities.sh

export cats_projects=( 'duke' 'mu' )

export black_cats_projects=( 'black-cats/kit' \
                             'black-cats/kishka' \
                             'black-cats/sasha' \
                             'black-cats/jules' )

export all_projects=( 'mu' 'duke' \
                      'black-cats/kit' \
                      'black-cats/kishka' \
                      'black-cats/sasha' \
                      'black-cats/jules' )

test_cats_default_herd_branches() {
    echo "TEST: cats projects on default branches"
    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1
        test_branch master
        popd || exit 1
    done
    pushd mu || exit 1
    test_branch knead
    popd || exit 1
    pushd duke || exit 1
    test_branch purr
    popd || exit 1
}

prepare_cats_example
cd "$CATS_EXAMPLE_DIR" || exit 1

print_double_separator
echo "TEST: Test clowder reset"

test_reset() {
    print_single_separator
    echo "TEST: clowder reset"
    clowder link || exit 1
    clowder herd $PARALLEL || exit 1

    COMMIT_MESSAGE='Add new commits'
    pushd 'mu' || exit 1
    git pull origin master || exit 1
    test_number_commits 'HEAD' 'origin/knead' '0'
    UPSTREAM_COMMIT=$(git rev-parse HEAD)
    git reset --hard HEAD~3 || exit 1
    test_number_commits 'HEAD' 'origin/knead' '3'
    test_not_commit "$UPSTREAM_COMMIT"
    popd || exit 1

    clowder reset $PARALLEL || exit 1

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

    clowder reset $PARALLEL || exit 1

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

    clowder reset $PARALLEL || exit 1

    pushd 'mu' || exit 1
    test_number_commits 'HEAD' 'origin/knead' '0'
    test_number_commits 'origin/knead' 'HEAD' '0'
    test_commit  $UPSTREAM_COMMIT
    popd || exit 1
}
test_reset
