#! /bin/bash

# set -xv

print_separator()
{
    echo ''
    echo '--------------------------------------------------------------------------------'
    echo ''
}

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

print_separator

echo "TEST: Normal herd after breed"
./breed.sh  || exit 1
clowder herd  || exit 1
clowder meow || exit 1
./clean.sh || exit 1

print_separator

echo "TEST: Fail herd with missing clowder.yaml"
clowder herd && exit 1

echo "TEST: Herd version after breed"
./breed.sh || exit 1
clowder herd -v v0.1 || exit 1
clowder meow || exit 1

echo "TEST: Check current branches"
for project in "${projects[@]}"
do
	pushd $project &>/dev/null
    test_branch v0.1
    popd &>/dev/null
done

print_separator

echo "TEST: Make dirty repos"
for project in "${black_cat_projects[@]}"
do
	pushd $project &>/dev/null
    touch newfile
    git add newfile
    popd &>/dev/null
done
clowder meow || exit 1

echo "TEST: Groom when dirty"
clowder groom || exit 1
clowder meow || exit 1
echo "TEST: Groom when clean"
clowder groom || exit 1
clowder meow || exit 1

print_separator

echo "TEST: Make dirty repos"
for project in "${black_cat_projects[@]}"
do
	pushd $project &>/dev/null
    touch newfile
    git add newfile
    popd &>/dev/null
done
clowder meow || exit 1

echo "TEST: Fail herd with dirty repos"
clowder herd && exit 1
echo "TEST: Discard changes with groom"
clowder groom || exit 1
clowder meow || exit 1
echo "TEST: Successfully herd after groom"
clowder herd || exit 1
clowder meow || exit 1

echo "TEST: Check current branches"
for project in "${black_cat_projects[@]}"
do
	pushd $project &>/dev/null
    test_branch master
    popd &>/dev/null
done
pushd mu &>/dev/null
test_branch knead
popd &>/dev/null
pushd duke &>/dev/null
test_branch purr
popd &>/dev/null
echo ''

print_separator

echo "TEST: Create detached HEADs"
for project in "${black_cat_projects[@]}"
do
	pushd $project &>/dev/null
    git checkout master~2 &>/dev/null
    popd &>/dev/null
done
clowder meow || exit 1
echo "TEST: Successfully herd with detached HEADs"
clowder herd || exit 1
clowder meow || exit 1
echo "TEST: Herd a previously fixed version"
clowder herd -v v0.1 || exit 1
clowder meow || exit 1
echo "TEST: Normal herd after herding a previously fixed version"
clowder herd || exit 1
clowder meow || exit 1

print_separator

echo "TEST: Make dirty clowder repo"
pushd clowder &>/dev/null
touch newfile
git add newfile
popd &>/dev/null
clowder meow || exit 1

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

print_separator

echo "TEST: Run forall command"
clowder forall -c 'git status' || exit 1
echo "TEST: Run forall command for specific groups"
clowder forall -g cats -c 'git status' || exit 1

print_separator

echo "TEST: Fail herding a previously fixed version"
clowder herd -v v100 && exit 1
echo "TEST: Fail fixing a previously fixed version"
clowder fix -v v0.1 && exit 1
echo "TEST: Successfully fix a new version"
clowder fix -v v0.11 || exit 1
clowder meow || exit 1

print_separator

echo "TEST: Make dirty repos"
for project in "${black_cat_projects[@]}"
do
	pushd $project &>/dev/null
    touch newfile
    git add newfile
    popd &>/dev/null
done
clowder meow -v || exit 1

echo "TEST: Fail herd with dirty repos"
clowder herd && exit 1
echo "TEST: Stash changes when dirty"
clowder stash || exit 1
clowder meow || exit 1
echo "TEST: Stash changes when clean"
clowder stash || exit 1
clowder meow || exit 1

print_separator

echo "TEST: Remove directories"
rm -rf duke mu
echo "TEST: Herd with 2 missing directories"
clowder herd || exit 1
clowder meow || exit 1

print_separator

echo "TEST: Herd fixed version to test herding select groups"
clowder herd -v v0.11 || exit 1
clowder meow || exit 1

print_separator

echo "TEST: Herd only specific group"
clowder herd -g cats || exit 1
clowder meow || exit 1

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

echo "TEST: Fail with unrecognized command"
clowder cat && exit 1

print_separator
echo "TEST: Fail herd with invalid yaml"
pushd clowder &>/dev/null
git checkout invalid-yaml
popd &>/dev/null
clowder herd && exit 1

print_separator
pushd clowder &>/dev/null
git checkout master
popd &>/dev/null
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
