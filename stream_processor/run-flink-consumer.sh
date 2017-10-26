#!/bin/bash

cd kafka-flink-101
mvn exec:java -Dexec.mainClass=com.inatel.demos.ReadFromKafka
