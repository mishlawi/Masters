#!/bin/sh

# Install missing dependencies & build project .jar
mvn clean compile assembly:single
