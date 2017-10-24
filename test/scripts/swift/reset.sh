#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

print_double_separator
echo 'TEST: swift projects reset'
print_double_separator
cd "$SWIFT_EXAMPLE_DIR" || exit 1

export_commits() {
    pushd 'swift' || exit 1
    export SWIFT_COMMIT
    SWIFT_COMMIT="$(git rev-parse HEAD)"
    popd || exit 1
    pushd 'clang' || exit 1
    export CLANG_COMMIT
    CLANG_COMMIT="$(git rev-parse HEAD)"
    popd || exit 1
    pushd 'compiler-rt' || exit 1
    export COMPILER_RT_COMMIT
    COMPILER_RT_COMMIT="$(git rev-parse HEAD)"
    popd || exit 1
    pushd 'lldb' || exit 1
    export LLDB_COMMIT
    LLDB_COMMIT="$(git rev-parse HEAD)"
    popd || exit 1
    pushd 'llvm' || exit 1
    export LLVM_COMMIT
    LLVM_COMMIT="$(git rev-parse HEAD)"
    popd || exit 1
    pushd 'swift-corelibs-foundation' || exit 1
    export SWIFT_CORELIBS_FOUNDATION_COMMIT
    SWIFT_CORELIBS_FOUNDATION_COMMIT="$(git rev-parse HEAD)"
    popd || exit 1
    pushd 'swift-corelibs-libdispatch' || exit 1
    export SWIFT_CORELIBS_LIBDISPATCH_COMMIT
    SWIFT_CORELIBS_LIBDISPATCH_COMMIT="$(git rev-parse HEAD)"
    popd || exit 1
    pushd 'swift-corelibs-xctest' || exit 1
    export SWIFT_CORELIBS_XCTEST_COMMIT
    SWIFT_CORELIBS_XCTEST_COMMIT="$(git rev-parse HEAD)"
    popd || exit 1
    pushd 'swift-integration-tests' || exit 1
    export SWIFT_INTEGRATION_TESTS_COMMIT
    SWIFT_INTEGRATION_TESTS_COMMIT="$(git rev-parse HEAD)"
    popd || exit 1
    pushd 'swift-xcode-playground-support' || exit 1
    export SWIFT_XCODE_PLAYGROUND_SUPPORT_COMMIT
    SWIFT_XCODE_PLAYGROUND_SUPPORT_COMMIT="$(git rev-parse HEAD)"
    popd || exit 1
    pushd 'llbuild' || exit 1
    export LLBUILD_COMMIT
    LLBUILD_COMMIT="$(git rev-parse HEAD)"
    popd || exit 1
    pushd 'swiftpm' || exit 1
    export SWIFTPM_COMMIT
    SWIFTPM_COMMIT="$(git rev-parse HEAD)"
    popd || exit 1
    pushd 'cmark' || exit 1
    export CMARK_COMMIT
    CMARK_COMMIT="$(git rev-parse HEAD)"
    popd || exit 1
    pushd 'ninja' || exit 1
    export NINJA_COMMIT
    NINJA_COMMIT="$(git rev-parse HEAD)"
    popd || exit 1
}

test_commits() {
    pushd 'swift' || exit 1
    test_commit $SWIFT_COMMIT
    popd || exit 1
    pushd 'clang' || exit 1
    test_commit $CLANG_COMMIT
    popd || exit 1
    pushd 'compiler-rt' || exit 1
    test_commit $COMPILER_RT_COMMIT
    popd || exit 1
    pushd 'lldb' || exit 1
    test_commit $LLDB_COMMIT
    popd || exit 1
    pushd 'llvm' || exit 1
    test_commit $LLVM_COMMIT
    popd || exit 1
    pushd 'swift-corelibs-foundation' || exit 1
    test_commit $SWIFT_CORELIBS_FOUNDATION_COMMIT
    popd || exit 1
    pushd 'swift-corelibs-libdispatch' || exit 1
    test_commit $SWIFT_CORELIBS_LIBDISPATCH_COMMIT
    popd || exit 1
    pushd 'swift-corelibs-xctest' || exit 1
    test_commit $SWIFT_CORELIBS_XCTEST_COMMIT
    popd || exit 1
    pushd 'swift-integration-tests' || exit 1
    test_commit $SWIFT_INTEGRATION_TESTS_COMMIT
    popd || exit 1
    pushd 'swift-xcode-playground-support' || exit 1
    test_commit $SWIFT_XCODE_PLAYGROUND_SUPPORT_COMMIT
    popd || exit 1
    pushd 'llbuild' || exit 1
    test_commit $LLBUILD_COMMIT
    popd || exit 1
    pushd 'swiftpm' || exit 1
    test_commit $SWIFTPM_COMMIT
    popd || exit 1
    pushd 'cmark' || exit 1
    test_commit $CMARK_COMMIT
    popd || exit 1
    pushd 'ninja' || exit 1
    test_commit $NINJA_COMMIT
    popd || exit 1
}

test_reset_swift_4_0_branch() {
    print_single_separator
    echo "TEST: clowder reset timestamp"
    ./clean.sh
    git clone https://github.com/apple/swift.git || exit 1
    swift/utils/update-checkout --scheme swift-4.0-branch --reset-to-remote --clone --clean || exit 1
    swift/utils/update-checkout --scheme swift-4.0-branch --match-timestamp || exit 1

    export_commits

    ./init.sh || exit 1
    clowder herd $PARALLEL || exit 1
    clowder link -v reset-timestamp-swift-4.0-branch || exit 1
    clowder herd $PARALLEL || exit 1
    clowder reset $PARALLEL --timestamp apple/swift || exit 1

    test_commits
}
test_reset_swift_4_0_branch

test_reset_swift_4_1_branch() {
    print_single_separator
    echo "TEST: clowder reset timestamp"
    ./clean.sh
    git clone https://github.com/apple/swift.git || exit 1
    swift/utils/update-checkout --scheme swift-4.1-branch --reset-to-remote --clone --clean || exit 1
    swift/utils/update-checkout --scheme swift-4.1-branch --match-timestamp || exit 1

    export_commits

    ./init.sh || exit 1
    clowder herd $PARALLEL || exit 1
    clowder link -v reset-timestamp-swift-4.1-branch || exit 1
    clowder herd $PARALLEL || exit 1
    clowder reset $PARALLEL --timestamp apple/swift || exit 1

    test_commits
}
test_reset_swift_4_1_branch
