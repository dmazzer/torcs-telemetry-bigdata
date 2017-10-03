#!/bin/bash

file="./udp-kafka-bridge-assembly-0.1.jar"
if [ -f "$file" ]
then
	echo "$file found."
else
	echo "$file not found, downloading"
	wget -c https://github.com/agaoglu/udp-kafka-bridge/releases/download/v0.1/udp-kafka-bridge-assembly-0.1.jar
fi

java -Dconfig.file=udp-bridge.conf -jar udp-kafka-bridge-assembly-0.1.jar
