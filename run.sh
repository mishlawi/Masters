#!/bin/bash

# Run the built .jar and pass the IP arguments to it
java -jar target/ott-1.0-SNAPSHOT.jar "${@:1}"
