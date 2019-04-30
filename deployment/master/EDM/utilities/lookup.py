#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import json
import urllib2
import base64

# need to add http
base_url = "http://173.230.147.105:8500"  # consul server, currently only one server due to cost
# base_url = "http://master:8500"  # consul server, currently only one server due to cost
private2public = {"192.168.216.44": "173.230.147.105", "192.168.192.66": "192.155.85.20"}


def lookup_worker_ip(instance_id):
    """
    Can call this method before the docker containers have been created
    look up worker ip based on instance id using consul kv
    url e.g. "http://173.230.147.105:8500/v1/kv/instance/5c91ee80f9bf8d626ded8/ip"
    :param instance_id:
    :return:
    """
    # docker exec -ti consul-server1 consul kv get instance/${instance_id}/ip
    # curl http://173.230.147.105:8500/v1/kv/instance/5c91ee80f9bf8d626ded8/ip
    # decode base64 Value
    url = base_url + "/v1/kv/instance/" + instance_id + "/ip"
    print(url)
    try:
        response = urllib2.urlopen(url)
        kv = json.loads(response.read())[0]
        public_ip = base64.b64decode(kv["Value"])
        return public_ip + ":8833"
    except:  # TODO: specify accurate exception type
        # TODO: Log this error, 404 is the most common reason here
        return None


def lookup_service(instance_id):
    """
    Can ONLY call this method AFTER the docker containers have been created
    look up service ip:port based on instance id
    url e.g. "http://master:8500/v1/catalog/service/web.5c91ee80f9bf8d626ded8241"
    :param instance_id:
    :return:
    """
    url = base_url + "/v1/catalog/service/web." + instance_id
    print(url)
    try:
        response = urllib2.urlopen(url)
        # if not exist, reponse = []
        parse_resp = json.loads(response.read())
        if len(parse_resp) == 0:
            # TODO: Log this warning
            print('In lookup_service: length of the response is 0, instance_id=' + instance_id)
            return
        service = parse_resp[0]
        private_ip = service["ServiceAddress"]
        public_ip = private2public[private_ip]
        port = service["ServicePort"]
        return public_ip + ":" + str(port)
    except:
        # TODO: Log this error, 404 is the most common reason here
        return None


if __name__ == '__main__':
    # print(lookup_worker("5c91ee80f9bf8d626ded8241"))
    # print(lookup_worker("123"))
    print(lookup_service("5c91ee80f9bf8d626ded8241"))


