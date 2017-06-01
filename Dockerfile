FROM python:3.6.1
MAINTAINER Dan McCombs <dsmccombs@gmail.com>

COPY . /docker

RUN pip3 install -r /docker/requirements.txt

WORKDIR /docker

ENTRYPOINT /bin/bash
