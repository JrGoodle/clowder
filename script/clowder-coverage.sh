#!/usr/bin/env bash

aws s3 sync "s3://clowder-coverage/coverage/$BUILD_NUMBER" coverage/
cc-test-reporter sum-coverage --output - --parts $PARTS coverage/codeclimate.*.json | \
  cc-test-reporter upload-coverage --input -
