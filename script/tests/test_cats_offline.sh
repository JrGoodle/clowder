#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

export all_projects=( 'mu' 'duke' \
                      'black-cats/kit' \
                      'black-cats/kishka' \
                      'black-cats/sasha' \
                      'black-cats/jules' )

echo 'Make sure your network connection is enabled'
# https://unix.stackexchange.com/a/293941
read -n 1 -s -r -p "Press any key to continue"
echo ''
echo ''

prepare_cats_example
cd "$CATS_EXAMPLE_DIR" || exit 1

print_double_separator
echo "TEST: Test clowder offline"

./clean.sh || exit 1
./init.sh || exit 1
clowder herd || exit 1

echo 'Disable your network connection'
# https://unix.stackexchange.com/a/293941
read -n 1 -s -r -p "Press any key to continue"
echo ''
echo ''

print_double_separator
echo 'TEST: clowder branch'
clowder branch || exit 1
print_single_separator
echo 'TEST: clowder branch -r'
clowder branch -r || exit 1
print_single_separator
echo 'TEST: clowder branch -a'
clowder branch -a || exit 1
print_single_separator
echo 'TEST: clowder clean'
clowder clean || exit 1
print_single_separator
echo 'TEST: clowder diff'
clowder diff || exit 1
print_single_separator
echo 'TEST: clowder forall'
clowder forall -c 'git status' || exit 1
print_single_separator
echo 'TEST: clowder herd'
clowder herd && exit 1
print_single_separator
echo 'TEST: clowder link'
clowder link -v v0.1 || exit 1
clowder link || exit 1
print_single_separator
echo 'TEST: clowder prune'
clowder prune branch || exit 1
print_single_separator
echo 'TEST: clowder prune -r'
clowder prune -r branch && exit 1
print_single_separator
echo 'TEST: clowder prune -a'
clowder prune -a branch && exit 1
print_single_separator
echo 'TEST: clowder repo add'
clowder repo add . || exit 1
print_single_separator
echo 'TEST: clowder repo checkout'
clowder repo checkout tags || exit 1
clowder repo checkout master || exit 1
print_single_separator
echo 'TEST: clowder repo clean'
clowder repo clean || exit 1
print_single_separator
echo 'TEST: clowder repo commit'
pushd .clowder
touch newfile || exit 1
git add newfile || exit 1
popd
clowder repo commit 'Add newfile' || exit 1
pushd .clowder
git reset --hard HEAD~1 || exit 1
popd
print_single_separator
echo 'TEST: clowder repo pull'
clowder repo pull && exit 1
print_single_separator
echo 'TEST: clowder repo push'
clowder repo push && exit 1
print_single_separator
echo 'TEST: clowder repo run'
clowder repo run 'git status' || exit 1
print_single_separator
echo 'TEST: clowder repo status'
clowder repo status || exit 1
print_single_separator
echo 'TEST: clowder save'
clowder save offline_version || exit 1
print_single_separator
echo 'TEST: clowder start'
clowder start local_branch || exit 1
for project in "${all_projects[@]}"; do
	pushd $project
    test_branch 'local_branch'
    popd
done
print_single_separator
echo 'TEST: clowder start -t'
clowder start -t tracking_branch && exit 1
print_single_separator
echo 'TEST: clowder stash'
clowder stash || exit 1
print_single_separator
echo 'TEST: clowder status'
clowder status || exit 1
print_single_separator
echo 'TEST: clowder status -f'
clowder status -f && exit 1
print_single_separator
echo 'TEST: clowder sync'
clowder sync && exit 1
print_single_separator
echo 'TEST: clowder init'
rm -rf .clowder || exit 1
clowder init git@github.com:JrGoodle/cats.git && exit 1

echo 'You can enable your network connection again'
echo ''
