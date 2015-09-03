#! /bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )"

echo 'Create source distribution'
echo '--------------------------'
sudo python3 setup.py sdist
echo ''

echo 'Create wheel'
echo '------------'
sudo python3 setup.py bdist_wheel

# echo 'Upload with twine'
# twine upload dist/*
