#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

rm -f clowder.yaml
rm -rf clowder
rm -rf .clowder
rm -rf cocos2d-objc
rm -rf cocos2d-x
