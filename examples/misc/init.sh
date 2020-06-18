#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

if [ -z "$COMMAND" ]; then
    COMMAND='clowder'
fi

declare -f begin_command > /dev/null && begin_command
if [ -n "$CIRCLECI" ]; then
    $COMMAND init git@github.com:jrgoodle/misc-clowder-tests.git || exit 1
else
    $COMMAND init https://github.com/jrgoodle/misc-clowder-tests.git || exit 1
fi
declare -f end_command > /dev/null && end_command
