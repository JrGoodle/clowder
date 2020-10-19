#!/usr/bin/env bash

exit_failure() {
    echo "$1"
    echo ''
    exit 1
}
export -f exit_failure

h1() {
    local message="$1"
    echo ''
    o "$message"
    separator "$message" '='
}
export -f h1

h2() {
    local message="$1"
    echo ''
    o "$message"
    separator "$message" '-'
}
export -f h2

h3() {
    echo ''
    o "* $1"
}
export -f h3

h4() {
    echo ''
    o "** $1"
}
export -f h4

h5() {
    echo ''
    o "*** $1"
}
export -f h5

o() {
    echo "$1"
}
export -f o

separator() {
    local message="$1"
    local separator_character="$2"
    local count="${#message}"
    eval printf -- "${separator_character}%.s" "{1..${count}}"
    echo ''
}
export -f separator

run() {
    local components=("$@")
    local run_command="${components[*]}"
    echo "> ${run_command}"
    eval "$run_command"
}
export -f run

current_commit() {
    git rev-parse --verify HEAD
}
export -f current_commit

tag_commit() {
    local tag="$1"
    git rev-parse "$tag"^0
}
export -f tag_commit

current_branch() {
    git branch --show-current
}
export -f current_branch

assert_file_exists() {
    local test_file="$1"
    if [[ ! -f "$test_file" ]]; then
        exit_failure "File missing ${test_file}"
    fi
    echo "File exists ${test_file}"
}
export -f assert_file_exists

assert_git_clean() {
    o "Assert git repo is clean"
    if [[ ! "$(git diff --cached --quiet)" ]]; then
        exit_failure "Dirty git repo"
    fi
}
export -f assert_git_clean

assert_git_branch() {
    local expected_branch="$1"
    o "Assert current branch is ${expected_branch}"
    if [[ "$expected_branch" != "$(current_branch)" ]]; then
        o "Expected branch: ${expected_branch}"
        exit_failure "Current branch: $(current_branch)"
    fi
}
export -f assert_git_clean

if [ -z ${PLATFORM+x} ]; then
    case "$(uname)" in
        Linux*) export PLATFORM="linux";;
        Darwin*) export PLATFORM="darwin";;
        CYGWIN*) export PLATFORM="windows";;
    esac
    o "PLATFORM: $PLATFORM"
fi
