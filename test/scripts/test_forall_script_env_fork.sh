#!/usr/bin/env bash

MISC_DIR="$(cd "${MISC_EXAMPLE_DIR}" || exit 1; pwd)"

echo "CLOWDER_PATH = $CLOWDER_PATH"
if [ $CLOWDER_PATH != "$MISC_DIR" ]; then
    exit 1
fi

echo "PROJECT_PATH = $PROJECT_PATH"
if [ $PROJECT_PATH != "$MISC_DIR/gyp" ]; then
    exit 1
fi

echo "PROJECT_NAME = $PROJECT_NAME"
if [ $PROJECT_NAME != "external/gyp" ]; then
    exit 1
fi

echo "PROJECT_REMOTE = $PROJECT_REMOTE"
if [ $PROJECT_REMOTE != "upstream" ]; then
    exit 1
fi

echo "PROJECT_REF = $PROJECT_REF"
if [ $PROJECT_REF != "refs/heads/master" ]; then
    exit 1
fi

echo "PROJECT_ALIAS = $PROJECT_ALIAS"
if [ $PROJECT_ALIAS != "gyp" ]; then
    exit 1
fi

echo "FORK_REMOTE = $FORK_REMOTE"
if [ -z "$FORK_REMOTE" ]; then
    exit 1
fi
if [ $FORK_REMOTE != "origin" ]; then
    exit 1
fi

echo "FORK_NAME = $FORK_NAME"
if [ -z "$FORK_NAME" ]; then
    exit 1
fi
if [ $FORK_NAME != "JrGoodle/gyp" ]; then
    exit 1
fi

echo "FORK_REF = $FORK_REF"
if [ -z "$FORK_REF" ]; then
    exit 1
fi
if [ $FORK_REF != "refs/heads/fork-branch" ]; then
    exit 1
fi

