#!/bin/bash

# replace_addr_in_container.sh, run inside the container
old_addr=$1":"$2

new_addr=$3":"$4

# replace and save ip:port in api.json
sed -i "s/$old_addr/$new_addr/g" api.json

# server_ip in Server.js keeps 0.0.0.0, and port keeps 2000 (for outside to visit)
