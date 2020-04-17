#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

if [ "$ACCESS_LEVEL" == "write" ]; then
    print_double_separator
    echo 'TEST: cats protocol'
    print_double_separator
    cd "$CATS_EXAMPLE_DIR" || exit 1
    ./clean.sh
    ./init.sh
    $COMMAND herd --protocol 'https' $PARALLEL || exit 1

    if [ -z "$CIRCLECI" ]; then
        pushd mu || exit 1
        test_remote_url 'origin' 'https://github.com/JrGoodle/mu.git'
        popd || exit 1
        pushd duke || exit 1
        test_remote_url 'origin' 'https://github.com/JrGoodle/duke.git'
        popd || exit 1
    fi

    ./clean.sh
    ./init.sh
    $COMMAND herd --protocol 'ssh' $PARALLEL || exit 1

    pushd mu || exit 1
    test_remote_url 'origin' 'git@github.com:JrGoodle/mu.git'
    popd || exit 1
    pushd duke || exit 1
    test_remote_url 'origin' 'git@github.com:JrGoodle/duke.git'
    popd || exit 1
fi
