#!/usr/bin/env bash

# FIXME: Figure out tests for this
# echo "CLOWDER_PATH = $CLOWDER_PATH"
# if [ $CLOWDER_PATH != "$CATS_DIR" ]; then
#     exit 1
# fi

# echo "PROJECT_PATH = $PROJECT_PATH"
# if [ $PROJECT_PATH != "$CATS_DIR/duke" ]; then
#     exit 1
# fi

echo "PROJECT_NAME = $PROJECT_NAME"
if [ $PROJECT_NAME != "jrgoodle/duke" ]; then
    exit 1
fi

echo "PROJECT_REMOTE = $PROJECT_REMOTE"
if [ $PROJECT_REMOTE != "origin" ]; then
    exit 1
fi

echo "UPSTREAM_REMOTE = $UPSTREAM_REMOTE"
if [ -n "$UPSTREAM_REMOTE" ]; then
    exit 1
fi

echo "PROJECT_REF = $PROJECT_REF"
if [ $PROJECT_REF != "refs/heads/purr" ]; then
    exit 1
fi
