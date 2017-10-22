#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

if [ "$1" = 'parallel' ]; then
    PARALLEL='--parallel'
fi

. test_utilities.sh

print_double_separator
echo 'TEST: swift projects reset'
print_double_separator
cd "$SWIFT_EXAMPLE_DIR" || exit 1
./init.sh

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

test_reset() {
    print_single_separator
    echo "TEST: clowder reset timestamp"
    clowder link -v reset-timestamp-swift-4.0-branch || exit 1
    clowder herd $PARALLEL || exit 1

    pushd 'swift' || exit 1
    git checkout swift-4.0-branch
    popd || exit 1

    clowder reset $PARALLEL --timestamp apple/swift || exit 1

    pushd 'swift' || exit 1
    test_commit 'e004d80f1a5a40d957aba1ed277ef2eaf57c5a28'
    popd || exit 1
    pushd 'clang' || exit 1
    test_commit 'ab7472e733a4081d672e2ef9a8e2011d941d1347'
    popd || exit 1
    pushd 'compiler-rt' || exit 1
    test_commit '2c7fe45c2bc76b4e928d65694cdbfcfcca49d008'
    popd || exit 1
    pushd 'lldb' || exit 1
    test_commit '855bfe02537689163d99ad28f5b8c97d2f190417'
    popd || exit 1
    pushd 'llvm' || exit 1
    test_commit '2dedb62a0bcb69354e15a54be89fb5dfa63275d2'
    popd || exit 1
    pushd 'swift-corelibs-foundation' || exit 1
    test_commit '8afed758bec4495937c82b68ca1dfe76c2383325'
    popd || exit 1
    pushd 'swift-corelibs-libdispatch' || exit 1
    test_commit '7ef9cde3dc931e794f5ba21eabcf308db31c2972'
    popd || exit 1
    pushd 'swift-corelibs-xctest' || exit 1
    test_commit '73190ac9eec3099dcf82cbaecb82dbbe0c1ded98'
    popd || exit 1
    pushd 'swift-integration-tests' || exit 1
    test_commit 'ef82eb354adf1fa3c0d0e498c5da227ffe81edcf'
    popd || exit 1
    pushd 'swift-xcode-playground-support' || exit 1
    test_commit '05737c49f04b9089392b599ad529ab91c7119a75'
    popd || exit 1
    pushd 'llbuild' || exit 1
    test_commit '4c6e96719729ba1d8866730693b745696ab4ccc2'
    popd || exit 1
    pushd 'swiftpm' || exit 1
    test_commit 'f47adf512a750c790e07f58aa26b2bca95019a2d'
    popd || exit 1
    pushd 'cmark' || exit 1
    test_commit 'd875488a6a95d5487b7c675f79a8dafef210a65f'
    popd || exit 1
    pushd 'ninja' || exit 1
    test_commit '253e94c1fa511704baeb61cf69995bbf09ba435e'
    popd || exit 1
}
test_reset
