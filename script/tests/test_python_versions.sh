#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

# export cats_projects=( 'duke' 'mu' )

export black_cats_projects=( 'black-cats/kit' \
                             'black-cats/kishka' \
                             'black-cats/sasha' \
                             'black-cats/jules' )

# export all_projects=( 'mu' 'duke' \
#                       'black-cats/kit' \
#                       'black-cats/kishka' \
#                       'black-cats/sasha' \
#                       'black-cats/jules' )

test_cats_default_herd_branches() {
    echo "TEST: cats projects on default branches"
    for project in "${black_cats_projects[@]}"; do
    	pushd $project
        test_branch master
        popd
    done
    pushd mu
    test_branch knead
    popd
    pushd duke
    test_branch purr
    popd
}

test_herd() {
    print_single_separator
    echo "TEST: clowder herd"
    ./clean.sh || exit 1
    ./init.sh || exit 1
    clowder herd || exit 1
    test_cats_default_herd_branches
    clowder status || exit 1
}

test_python_version() {
    print_double_separator
    # echo "TEST: Python ${1}.${2}"
    echo "TEST: Python $1"
    rm -rf "$PYTHON_VERSIONS_DIR" || exit 1
    mkdir -p "$PYTHON_VERSIONS_DIR" || exit 1
    pushd "$PYTHON_VERSIONS_DIR" || exit 1
    PY_PATH="$( which python$1 )"
    virtualenv -p $PY_PATH cats || exit 1
    cp -r "$EXAMPLES_DIR/cats/" "$PYTHON_VERSIONS_DIR/cats" || exit 1
    pushd cats
    . bin/activate || exit 1
    pip install $CLOWDER_PROJECT_DIR || exit 1
    test_herd
    popd
    deactivate || exit 1
    popd
}

print_double_separator
echo "TEST: Python versions"

test_python_version 2
test_python_version 3

# print_double_separator
# echo "TEST: Python 2.7"
# test_python_version 2 7

# print_double_separator
# echo "TEST: Python 3.0.1"
# test_python_version 3 0 1

# print_double_separator
# echo "TEST: Python 3.2"
# test_python_version 3 2

# print_double_separator
# echo "TEST: Python 3.3"
# test_python_version 3 3

# print_double_separator
# echo "TEST: Python 3.4"
# test_python_version 3 4

# print_double_separator
# echo "TEST: Python 3.5"
# test_python_version 3 5
