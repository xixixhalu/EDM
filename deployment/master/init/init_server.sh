#!/bin/bash
apt-get update
apt-get install -y python-pip vim ssh git jq unzip

wget -qO- https://get.docker.com/ | sh

groupadd docker
sudo gpasswd -a $USER docker
# need to restart docker to enable docker command w/o sudo
sudo service docker restart

# two ways of installing docker-compose, currently use curl
# pip install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

docker pull consul:latest
docker pull nginx:latest
docker pull gogs/gogs:latest


# install dependencies of EDM
pip install flask

apt-get install -y build-essential checkinstall libssl-dev
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.31.0/install.sh | bash
command -v nvm
nvm install 5.0
nvm use 5.0
nvm alias default node

apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
apt-get update
apt-get install -y mongodb-org

npm install forever -g
python -m easy_install pymongo
pip install flask-login
pip install Flask-PyMongo
apt-get install -y libpq-dev python-dev libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev libffi-dev python-lxml
pip install flask-bcrypt
pip install pytz
pip install plantweb
