#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

if [ "$ACCESS_LEVEL" == "write" ]; then
    print_double_separator
    echo 'TEST: swift configure remotes write'
    cd "$SWIFT_EXAMPLE_DIR" || exit 1
    ./init.sh

    mkdir swift-source || exit 1
    pushd swift-source || exit 1
    clowder init git@github.com:JrGoodle/swift-clowder.git -b test || exit 1
    clowder link -v jrgoodle-fork || exit 1

    test_configure_remotes_herd() {
        git clone git@github.com:apple/swift.git || exit 1
        ./swift/utils/update-checkout --clone
        pushd swift || exit 1
        test_remote_url 'origin' 'git@github.com:apple/swift.git'
        popd || exit 1
        clowder herd $PARALLEL || exit 1
        pushd swift || exit 1
        test_remote_url 'origin' 'git@github.com:JrGoodle/swift.git'
        test_remote_url 'upstream' 'git@github.com:apple/swift.git'
        popd || exit 1
        rm -rf swift
    }
    test_configure_remotes_herd

    test_configure_remotes_sync() {
        git clone git@github.com:apple/swift.git || exit 1
        ./swift/utils/update-checkout --clone-with-ssh
        pushd swift || exit 1
        test_remote_url 'origin' 'git@github.com:apple/swift.git'
        popd || exit 1
        clowder sync $PARALLEL || exit 1
        pushd swift || exit 1
        test_remote_url 'origin' 'git@github.com:JrGoodle/swift.git'
        test_remote_url 'upstream' 'git@github.com:apple/swift.git'
        popd || exit 1
        rm -rf swift
    }
    test_configure_remotes_sync

    popd || exit 1
    rm -rf swift-source
fi
