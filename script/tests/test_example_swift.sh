#!/usr/bin/env bash

# set -xv

pushd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

print_double_separator
echo 'TEST: swift projects example test script'
print_double_separator

if [ -z "$TRAVIS_OS_NAME" ]; then
    setup_local_test_directory
fi

cd "$SWIFT_EXAMPLE_DIR" || exit 1

export project_paths=( 'clang' \
                       'cmark' \
                       'compiler-rt' \
                       'llbuild' \
                       'lldb' \
                       'llvm' \
                       'ninja' \
                       'swift-corelibs-foundation' \
                       'swift-corelibs-libdispatch' \
                       'swift-corelibs-xctest' \
                       'swift-integration-tests' \
                       'swift-xcode-playground-support' \
                       'swiftpm' )

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

export fork_paths=( 'swift' )

export fork_projects=( 'apple/swift' )

test_clowder_version

test_init_herd() {
    print_double_separator
    echo "TEST: Normal herd after init"
    "$SWIFT_EXAMPLE_DIR/clean.sh"
    "$SWIFT_EXAMPLE_DIR/init.sh"  || exit 1
    clowder link -v travis-ci || exit 1
    clowder herd || exit 1
    clowder status || exit 1
    # echo "TEST: Check current branches are on master"
    # for project in "${project_paths[@]}"; do
    # 	pushd $project
    #     test_branch master
    #     test_tracking_branch_exists master
    #     popd
    # done
    # for project in "${fork_paths[@]}"; do
    #     pushd $project
    #     test_branch master
    #     test_tracking_branch_exists master
    #     popd
    # done
}
test_init_herd

test_help() {
    print_double_separator
    clowder link
    clowder herd
    "$TEST_SCRIPT_DIR/tests/test_help.sh" "$SWIFT_EXAMPLE_DIR"
}
test_help

popd
