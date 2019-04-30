#!/bin/bash

# command exmmple: sh auto_repo.sh Liuyin Generalization 5c79c969f9bf8d1c66e1f8f8

# create user
docker exec -t mygogs ./gogs admin create-user --name=$1 --password=nopassword --email=$1@user.com --admin=false

# search user token, if not exist, create one
token=$(curl -u $1:nopassword http://173.230.147.105:10080/api/v1/users/$1/tokens | jq -r '.[0].sha1')

if [ -z "$token" ] || [ ${token} = "null" ]; then
    echo "Empty token, generating..."
    token=$(curl -X POST -H "content-type: application/json" -d '{"name":"my_api_token"}' http://$1:nopassword@173.230.147.105:10080/api/v1/users/$1/tokens -s | jq -r '.sha1')
    echo "New token:"${token}
else
    echo "token is not empty, existing token = $token"
fi

# create repo
echo "creating repo..."
curl -H "Content-Type: application/json" -d '{"name": "'"$3"'", "description": "init repo", "private": true}' -X POST http://173.230.147.105:10080/api/v1/user/repos?token=${token}

# upload all instances in user/project/instance folder
cd /root/workspace/EDM/generated_code/$1/$2/$3
git init
git config user.name $1
git config user.email ${1}"@user.com"
git add --all
git commit -m "auto commit"
#git remote add origin http://$1:nopassword@173.230.147.105:10080/$1/$2_$3.git
# git push -u origin master
git push http://$1:nopassword@173.230.147.105:10080/$1/$3.git --all

# build images (do not run containers at this time)
curl http://192.155.85.20:8833/build_image/\?user_name=$1\&project_name=$2\&instance_id=$3

# TODO: remove
#docker restart mygogs
