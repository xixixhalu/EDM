#!/bin/bash

# This script deletes corresponding containers (web and mongo) and also delete images
# Command example:
# sh container_delete.sh Liuyin Generalization 5c91ee80f9bf8d626ded8241


lower_user_name=$(echo $1 | tr '[A-Z]' '[a-z]')
lower_project_name=$(echo $2 | tr '[A-Z]' '[a-z]')
instance_id=$3

# first stop
UNAME=${lower_user_name} PNAME=${lower_project_name} IID=${instance_id} docker-compose -p ${instance_id} stop

# force rm
UNAME=${lower_user_name} PNAME=${lower_project_name} IID=${instance_id} docker-compose -p ${instance_id} rm -f

# delete images
docker image rm web.${lower_user_name}.${lower_project_name}.${instance_id}
docker image rm mongo.${lower_user_name}.${lower_project_name}.${instance_id}


# delete local repo folder
repo_path="/root/workspace/server_tmpl/web/repos/"$1"/"$2"/"${instance_id}
echo "deleting path: "${repo_path}
rm -rf repo_path

# TODO: delete KV as well
host_ip=$(curl ifconfig.me -s)
docker exec -ti consul-client1 consul kv delete instance/${instance_id}/ip

# remove unused network
# see https://stackoverflow.com/questions/43720339/docker-error-could-not-find-an-available-non-overlapping-ipv4-address-pool-am
docker network prune --force

# TODO: delete repo on gogs
