#!/bin/bash

KAFKA_PATH=../../bigdata-tools/kafka_2.12-0.11.0.1

echo "Starting Kafka Console Producer"
$KAFKA_PATH/bin/kafka-console-producer.sh --topic flink-demo --broker-list localhost:9092




