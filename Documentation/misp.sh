#!/bin/bash

docker stop misp_container

docker rm misp_container

docker run -td --name="misp_container" \
    -v /docker/misp-db:/var/lib/mysql \
    -p 80:80 -p 3306:3306 -p 443:443 -p 6666:6666\
    --privileged=true harvarditsecurity/misp
