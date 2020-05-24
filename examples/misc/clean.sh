#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

echo 'Clean misc example directory'

rm -rf clowder
rm -rf .clowder
rm -f clowder.yaml
rm -f clowder.yml
rm -rf djinni
rm -rf gyp
rm -rf sox
rm -rf sox-code
