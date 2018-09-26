import os

from code_generator import generate_code
from utilities.config_util import ConfigUtil
from utilities.file_op import fileOps
from database_manager.dbOps import dbOps

from flask import flash, Response, jsonify, current_app, Blueprint
from flask import render_template, Flask, request, redirect, url_for, send_from_directory, session
from flask_login import login_user, logout_user, login_required, LoginManager, current_user, UserMixin
import bcrypt
from werkzeug.utils import secure_filename
import base64
from bson import binary
from bson.json_util import dumps
from bson.objectid import ObjectId
import subprocess as sp
import time

from database_manager.setup import mgInstance
from uml_parser.parse_dm_file import Analyzer as p
from authentication.User import User
from config import config


cwd = os.getcwd()
main_bp = Blueprint('main_bp', __name__, static_folder= cwd + '/static', template_folder=cwd +'/templates')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@main_bp.route('/')
def index():
    if 'username' in session:
        history = mgInstance.mongo.db.history
        history_data = history.find_one({'username': session['username']})

        if history_data is None:
            history_data = []
        else:
            history_data = dumps(history_data['uploads'])
        
        # Pass required data to the template
        description_data = {
            "history_data": history_data
        }
        return render_template('user_profile.html', **description_data)
    return render_template('homepage.html')



@main_bp.route('/login', methods=['POST'])
def login():
    users = mgInstance.mongo.db.users
    findresult = users.find_one({'username': request.form['uname']})

    if findresult:
        if bcrypt.hashpw(request.form['psw'].encode('utf-8'),
                         findresult['password'].encode('utf-8')) == findresult[
                             'password'].encode('utf-8'):
            session['username'] = request.form['uname']
            newuser = User(mgInstance.mongo, request.form['uname'])
            #login user in flask_login
            login_user(newuser)
            return redirect(url_for('main_bp.index'))
    return 'Invalid username/password combination'


@main_bp.route('/register', methods=['POST'])
def register():
    users = mgInstance.mongo.db.users
    username = request.form['uname']
    existing_user = users.find_one({'username': request.form['uname']})

    if existing_user is None:
        hashpass = bcrypt.hashpw(request.form['psw'].encode('utf-8'),
                                 bcrypt.gensalt())
        users.insert({
            'username': request.form['uname'],
            'password': hashpass,
            'email': request.form['email']
        })
        session['username'] = request.form['uname']
        newuser = User(mgInstance.mongo, request.form['uname'])
        #login user in flask_login
        login_user(newuser)

        key = User.create_random_key()
        validtill = User.create_expiry_object()
        userprofile = {
            "username": username,
            "key": key,
            "validtill": validtill
        }
        mgInstance.mongo.db.authentication.insert(userprofile)
        mgInstance.mongo.db.history.insert({"username": username, "uploads": []})

        return redirect(url_for('main_bp.index'))

    return 'That username already exists!'


@main_bp.route('/upload')
@login_required
def upload_xml():
    return render_template('xml_upload.html')

@main_bp.route('/update' , methods=['GET'])
@login_required
def update_xml():

    file_id = request.args['fileId']
    domain_model_name = request.args['domainModelName']

    # Pass required data to the template
    description_data = {
        "domainModelName": domain_model_name,
        "fileId": file_id
    }

    return render_template('xml_update.html',**description_data)


'''
# add file to database without generate server code
@app.route('/uploadtodb', methods=['POST'])
@login_required
def uploadtodb():
    username = request.form['username']
    dmname = request.form['dmname']

    response = {}

    if username == None or dmname == None or len(username) == 0 or len(
            dmname) == 0:
        response["status"] = "fail"
        response["response"] = "Insufficient parameters"
        return jsonify(response)

    if 'modelfile' not in request.files:
        response["status"] = "fail"
        response["response"] = "model file not exist"
        return jsonify(response)
    f = request.files['modelfile']
    if f.filename == '':
        response["status"] = "fail"
        response["response"] = "file not selected"
        return jsonify(response)

    allcontent = f.read()
    if saveFileToDB(username,dmname,allcontent) is True:
        response["status"] = "success"
        response["response"] = "successfully upload model file"
    else:
        response["status"] = "fail"
        response["response"] = "error in saving to database"
    return jsonify(response)
'''

# generate server code and save file into database
@main_bp.route('/result', methods=['GET', 'POST'])
@login_required
def result():

    ana = p()
    if request.method == 'POST':
        filename_str = ""
        output_dir = os.path.join(config.get('Output', 'output_path')) + "/" + session['username']
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename_str = filename.split(".")[0]

            all_content = file.read()
            
            # save file into database
            file_id = dbOps.saveFileToDB(mgInstance.mongo, current_user.username, filename_str, all_content)

            # save file to path
            output_dir = output_dir + "/" + filename_str + "/" + str(file_id)
            with fileOps.safe_open_w(output_dir + "/" + filename) as f:
                f.write(all_content)
                       
            # Parse XML and generate JSON
            ana.DM_File_Analyze(output_dir, {'DM_Input_type': "Simple_XML"}, filename_str)
            
            # Parse JSON and generate code
            model_display_data, server_url = generate_code.generate_all(filename_str, output_dir)

            authen_key = dbOps.getAuthenKey(mgInstance.mongo, session['username'])
         

            # Pass required data to the template
            description_data = {
                "model_display_data": model_display_data,
                "server_url": server_url,
                "authen_key" : authen_key
            }

            # write description_data into json file
            generate_code.write_description_to_file(filename_str, output_dir, description_data)

            # Render the template
            return redirect(url_for('main_bp.index'))
            
        else:
            flash('File type is not allowed')
            return redirect(request.url)
    return redirect(request.url)

#Run the specified instance
@main_bp.route('/runinstance', methods=['POST', 'GET'])
@login_required
def run_instance():
    if request.method == 'POST':
        base_path = os.path.join(config.get('Output', 'output_path'))
        user_path = "/" + session['username']
        instance_path = "/" + request.form['domainModelName'] + "/" + request.form['fileId']
        server_path = "/" + "Server" + "/" + "Server.js"

        final_path = base_path + user_path + instance_path + server_path

        child_process = sp.Popen(["node", final_path])
        # Temporary solution..
        time.sleep(0.5)

        if child_process.poll() == None:
            flash('Successful to run the specified instance')
        else:
            flash('Failed to run the specified instance')
        return redirect(url_for('main_bp.index'))
    return redirect(url_for('main_bp.index'))

#Update instance with a new UML
@main_bp.route('/updateinstance', methods=['GET','POST'])
@login_required
def update_instance():

    ana = p()
    if request.method == 'POST':

        oldfile_id = request.form['fileId']
        domain_model_name = request.form['domainModelName']


        file = request.files['file']
      
        filename_str = ""
        output_dir = os.path.join(config.get('Output', 'output_path')) + "/" + session['username']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename_str = filename.split(".")[0]

            all_content = file.read()
            b64content = base64.standard_b64encode(all_content)
          # get bson object
            bincontent = binary.Binary(b64content)
            #print all_content

            # save file into database
            #newfile_id = dbOps.saveFileToDB(mongo, current_user.username, filename_str, all_content)
            #print newfile_id

            # save file to path
            output_dir = output_dir + "/" + filename_str + "/" + str(oldfile_id)
            with fileOps.safe_open_w(output_dir + "/" + filename) as f:
                f.write(all_content)
                f.close()

            username = session['username']

            dbOps.updateInstanceDb(mgInstance.mongo, username, domain_model_name, oldfile_id, bincontent)

            file_dir = os.path.join(config.get('Output', 'output_path')) + "/" + username + "/" + domain_model_name + "/" + str(oldfile_id)

            # Parse XML and generate JSON
            ana.DM_File_Analyze(output_dir, {'DM_Input_type': "Simple_XML"}, filename_str)
            
            # Parse JSON and generate code
            model_display_data, server_url = generate_code.generate_all(filename_str, output_dir)

            authen_key = dbOps.getAuthenKey(mgInstance.mongo, session['username'])
         

            # Pass required data to the template
            description_data = {
                "model_display_data": model_display_data,
                "server_url": server_url,
                "authen_key" : authen_key
            }

            # write description_data into json file
            generate_code.write_description_to_file(filename_str, output_dir, description_data)

        return redirect(url_for('main_bp.index'))
  
    #return redirect(url_for('index'))  
    return redirect(url_for('main_bp.update_instance'))


@main_bp.route('/deleteinstance', methods=['GET', 'POST'])
@login_required
def delete_instance():
    if request.method == 'POST':
        file_id = request.form['fileId']
        domain_model_name = request.form['domainModelName']

        if file_id is None:
            flash('File id is not specified')
            return redirect(request.url)

        if domain_model_name is None:
            flash('Domain model name is not specified')
            return redirect(request.url)

        username = session['username']

        dbOps.deleteInstanceFromDB(mgInstance.mongo, username, domain_model_name, file_id)
        
        file_dir = os.path.join(config.get('Output', 'output_path')) + "/" + username + "/" + domain_model_name + "/" + file_id
        fileOps.safe_delete_dir(file_dir)

        flash('Successfully deleted')
        return redirect(url_for('main_bp.index'))
    return redirect(url_for('main_bp.index'))


@main_bp.route('/detailinstance', methods=['GET'])
@login_required
def detail_instance():

    file_id = request.args['fileId']
    domain_model_name = request.args['domainModelName']

    json_dir = os.path.join(config.get('Output', 'output_path')) + "/" + session['username']
    json_dir = json_dir + "/" + domain_model_name + "/" + str(file_id)

    # Get description_data from json file
    meta_data = generate_code.read_description_from_file(domain_model_name, json_dir)

    model_display_data = meta_data["model_display_data"]

    # Pass required data to the template
    description_data = {
        "model_display_data": model_display_data
    }

    return render_template('reference.html', **description_data)



@main_bp.route('/serverstatus', methods=['GET'])
@login_required
def serverstatus():
   
    file_id = request.args['fileId']
    domain_model_name = request.args['domainModelName']

    json_dir = os.path.join(config.get('Output', 'output_path')) + "/" + session['username']
    json_dir = json_dir + "/" + domain_model_name + "/" + str(file_id)

    # Get description_data from json file
    meta_data = generate_code.read_description_from_file(domain_model_name, json_dir)
   
    server_url = meta_data["server_url"]
    authen_key = meta_data["authen_key"]

    # Pass required data to the template
    description_data = {
        "server_url": server_url,
        "authen_key": authen_key
    }
    return render_template('server_status.html', **description_data)


@main_bp.route('/description')
@login_required
def description():
    return render_template('description.html')

@main_bp.route('/diagram')
@login_required
def get_diagram():
    file_id = request.args['fileId']
    domain_model_name = request.args['domainModelName']
    path = 'generated_code' + '/' + session['username'] + '/' + domain_model_name + '/' + file_id
    return send_from_directory(path, 'diagram.svg')

@main_bp.route('/generated_code/<path:path>')
@login_required
def generated_code(path):
    return send_from_directory('generated_code', path)


@main_bp.route('/logout')
@login_required
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    #logout user in flask_login
    logout_user()
    return redirect(url_for('main_bp.index'))

# return user's upload history,
# every file will be given its fileid and download url
@main_bp.route('/filelist')
@login_required
def filelist():
    response = {}
    findresult = mgInstance.mongo.db.history.find_one({
        "username": current_user.username,
    },{"_id":0,"username":0})

    if findresult is None:
        response["message"] = "no such user"
    else:
        for i, imode in enumerate(findresult["uploads"]):
            for j, jfile in enumerate(imode["files"]):
                fileid = jfile["file"]
                prefix = "/downloadfile?username=" + current_user.username + "&fileid="
                findresult["uploads"][i]["files"][j]["file"]=str(fileid)
                findresult["uploads"][i]["files"][j]["fileurl"] = prefix + str(fileid)

        response = findresult

    return jsonify(response)

# return xml by given fileid
@main_bp.route('/downloadfile',methods=['GET'])
@login_required
def downloadfile():
    response = {}
    username = request.args.get('username')
    fileid = ObjectId(request.args.get('fileid'))
    if current_user.username != username:
        response["message"] = "file not belong to this user"
        return response

    historycol = mgInstance.mongo.db.history
    findresult = historycol.find_one({
        "username": username,
    })
    if findresult is None:
        response["message"] = "no such user"
    else:
        for imode in findresult["uploads"]:
            for jfile in imode["files"]:
                if fileid == jfile["file"]:
                    newfind = mgInstance.mongo.db.filedb.find_one({"_id": fileid})
                    if newfind is not None:
                        xmlfile = base64.standard_b64decode(newfind["file"])
                        return Response(xmlfile, mimetype='text/xml')

        response["message"] = "no such file"

    return jsonify(response)

