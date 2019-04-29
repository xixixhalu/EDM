#!/bin/bash

# This script composes and run containers, assign $instance_id as project name so to use same docker-compose.yml
# Command example:
# sh container_start.sh Liuyin Generalization 5c91ee80f9bf8d626ded8241

lower_user_name=$(echo $1 | tr '[A-Z]' '[a-z]')
lower_project_name=$(echo $2 | tr '[A-Z]' '[a-z]')
instance_id=$3

# UNAME=liuyin PNAME=composition IID=5c9c1f64f9bf8d7675c08dc7 docker-compose -p 5c9c1f64f9bf8d7675c08dc7 up -d
UNAME=${lower_user_name} PNAME=${lower_project_name} IID=${instance_id} docker-compose -p ${instance_id} up -d

# replace ip and port
# TODO: potential problem, container port may change before it ups completely, need to wait a few second
sleep 7
sh /root/workspace/server_tmpl/web/replace_addr_on_host.sh ${instance_id}"_web_1"
