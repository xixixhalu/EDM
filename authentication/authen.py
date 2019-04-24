from flask import Blueprint, request, jsonify, current_app
from flask_login import UserMixin, current_user, login_required
import datetime as dt
import pytz
import uuid

from authentication.User import User
from database_manager.setup import mgInstance


authen_bp = Blueprint("authen_bp", __name__)

# return token for current user
# because when User instance initial, it will check
# if token is valid and refresh token if it is expired,
# so this method will always return valid token.
@authen_bp.route('/requesttoken')
@login_required
def requesttoken():
    # userprofile=load_user(mongo, current_user.get_id())
    userprofile = current_user
    response = {}
    response['key'] = userprofile.key
    return jsonify(response)


# this api is used by generated server to check if 
# token and username is valid
@authen_bp.route('/verifykey', methods=['POST'])
def verifykeyapi():
    response = {}
    username = request.form['username']
    usertoken = request.form['key']
    if verifykey(username, usertoken, mgInstance.mongo) is True:
        response["valid"] = True
    else:
        response["valid"] = False

    return jsonify(response)

def verifykey(username, usertoken, dbengine):
    authentcol = dbengine.db.authentication
    findresult = authentcol.find_one({"username": username})
    if findresult == None:
        return False

    # check if current token of this user is expired
    validtill = findresult["validtill"]
    delta = dt.datetime.now(pytz.utc) - pytz.timezone("UTC").localize(validtill)
    #delta = dt.datetime.now(pytz.utc) - validtill
    if delta >= dt.timedelta():
        User.refreshToken(username, dbengine)
        findresult = authentcol.find_one({"username": username})
    if findresult["key"] == usertoken:
        return True

    return False