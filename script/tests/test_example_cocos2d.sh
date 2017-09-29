#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

export external_projects=( 'external/Chipmunk' \
                           'external/ObjectAL' \
                           'external/SSZipArchive' )

print_double_separator
echo 'TEST: cocos2d example test script'
print_double_separator

if [ -z "$TRAVIS_OS_NAME" ]; then
    setup_local_test_directory
fi

cd "$COCOS2D_EXAMPLE_DIR" || exit 1

./init.sh

test_recurse() {
    print_single_separator
    echo "TEST: Herd recursive submodules"
    clowder herd || exit 1
    for project in "${external_projects[@]}"; do
    	if [ ! -d "$project" ]; then
            exit 1
        fi
    done
}
test_recurse

./clean.sh

test_no_recurse() {
    print_single_separator
    echo "TEST: Herd without updating submodules"
    clowder link -v no-recurse
    clowder herd || exit 1
    for project in "${external_projects[@]}"; do
    	if [ -d "$project" ]; then
            exit 1
        fi
    done
}
test_no_recurse
