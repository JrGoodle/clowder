#! /bin/bash

cd $TRAVIS_BUILD_DIR/examples/cats
./breed.sh && clowder herd && clowder meow && ./clean.sh || exit 1
./breed.sh && clowder herd -v v0.1 && clowder herd && clowder meow && ./clean.sh || exit 1
