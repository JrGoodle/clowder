#!/usr/bin/env bash

set -e

# Set up demo directory
CLOWDER_PROJECTS_PATH=$(cd "${CLOWDER_PROJECT_PATH}/.."; pwd)
pushd "$CLOWDER_PROJECTS_PATH"
rm -rf demo
mkdir -p demo
pushd demo

# Create examples directory
mkdir -p examples
pushd examples

l
clowder init git@github.com:JrGoodle/clowder-examples.git
l
l .clowder
l .clowder/versions

clowder herd
l

clowder status

pushd mu
git herd

popd
clowder link cool-projects
l
clowder herd
l .clowder/versions

clowder save my-version
l .clowder/versions
cat .clowder/versions/my-version.clowder.yml

clowder link my-version
l

clowder status
clowder herd
clowder status

# Create cats directory
popd
mkdir -p cats
pushd cats

clowder init git@github.com:JrGoodle/cats.git

clowder herd
clowder link lfs
l
l mu
clowder herd
l mu

clowder link submodules
l
l mu
clowder herd
l mu/ash
l mu/ash/duffy
