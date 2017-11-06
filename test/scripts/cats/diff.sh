#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh
$COMMAND herd $PARALLEL || exit 1

export black_cats_projects=( 'black-cats/kit' \
                             'black-cats/kishka' \
                             'black-cats/sasha' \
                             'black-cats/jules' )

print_double_separator
echo "TEST: Test clowder diff"

test_diff() {
    print_single_separator
    make_dirty_repos "${black_cats_projects[@]}"

    for project in "${black_cats_projects[@]}"; do
        pushd $project || exit 1 || exit 1
        test_git_dirty
        popd || exit 1
    done

    echo "TEST: Display diff"
    $COMMAND status || exit 1
    $COMMAND diff || exit 1
    $COMMAND clean || exit 1
}
test_diff
