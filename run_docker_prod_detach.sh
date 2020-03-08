#!/usr/bin/env bash
docker run --net=host -v /srv/docker/camera_security:/srv -v /tmp:/tmp -d camera_security

