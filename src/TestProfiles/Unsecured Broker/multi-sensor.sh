#!/bin/bash

trap 'kill $(jobs -p)' SIGINT SIGTERM EXIT

echo "simulating $1 poisoned sensor for unsecured broker testing"
for i in $(seq 1 $1)
do
    python3 extraNode.py "/home/ubuntu/data/data_$i.csv" &
    echo "$i sensor deployed!"
done 
sleep $2
