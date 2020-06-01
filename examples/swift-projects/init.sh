#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

if [ -z "$COMMAND" ]; then
    COMMAND='clowder'
fi

declare -f begin_command > /dev/null && begin_command
$COMMAND init https://github.com/jrgoodle/swift-clowder.git || exit 1
declare -f end_command > /dev/null && end_command
exit # Don't propagate error
