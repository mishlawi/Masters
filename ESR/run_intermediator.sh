#!/bin/bash

# Run the built .jar and pass the IP arguments to it
java -jar intermediator/target/intermediator-1.0-SNAPSHOT-jar-with-dependencies.jar "${@:1}"
