#!/bin/bash

if ! docker_loc="$(type -p "$docker")" || [[ -z $docker_loc ]]; then
  # install docker if not installed
  yum install -y docker
  systemctl start docker
  systemctl enable docker
  systemctl status docker
fi

docker login -u blusapphire -p triT@n76 docker01.blusapphire.net

docker ps -a | awk '{ print $1,$2 }' | grep "misp:v1\.1" | awk '{print $1 }' | xargs -I {} docker rm -f {}
docker rmi docker01.blusapphire.net/tisources/misp:v1.1
docker volume prune

docker pull docker01.blusapphire.net/tisources/misp:v1.1

docker run -it --rm -v /opt/499/data:/var/lib/mysql harvarditsecurity/misp /init-db

docker run -td --name="misp_container" \
    -v /docker/misp-db:/var/lib/mysql \
    -p 80:80 -p 3306:3306 -p 443:443 -p 6666:6666\
    --privileged=true harvarditsecurity/misp

docker logout docker01.blusapphire.net
