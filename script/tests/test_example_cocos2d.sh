#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

export external_projects=( 'cocos2d-objc/external/Chipmunk' \
                           'cocos2d-objc/external/ObjectAL' \
                           'cocos2d-objc/external/SSZipArchive' )

print_double_separator
echo 'TEST: cocos2d example test script'
print_double_separator

if [ -z "$TRAVIS_OS_NAME" ]; then
    setup_local_test_directory
fi

cd "$COCOS2D_EXAMPLE_DIR" || exit 1

./clean.sh
./init.sh || exit 1

test_recurse() {
    print_single_separator
    echo "TEST: Herd recursive submodules"
    clowder herd || exit 1
    clowder status || exit 1
    for project in "${external_projects[@]}"; do
        echo "TEST: Check that $project submodule was initialized"
    	if [ ! -f "$project/.git" ]; then
            echo "TEST: Submodule should exist"
            exit 1
        fi
    done
}
test_recurse

./clean.sh
./init.sh || exit 1

test_no_recurse() {
    print_single_separator
    echo "TEST: Herd without updating submodules"
    clowder link -v no-recurse || exit 1
    clowder herd || exit 1
    clowder status || exit 1
    for project in "${external_projects[@]}"; do
        echo "TEST: Check that $project submodule wasn't initialized"
    	if [ -f "$project/.git" ]; then
            echo "TEST: Submodule shouldn't exist"
            exit 1
        fi
    done
}
test_no_recurse
