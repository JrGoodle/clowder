#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

echo 'Clean swift example directory'

export files=( 'swift' \
               'cmark' \
               'llbuild' \
               'swift-tools-support-core' \
               'swiftpm' \
               'swift-driver' \
               'swift-syntax' \
               'swift-stress-tester' \
               'swift-corelibs-xctest' \
               'swift-corelibs-foundation' \
               'swift-corelibs-libdispatch' \
               'swift-integration-tests' \
               'swift-xcode-playground-support' \
               'indexstore-db' \
               'sourcekit-lsp' \
               'swift-format' \
               'pythonkit' \
               'tensorflow-swift-apis' \
               'swift-argument-parser' \
               'ninja' \
               'icu' \
               'yams' \
               'cmake' \
               'llvm-project' \
               'clowder.yaml' \
               'clowder.yml' \
               '.clowder' )

for file in "${files[@]}"; do
    rm -rf "$file"
done
