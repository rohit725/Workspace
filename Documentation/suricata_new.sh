#!/bin/bash

if [ ! -x "$(command -v docker)" ]; then
  #install docker if not installed
  sudo yum remove -y docker docker-common docker-selinux docker-engine docker-ce-cli
  sudo rm -rf /var/lib/docker
  sudo rm -rf /etc/docker
  sudo yum install -y docker
  sudo systemctl start docker
  sudo systemctl enable docker
  systemctl status docker
fi

docker login -u blusapphire -p triT@n76 docker01.blusapphire.net

# Remove existing container & image
docker ps -a | awk '{ print $1,$2 }' | grep "pcap_analysis:v1\.1" | awk '{print $1 }' | xargs -I {} docker rm -f {}
docker rmi docker01.blusapphire.net/master/pcap_analysis:v1.1

# Pull new image from docker01.blusapphire.net
docker pull docker01.blusapphire.net/master/pcap_analysis:v1.1

mkdir -p /opt/blusapphire/docker_files

# Start the container
container_id=$(docker run -td --name="suricata_container" -v /opt/blusapphire/docker_files:/var/log/suricata/logs --restart always --workdir "/etc/suricata" docker01.blusapphire.net/master/pcap_analysis:v1.1)
docker exec -it $container_id /bin/sh -c "sed -i -- 's/SURICATA //g' /etc/suricata/rules/*.rules"

docker logout docker01.blusapphire.net
