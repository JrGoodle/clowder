#! /bin/bash

cd $TRAVIS_BUILD_DIR/examples/cats
./breed.sh && clowder herd -a && ./clean.sh || exit 1
./breed.sh && clowder herd && ./clean.sh || exit 1
./breed.sh && clowder herd -v v0.1 && clowder herd && ./clean.sh || exit 1
./breed.sh && clowder herd -a -v v0.1 && clowder herd -a && ./clean.sh || exit 1
