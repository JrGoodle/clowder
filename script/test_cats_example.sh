#!/usr/bin/env bash

# set -xv

echo 'TEST: cats example test script'

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

if [ -n "$TRAVIS_OS_NAME" ]; then
    if [ "$TRAVIS_OS_NAME" = "osx" ]; then
        ./unittests.sh || exit 1
    fi
fi

. test_utilities.sh
../examples/cats/clean.sh

if [ -n "$TRAVIS_OS_NAME" ]; then
    cd ../examples/cats || exit 1
else
    rm -rf "$HOME/.clowder_tests"
    mkdir -p "$HOME/.clowder_tests" && cp -r ../examples/cats "$HOME/.clowder_tests/cats"
    cd "$HOME/.clowder_tests/cats" || exit 1
fi

export projects=( 'black-cats/kit' \
                  'black-cats/kishka' \
                  'black-cats/sasha' \
                  'black-cats/jules' )

test_init_branch()
{
    print_separator
    echo "TEST: Test clowder init branch"

    clowder init https://github.com/jrgoodle/cats.git -b tags

    pushd .clowder
    test_branch tags
    popd

    rm -rf .clowder clowder.yaml
}
test_init_branch

test_command
test_clowder_version
test_init_herd_version
test_branch_version "${projects[@]}"
test_init_herd

test_branches()
{
    print_separator
    echo "TEST: Test branches"
    test_branch_master "${projects[@]}"
    pushd mu
    test_branch knead
    popd
    pushd duke
    test_branch purr
    popd
}
test_branches

test_status_groups 'black-cats'
test_status_projects 'jrgoodle/mu' 'jrgoodle/duke'

test_clean()
{
    print_separator
    echo "TEST: Clean repos"
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
test_clean 'black-cats'

test_clean_projects()
{
    print_separator
    echo "TEST: Clean projects"
    make_dirty_repos "${projects[@]}"
    echo "TEST: Clean specific project when dirty"
    clowder clean -p "$@" || exit 1
    clowder status || exit 1
    echo "TEST: Clean all when dirty"
    clowder clean || exit 1
    clowder status || exit 1
}
test_clean_projects 'jrgoodle/kit'

test_clean_missing_directories 'mu' 'duke'
test_herd_dirty_repos "${projects[@]}"
test_herd_detached_heads "${projects[@]}"
test_herd 'duke' 'mu'
test_forall 'cats'
test_forall_projects 'jrgoodle/kit' 'jrgoodle/kishka'
test_save

test_stash()
{
    print_separator
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
test_stash 'black-cats'

test_stash_projects()
{
    print_separator
    make_dirty_repos "${projects[@]}"
    echo "TEST: Stash specific projects when dirty"
    clowder stash -p "$@" || exit 1
    clowder status || exit 1
    echo "TEST: Stash all changes when dirty"
    clowder stash || exit 1
    clowder status || exit 1
}
test_stash_projects 'jrgoodle/kit'

test_stash_missing_directories 'mu' 'duke'
test_herd_groups 'cats'

test_herd_missing_branches()
{
    print_separator
    echo "TEST: Herd v0.1 to test missing default branches"
    clowder link -v v0.1 || exit 1
    clowder herd || exit 1
    echo "TEST: Delete default branches locally"
    pushd mu
    git branch -D knead
    popd
    pushd duke
    git branch -D purr
    popd
    echo "TEST: Herd existing repo's with no default branch locally"
    clowder link || exit 1
    clowder herd || exit 1
    clowder status || exit 1
}
test_herd_missing_branches

test_save_missing_directories 'duke' 'mu'

test_no_versions()
{
    print_separator
    echo "TEST: Test clowder repo with no versions saved"
    clowder repo checkout no-versions || exit 1
    clowder link -v saved-version && exit 1
    clowder herd || exit 1
    clowder status || exit 1
    clowder repo checkout master || exit 1
}
test_no_versions

test_herd_projects 'jrgoodle/kit' 'jrgoodle/kishka'

test_invalid_yaml()
{
    print_separator
    echo "TEST: Fail herd with invalid yaml"

    pushd .clowder/versions
    test_cases=( $(ls -d test-*) )
    popd

    for test in "${test_cases[@]}"
    do
        clowder link -v $test || exit 1
        clowder herd && exit 1
        rm clowder.yaml
    done
}
test_invalid_yaml

test_herd_sha()
{
    print_separator
    echo "TEST: Test herd of static commit hash refs"
    clowder repo checkout static-refs || exit 1
    clowder herd || exit 1
    clowder status || exit 1
    clowder repo checkout master || exit 1
}
test_herd_sha

test_herd_tag()
{
    print_separator
    echo "TEST: Test herd of tag refs"
    clowder repo checkout tags || exit 1
    clowder herd || exit 1
    clowder status || exit 1
    clowder repo checkout master || exit 1
}
test_herd_tag

test_start()
{
    print_separator
    echo "TEST: Start new branch"
    clowder herd

    clowder start start_branch || exit 1
    # TODO: clowder herd -b
    # clowder herd -b master -g black-cats
    clowder forall -g black-cats -c 'git fetch origin master'
    clowder forall -g black-cats -c 'git checkout master'

    pushd mu
    test_branch start_branch
    popd
    pushd duke
    test_branch start_branch
    popd
    pushd black-cats/jules
    test_branch master
    popd
    pushd black-cats/kishka
    test_branch master
    popd

    clowder start start_branch || exit 1

    pushd black-cats/jules
    test_branch start_branch
    popd
    pushd black-cats/kishka
    test_branch start_branch
    popd
}
test_start

if [ -z "$TRAVIS_OS_NAME" ]; then
    test_start_tracking()
    {
        print_separator
        echo "TEST: Test start tracking branch"
        clowder herd

        echo "TEST: No local or remote branches"
        clowder prune -af tracking_branch || exit 1
        clowder start -t tracking_branch || exit 1

        pushd duke
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd mu
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd black-cats/jules
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd black-cats/kishka
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd

        echo "TEST: Existing local branch checked out, remote tracking branch exists"
        clowder prune -af tracking_branch || exit 1
        clowder start -t tracking_branch || exit 1
        clowder start -t tracking_branch || exit 1

        echo "TEST: Existing local branch not checked out, remote tracking branch exists"
        clowder prune -af tracking_branch || exit 1
        clowder start -t tracking_branch || exit 1
        clowder forall -c 'git checkout master' || exit 1
        clowder start -t tracking_branch || exit 1

        echo "TEST: No local branch, existing remote branch"
        clowder prune -af tracking_branch || exit 1
        clowder start -t tracking_branch || exit 1
        clowder prune -f tracking_branch || exit 1
        clowder start -t tracking_branch && exit 1

        pushd duke
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_no_tracking_branch_exists tracking_branch
        popd
        pushd mu
        test_branch knead
        test_remote_branch_exists tracking_branch
        test_no_tracking_branch_exists tracking_branch
        popd
        pushd black-cats/jules
        test_branch master
        test_remote_branch_exists tracking_branch
        test_no_tracking_branch_exists tracking_branch
        popd
        pushd black-cats/kishka
        test_branch master
        test_remote_branch_exists tracking_branch
        test_no_tracking_branch_exists tracking_branch
        popd

        echo "TEST: Existing local branch checked out, existing remote branch, no tracking relationship"
        clowder prune -af tracking_branch || exit 1
        clowder start -t tracking_branch || exit 1
        clowder prune -f tracking_branch || exit 1
        clowder forall -c 'git checkout -b tracking_branch' || exit 1
        clowder start -t tracking_branch && exit 1

        echo "TEST: Existing local branch not checked out, existing remote branch, no tracking relationship"
        clowder prune -af tracking_branch || exit 1
        clowder start -t tracking_branch || exit 1
        clowder prune -f tracking_branch || exit 1
        clowder forall -c 'git checkout -b tracking_branch' || exit 1
        clowder forall -c 'git checkout master' || exit 1
        clowder start -t tracking_branch && exit 1

        echo "TEST: Existing local branch checked out, no remote branch"
        clowder prune -af tracking_branch
        clowder start tracking_branch || exit 1
        clowder start -t tracking_branch || exit 1

        pushd duke
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd mu
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd black-cats/jules
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd black-cats/kishka
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd

        echo "TEST: Existing local branch not checked out, no remote branch"
        clowder prune -r tracking_branch
        clowder start tracking_branch || exit 1
        clowder forall -c 'git checkout master'
        clowder start -t tracking_branch || exit 1

        pushd duke
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd mu
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd black-cats/jules
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
        pushd black-cats/kishka
        test_branch tracking_branch
        test_remote_branch_exists tracking_branch
        test_tracking_branch_exists tracking_branch
        popd
    }
    test_start_tracking
fi

test_prune()
{
    print_separator
    echo "TEST: Test clowder prune branch"
    clowder herd

    clowder start prune_branch
    clowder prune -f prune_branch || exit 1

    pushd duke
    test_branch purr
    test_no_local_branch_exists prune_branch
    popd
    pushd mu
    test_branch knead
    test_no_local_branch_exists prune_branch
    popd
    pushd black-cats/jules
    test_branch master
    test_no_local_branch_exists prune_branch
    popd
    pushd black-cats/kishka
    test_branch master
    test_no_local_branch_exists prune_branch
    popd

    clowder start prune_branch
    clowder prune -f prune_branch -g black-cats || exit 1

    pushd duke
    test_branch prune_branch
    popd
    pushd mu
    test_branch prune_branch
    popd
    pushd black-cats/jules
    test_branch master
    test_no_local_branch_exists prune_branch
    popd
    pushd black-cats/kishka
    test_branch master
    test_no_local_branch_exists prune_branch
    popd

    echo "TEST: Test clowder force prune branch"

    clowder start prune_branch
    pushd duke
    touch something
    git add something
    git commit -m 'something'
    popd
    pushd mu
    touch something
    git add something
    git commit -m 'something'
    popd

    clowder prune prune_branch && exit 1
    clowder prune -f prune_branch || exit 1

    pushd duke
    test_branch purr
    popd
    pushd mu
    test_branch knead
    popd

    if [ -z "$TRAVIS_OS_NAME" ]; then
        echo "TEST: Test clowder prune remote branch"

        clowder prune -af prune_branch || exit 1
        clowder start -t prune_branch -p jrgoodle/duke || exit 1
        clowder prune -f prune_branch || exit 1

        pushd duke
        test_no_local_branch_exists prune_branch
        test_remote_branch_exists prune_branch
        popd

        clowder prune -r prune_branch || exit 1

        pushd duke
        test_no_local_branch_exists prune_branch
        test_no_remote_branch_exists prune_branch
        popd

        echo "TEST: Test clowder prune all - delete local and remote branch"
        clowder start -t prune_branch -p jrgoodle/duke || exit 1

        pushd duke
        test_local_branch_exists prune_branch
        test_remote_branch_exists prune_branch
        popd

        clowder prune -af prune_branch || exit 1

        pushd duke
        test_no_local_branch_exists prune_branch
        test_no_remote_branch_exists prune_branch
        popd
    fi
}
test_prune

test_clowder_repo()
{
    print_separator
    echo "TEST: Test clowder repo command"
    clowder repo checkout ref_that_doesnt_exist && exit 1
    clowder repo add file_that_doesnt_exist && exit 1
}
test_clowder_repo

test_clowder_import()
{
    print_separator
    echo "TEST: Test clowder file with default import"

    clowder link
    clowder herd
    clowder link -v import-default
    clowder herd
    pushd black-cats/jules
    test_branch import-default
    popd
    pushd black-cats/kishka
    test_branch import-default
    popd
    pushd black-cats/kit
    test_branch import-default
    popd
    pushd black-cats/sasha
    test_branch import-default
    popd

    echo "TEST: Test clowder file with version import"
    clowder link
    clowder herd
    clowder link -v import-version
    clowder herd
    pushd black-cats/jules
    test_branch import-version
    popd
    pushd black-cats/kishka
    test_branch import-version
    popd
    pushd black-cats/kit
    test_branch import-version
    popd
    pushd black-cats/sasha
    test_branch import-version
    popd
}
test_clowder_import

test_print()
{
    print_separator

    clowder repo checkout master || exit 1

    clowder link -v 'missing-defaults'
    clowder herd
    print_help

    clowder link
    clowder herd
    print_help
}
test_print
