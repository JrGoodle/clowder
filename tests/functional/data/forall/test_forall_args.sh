#!/usr/bin/env bash

if [ -z "$1" ]; then
    exit 1
fi

if [ "$1" != 'one' ]; then
    exit 1
fi

if [ -z "$2" ]; then
    exit 1
fi

if [ "$2" != 'two' ]; then
    exit 1
fi
