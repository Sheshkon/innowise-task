#!/bin/sh
set -x
awslocal s3 mb s3://${S3_BUCKET}
set +x

awslocal dynamodb create-table --cli-input-json file:///docker-entrypoint-initaws.d/dynamodb_conf/schema.json