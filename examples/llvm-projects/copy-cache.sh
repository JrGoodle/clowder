#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

echo 'Copy llvm cache'

./clean.sh
cp -a cached/. ./
rm -f clowder.yaml
clowder link || exit 1
