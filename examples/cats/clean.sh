#!/usr/bin/env bash

set -eu
#set -x

cd "$( dirname "${BASH_SOURCE[0]}" )"
rm -rf clowder
rm -rf .clowder
rm -rf black-cats
rm -rf duke
rm -rf mu
rm -rf polkabot
rm -f clowder.yaml
