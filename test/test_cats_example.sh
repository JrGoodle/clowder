#! /bin/bash

cd $TRAVIS_BUILD_DIR/examples/cats
./breed.sh && clowder herd -a && ./clean.sh
./breed.sh && clowder herd && ./clean.sh
./breed.sh && clowder herd -v v0.1 && ./clean.sh
