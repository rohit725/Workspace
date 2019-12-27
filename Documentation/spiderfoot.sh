#!/bin/bash

docker stop spiderfoot_container

docker rm spiderfoot_container

docker run -td --name="spiderfoot_container" -v /opt/blusapphire/docker_apps/Spiderfoot/spiderfoot-volume/spiderfoot.db:/home/spiderfoot/spiderfoot.db:rw \
    -v /opt/blusapphire/docker_apps/Spiderfoot/spiderfoot-volume/spiderfoot.db-shm:/home/spiderfoot/spiderfoot.db-shm:rw \
    -v /opt/blusapphire/docker_apps/Spiderfoot/spiderfoot-volume/spiderfoot.db-wal:/home/spiderfoot/spiderfoot.db-wal:rw \
    -p 5001:5001 \
    --privileged=true spiderfoot
