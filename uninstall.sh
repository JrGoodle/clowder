#! /bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )"
sudo -H pip3 uninstall clowder
sudo -H rm -rf clowder.egg-info
sudo -H rm -rf dist
sudo -H rm -rf build
