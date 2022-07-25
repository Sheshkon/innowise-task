#!/bin/sh
echo 'start celery worker'
MAX_TRIES_CONNECTIONS=5
sleep 10
result=$(curl -s "$LOCALSTACK_ENDPOINT_URL")
tries_connections=0

while [ "$result" != '{"status": "running"}' ] && [ "$tries_connections" != "$MAX_TRIES_CONNECTIONS" ]
do
  result=$(curl -s "$LOCALSTACK_ENDPOINT_URL")
  tries_connections=$((tries_connections+1))
  sleep 5
done

if [ "$tries_connections" = "$MAX_TRIES_CONNECTIONS" ]; then
  echo 'failed start worker: cannot connect to aws services'
else
  celery -A innotter worker -l INFO
  echo 'celery worker started'
fi
