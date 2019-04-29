from flask import Flask
from flask import request
import os
import subprocess

app = Flask(__name__)

originalWD = os.getcwd()  # record our original working directory


@app.route('/build_image/', methods=['GET'])
def build_image():
    """
    Build web (node, for Server) and mongo images,
    Need user_name, project_name for pull code from repos
    Tag images as web.user_name.project_name.instance_id and mongo.user_name.project_name.instance_id
    http://192.155.85.20:8833/create_container/?user_name=Liuyin&project_name=Generalization&instance_id=5c79c969f9bf8d1c66e1f8f8
    :return:
    """
    user_name, project_name, instance_id, msg = get_base_params()
    if msg is not None:
        return msg
    print('build_image')
    p = subprocess.Popen(["sh ./build_image.sh %s %s %s" %(user_name, project_name, instance_id)],
                         cwd="/root/workspace/server_tmpl", shell=True)
    # p.wait()
    return 'building images on worker: ' + user_name + '.' + project_name + '.' + instance_id


@app.route('/start_container/', methods=['GET'])
def start_container():
    """
    start containers
    need instance_id to specify which images to use
    :return:
    """
    user_name, project_name, instance_id, msg = get_base_params()
    if msg is not None:
        return msg
    print('start_container')
    p = subprocess.Popen(["sh ./container_start.sh %s %s %s" %(user_name, project_name, instance_id)],
                         cwd="/root/workspace/server_tmpl", shell=True)
    # p.wait()
    return 'creating containers: ' + user_name + '.' + project_name + '.' + instance_id


@app.route('/stop_container/', methods=['GET'])
def stop_container():
    user_name, project_name, instance_id, msg = get_base_params()
    if msg is not None:
        return msg
    print('stop_container')
    p = subprocess.Popen(["sh ./container_stop.sh %s %s %s" %(user_name, project_name, instance_id)],
                         cwd="/root/workspace/server_tmpl", shell=True)
    # p.wait()
    return 'stopping containers: ' + instance_id


@app.route('/delete_container/', methods=['GET'])
def delete_container():
    """
    delete containers and images
    :return:
    """
    user_name, project_name, instance_id, msg = get_base_params()
    if msg is not None:
        return msg
    print('delete_container')
    p = subprocess.Popen(["sh ./container_delete.sh %s %s %s" %(user_name, project_name, instance_id)],
                         cwd="/root/workspace/server_tmpl", shell=True)
    # p.wait()
    return 'deleting containers and images: ' + instance_id


@app.route('/refresh_container/', methods=['GET'])
def refresh_container():
    """
    refresh container
    Refreshing here refers to the Server code has changed
    step1: pull code (what's the original logic? should I update the code or just create a new repo?)
    step2: build new images
    step3: run containers
    :return:
    """
    pass


@app.route('/test/', methods=['GET'])
def test():
    """
    http://192.155.85.20:8833/test/?user_name=Liuyin&project_name=Generalization&instance_id=5c79c969f9bf8d1c66e1f8f8
    :return:
    """
    user_name, project_name, instance_id, msg = get_base_params()
    if msg is not None:
        return msg
    return 'received: ' + user_name + '.' + project_name + '.' + instance_id


def get_base_params():
    user_name = request.args.get("user_name")
    if user_name is None:
        return None, None, None, 'Please provide user_name'

    project_name = request.args.get("project_name")
    if project_name is None:
        return None, None, None, 'Please provide project_name'

    instance_id = request.args.get("instance_id")
    if instance_id is None:
        return None, None, None, 'Please provide instance_id'

    return user_name, project_name, instance_id, None


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8833)


