#!/bin/bash

apt-get update
apt-get install -y vim ssh python-pip git jq unzip

wget -qO- https://get.docker.com/ | sh

groupadd docker
sudo gpasswd -a $USER docker
# need to restart docker to enable docker command w/o sudo
sudo service docker restart

# two ways of installing docker-compose, currently use curl
# pip install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

pip install flask
docker pull consul:latest
docker pull gliderlabs/registrator:latest
docker pull node:5.0
docker pull mongo:latest
