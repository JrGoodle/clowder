#! /bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )" || exit 1
sudo -H rm -rf clowder.egg-info
sudo -H rm -rf dist
sudo -H rm -rf build
sudo -H pip3 uninstall clowder
