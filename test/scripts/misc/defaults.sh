#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

print_double_separator
echo "TEST: Test clowder defaults"
print_double_separator
cd "$MISC_EXAMPLE_DIR" || exit 1

test_herd_defaults() {
    echo "TEST: Herd defaults ssh"
    ./clean.sh
    ./init.sh || exit 1
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    pushd djinni || exit 1
    test_branch 'master'
    test_remote_url 'origin' 'git@github.com:JrGoodle/djinni.git'
    test_remote_url 'upstream' 'git@github.com:dropbox/djinni.git'
    popd || exit 1
    pushd gyp || exit 1
    test_branch 'fork-branch'
    test_remote_url 'origin' 'git@github.com:JrGoodle/gyp.git'
    test_remote_url 'upstream' 'https://chromium.googlesource.com/external/gyp.git'
    popd || exit 1
    pushd sox || exit 1
    test_branch 'master'
    test_remote_url 'origin' 'git@github.com:JrGoodle/sox.git'
    test_remote_url 'upstream' 'https://git.code.sf.net/p/sox/code.git'
    popd || exit 1
}
test_herd_defaults

test_herd_defaults_override_https() {
    echo "TEST: Herd defaults override https"
    ./clean.sh
    ./init.sh || exit 1
    begin_command
    $COMMAND herd $PARALLEL -p https || exit 1
    end_command
    pushd djinni || exit 1
    test_branch 'master'
    test_remote_url 'origin' 'https://github.com/JrGoodle/djinni.git'
    test_remote_url 'upstream' 'https://github.com/dropbox/djinni.git'
    popd || exit 1
    pushd gyp || exit 1
    test_branch 'fork-branch'
    test_remote_url 'origin' 'https://github.com/JrGoodle/gyp.git'
    test_remote_url 'upstream' 'https://chromium.googlesource.com/external/gyp.git'
    popd || exit 1
    pushd sox || exit 1
    test_branch 'master'
    test_remote_url 'origin' 'https://github.com/JrGoodle/sox.git'
    test_remote_url 'upstream' 'https://git.code.sf.net/p/sox/code.git'
    popd || exit 1
}
test_herd_defaults_override_https

test_herd_defaults_config_https() {
    echo "TEST: Herd defaults config https"
    ./clean.sh
    ./init.sh || exit 1
    begin_command
    $COMMAND config set protocol https || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    pushd djinni || exit 1
    test_branch 'master'
    test_remote_url 'origin' 'https://github.com/JrGoodle/djinni.git'
    test_remote_url 'upstream' 'https://github.com/dropbox/djinni.git'
    popd || exit 1
    pushd gyp || exit 1
    test_branch 'fork-branch'
    test_remote_url 'origin' 'https://github.com/JrGoodle/gyp.git'
    test_remote_url 'upstream' 'https://chromium.googlesource.com/external/gyp.git'
    popd || exit 1
    pushd sox || exit 1
    test_branch 'master'
    test_remote_url 'origin' 'https://github.com/JrGoodle/sox.git'
    test_remote_url 'upstream' 'https://git.code.sf.net/p/sox/code.git'
    popd || exit 1
}
test_herd_defaults_config_https
