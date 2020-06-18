#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

print_double_separator
echo "TEST: Test clowder protocol"
print_double_separator
cd "$MISC_EXAMPLE_DIR" || exit 1

test_herd_protocol_default_ssh() {
    echo "TEST: Herd protocol default ssh"
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
test_herd_protocol_default_ssh

test_herd_protocol_default_https() {
    echo "TEST: Herd protocol default https"
    ./clean.sh
    ./init.sh || exit 1
    begin_command
    $COMMAND link https || exit 1
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
test_herd_protocol_default_https

test_herd_protocol_default_ssh_override_https() {
    echo "TEST: Herd protocol default ssh override https"
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
test_herd_protocol_default_ssh_override_https

test_herd_protocol_default_https_override_ssh() {
    echo "TEST: Herd protocol default https override ssh"
    ./clean.sh
    ./init.sh || exit 1
    begin_command
    $COMMAND link https || exit 1
    end_command
    begin_command
    $COMMAND herd $PARALLEL -p ssh || exit 1
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
test_herd_protocol_default_https_override_ssh

test_herd_protocol_default_ssh_config_https() {
    echo "TEST: Herd protocol default ssh config https"
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
test_herd_protocol_default_ssh_config_https

test_herd_protocol_default_https_config_ssh() {
    echo "TEST: Herd protocol default https config ssh"
    ./clean.sh
    ./init.sh || exit 1
    begin_command
    $COMMAND link https || exit 1
    end_command
    begin_command
    $COMMAND config set protocol ssh || exit 1
    end_command
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
test_herd_protocol_default_https_config_ssh
