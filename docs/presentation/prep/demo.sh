#!/usr/bin/env bash

set -e

pushd () {
    command pushd "$@" > /dev/null
}

popd () {
    command popd "$@" > /dev/null
}

wait() {
    printf "\n"
    tput sc
    read -n 1 -rsp "waitng to continue"
    tput rc; tput el
}

run() {
    printf "$ "
    echo "$@"
    wait
    "$@"
    wait
}

# Set up demo directory
DEMO_PATH=$(cd "${CLOWDER_PROJECT_PATH}/../demo"; pwd)
rm -rf "$DEMO_PATH"
mkdir -p "$DEMO_PATH"
pushd "$DEMO_PATH"

# Create examples directory
mkdir -p examples
run pushd examples

run l
run clowder init git@github.com:JrGoodle/clowder-examples.git
run l
run l .clowder
run l .clowder/versions

run clowder herd
run l

run clowder status

run pushd mu
run git herd

run popd
run clowder link cool-projects
run l
run clowder herd
run l .clowder/versions
run clowder save my-version
run l .clowder/versions
run cat .clowder/versions/my-version.clowder.yml
run clowder link my-version
run l
run clowder status
run clowder header
run clowder status

# Create cats directory
run popd
mkdir -p cats
run pushd cats

run clowder init git@github.com:JrGoodle/cats.git

run clowder herd
run clowder link lfs
run l
run l mu
run clowder herd
run l

run clowder link submodules
run l
run l mu
run clowder herd
run l mu/ash
run l mu/ash/duffy
