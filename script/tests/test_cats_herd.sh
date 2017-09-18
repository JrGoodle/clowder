#!/usr/bin/env bash

pushd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

export projects=( 'black-cats/kit' \
                  'black-cats/kishka' \
                  'black-cats/sasha' \
                  'black-cats/jules' )

clowder forall -c 'git checkout -b v0.1'
echo "TEST: Check current branches"
for project in "${projects[@]}"; do
	pushd $project
    test_branch v0.1
    popd
done

test_herd()
{
    print_separator
    echo "TEST: Check current branches are on master"
    clowder herd
    for project in "${projects[@]}"; do
    	pushd $project
        test_branch master
        popd
    done
    pushd mu
    test_branch knead
    popd
    pushd duke
    test_branch purr
    popd
}
test_herd

test_herd_dirty_repos()
{
    print_separator
    make_dirty_repos "$@"
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
test_herd_dirty_repos "${projects[@]}"

test_herd_detached_heads()
{
    print_separator
    echo "TEST: Create detached HEADs"
    for project in "$@"
    do
    	pushd $project
        git checkout master~2
        popd
    done
    clowder status || exit 1
    echo "TEST: Successfully herd with detached HEADs"
    clowder herd || exit 1
}
test_herd_detached_heads "${projects[@]}"

test_herd()
{
    print_separator
    echo "TEST: Successfully herd a previously saved version"
    clowder link -v v0.1 || exit 1
    clowder herd || exit 1
    echo "TEST: Successfully herd after herding a previously saved version"
    clowder link || exit 1
    clowder herd || exit 1
    echo "TEST: Remove directories"
    rm -rf "$@"
    echo "TEST: Successfully herd with missing directories"
    clowder herd || exit 1
}
test_herd 'duke' 'mu'

test_herd_groups()
{
    print_separator
    echo "TEST: Herd saved version to test herding select groups"
    clowder link -v v0.1 || exit 1
    clowder herd || exit 1
    print_separator
    echo "TEST: Herd only specific groups"
    clowder herd -g "$@" || exit 1
    clowder status || exit 1
}
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

test_herd_projects()
{
    print_separator
    echo "TEST: Successfully herd specific projects"
    clowder herd -p "$@" || exit 1
}
test_herd_projects 'jrgoodle/kit' 'jrgoodle/kishka'

popd
