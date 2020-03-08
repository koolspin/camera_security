#!/usr/bin/env bash
docker run --net=host -v /srv/docker/camera_security:/srv -v /tmp:/tmp -i -t camera_security /bin/sh
