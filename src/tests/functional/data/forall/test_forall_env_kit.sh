#!/usr/bin/env bash

# FIXME: Figure out tests for this
# echo "CLOWDER_PATH = $CLOWDER_PATH"
# if [ $CLOWDER_PATH != "$CATS_DIR" ]; then
#     exit 1
# fi
#
# echo "PROJECT_PATH = $PROJECT_PATH"
# if [ $PROJECT_PATH != "$CATS_DIR/black-cats/kit" ]; then
#     exit 1
# fi

echo "PROJECT_NAME = $PROJECT_NAME"
if [ $PROJECT_NAME != "jrgoodle/kit" ]; then
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
if [ $PROJECT_REF != "refs/heads/master" ]; then
    exit 1
fi
