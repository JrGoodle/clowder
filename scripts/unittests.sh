#! /bin/bash

cd ${TRAVIS_BUILD_DIR}
python3 -m unittest discover -v
