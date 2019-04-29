# User Guide

<br/>

## Author: Liuyin Huang

<br/>



## Architecture

![architecture](https://github.com/louiehuang/EDM_Deployment/raw/master/architecture.png)

To create and run a new instance, we have 2 steps according to the requirement:

- First, Generate Server code , upload to gogs (from main system) and build images (on worker)
- Second, Run containers only when user clicks `run`



For step1, details steps are: 

- A **[Main system]** Main system accepts user request (upload xml file).
- B **[Main system]** Main system call `upload_code` method: 
  - B.1 **[Main system]** Main system (creates user and repo first if they do not exist) pushes the generated Server code to gogs. When finishing pushing, call `build_image` API on LB, this request will be sent to one of the worker by LB. 
  - B.2 **[Worker]** The `build_image` request goes to a worker node selected by LB, this worker node will pull the corresponding server code from gogs and run scripts to build docker images and finally put the worker ip to Consul K/V for later looking up (key is `instance/${instance_id}/ip`).



For step2, details steps are: 

- C **[Main system]** Main system call `start_container` method to run containers.

- D **[Main system]** This time, the `start_container` request should go to its corresponding worker node (the one selected by LB in step `B.1`). The reason we record worker ip in step `B.2` is for the use here, so that we know where this request should go to.
- E **[Worker]** The `start_container` request goes to the correct worker node. This worker node will run the containers by docker-compose and replace `ip:port` in the Server when finishing running. (for outside world to visit)
- F **[Worker]** There is a registrator container and a consul client container running on each worker node. Each time we run a new docker container, registrator will know this event and register the information of that new container to consul client, and consul client will forward the info to consul server.





## Configuration

I've rebuild my servers, make them clean Ubuntu 14.04 LTS, and ran following steps to test whether there is any bug in my scripts. => Works fine. There should not be any big problem if you also start with a clean Ubuntu 14.04 LTS server. 



### Prepare Servers

In this text, I'll use two Ubuntu servers (14.04 LTS, same as the requirement in this DR) as example, one is used as master and the other is used as worker. Each server has its own public ip and private ip. 



#### Servers IPs

- master,  public ip: 173.230.147.105, private ip: 192.168.216.44
- worker1, public ip: 192.155.85.20, private ip: 192.168.192.66



If you use macOS, for your convenience, you can add those ip to  `/etc/hosts` with alias, so that you can ssh those servers using their alias instead of ip, i.e. `ssh root@master`

```shell
# /etc/hosts
173.230.147.105  master
192.155.85.20    worker1
```



Use scp or ansible to put all needed files on corresponding servers.



### Init Server

I wrote a script to initilize the servers (both master and workers), just run `echo *your_password* | sudo -S sh init_server.sh` , where `*your_password*` is your password for sudo user, its a variable, not an actual password... 

init master

```shell
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
```

init worker

```shell
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
```

If you have a lot workers to config, ansible could help you a lot. (I  do not think we'll have that lot workers in short term, so for now I just config them manually)



### Config Master

Since I only have very limited servers (2), I'll run EDM, Consul Server (only 1 server) and Nginx Load Balancer and Gogs all on the master node. 

(If you have more servers to use, you should sepeprate those components and may want to run more than 1 Consul server. It's pretty easy to do that, just run the commands I'll talk on different servers.)



All following command can also be combined in a single script, you just need to confirm the IPs. And please run these command after you create the folder needed if there is `-v` option in docker command.



#### Consul Server

Run consul server

```shell
docker run -d --net=host --name=consul-server1 --restart=always \
             -e 'CONSUL_LOCAL_CONFIG={"skip_leave_on_interrupt": true}' \
             consul agent -server -bootstrap -bind=192.168.216.44 -node=consul-server1 \
             -data-dir=/tmp/consul-data-dir -client 0.0.0.0 -ui
```

`192.168.216.44` is the master ip. And we name this server as `consul-server1` (or whatever you prefer)

You can visit `http://173.230.147.105:8500`, the simple UI provided by Consul



#### Nginx (LB)

This nginx service is used as a simple load balancer (on http level). The main system will call APIs on workers to build images and start/stop/delete containers, these requests should be distributed to different worker nodes in some LB manner to make sure the workload of each worker is similar.

All config files needed are included in `master/nginx` folder, the first thing you need, of course, is the `nginx.conf`, I added our server ips in it. 

```
    upstream container_backend {
        server 192.168.192.66:8833;
        # server 192.168.192.67:8833;
    }

    server {
        listen 80;
        server_name 173.230.147.105;

        location /{
            proxy_pass http://container_backend;
            proxy_set_header Host       $host;
            proxy_set_header X-Real-IP      $remote_addr;
            proxy_set_header X-Forwarded-For    $proxy_add_x_forwarded_for;
        }
    }
```

This conf is pretty straightforward, what it does is just forward requests it receives to one of the worker (currently just 1) in round robin manner (you can specify other lb algorithm).

`173.230.147.105` is our master ip, this server receives requests, and forward to `192.168.192.66:8833`, our worker. If we have more workers, just add their ips in `upstream container_backend`. 

`Dockerfile` just add this conf to `/etc/nginx`

Build image, run `docker build -t nginx_lb .` Notice the `.`, this is the context location (current folder in this case)

Run `docker-compose -f docker-compose.yml up -d`

If you have more workers to config, Consul-Template is a good tool to choose.

For now, I'm using Nginx's round robin and Consul K/V for loading balancing and routing. Consistent hash is another way to do this work. And if in the future, our project gets bigger and has much more instances, round robin may not be a reasonable way, it would be better dispatch "create containers" request based on the weight of each server (e.g. the number of running container on that server, or cpu usage, etc.) 





#### Private Repo (Gogs)

Server code generated in EDM main system will be uploaded to gogs repo (create user if not exist and create repo if not exist). 

Currently, I use gogs as the private repo. But it seems that gogs has a problem and I cannot find its cause - **Gogs may throw 500 internal error when you try to make request to it after running for a while (typically more than 1 day). But if you restart gogs, `docker restart mygogs`, the problem disappears.** 

Logs in gogs are not really helpful to debug this... Gogs doc says it needs `2CPU, 512MB RAM`, not sure whether this is the problem since my server only has 1 CPU. The easiest way to work around this issue is using crontab to restart gogs once a day. But this is not a good solution… 

In fact, my first choice was **Gitlab**, I discard that plan because I found out to run Gitlab smoothly, you need 3GB RAM (my servers only have 1GB RAM…)

If you plan not using gogs, you can choose bitbucket or simply build an apache/nginx file server. But if you want to try gogs, following is the configuration steps:

Run

```
docker run -d --name=mygogs -e USER='git' -p 10022:22 -p 10080:3000 -v /root/workspace/data/gogs:/data gogs/gogs
```

You need to create `/root/workspace/data/gogs` folder first, this folder is used for data persistence. (-v option)

`10080` is the port exposed to outside world, i.e. you can visit gogs at `http://173.230.147.105:10080`

The first time you visit this page, you may need to do some simple configuration:

- Database Type: SQLite3
- Path: data/gogs.db
- Repository Root Path: /data/git/gogs-repositories
- SSH Port: 10022
- HTTP Port: 3000
- Domain: 173.230.147.105
- Application URL: http://173.230.147.105:10080/

You can also create an admin user through that bootstrap page if you prefer.



### Config Worker

At worker node, you need to configure consul client and registrator. Whenever you create new container, registrator will know this event and register the related info to consul client (in our consul cluster mode), and consul clinet will sync its info to consul server.

#### Consul Client

```shell
docker run -d --net=host --name=consul-client1  --restart=always \
            -e 'CONSUL_LOCAL_CONFIG={"leave_on_terminate": true}' \
            consul agent -bind=192.168.192.66 -retry-join=192.168.216.44   \
            -node-id=$(uuidgen | awk '{print tolower($0)}') \
            -node=consul-client1 -client 0.0.0.0 -ui
```

For consul client, `192.168.192.66` is the worker ip and `192.168.216.44` is the master ip, meaning this worker will join `192.168.216.44` in a retry manner. 



#### Registrator

```shell
docker run -d --name=registrator \
             -v /var/run/docker.sock:/tmp/docker.sock \
             --net=host \
             gliderlabs/registrator -ip="192.168.192.66" consul://192.168.192.66:8500
```



#### Flask API

Create path `/root/workspace/flask`, this flask server provides several APIs to operate docker containers, just see the code. 





## Implementation

In this section, I'll talk about some of my implementations in case you do not know why I do that.

I'll mainly discuss `upload_code` and `start_container` here, the rest methods are similar to `start_container` .



### upload_code

#### Master

After user uploads his xml file, the request goes to route `/result`, Server code will be generated here, and we call `container_op.upload_code(session['username'], filename_str, file_id)` right before return the result page. This method simply runs `auto_repo.sh` script with 3 parameter - user name, project name and instance id (file id). 

What `auto_repo.sh` does are:

- Create user on gogs. (All users' password is set to `nopassword` string) It's OK if user already exists, though you can add some code to check.
- Search user token, if this user does not have a token, create one. The user token is used for operating this user's gogs repos
- Create Repo, name it as the instance id (file id). It's also OK if the repo already exists, though you can add some code to check. 
- Upload server code to the repo we just created. Here is just some git command. 
- Call `build_image` APIs on **Nginx LB**. LB will dispatch this request to a worker node it selects. 



#### Worker

The worker selected by LB will receive the `build_image` request by `build_image()` method in `app.py`. This method simply runs `build_image.sh`. Here I use **`subprocess.Popen()`** method to run the script, whether we wait or not depends on the requirements, currently I just run the script asynchronously.

What `build_image.sh` does are:

- Clone server code from gogs
- Generate init_mongo.js from init_mongo_tmpl to config mongo container
- Build mongo image
- Copy node_modules to repo folder and build Node image (TODO: copy node_modules to a pre-defined image so we do not have to copy there modules each time we build the node image, small improvement)
- Put worker ip to Consul KV, key is `instance/${instance_id}/ip`. So we can find this worker on other nodes when we call other APIs.



### start_container

Once we have built the images, the user can run his containers. User clicks the `run` button, and this will be routed to `run_instance()` in `views.py`. 

The line `container_op.start_container(user_name, domain_model_name, file_id)` is what I add to make request to worker. Let's take a closer look at what `start_container` does. 

First, it finds the worker ip according the instance id (file id), and this is done by query consul K/V. `lookup_worker_ip()` returns ip and port, where the port is hard-coded as `8833`. (flask API port)

Second, we make `start_container` request to the corresponding worker node. 

Third, again, this worker node runs `container_start.sh` by `subprocess.Popen`. This script will compose the containers (docker-compose). 

Once the containers are fully started, replace `ip:port` from `0.0.0.0:2000` to `worker_ip:container_port` in the Server folder (in web container). Notice that the container's port may change before it ups completely, so we may need to wait a few second (currently set to 7 seconds), so total start time is around 8 seconds which is still faster than the original system (run instance locally). Change this replace logic to other place, e.g. when user clicks `detail` button could let user not feel he's waiting a long time. Just remember to check whether the container is at a stable status. No sure whether is there better idea to eliminate this problem totally. 



### stop_container

Similar logic,  change `worker_ip:container_port` back to `0.0.0.0:2000` and stop containers.



### delete_container

- Stop containers
- Remove images
- Delete local repo folder
- Delete Consul K/V
- **Prune unused network** (This is important since docker has a limitation for network created, 31)





## TODO



- Copy node_modules to a pre-defined image so we do not have to copy there modules each time we build the node image, small improvement)
- Write a nicer script to initialize master and worker
- Refactor the docker scripts, config ips automatically
- Regenerate Code Logic
- Before user clicks any button, check whether he is allowed to do so, e.g. Do not let user click "details" button before the containers fully started. (When it's done, notify the main system)
- Do not build images? Save some space but not necessary.


