import os
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

import base64
from bson import binary
import datetime as dt
import pytz


class dbOps:

    @staticmethod
    def registerRunningInstance(mongo, username, modelName, fileId):
        mongo.db.running_instance.update(
                    {
                        "username": username
                    },
                    {
                        "$push" : {
                            "instances": {
                                "date":dt.datetime.now(pytz.utc),
                                "domainModelName": modelName,
                                "file":ObjectId(fileId)
                            }
                    
                        }
                    },
                    upsert = True
                )

    @staticmethod
    def stopRunningInstance(mongo, username, modelName, fileId):
        mongo.db.running_instance.update(
                    {
                        "username": username
                    },
                    {
                        "$pull" : {
                            "instances": {
                                "domainModelName": modelName,
                                "file":ObjectId(fileId)
                            }
                    
                        }
                    }
                )
    
    @staticmethod
    def updateInstanceDb(mongo, username, modelName, fileId, filecontent):
        
        #find id and update the file content
        mongo.db.filedb.update(
            { 
                '_id': ObjectId(fileId)  
            },
            {
                '$set':{
                    'file': filecontent
                }
            }
        )

        #change the datetime in history
        getfile = list(mongo.db.history.aggregate([
            {"$unwind" : "$uploads"}, {"$unwind": "$uploads.files"},
            {"$match" : {"uploads.files.file" : ObjectId(fileId)}}
        ]))[0]
        date = getfile["uploads"]["files"]["date"]
        #print date
            
        mongo.db.history.update(
                    {
                        "username": username,
                        "uploads.files.file":ObjectId(fileId)
                    },
                    {
                        "$pull" : {
                            "uploads.$.files": {
                            "file":ObjectId(fileId),}
                    
                        }
                    }
                )
        mongo.db.history.update(
                    {
                        "username": username,
                        "uploads.domainModelName":modelName
                    },
                    {
                        "$push" : {
                            "uploads.$.files": {
                                "date":date,
                                "file":ObjectId(fileId),
                                "updated": dt.datetime.now(pytz.utc)
                            }
                    
                        }
                    }
                )
        return True

    @staticmethod
    def saveFileToDB(mongo, username, dmname, filecontent):
        # Parameters: 
        #######################################################
        # username: str or unicode
        # dmname: str or unicode    
        # filecontent : str, text content of the model filecontent
        # pathid : str, uuid, direct to the corresponding output path
        # Returns: bool, True if successfully saved
        if type(filecontent) is not str:
            return False
        # to save file as bson, we need base64 encode first 
        b64content = base64.standard_b64encode(filecontent)
        # get bson object
        bincontent = binary.Binary(b64content)
        fileid = mongo.db.filedb.insert({"file": bincontent})

        #if this user doesn't upload history in database, create one
        userresult = mongo.db.history.find_one({"username": username})
        if userresult == None:
            mongo.db.history.insert({"username": username, "uploads": []})

        domainresult = mongo.db.history.find_one({
                "username": username,
                "uploads": {
                    "$elemMatch": {
                        "domainModelName": dmname
                    }
                }
            })
        if domainresult == None:
            mongo.db["history"].update({
                    "username": username
                }, {
                    "$push": {
                        "uploads": {
                            "domainModelName": dmname,
                            "files": []
                        }
                    }
                }
            )
        mongo.db["history"].update({
                "username": username,
                "uploads.domainModelName": dmname
            }, {
                "$push": {
                    "uploads.$.files": {
                        "file": fileid,
                        "date": dt.datetime.now(pytz.utc)
                    }
                }
            })
        return fileid

    @staticmethod
    def getAuthenKey(mongo, username):
        user = mongo.db.authentication.find_one({'username': username})
        return user['key']

    @staticmethod
    def deleteInstanceFromDB(mongo, username, modelName, fileId):
        # remove record from history
        # TODO: instead of removing, just inserting a flag
        mongo.db.history.update({
                "username": username,
                "uploads": {
                    "$elemMatch" : {
                        "domainModelName": modelName
                    }
                }
            },
            {
                "$pull": {
                    "uploads.$.files": {
                        "file": ObjectId(fileId)
                    }
                }
            }
        )

        # if size(uploads) equals 0, remove its parent object
        mongo.db.history.update(
            {
                "username": username,
                "uploads.domainModelName": modelName,
            },
            {
                "$pull" : {
                    "uploads" : {
                        "files" : {
                            "$size": 0
                        }
                    }
                }
            }
        )

        # remove record from filedb
        mongo.db.filedb.remove({'_id': ObjectId(fileId)})

        return True

