#!/usr/bin/env bash

# Adapted from: https://circleci.com/docs/2.0/artifacts/#downloading-all-artifacts-for-a-build-on-circleci

set -euo pipefail
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."
# shellcheck disable=SC1091
. 'script/utils.sh'

if [ -z ${CIRCLE_TOKEN+x} ]; then
    exit_failure 'Requires CIRCLE_TOKEN is set'
fi

OUTPUT_DIR="${PWD}/build/artifacts/circleci"
run rm -rf "$OUTPUT_DIR"
run mkdir -p "$OUTPUT_DIR"
run pushd "$OUTPUT_DIR"

CIRCLE_BUILD_NUMBER="${1+NOT_SET}"
if [ "$CIRCLE_BUILD_NUMBER" == 'NOT_SET' ]; then
    h1 "Download artifacts for latest build"
    curl -H "Circle-Token: ${CIRCLE_TOKEN}" 'https://circleci.com/api/v1.1/project/github/JrGoodle/clowder/latest/artifacts' \
        | grep -o 'https://[^"]*' \
        | wget --verbose --header "Circle-Token: $CIRCLE_TOKEN" --input-file -
    exit
fi

h1 "Download artifacts for build number ${CIRCLE_BUILD_NUMBER}"
curl -H "Circle-Token: ${CIRCLE_TOKEN}" "https://circleci.com/api/v1.1/project/github/JrGoodle/clowder/${CIRCLE_BUILD_NUMBER}/artifacts" \
    | grep -o 'https://[^"]*' \
    | wget --verbose --header "Circle-Token: $CIRCLE_TOKEN" --input-file -
