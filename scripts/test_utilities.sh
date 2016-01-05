#! /bin/bash

make_dirty_clowder_repo()
{
    echo "TEST: Make dirty clowder repo"
    clowder repo 'touch newfile'
    clowder repo 'git add newfile'
    clowder status || exit 1
}

make_dirty_repos()
{
    print_separator
    echo "TEST: Make dirty repos"
    for project in "${projects[@]}"
    do
    	pushd $project &>/dev/null
        touch newfile
        git add newfile
        popd &>/dev/null
    done
    clowder status -v || exit 1
}

test_branch()
{
    local git_branch
    git_branch=$(git rev-parse --abbrev-ref HEAD)
    [[ "$1" = "$git_branch" ]] && echo "TEST: On correct branch: $1" || exit 1
}

test_branch_master()
{
    print_separator
    echo "TEST: Check current branches"
    for project in "${projects[@]}"
    do
    	pushd $project &>/dev/null
        test_branch master
        popd &>/dev/null
    done
}

test_branch_version()
{
    print_separator
    clowder forall 'git checkout -b v0.1'
    echo "TEST: Check current branches"
    for project in "${projects[@]}"
    do
    	pushd $project &>/dev/null
        test_branch v0.1
        popd &>/dev/null
    done
}

test_breed_herd()
{
    print_separator
    echo "TEST: Normal herd after breed"
    ./clean.sh
    ./breed.sh  || exit 1
    clowder herd  || exit 1
    clowder status || exit 1
}

test_breed_herd_version()
{
    print_separator
    echo "TEST: Herd version after breed"
    ./clean.sh || exit 1
    ./breed.sh || exit 1
    clowder herd -v v0.1 || exit 1
}

test_clowder_version()
{
    print_separator
    echo "TEST: Print clowder version"
    clowder --version || exit 1
    clowder --v || exit 1
}

test_command()
{
    print_separator
    echo "TEST: Fail with unrecognized command"
    clowder cat && exit 1
    ./clean.sh || exit 1
    echo "TEST: Fail herd with missing clowder.yaml"
    clowder herd && exit 1
}

test_fix()
{
    print_separator
    echo "TEST: Fail herding a previously fixed version"
    clowder herd -v v100 && exit 1
    echo "TEST: Fail fixing a previously fixed version"
    clowder fix v0.1 && exit 1
    echo "TEST: Successfully fix a new version"
    clowder fix v0.11 || exit 1
    echo "TEST: Successfully fix version with path separator in input name"
    clowder fix path/separator
    clowder herd -v path-separator || exit 1
    clowder status || exit 1
}

test_fix_missing_directories()
{
    print_separator
    echo "TEST: Remove directories"
    rm -rf "$@"
    echo "TEST: Fail fixing version with missing directories"
    clowder fix missing-directories && exit 1
}

test_forall()
{
    print_separator
    echo "TEST: Run forall command"
    clowder forall 'git status' || exit 1
    echo "TEST: Run forall command for specific groups"
    clowder forall 'git status' -g "$@" || exit 1
}

test_forall_projects()
{
    print_separator
    echo "TEST: Run forall command for specific projects"
    clowder forall 'git status' -p "$@" || exit 1
}

test_clean()
{
    print_separator
    make_dirty_repos "${projects[@]}"
    echo "TEST: Clean specific group when dirty"
    clowder clean -g "$@" || exit 1
    clowder status || exit 1
    echo "TEST: Clean all when dirty"
    clowder clean || exit 1
    clowder status || exit 1
    echo "TEST: Clean when clean"
    clowder clean || exit 1
}

test_clean_missing_directories()
{
    rm -rf "$@"
    echo "TEST: Discard all changes when directories are missing"
    clowder clean || exit 1
    clowder status || exit 1
    clowder herd || exit 1
}

test_clean_projects()
{
    print_separator
    make_dirty_repos "${projects[@]}"
    echo "TEST: Clean specific project when dirty"
    clowder clean -p "$@" || exit 1
    clowder status || exit 1
    echo "TEST: Clean all when dirty"
    clowder clean || exit 1
    clowder status || exit 1
}

test_herd()
{
    print_separator
    echo "TEST: Successfully herd a previously fixed version"
    clowder herd -v v0.1 || exit 1
    echo "TEST: Successfully herd after herding a previously fixed version"
    clowder herd || exit 1
    echo "TEST: Remove directories"
    rm -rf "$@"
    echo "TEST: Successfully herd with missing directories"
    clowder herd || exit 1
}

test_herd_detached_heads()
{
    print_separator
    echo "TEST: Create detached HEADs"
    for project in "${projects[@]}"
    do
    	pushd $project &>/dev/null
        git checkout master~2
        popd &>/dev/null
    done
    clowder status || exit 1
    echo "TEST: Successfully herd with detached HEADs"
    clowder herd || exit 1
}

test_herd_dirty_repos()
{
    print_separator
    make_dirty_repos "${projects[@]}"
    echo "TEST: Fail herd with dirty repos"
    clowder herd && exit 1
    echo "TEST: Discard changes with clean"
    clowder clean || exit 1
    clowder status || exit 1
    echo "TEST: Successfully herd after clean"
    clowder herd || exit 1
    echo "TEST: Successfully herd twice"
    clowder herd || exit 1
}

test_herd_projects()
{
    print_separator
    echo "TEST: Successfully herd specific projects"
    clowder herd -p "$@" || exit 1
}

test_status_groups()
{
    print_separator
    echo "TEST: Test status for specific groups"
    clowder status -g "$@" || exit 1
}

test_stash()
{
    make_dirty_repos "${projects[@]}"
    echo "TEST: Fail herd with dirty repos"
    clowder herd && exit 1
    echo "TEST: Stash specific groups when dirty"
    clowder stash -g "$@" || exit 1
    clowder status || exit 1
    echo "TEST: Stash all changes when dirty"
    clowder stash || exit 1
    clowder status || exit 1
    echo "TEST: Stash changes when clean"
    clowder stash || exit 1
}

test_stash_missing_directories()
{
    rm -rf "$@"
    echo "TEST: Stash all changes when directories are missing"
    clowder stash || exit 1
    clowder status || exit 1
    clowder herd || exit 1
}

test_stash_projects()
{
    make_dirty_repos "${projects[@]}"
    echo "TEST: Stash specific projects when dirty"
    clowder stash -p "$@" || exit 1
    clowder status || exit 1
    echo "TEST: Stash all changes when dirty"
    clowder stash || exit 1
    clowder status || exit 1
}

test_herd_groups()
{
    print_separator
    echo "TEST: Herd fixed version to test herding select groups"
    clowder herd -v v0.1 || exit 1
    print_separator
    echo "TEST: Herd only specific groups"
    clowder herd -g "$@" || exit 1
    clowder status || exit 1
}

print_help()
{
    print_separator
    echo "TEST: Help output"
    print_separator
    echo "TEST: clowder -h"
    clowder -h
    print_separator
    echo "TEST: clowder breed -h"
    clowder breed -h
    print_separator
    echo "TEST: clowder herd -h"
    clowder herd -h
    print_separator
    echo "TEST: clowder fix -h"
    clowder fix -h
    print_separator
    echo "TEST: clowder forall -h"
    clowder forall -h
    print_separator
    echo "TEST: clowder clean -h"
    clowder clean -h
    print_separator
    echo "TEST: clowder status -h"
    clowder status -h
    print_separator
    echo "TEST: clowder stash -h"
    clowder stash -h
}

print_separator()
{
    echo ''
    echo '--------------------------------------------------------------------------------'
    echo ''
}
