#!/usr/bin/env bash

pushd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

rm -rf clowder
rm -rf .clowder
rm -rf klee
rm -rf libclc
rm -rf lldb
rm -rf llvm
rm -rf lnt
rm -rf openmp
rm -rf polly
rm -rf poolalloc
rm -rf test-suite
rm -rf vmkit
rm -rf zorg
rm -f clowder.yaml

popd
