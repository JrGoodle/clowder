#! /bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )"
cd ../..

python3 -m unittest discover -v
