#!/bin/bash

# This script stops corresponding containers (web and mongo)
# Command example:
# sh container_stop.sh Liuyin Generalization 5c79c969f9bf8d1c66e1f8f8
# sh container_stop.sh test Generalization 5c7f87eaf9bf8d5780e0050c


lower_user_name=$(echo $1 | tr '[A-Z]' '[a-z]')
lower_project_name=$(echo $2 | tr '[A-Z]' '[a-z]')
instance_id=$3

sh /root/workspace/server_tmpl/web/replace_back_addr_on_host.sh ${instance_id}"_web_1"
sleep 2

UNAME=${lower_user_name} PNAME=${lower_project_name} IID=${instance_id} docker-compose -p ${instance_id} stop

# when stopping the container, port assigned to this container will be removed
# so in order to replace ip:port next time we start the container, current ip:port should be changed back to
# the original placeholder
