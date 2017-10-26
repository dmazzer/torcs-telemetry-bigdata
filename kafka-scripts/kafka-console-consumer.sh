#!/bin/bash

KAFKA_PATH=../../bigdata-tools/kafka_2.12-0.11.0.1

echo "Starting Kafka Console Consumer"
$KAFKA_PATH/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic flink-demo
