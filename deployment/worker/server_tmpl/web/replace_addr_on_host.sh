#!/bin/bash

# replace_addr_on_host.sh, run on host
# sh replace_addr_on_host.sh 5c91ee80f9bf8d626ded8241_web_1

docker_name=$1

old_ip="0.0.0.0"
old_port="2000"

new_ip=$(curl ifconfig.me -s)
new_port=$(docker inspect ${docker_name} | jq -r ".[0].NetworkSettings.Ports | .[\"2000/tcp\"] | .[0].HostPort")

echo ${old_ip}":"${old_port}" -> "${new_ip}":"${new_port}

docker exec -ti ${docker_name} sh replace_addr_in_container.sh ${old_ip} ${old_port} ${new_ip} ${new_port}
