#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

if [ -z "$COMMAND" ]; then
    COMMAND='clowder'
fi

rm -rf cached || exit 1
mkdir -p cached || exit 1
pushd cached || exit 1
$COMMAND init https://github.com/jrgoodle/cats.git || exit 1
$COMMAND herd $PARALLEL || exit 1
rm -f clowder.yaml
popd || exit 1
