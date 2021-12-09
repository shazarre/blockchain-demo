#!/bin/sh
set -e

for i in 2 3;
do
  curl --request POST  \
    --url http://127.0.0.1:5001/node \
    --header 'Content-Type: application/json' \
    --data "{\"address\": \"http://blockchain-node-$i:5000\"}"
done
