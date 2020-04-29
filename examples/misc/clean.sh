#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

rm -rf clowder
rm -rf .clowder
rm -f clowder.yaml
rm -rf djinni
rm -rf gyp
rm -rf sox
