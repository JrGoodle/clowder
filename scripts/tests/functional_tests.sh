#! /bin/bash

test_branch()
{
    local git_branch
    git_branch=$(git rev-parse --abbrev-ref HEAD)
    # echo "TEST: Current branch: $git_branch"
    # echo "TEST: Test branch: $1"
    [[ "$1" = "$git_branch" ]] && echo "TEST: On correct branch: $1" || exit 1
}

projects=( 'black-cats/kit' \
           'black-cats/kishka' \
           'black-cats/sasha' \
           'black-cats/jules' \
           'mu' \
           'duke' )

black_cat_projects=( 'black-cats/kit' \
                     'black-cats/kishka' \
                     'black-cats/sasha' \
                     'black-cats/jules' )

cd $TRAVIS_BUILD_DIR/examples/cats

test_breed_herd()
{
    print_separator
    echo "TEST: Normal herd after breed"
    ./breed.sh  || exit 1
    clowder herd  || exit 1
    clowder meow || exit 1
}

test_meow_groups()
{
    echo "TEST: Test meow for specific groups"
    clowder meow -g "$@" || exit 1
}

test_breed_herd_version()
{
    echo "TEST: Herd version after breed"
    ./breed.sh || exit 1
    clowder herd -v "$1" || exit 1
    clowder meow || exit 1
    clowder forall 'git checkout -b v0.1'
}

test_branch_version()
{
    local projects=("${@}")
    echo "TEST: Check current branches"
    for project in "${projects[@]}"
    do
    	pushd $project &>/dev/null
        test_branch v0.1
        popd &>/dev/null
    done
}

test_groom()
{
    print_separator
    make_dirty_repos "${projects[@]}"
    echo "TEST: Groom specific group when dirty"
    clowder groom -g "$@" || exit 1
    clowder meow || exit 1
    echo "TEST: Groom all when dirty"
    clowder groom || exit 1
    clowder meow || exit 1
    echo "TEST: Groom when clean"
    clowder groom || exit 1
    clowder meow || exit 1
}

test_dirty_repos()
{
    print_separator
    make_dirty_repos "${projects[@]}"
    echo "TEST: Fail herd with dirty repos"
    clowder herd && exit 1
    echo "TEST: Discard changes with groom"
    clowder groom || exit 1
    clowder meow || exit 1
    echo "TEST: Successfully herd after groom"
    clowder herd || exit 1
    clowder meow || exit 1
    echo "TEST: Successfully herd twice"
    clowder herd || exit 1
    clowder meow || exit 1
}

test_branch_master()
{
    local projects=("${@}")
    echo "TEST: Check current branches"
    for project in "${projects[@]}"
    do
    	pushd $project &>/dev/null
        test_branch master
        popd &>/dev/null
    done
}
test_branch_master "${black_cat_projects[@]}"
pushd mu &>/dev/null
test_branch knead
popd &>/dev/null
pushd duke &>/dev/null
test_branch purr
popd &>/dev/null

create_detached_heads()
{
    print_separator
    local projects=("${@}")
    echo "TEST: Create detached HEADs"
    for project in "${projects[@]}"
    do
    	pushd $project &>/dev/null
        git checkout master~2 &>/dev/null
        popd &>/dev/null
    done
    clowder meow || exit 1
}

test_herd()
{
    echo "TEST: Herd a previously fixed version"
    clowder herd -v v0.1 || exit 1
    clowder meow || exit 1
    echo "TEST: Normal herd after herding a previously fixed version"
    clowder herd || exit 1
    clowder meow || exit 1
    echo "TEST: Remove directories"
    rm -rf duke mu
    echo "TEST: Herd with 2 missing directories"
    clowder herd || exit 1
    clowder meow || exit 1
}

test_herd_detached_heads()
{
    create_detached_heads "${projects[@]}"
    echo "TEST: Successfully herd with detached HEADs"
    clowder herd || exit 1
    clowder meow || exit 1
}

test_sync()
{
    print_separator
    make_dirty_clowder_repo
    echo "TEST: Fail sync with dirty clowder repo"
    clowder sync && exit 1
    clowder meow || exit 1
    echo "TEST: Discard changes in clowder repo"
    pushd clowder &>/dev/null
    git reset --hard
    popd &>/dev/null
    echo "TEST: Successfully sync after discarding changes"
    clowder sync || exit 1
    clowder meow || exit 1
    echo "TEST: Successfully sync twice"
    clowder sync || exit 1
    clowder meow || exit 1
}

test_forall()
{
    print_separator
    echo "TEST: Run forall command"
    clowder forall 'git status' || exit 1
    echo "TEST: Run forall command for specific groups"
    clowder forall 'git status' -g "$@" || exit 1
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
    clowder meow || exit 1
    echo "TEST: Successfully fix version with path separator in input name"
    clowder fix path/separator
    clowder herd -v path-separator || exit 1
    clowder meow || exit 1
}

test_fix_missing_directories()
{
    echo "TEST: Remove directories"
    rm -rf "$@"
    echo "TEST: Fail fixing version with missing directories"
    clowder fix missing-directories && exit 1
    clowder meow || exit 1
}

make_dirty_clowder_repo()
{
    echo "TEST: Make dirty clowder repo"
    pushd clowder &>/dev/null
    touch newfile
    git add newfile
    popd &>/dev/null
    clowder meow || exit 1
}

make_dirty_repos()
{
    print_separator
    local projects=("${@}")
    echo "TEST: Make dirty repos"
    for project in "${projects[@]}"
    do
    	pushd $project &>/dev/null
        touch newfile
        git add newfile
        popd &>/dev/null
    done
    clowder meow -v || exit 1
}

test_stash()
{
    make_dirty_repos "${projects[@]}"
    echo "TEST: Fail herd with dirty repos"
    clowder herd && exit 1
    echo "TEST: Stash specific groups when dirty"
    clowder stash -g "$@" || exit 1
    clowder meow || exit 1
    echo "TEST: Stash all changes when dirty"
    clowder stash || exit 1
    clowder meow || exit 1
    echo "TEST: Stash changes when clean"
    clowder stash || exit 1
    clowder meow || exit 1
}

test_herd_groups()
{
    print_separator
    echo "TEST: Herd fixed version to test herding select groups"
    clowder herd -v v0.1 || exit 1
    clowder meow || exit 1
    print_separator
    echo "TEST: Herd only specific group"
    clowder herd -g "$@" || exit 1
    clowder meow || exit 1
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
    echo "TEST: clowder groom -h"
    clowder groom -h
    print_separator
    echo "TEST: clowder meow -h"
    clowder meow -h
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
