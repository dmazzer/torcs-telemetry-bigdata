#!/bin/bash

IP='127.0.0.1'
PORT=7000

echo "Starting UDP Server. Listening ip $IP and port $PORT."

nc -ul $IP $PORT


