#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

export project_paths=( 'djinni' \
                       'gyp' \
                       'sox' )

export projects=( 'dropbox/djinni' \
                  'external/gyp' \
                  'p/sox/code' )

print_double_separator
echo "TEST: Test clowder sources"
cd "$MISC_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh || exit 1
$COMMAND herd $PARALLEL || exit 1

test_djinni_remotes() {
    pushd djinni || exit 1
    test_remote_url 'origin' 'git@github.com:JrGoodle/djinni.git'
    test_remote_url 'upstream' 'git@github.com:dropbox/djinni.git'
    popd || exit 1
}

test_gyp_remotes() {
    pushd gyp || exit 1
    test_remote_url 'origin' 'git@github.com:JrGoodle/gyp.git'
    test_remote_url 'upstream' 'https://chromium.googlesource.com/external/gyp.git'
    popd || exit 1
}

test_sox_remotes() {
    pushd sox || exit 1
    test_remote_url 'origin' 'git@github.com:JrGoodle/sox.git'
    test_remote_url 'upstream' 'https://git.code.sf.net/p/sox/code.git'
    popd || exit 1
}

test_djinni_remotes
test_gyp_remotes
test_sox_remotes
