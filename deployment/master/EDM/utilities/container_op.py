#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import urllib2
import os
from utilities.lookup import lookup_worker_ip, lookup_service

# URL of Nginx server
params_tmpl = "?user_name=%s&project_name=%s&instance_id=%s"


def upload_code(user_name, project_name, instance_id):
    """
    Upload code AND build image
    Create repo user -> create repo -> push code -> build image
    Pass request to LB to choose a worker (in build_image process)
    """
    command = 'sh /root/workspace/EDM/utilities/auto_repo.sh ' + user_name + ' ' + project_name + ' ' + instance_id
    print('upload_code: ' + command)
    os.system(command)


def start_container(user_name, project_name, instance_id):
    """
    Start containers
    Lookup worker ip through tiny hook
    """
    worker_addr = lookup_worker_ip(instance_id)
    print('Test start_container: ' + user_name + " " + project_name + " " + instance_id)
    make_request(worker_addr, "start_container", user_name, project_name, instance_id)


def stop_container(user_name, project_name, instance_id):
    """
    Stop containers
    Look up service address, ip+port
    http://192.155.85.20:8833/start_container/?user_name=Liuyin&project_name=Composition&instance_id=5c9c1580f9bf8d645b2a9584
    """
    worker_addr = lookup_worker_ip(instance_id)
    make_request(worker_addr, "stop_container", user_name, project_name, instance_id)


def delete_container(user_name, project_name, instance_id):
    worker_addr = lookup_worker_ip(instance_id)
    make_request(worker_addr, "delete_container", user_name, project_name, instance_id)


def refresh_container(user_name, project_name, instance_id):
    # TODO: regenerate code and upload to gogs
    # when is the code regen?
    worker_addr = lookup_worker_ip(instance_id)
    make_request(worker_addr, "refresh_container", user_name, project_name, instance_id)


def make_request(addr, method_name, user_name, project_name, instance_id):
    params_str = params_tmpl % (user_name, project_name, instance_id)
    if addr is None:
        # TODO: log
        print("no container address")
        # addr = "http://192.155.85.20:8833"
        return
    # urllib2 need to specify http explicitly
    request_url = "http://" + addr + "/" + method_name + "/" + params_str
    print("make_request: " + request_url)
    response = urllib2.urlopen(request_url)
    # TODO: check response content, such as status_code and err_msg


if __name__ == '__main__':
    print('test')


