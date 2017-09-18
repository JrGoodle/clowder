#!/usr/bin/env bash

pushd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

rm -rf clowder
rm -rf .clowder
rm -rf black-cats
rm -rf duke
rm -rf mu
rm -f clowder.yaml

popd
