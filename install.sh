#!/usr/bin/env bash

set -eu
#set -x

cd "$( dirname "${BASH_SOURCE[0]}" )"
sudo python3 setup.py install
