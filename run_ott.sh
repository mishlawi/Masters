#!/bin/bash

# Run the built .jar and pass the IP arguments to it
java -jar ott/target/ott-1.0-SNAPSHOT-jar-with-dependencies.jar "${@:1}"
