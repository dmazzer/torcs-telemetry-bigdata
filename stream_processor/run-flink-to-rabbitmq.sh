#!/bin/bash

cd kafka-flink-101
mvn exec:java -Dexec.mainClass=com.inatel.demos.SendToTeams -Dexec.args="$1 $2"
