#!/usr/bin/env bash
docker run --net=host -v /mnt/extdisk1/srv/docker/camera_security:/srv -v /tmp:/tmp -i -t camera_security /bin/sh
