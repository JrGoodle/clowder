#! /bin/bash

# set -xv

echo 'TEST: srclib example test script'

cd "$( dirname "${BASH_SOURCE[0]}" )" || exit 1
source test_utilities.sh
cd ../examples/srclib || exit 1

test_herd_missing_branches()
{
    print_separator
    echo "TEST: Herd v0.1 to test missing default branches"
    clowder herd -v v0.1 || exit 1
    echo "TEST: Delete default branches locally"
    pushd srclib &>/dev/null
    git branch -D master
    popd &>/dev/null
    pushd srcco &>/dev/null
    git branch -D master
    popd &>/dev/null
    echo "TEST: Herd existing repo's with no default branch locally"
    clowder herd || exit 1
    clowder status || exit 1
}

export projects=( 'samples/srclib-sample' \
                  'sourcegraph-talks' \
                  'srcco' \
                  'srclib' \
                  'toolchains/srclib-c' \
                  'toolchains/srclib-cpp' \
                  'toolchains/srclib-csharp' \
                  'toolchains/srclib-go' \
                  'toolchains/srclib-haskell' \
                  'toolchains/srclib-java' \
                  'toolchains/srclib-javascript' \
                  'toolchains/srclib-php' \
                  'toolchains/srclib-python' \
                  'toolchains/srclib-ruby' \
                  'toolchains/srclib-scala' )

export selected_projects=( 'samples/srclib-sample' \
                           'sourcegraph-talks' \
                           'srcco' \
                           'srclib' )

test_command
test_clowder_version

test_breed_herd_version
test_branch_version

test_breed_herd
test_branch_master
test_status_groups 'srclib' 'projects'
test_clean 'srclib' 'projects'
test_clean_projects 'sourcegraph/srclib'
test_herd_dirty_repos
test_herd_detached_heads
test_herd 'srclib' 'srcco'
test_forall 'srclib' 'projects'
test_forall_projects 'sourcegraph/srclib'
test_fix
test_stash 'srclib' 'projects'
test_stash_projects 'sourcegraph/srclib'
test_stash_missing_directories 'srclib'
test_herd_detached_heads
test_clean_missing_directories 'srclib'
test_herd_groups 'srclib' 'projects'
test_herd_missing_branches
test_fix_missing_directories 'srclib' 'srcco'
test_herd_projects 'sourcegraph/srclib-c'

print_help
