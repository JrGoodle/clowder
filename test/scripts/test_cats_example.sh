#! /bin/bash

test_branch()
{
    local git_branch
    git_branch=$(git rev-parse --abbrev-ref HEAD)
    echo "TEST: Current branch: $git_branch"
    echo "TEST: Test branch: $1"
    [[ "$1" = "$git_branch" ]] && echo "TEST: On correct branch: $1" || exit 1
}

cd $TRAVIS_BUILD_DIR/examples/cats

./breed.sh  || exit 1
clowder herd  || exit 1
clowder meow || exit 1
./clean.sh || exit 1

./breed.sh || exit 1
clowder herd -v v0.1 || exit 1

clowder meow || exit 1

projects=( 'black-cats/kit' \
            'black-cats/kishka' \
            'black-cats/sasha' \
            'black-cats/jules' \
            'mu' \
            'duke' )

for project in "${projects[@]}"
do
	pushd $project &>/dev/null
    test_branch clowder-fix/v0.1
    popd &>/dev/null
done

clowder meow || exit 1

for project in "${projects[@]}"
do
	pushd $project &>/dev/null
    touch newfile
    git add newfile
    popd &>/dev/null
done

clowder meow || exit 1
clowder herd || exit 1

for project in "${projects[@]}"
do
	pushd $project &>/dev/null
    test_branch master
    popd &>/dev/null
done

clowder meow || exit 1
