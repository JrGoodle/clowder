#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

print_double_separator
echo 'TEST: swift configure remotes'
cd "$SWIFT_EXAMPLE_DIR" || exit 1
./init.sh

"$TEST_SCRIPT_DIR/swift/write_configure_remotes.sh" || exit 1

test_configure_remotes_herd() {
    git clone https://github.com/apple/swift.git || exit 1
    ./swift/utils/update-checkout --clone
    pushd swift || exit 1
    test_remote_url 'origin' 'https://github.com/apple/swift.git'
    popd || exit 1
    clowder herd $PARALLEL || exit 1
    pushd swift || exit 1
    test_remote_url 'origin' 'https://github.com/JrGoodle/swift.git'
    test_remote_url 'upstream' 'https://github.com/apple/swift.git'
    popd || exit 1
    rm -rf swift
}

test_configure_remotes_fail_existing_remote() {
    git clone https://github.com/apple/swift.git || exit 1
    ./swift/utils/update-checkout --clone
    pushd swift || exit 1
    git remote add 'upstream' 'https://github.com/apple/swift.git'
    test_remote_url 'origin' 'https://github.com/apple/swift.git'
    test_remote_url 'upstream' 'https://github.com/apple/swift.git'
    popd || exit 1
    clowder herd && exit 1
    pushd swift || exit 1
    test_remote_url 'origin' 'https://github.com/apple/swift.git'
    test_remote_url 'upstream' 'https://github.com/apple/swift.git'
    git remote rm 'origin'
    git remote add 'origin' 'git@github.com:apple/swift.git'
    git remote rm 'upstream'
    git remote add 'upstream' 'git@github.com:apple/swift.git'
    test_remote_url 'origin' 'git@github.com:apple/swift.git'
    test_remote_url 'upstream' 'git@github.com:apple/swift.git'
    popd || exit 1
    clowder herd && exit 1
    pushd swift || exit 1
    test_remote_url 'origin' 'git@github.com:apple/swift.git'
    test_remote_url 'upstream' 'git@github.com:apple/swift.git'
    popd || exit 1
    rm -rf swift
}

test_local_swift_example() {
    mkdir swift-source || exit 1
    pushd swift-source || exit 1

    clowder init https://github.com/JrGoodle/swift-clowder.git -b test || exit 1
    clowder link -v jrgoodle-fork-travis-ci || exit 1

    test_configure_remotes_herd
    test_configure_remotes_fail_existing_remote

    popd || exit 1
    rm -rf swift-source
}
test_local_swift_example
