#!/usr/bin/env bash

set -euo pipefail

# FIXME: Figure out tests for this
# MISC_DIR="$(cd "${MISC_EXAMPLE_DIR}"; pwd)"

# echo "CLOWDER_PATH = $CLOWDER_PATH"
# if [ "$CLOWDER_PATH" != "$MISC_DIR" ]; then
#     exit 1
# fi

# echo "PROJECT_PATH = $PROJECT_PATH"
# if [ "$PROJECT_PATH" != "$MISC_DIR/gyp" ]; then
#     exit 1
# fi

echo "PROJECT_NAME = $PROJECT_NAME"
if [ "$PROJECT_NAME" != 'JrGoodle/gyp' ]; then
    exit 1
fi

echo "PROJECT_REMOTE = $PROJECT_REMOTE"
if [ "$PROJECT_REMOTE" != 'origin' ]; then
    exit 1
fi

echo "PROJECT_REF = $PROJECT_REF"
if [ "$PROJECT_REF" != 'refs/heads/fork-branch' ]; then
    exit 1
fi

echo "UPSTREAM_REMOTE = $UPSTREAM_REMOTE"
if [ -z "$UPSTREAM_REMOTE" ]; then
    exit 1
fi
if [ "$UPSTREAM_REMOTE" != 'upstream' ]; then
    exit 1
fi

echo "UPSTREAM_NAME = $UPSTREAM_NAME"
if [ -z "$UPSTREAM_NAME" ]; then
    exit 1
fi
if [ "$UPSTREAM_NAME" != 'external/gyp' ]; then
    exit 1
fi

echo "UPSTREAM_REF = $UPSTREAM_REF"
if [ -z "$UPSTREAM_REF" ]; then
    exit 1
fi
if [ "$UPSTREAM_REF" != 'refs/heads/master' ]; then
    exit 1
fi
