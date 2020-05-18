#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export EXAMPLES_DIR
EXAMPLES_DIR="$( cd $CURRENT_DIR/../../examples && pwd)"
export TEST_SCRIPT_DIR
TEST_SCRIPT_DIR="$( cd $CURRENT_DIR && pwd)"
export CLOWDER_PROJECT_DIR
CLOWDER_PROJECT_DIR="$( cd $CURRENT_DIR/../.. && pwd)"

if [ -n "$CI" ]; then
    export CATS_EXAMPLE_DIR="$CURRENT_DIR/../../examples/cats"
    export SWIFT_EXAMPLE_DIR="$CURRENT_DIR/../../examples/swift-projects"
    export MISC_EXAMPLE_DIR="$CURRENT_DIR/../../examples/misc"
else
    export CATS_EXAMPLE_DIR="$HOME/.clowder_tests/cats"
    export SWIFT_EXAMPLE_DIR="$HOME/.clowder_tests/swift-projects"
    export MISC_EXAMPLE_DIR="$HOME/.clowder_tests/misc"
fi

make_dirty_repos() {
    echo "TEST: Make dirty repos"
    for project in "$@"
    do
        pushd $project || exit 1
        touch newfile || exit 1
        git add newfile || exit 1
        popd || exit 1
    done
}

test_branch() {
    echo "TEST: Check local branch $1 is checked out"
    local git_branch
    git_branch=$(git rev-parse --abbrev-ref HEAD)
    echo "Expected branch: $1"
    echo "Current branch: $git_branch"
    [[ "$1" = "$git_branch" ]] && echo "TEST: On correct branch: $1" || exit 1
}

test_git_clean() {
    echo "TEST: Git repo is clean"
    git diff --cached --quiet || exit 1
}

test_commit() {
    echo "TEST: Check commit is checked out"
    local git_commit
    git_commit=$(git rev-parse HEAD)
    echo "Expected commit: $1"
    echo "Current commit: $git_commit"
    [[ "$1" = "$git_commit" ]] && echo "TEST: On correct commit: $1" || exit 1
}

test_commit_author_email() {
    echo "TEST: Check commit is checked out by author email"
    local git_author
    git_author=$(git log -1 --format="%ae" HEAD)
    echo "Expected author email: $1"
    echo "Current author email: $git_author"
    [[ "$1" = "$git_author" ]] && echo "TEST: Commit author is $1" || exit 1
}

test_commit_author_name() {
    echo "TEST: Check commit is checked out by author name"
    local git_author
    git_author=$(git log -1 --format="%an" HEAD)
    echo "Expected author name: $1"
    echo "Current author name: $git_author"
    [[ "$1" = "$git_author" ]] && echo "TEST: Commit author is $1" || exit 1
}

test_commit_timestamp() {
    echo "TEST: Check commit timestamp"
    local git_timestamp
    git_timestamp=$(git log -1 --format=%cI)
    echo "Expected timestamp: $1"
    echo "Current timestamp: $git_timestamp"
    [[ "$1" = "$git_timestamp" ]] && echo "TEST: Commit timestamp is $1" || exit 1
}

test_git_dirty() {
    echo "TEST: Git repo is dirty"
    git diff --cached --quiet && exit 1
}

test_head_detached() {
    echo "TEST: HEAD is detached"
    output="$(git status | head -1)"
    if [[ $output != 'HEAD detached at'* ]]; then
        exit 1
    fi
}

test_local_branch_exists() {
    echo "TEST: Local branch exists: $1"
    git rev-parse --quiet --verify "$1" || exit 1
}

test_no_local_branch_exists() {
    echo "TEST: Local branch doesn't exist: $1"
    git rev-parse --quiet --verify "$1" && exit 1
}

test_rebase_in_progress() {
    echo "TEST: Rebase is in progress"
    (test -d ".git/rebase-merge" || test -d ".git/rebase-apply") || exit 1
}

test_no_rebase_in_progress() {
    echo "TEST: No rebase is in progress"
    (test -d ".git/rebase-merge" || test -d ".git/rebase-apply") && exit 1
}

test_remote_branch_exists() {
    echo "TEST: Remote branch exists: $1"
    local remote_branch_count
    remote_branch_count="$(git ls-remote --heads origin $1 | wc -l | tr -d '[:space:]')"
    if [ "$remote_branch_count" -eq "0" ]; then
        exit 1
    fi
}

test_no_remote_branch_exists() {
    echo "TEST: Remote branch doesn't exist: $1"
    local remote_branch_count
    remote_branch_count="$(git ls-remote --heads origin $1 | wc -l | tr -d '[:space:]')"
    if [ "$remote_branch_count" -eq "1" ]; then
        exit 1
    fi
}

test_remote_url() {
    echo "TEST: Remote url of $1 is $2"
    local remote_url
    remote_url="$(git remote get-url $1)"
    if [ "$remote_url" != "$2" ]; then
        exit 1
    fi
}

test_tracking_branch_exists() {
    echo "TEST: Tracking branch exists: $1"
    git config --get branch.$1.merge || exit 1
}

test_no_tracking_branch_exists() {
    echo "TEST: Tracking branch doesn't exist: $1"
    git config --get branch.$1.merge && exit 1
}

test_no_untracked_files() {
    echo "TEST: No untracked files exist"
    files="$(git ls-files -o -d --exclude-standard | sed q | wc -l| tr -d '[:space:]')"
    if [ "$files" != "0" ]; then
        exit 1
    fi
}

test_not_commit() {
    echo "TEST: Check commit is not checked out"
    if [ "$1" == "$(git rev-parse HEAD)" ]; then
        echo "TEST: On different commit than $1"
        exit 1
    fi
}

test_number_commits() {
    local TO="$1"
    local FROM="$2"
    local COUNT="$3"
    echo "TEST: Check number of commits is $COUNT"
    local commit_count
    commit_count="$(git rev-list $TO..$FROM --count)"
    echo "TEST: Commit count $commit_count"
    [[ "$COUNT" = "$commit_count" ]] && echo "TEST: Correct number of commits: $COUNT" || exit 1
}

test_commit_messages() {
    echo "TEST: Commit messages are the same"
    echo "First message: $1"
    echo "Second message: $2"
    if [ "$1" != "$2" ]; then
        exit 1
    fi
}

test_untracked_files() {
    echo "TEST: Untracked files exist"
    files="$(git ls-files -o -d --exclude-standard | sed q | wc -l| tr -d '[:space:]')"
    if [ "$files" != "1" ]; then
        exit 1
    fi
}

test_directory_exists() {
    echo "TEST: Directory exists"
    if [ ! -d "$1" ]; then
        exit 1
    fi
}

test_no_directory_exists() {
    echo "TEST: No drectory exists"
    if [ -d "$1" ]; then
        exit 1
    fi
}

test_file_exists() {
    echo "TEST: File exists"
    if [ ! -f "$1" ]; then
        exit 1
    fi
}

test_no_file_exists() {
    echo "TEST: No file exists"
    if [ -f "$1" ]; then
        exit 1
    fi
}

print_single_separator() {
    echo '--------------------------------------------------------------------------------'
}

print_double_separator() {
    echo '================================================================================'
}

begin_command() {
    echo '====================================**BEGIN**===================================='
}
export -f begin_command

end_command() {
    echo '=====================================**END**====================================='
}
export -f end_command
