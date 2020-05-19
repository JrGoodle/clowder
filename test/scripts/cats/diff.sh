#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh || exit 1
begin_command
$COMMAND herd $PARALLEL || exit 1
end_command

export black_cats_projects=( 'black-cats/kit' \
                             'black-cats/kishka' \
                             'black-cats/sasha' \
                             'black-cats/june' )

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
    begin_command
    $COMMAND status || exit 1
    end_command
    begin_command
    $COMMAND diff || exit 1
    end_command
    begin_command
    $COMMAND diff jrgoodle/mu jrgoodle/duke || exit 1
    end_command
    begin_command
    $COMMAND clean || exit 1
    end_command
}
test_diff
