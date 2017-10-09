#!/usr/bin/env bash

LLVM_DIR="$(cd "${LLVM_EXAMPLE_DIR}" || exit 1; pwd)"

echo "CLOWDER_PATH = $CLOWDER_PATH"
if [ $CLOWDER_PATH != "$LLVM_DIR" ]; then
    exit 1
fi

echo "PROJECT_PATH = $PROJECT_PATH"
if [ $PROJECT_PATH != "$LLVM_DIR/llvm/tools/clang" ]; then
    exit 1
fi

echo "PROJECT_NAME = $PROJECT_NAME"
if [ $PROJECT_NAME != "llvm-mirror/clang" ]; then
    exit 1
fi

echo "PROJECT_REMOTE = $PROJECT_REMOTE"
if [ $PROJECT_REMOTE != "upstream" ]; then
    exit 1
fi

echo "FORK_REMOTE = $FORK_REMOTE"
if [ -z "$FORK_REMOTE" ]; then
    exit 1
fi
if [ $FORK_REMOTE != "origin" ]; then
    exit 1
fi

echo "PROJECT_REF = $PROJECT_REF"
if [ $PROJECT_REF != "refs/heads/master" ]; then
    exit 1
fi
