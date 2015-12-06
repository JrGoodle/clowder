#!/usr/bin/env bash

set -eu
#set -x

cd "$( dirname "${BASH_SOURCE[0]}" )"
rm -rf clowder
rm -rf .clowder
rm -rf samples
rm -rf sourcegraph-talks
rm -rf srcco
rm -rf srclib
rm -rf toolchains
rm -f clowder.yaml
