#! /bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )"
source functional_tests.sh
cd ../../examples/cats

test_herd_missing_branches()
{
    print_separator
    echo "TEST: Herd v0.1 to test missing default branches"
    clowder herd -v v0.1 || exit 1
    echo "TEST: Delete default branches locally"
    pushd mu &>/dev/null
    git branch -D knead
    popd &>/dev/null
    pushd duke &>/dev/null
    git branch -D purr
    popd &>/dev/null
    echo "TEST: Herd existing repo's with no default branch locally"
    clowder herd || exit 1
    clowder meow || exit 1
}

test_herd_missing_groups()
{
    echo "TEST: Test herd of missing group"
    pushd clowder &>/dev/null
    git checkout master
    popd &>/dev/null
    clowder herd -v missing-groups
    clowder herd -g slavic || exit 1
    clowder meow || exit 1
}

test_herd_sha()
{
    print_separator
    echo "TEST: Test herd of static commit hash refs"
    pushd clowder &>/dev/null
    git checkout static-refs
    popd &>/dev/null
    clowder herd || exit 1
    clowder meow || exit 1
}

test_herd_tag()
{
    print_separator
    echo "TEST: Test herd of tag refs"
    pushd clowder &>/dev/null
    git checkout tags
    popd &>/dev/null
    clowder herd || exit 1
    clowder meow || exit 1
}

test_invalid_yaml()
{
    print_separator
    echo "TEST: Fail herd with invalid yaml"
    pushd clowder &>/dev/null
    git checkout invalid-yaml
    popd &>/dev/null
    clowder herd && exit 1
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

test_command
test_breed_herd
test_meow_groups 'cats'
test_invalid_yaml
test_breed_herd_version 'v0.1'
test_branch_version
test_groom
test_dirty_repos

test_branch_master "${projects[@]}"
pushd mu &>/dev/null
test_branch knead
popd &>/dev/null
pushd duke &>/dev/null
test_branch purr
popd &>/dev/null

test_herd_detached_heads
test_herd
test_sync
test_forall 'cats'
test_fix
test_stash
test_herd_groups
test_herd_missing_branches
test_invalid_yaml
test_herd_sha
test_herd_tag
test_herd_missing_groups
test_fix_missing_directories 'duke' 'mu'

print_help
