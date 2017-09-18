#!/usr/bin/env bash

pushd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

clowder init https://github.com/jrgoodle/llvm-projects.git

popd
