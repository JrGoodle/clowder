#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

print_double_separator
echo "TEST: Python 2"

rm -rf "$PYTHON_VERSIONS_DIR" || exit 1
mkdir -p "$PYTHON_VERSIONS_DIR" || exit 1
cd "$PYTHON_VERSIONS_DIR" || exit 1

PY_PATH="$( which python )"
virtualenv -p $PY_PATH python2 || exit 1
. python2/bin/activate || exit 1

pip install $CLOWDER_PROJECT_DIR || exit 1

$TEST_SCRIPT_DIR/tests/test_example_cats.sh

deactivate || exit 1
