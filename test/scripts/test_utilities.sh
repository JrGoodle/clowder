#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export EXAMPLES_DIR
EXAMPLES_DIR="$( cd $CURRENT_DIR/../../examples && pwd)"
export TEST_SCRIPT_DIR
TEST_SCRIPT_DIR="$( cd $CURRENT_DIR && pwd)"
export CLOWDER_PROJECT_DIR
CLOWDER_PROJECT_DIR="$( cd $CURRENT_DIR/../.. && pwd)"

if [ -n "$TRAVIS_OS_NAME" ]; then
    export CATS_EXAMPLE_DIR="$CURRENT_DIR/../../examples/cats"
    export LLVM_EXAMPLE_DIR="$CURRENT_DIR/../../examples/llvm-projects"
    export SWIFT_EXAMPLE_DIR="$CURRENT_DIR/../../examples/swift-projects"
    export COCOS2D_EXAMPLE_DIR="$CURRENT_DIR/../../examples/cocos2d-objc"
    export PYTHON_VERSIONS_DIR="$CURRENT_DIR/../../python2_virtualenv"
else
    export CATS_EXAMPLE_DIR="$HOME/.clowder_tests/cats"
    export LLVM_EXAMPLE_DIR="$HOME/.clowder_tests/llvm-projects"
    export SWIFT_EXAMPLE_DIR="$HOME/.clowder_tests//swift-projects"
    export COCOS2D_EXAMPLE_DIR="$HOME/.clowder_tests/cocos2d-objc"
    export PYTHON_VERSIONS_DIR="$HOME/python2_virtualenv"
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
    [[ "$1" = "$git_commit" ]] && echo "TEST: On correct commit: $1" || exit 1
}

test_commit_author_email() {
    echo "TEST: Check commit is checked out by author email"
    local git_author
    git_author=$(git log -1 --format="%ae" HEAD)
    [[ "$1" = "$git_author" ]] && echo "TEST: Commit author is $1" || exit 1
}

test_commit_author_name() {
    echo "TEST: Check commit is checked out by author name"
    local git_author
    git_author=$(git log -1 --format="%an" HEAD)
    [[ "$1" = "$git_author" ]] && echo "TEST: Commit author is $1" || exit 1
}

test_commit_timestamp() {
    echo "TEST: Check commit timestamp"
    local git_timestamp
    git_timestamp=$(git log -1 --format=%cI)
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

function test_commit_messages() {
    echo "TEST: Commit messages are the same"
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

test_clowder_version() {
    print_double_separator
    echo "TEST: Print clowder version"
    clowder --version || exit 1
}

test_command() {
    print_double_separator
    echo "TEST: Clowder command"
    print_single_separator
    echo "TEST: Fail with unrecognized command"
    clowder cat && exit 1
    echo "TEST: Fail with no arguments"
    clowder && exit 1
    echo ''
}

test_directory_exists() {
    if [ ! -d "$1" ]; then
        exit 1
    fi
}

test_no_directory_exists() {
    if [ -d "$1" ]; then
        exit 1
    fi
}

test_file_exists() {
    if [ ! -f "$1" ]; then
        exit 1
    fi
}

test_no_file_exists() {
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
