#!/bin/bash

cd kafka-flink-101
mvn exec:java -Dexec.mainClass=com.grallandco.demos.SpeedAvg
