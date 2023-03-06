#!/bin/bash

sed -i 's/host: localhost/host: wikidb/g' /config.yml
sed -i 's/db: wiki/db: wiki/g' /config.yml
sed -i 's/user: wikijs/user: root/g' /config.yml
sed -i 's/pass: wikijsrocks/pass: wiki/g' /config.yml
