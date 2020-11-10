# shellcheck shell=bash

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
export -f assert_git_branch
