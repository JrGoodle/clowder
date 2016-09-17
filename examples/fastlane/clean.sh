#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
rm -rf clowder
rm -rf .clowder
rm -f clowder.yaml

rm -rf fastlane
