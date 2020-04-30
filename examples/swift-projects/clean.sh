#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

echo 'Clean swift example directory'

rm -rf clowder
rm -rf .clowder
rm -rf clang
rm -rf cmark
rm -rf compiler-rt
rm -rf llbuild
rm -rf lldb
rm -rf llvm
rm -rf ninja
rm -rf swift
rm -rf swift-corelibs-foundation
rm -rf swift-corelibs-libdispatch
rm -rf swift-corelibs-xctest
rm -rf swift-integration-tests
rm -rf swift-xcode-playground-support
rm -rf swiftpm
rm -f clowder.yaml
