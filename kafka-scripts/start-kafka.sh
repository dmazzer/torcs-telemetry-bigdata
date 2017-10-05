#!/bin/bash

KAFKA_PATH=../../bigdata-tools/kafka_2.12-0.11.0.1

echo "Starting Zookeeper"
$KAFKA_PATH/bin/zookeeper-server-start.sh $KAFKA_PATH/config/zookeeper.properties &

sleep 5

echo "Starting Kafka Server"
$KAFKA_PATH/bin/kafka-server-start.sh $KAFKA_PATH/config/server.properties &

sleep 10

echo "Zookeeper and Kafka should be up and running..."



