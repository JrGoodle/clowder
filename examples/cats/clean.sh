#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

echo 'Clean cats example directory'

rm -rf clowder
rm -rf .clowder
rm -rf black-cats
rm -rf duke
rm -rf mu
rm -f clowder.yaml
