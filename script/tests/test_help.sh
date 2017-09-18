#!/usr/bin/env bash

pushd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

pushd "$1"

print_separator
echo "TEST: Help output"
print_separator
echo "TEST: clowder -h"
clowder -h
print_separator
echo "TEST: clowder clean -h"
clowder clean -h
print_separator
echo "TEST: clowder diff -h"
clowder diff -h
print_separator
echo "TEST: clowder forall -h"
clowder forall -h
print_separator
echo "TEST: clowder herd -h"
clowder herd -h
print_separator
echo "TEST: clowder init -h"
clowder init -h
print_separator
echo "TEST: clowder link -h"
clowder link -h
print_separator
echo "TEST: clowder prune -h"
clowder prune -h
print_separator
echo "TEST: clowder repo -h"
clowder repo -h
print_separator
echo "TEST: clowder repo add -h"
clowder repo add -h
print_separator
echo "TEST: clowder repo checkout -h"
clowder repo checkout -h
print_separator
echo "TEST: clowder repo clean -h"
clowder repo clean -h
print_separator
echo "TEST: clowder repo commit -h"
clowder repo commit -h
print_separator
echo "TEST: clowder repo pull -h"
clowder repo pull -h
print_separator
echo "TEST: clowder repo push -h"
clowder repo push -h
print_separator
echo "TEST: clowder repo run -h"
clowder repo run -h
print_separator
echo "TEST: clowder repo status -h"
clowder repo status -h
print_separator
echo "TEST: clowder save -h"
clowder save -h
print_separator
echo "TEST: clowder start -h"
clowder start -h
print_separator
echo "TEST: clowder stash -h"
clowder stash -h
print_separator
echo "TEST: clowder status -h"
clowder status -h

popd

popd
