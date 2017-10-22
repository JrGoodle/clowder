#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

print_double_separator
echo 'TEST: swift projects example test script'
print_double_separator

if [ -z "$TRAVIS_OS_NAME" ]; then
    setup_local_test_directory
fi

cd "$SWIFT_EXAMPLE_DIR" || exit 1

export project_paths=( 'cmark' \
                       'llbuild' \
                       'swift-corelibs-foundation' \
                       'swift-corelibs-libdispatch' \
                       'swift-corelibs-xctest' \
                       'swift-integration-tests' \
                       'swift-xcode-playground-support' \
                       'swiftpm' )

export llvm_project_paths=( 'clang' \
                            'compiler-rt' \
                            'lldb' \
                            'llvm' )

export projects=( 'apple/swift-clang' \
                  'apple/swift-cmark' \
                  'apple/swift-compiler-rt' \
                  'apple/swift-llbuild' \
                  'apple/swift-lldb' \
                  'apple/swift-llvm' \
                  'ninja-build/ninja' \
                  'apple/swift' \
                  'apple/swift-corelibs-foundation' \
                  'apple/swift-corelibs-libdispatch' \
                  'apple/swift-corelibs-xctest' \
                  'apple/swift-integration-tests' \
                  'apple/swift-xcode-playground-support' \
                  'apple/swift-package-manager' )

test_default_branches() {
    echo "TEST: Default branches checked out"
    for project in "${llvm_project_paths[@]}"; do
        pushd $project || exit 1
        test_branch stable
        popd || exit 1
    done
    for project in "${project_paths[@]}"; do
        pushd $project || exit 1
        test_branch master
        popd || exit 1
    done
    pushd swift || exit 1
    test_branch master
    popd || exit 1
    pushd ninja || exit 1
    test_branch release
    popd || exit 1
}

test_clowder_version

if [ "$ACCESS_LEVEL" == "write" ]; then
    mkdir swift-source || exit 1
    pushd swift-source || exit 1
    clowder init git@github.com:JrGoodle/swift-clowder.git || exit 1
    clowder link -v jrgoodle-fork || exit 1

    test_configure_remotes_herd() {
        git clone git@github.com:apple/swift.git || exit 1
        ./swift/utils/update-checkout --clone
        pushd swift || exit 1
        test_remote_url 'origin' 'git@github.com:apple/swift.git'
        popd || exit 1
        clowder herd || exit 1
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
        clowder sync || exit 1
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

test_configure_remotes_herd() {
    git clone https://github.com/apple/swift.git || exit 1
    ./swift/utils/update-checkout --clone
    pushd swift || exit 1
    test_remote_url 'origin' 'https://github.com/apple/swift.git'
    popd || exit 1
    clowder herd || exit 1
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

    clowder init https://github.com/JrGoodle/swift-clowder.git || exit 1
    clowder link -v jrgoodle-fork-travis-ci || exit 1

    test_configure_remotes_herd
    test_configure_remotes_fail_existing_remote

    popd || exit 1
    rm -rf swift-source
}
test_local_swift_example

"$TEST_SCRIPT_DIR/swift/config_versions.sh" || exit 1
"$TEST_SCRIPT_DIR/swift/reset.sh" || exit 1

test_help() {
    print_double_separator
    clowder link -v jrgoodle-fork-travis-ci || exit 1
    "$TEST_SCRIPT_DIR/test_help.sh" "$SWIFT_EXAMPLE_DIR" || exit 1
}
test_help
