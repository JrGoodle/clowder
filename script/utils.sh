# shellcheck shell=bash

bold() {
    if [ -n "$TERM" ] && [ "$TERM" != 'dumb' ]; then
        tput bold
    fi
}

underline() {
    if [ -n "$TERM" ] && [ "$TERM" != 'dumb' ]; then
        tput smul
    fi
}

normal() {
    if [ -n "$TERM" ] && [ "$TERM" != 'dumb' ]; then
        tput sgr0
    fi
}

exit_failure() {
    o ''
    bold
    o "$1"
    normal
    o ''
    exit 1
}
export -f exit_failure

h1() {
    local message="$1"
    o ''
    bold
    o "$message"
    separator "$message" '='
    normal
}
export -f h1

h2() {
    local message="$1"
    o ''
    bold
    o "$message"
    separator "$message" '-'
    normal
}
export -f h2

h3() {
    o ''
    bold
    underline
    o "# $1"
    normal
}
export -f h3

h4() {
    o ''
    bold
    underline
    o "## $1"
    normal
}
export -f h4

h5() {
    o ''
    bold
    underline
    o "### $1"
    normal
}
export -f h5

o() {
    printf '%s\n' "$*"
}
export -f o

b() {
    bold
    printf '%s\n' "$*"
    normal
}
export -f b

separator() {
    local message="$1"
    local separator_character="$2"
    local count="${#message}"
    eval printf -- "${separator_character}%.s" "{1..${count}}"
    o ''
}
export -f separator

run() {
    local components=("$@")
    local run_command="${components[*]}"
    bold
    o "> ${run_command}"
    normal
    eval "$run_command"
}
export -f run

run_ignore_errors() {
    local components=("$@")
    local run_command="${components[*]}"
    bold
    o "> ${run_command}"
    normal
    eval "$run_command" || true
}
export -f run_ignore_errors

assert_file_exists() {
    local test_file="$1"
    if [[ ! -f "$test_file" ]]; then
        exit_failure "File missing ${test_file}"
    fi
    echo "File exists ${test_file}"
}
export -f assert_file_exists

append_to_file() {
    local contents="$1"
    local output_file="$2"
    bold
    echo "> echo '${contents}' >> ${output_file}"
    normal
    echo "$contents" >> "$output_file"
}
export -f append_to_file

write_to_file() {
    local contents="$1"
    local output_file="$2"
    bold
    echo "> echo '${contents}' > ${output_file}"
    normal
    echo "$contents" > "$output_file"
}
export -f write_to_file

sudo_append_to_file() {
    local contents="$1"
    local output_file="$2"
    bold
    echo "> echo '${contents}' | sudo tee -a ${output_file}"
    normal
    echo "$contents" | sudo tee -a "$output_file"
}
export -f sudo_append_to_file

file_contains_string() {
    local match="$1"
    local input_file="$2"
    grep -q "$match" "$input_file" || return $?
}

if [ -z ${PLATFORM+x} ]; then
    case "$(uname)" in
        Linux*) export PLATFORM="linux";;
        Darwin*) export PLATFORM="darwin";;
        CYGWIN*) export PLATFORM="windows";;
    esac
fi
