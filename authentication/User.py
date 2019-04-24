from flask import Blueprint, request, current_app
from flask_login import UserMixin
import datetime as dt
import pytz
import uuid


# User class used in flask_login
# When a User instance created, it will check if this
# user is in the usermetadata database. If the user is
# not in the database, __init__ function will create a
# token for this user and save this user into database.
# This class also provide 3 static method used to create
# or refresh token. 
class User(UserMixin):

    def __init__(self, mongodbengine, username):
        self.username = username
        self.dbengine = mongodbengine
        self.key = -1
        self.validtill = dt.datetime.now(pytz.utc) - dt.timedelta(days=30)
        authentcol = self.dbengine.db.authentication
        findresult = authentcol.find_one({"username": self.username})
        if findresult is not None:
            if findresult["validtill"] is not None:
                tempvalidtill = findresult["validtill"]
                # check if current time is more than valid-till time 
                delta = pytz.timezone("UTC").localize(tempvalidtill)-dt.datetime.now(pytz.utc)
                #delta = tempvalidtill - dt.datetime.now(pytz.utc)
                if delta < dt.timedelta():
                    self.refreshToken(self.username, self.dbengine)
                newfind = authentcol.find_one({"username": self.username})
                self.validtill = newfind["validtill"]
                self.key = newfind["key"]
        else:
            self.key = User.create_random_key()
            self.validtill = User.create_expiry_object()
            authentcol.insert({
                "username": self.username,
                "key": self.key,
                "validtill": self.validtill
            })

        findresult = mongodbengine.db.history.find_one({
            "username":
            self.username
        })
        if findresult is None:
            mongodbengine.db.history.insert({
                "username": self.username,
                "uploads": []
            })

    @staticmethod
    def create_random_key():
        return str(uuid.uuid4())

    @staticmethod
    def create_expiry_object():
        return dt.datetime.now(pytz.utc) + dt.timedelta(days=30)

    @staticmethod
    def refreshToken(username, dbengine):
        authentcol = dbengine.db.authentication
        userprofile = authentcol.find_one({"username": username})
        if userprofile is not None:
            newkey = User.create_random_key()
            newvalidtill = User.create_expiry_object()
            updateresult = authentcol.update(
                {
                    "username": username
                }, {"$set": {
                    "key": newkey,
                    "validtill": newvalidtill
                }},
                upsert=False)
            if updateresult['updatedExisting'] is True:
                return True

        return False

    # this method will be called whenever using login_required decorator
    # currently, it only check if user's token is expired.
    # additional authentication for user can be add here.
    def is_authenticated(self):
        delta = dt.datetime.now(pytz.utc) - pytz.timezone("UTC").localize(self.validtill)
        #delta = dt.datetime.now(pytz.utc) - self.validtill
        if delta >= dt.timedelta():
            User.refreshToken(self.username, self.dbengine)
            authentcol = self.dbengine.db.authentication
            newfind = authentcol.find_one({"username": self.username})
            self.validtill = newfind["validtill"]
            self.key = newfind["key"]
        return True

    # get User class instance by given username
    def get_id(self):
        tempusername = self.username
        return tempusername.decode('utf-8')

    def is_active(self):
        return True

    def is_anonymous(self):
        return False