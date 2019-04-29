#!/bin/bash

# This script pulls user code and build docker images. Containers will not be created here
# Command example:
# sh build_image.sh Liuyin Generalization 5c91ee80f9bf8d626ded8241

user_name=$1
project_name=$2
instance_id=$3

repos_path="/root/workspace/server_tmpl/web/repos/"${user_name}"/"${project_name}

# pull user code
if [ ! -e ${repos_path} ]; then
    mkdir -p ${repos_path}
fi
cd ${repos_path}

# clone code
# TODO: if already exist, update repo?
git clone http://$1:nopassword@173.230.147.105:10080/${user_name}/${instance_id}.git

# jump back
cd /root/workspace/server_tmpl

# replace mongo template
sed "s/PROJECT_NAME/$project_name/g" < mongo/init_mongo_tmpl > mongo/init_mongo.js


# docker build -t tag needs LOWERCASE letters, docker images are temporary here
lower_user_name=$(echo $1 | tr '[A-Z]' '[a-z]')
lower_project_name=$(echo $2 | tr '[A-Z]' '[a-z]')

# build mongo image
docker build -t mongo.${lower_user_name}.${lower_project_name}.${instance_id} ./mongo

# Be aware of build context, path should be within the context, i.e. under web/ folder
server_path="repos/"${user_name}"/"${project_name}"/"${instance_id}"/Server/"

# copy node_modules to Server
unzip -o web/node_modules.zip -d "web/"${server_path}

# build node image
docker build --build-arg SERVER_PATH=${server_path} -t web.${lower_user_name}.${lower_project_name}.${instance_id} ./web

# put the ip of the worker that will hold docker containers of current service
host_ip=$(curl ifconfig.me -s)
# could use http api as well
docker exec -ti consul-client1 consul kv put instance/${instance_id}/ip ${host_ip}
