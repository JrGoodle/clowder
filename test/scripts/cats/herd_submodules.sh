#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

export external_projects=( 'mu/ash' \
                           'mu/ash/duffy')

print_double_separator
echo 'TEST: cats herd submodules'
print_double_separator
cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh || exit 1

test_recurse() {
    print_single_separator
    echo "TEST: Herd recursive submodules"
    begin_command
    $COMMAND link submodules || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    begin_command
    $COMMAND status || exit 1
    end_command
    for project in "${external_projects[@]}"; do
        echo "TEST: Check that $project submodule was initialized"
        if [ ! -f "$project/.git" ]; then
            echo "TEST: Submodule should exist"
            exit 1
        fi
    done
}
test_recurse

./clean.sh
./init.sh || exit 1

test_no_recurse() {
    print_single_separator
    echo "TEST: Herd without updating submodules"
    begin_command
    $COMMAND link submodules-no-recurse || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    begin_command
    $COMMAND status || exit 1
    end_command
    for project in "${external_projects[@]}"; do
        echo "TEST: Check that $project submodule wasn't initialized"
        if [ -f "$project/.git" ]; then
            echo "TEST: Submodule shouldn't exist"
            exit 1
        fi
    done
}
test_no_recurse
