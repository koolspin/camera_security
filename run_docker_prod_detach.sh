#!/usr/bin/env bash
docker run -p 2121:2121 -v /srv/docker/sunrise:/srv/sunrise -e SUNRISE_CONFIG='config_no_ssl.json' -d camera_security

