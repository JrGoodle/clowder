#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

clowder init https://github.com/jrgoodle/swift-clowder.git || exit 1
