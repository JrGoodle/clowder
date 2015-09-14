#!/bin/bash

i=0
test_scripts=('scripts/test_cats_example.sh' \
              'scripts/test_llvm_example.sh' \
              'scripts/test_srclib_example.sh' \
              'scripts/unittests.sh')
for testfile in "${test_scripts[@]}"; do
  if [ $(($i % $CIRCLE_NODE_TOTAL)) -eq $CIRCLE_NODE_INDEX ]
  then
    $testfile
  fi
  ((i=i+1))
done
