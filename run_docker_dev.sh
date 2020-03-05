#!/usr/bin/env bash
docker run -p 2121:2121 -v /srv/docker/sunrise:/srv/camera_security -e SUNRISE_CONFIG='config_ssl_auth.json' -i -t camera_security
