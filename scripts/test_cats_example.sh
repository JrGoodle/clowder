#! /bin/bash

set -xv

echo 'TEST: cats example test script'

cd "$( dirname "${BASH_SOURCE[0]}" )" || exit 1
source test_utilities.sh
cd ../examples/cats || exit 1

test_branches()
{
    test_branch_master "${projects[@]}"
    pushd mu &>/dev/null
    test_branch knead
    popd &>/dev/null
    pushd duke &>/dev/null
    test_branch purr
    popd &>/dev/null
}

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
    clowder status || exit 1
}

test_herd_missing_groups()
{
    echo "TEST: Test herd of missing group"
    clowder herd -v missing-groups
    clowder herd -g slavic || exit 1
    clowder status || exit 1
}

test_herd_sha()
{
    print_separator
    echo "TEST: Test herd of static commit hash refs"
    clowder repo 'git checkout static-refs'
    clowder herd || exit 1
    clowder status || exit 1
    clowder repo 'git checkout master'
}

test_herd_tag()
{
    print_separator
    echo "TEST: Test herd of tag refs"
    clowder repo 'git checkout tags'
    clowder herd || exit 1
    clowder status || exit 1
    clowder repo 'git checkout master'
}

test_invalid_yaml()
{
    print_separator
    echo "TEST: Fail herd with invalid yaml"

    clowder repo 'git checkout invalid-yaml'

    test_cases=( 'missing-default-arg' \
                 'unknown-defaults-arg' \
                 'missing-sources' \
                 'unknown-source-arg' \
                 'missing-project-arg' \
                 'unknown-project-arg' )

    for test in "${test_cases[@]}"
    do
      	clowder herd -v $test && exit 1
        clowder herd && exit 1
        rm clowder.yaml
    done

    pushd .clowder &>/dev/null
    git checkout master
    popd &>/dev/null
}

test_no_versions()
{
    print_separator
    echo "TEST: Test clowder repo with no versions saved"
    clowder repo 'git checkout no-versions'
    clowder herd -v saved-version && exit 1
    clowder herd || exit 1
    clowder status || exit 1
    clowder repo 'git checkout master'
}

# export projects=( 'black-cats/kit' \
#                   'black-cats/kishka' \
#                   'black-cats/sasha' \
#                   'black-cats/jules' \
#                   'mu' \
#                   'duke' )

export projects=( 'black-cats/kit' \
                  'black-cats/kishka' \
                  'black-cats/sasha' \
                  'black-cats/jules' )

test_command
test_clowder_version

test_init_herd_version
test_branch_version

test_init_herd
test_branches
test_status_groups 'black-cats'
test_invalid_yaml
test_clean 'black-cats'
test_clean_projects 'jrgoodle/kit'
test_clean_missing_directories 'mu' 'duke'
test_herd_dirty_repos
test_herd_detached_heads
test_herd 'duke' 'mu'
test_forall 'cats'
test_forall_projects 'jrgoodle/kit' 'jrgoodle/kishka'
test_save
test_stash 'black-cats'
test_stash_projects 'jrgoodle/kit'
test_stash_missing_directories 'mu' 'duke'
test_herd_groups 'cats'
test_herd_missing_branches
test_save_missing_directories 'duke' 'mu'
test_no_versions
test_herd_projects 'jrgoodle/kit' 'jrgoodle/kishka'

test_invalid_yaml
test_herd_sha
test_herd_tag
test_herd_missing_groups

print_help
