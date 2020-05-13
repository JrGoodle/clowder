#!/usr/bin/env bash

# set -xv

if [ -z $1 ]; then
    echo 'Required argument not specified'
    exit 1
fi

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

print_double_separator
echo "TEST: Create $1 cache"
print_double_separator

case "$1" in
    'cats')
        "$CATS_EXAMPLE_DIR/create-cache.sh" || exit 1
        ;;
    'misc')
        "$MISC_EXAMPLE_DIR/create-cache.sh" || exit 1
        ;;
    'swift')
        "$SWIFT_EXAMPLE_DIR/create-cache.sh" || exit 1
        ;;
    *)
        echo "Unknown argument: $1"
        exit 1
        ;;
esac
