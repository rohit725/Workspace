#!/bin/bash

if ! docker_loc="$(type -p "$docker")" || [[ -z $docker_loc ]]; then
  # install foobar here
  yum install -y docker
  systemctl start docker
  systemctl enable docker
  systemctl status docker
fi

docker login -u blusapphire -p triT@n76 docker01.blusapphire.net
docker pull docker01.blusapphire.net/master/pcap_analysis:v1.1
mkdir -p /opt/blusapphire/dockerfiles
docker run -td --name="suricata_container" -v /opt/blusapphire/dockerfiles:/var/log/suricata/logs docker01.blusapphire.net/master/pcap_analysis:v1.1
