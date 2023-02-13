#!/bin/sh
echo 'start web'
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
  echo 'failed start web: cannot connect to localstack services'
else
  python manage.py migrate
  python manage.py runserver 0.0.0.0:8000
  echo 'web started'
fi
