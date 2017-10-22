#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

print_double_separator
echo 'TEST: swift projects reset'
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
