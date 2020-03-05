FROM balenalib/raspberrypi3-debian

MAINTAINER Colin Turner <koolspin245@gmail.com>

RUN apt-get update && apt-get -y install \
    curl \
    python3 \
    python3-pip \
    vim

# Take advantage of Docker cached layers and only re-install when necessary
ADD requirements.txt /tmp/requirements.txt
RUN cd /tmp && pip3 install -r requirements.txt

# Keep this here to take advantage of cached layers
# Speeds up Docker build a lot
WORKDIR /code
ADD . /code

EXPOSE 2121 2121

WORKDIR "app"
CMD ["python3", "./main.py"]

