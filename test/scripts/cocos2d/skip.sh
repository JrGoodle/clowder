#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

export external_projects=( 'cocos2d-objc/external/Chipmunk' \
                           'cocos2d-objc/external/ObjectAL' \
                           'cocos2d-objc/external/SSZipArchive' )

print_double_separator
echo 'TEST: cocos2d clean'
print_double_separator
cd "$COCOS2D_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh
