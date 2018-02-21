'''
	Author : nitin.jamadagni@gmail.com
	precursors : Flask
	Usage : python core.py OPT <host> <port>
			OPT : SETUP/RUN
'''


'''
Imports section
'''
from flask import Flask, jsonify, request
import sys
from pymongo import MongoClient
import uuid
import datetime as dt


'''
Setup and globals
'''
if len(sys.argv) is not 4:
	print "Usage : python core.py OPT <host> <port>\n OPT : SETUP/RUN"
app = Flask("authentication_service")
client = MongoClient('localhost' , 27017)
db = client["usermetadata"]





'''
Utility functions
'''
def setupandexit():
	'''
		db : usermetadata
			collection : authentication :
										{
											username :
											key :
											validtill :
										}
			collection : history : 
										{
											username : 
											uploads : 
													{
														domainModelName : 	[ 
																				{	
																					file : 
																			 		date : 
																				}
																			]
													}
										}
	'''
	db.create_collection("authentication")
	db["authentication"].create_index([('username',pymongo.ASCENDING)],unique=True)
	db.create_collection("history")
	db["history"].create_index([('username',pymongo.ASCENDING)],unique=True)

def create_random_key():
	return str(uuid.uuid4())

def create_expiry_object():
	return dt.datetime.now() + dt.timedelta(days = 30)





'''
Main Functionalities
'''
# NITIN : NOTE : assuming the user has same token for all his domain models, change later for an exclusive token for each domain model
@app.route('/')
def default():
	response = {"status" : "success",\
				"response" : "Use the following  model for service\n \
				1. /register/<username> [] [response of a token] \n\
				2. /authenticate/<username> [send 'key' : key_value in header] [response of a authentication accept] \n\
				3. /refreshtoken/<username> [send 'key' : key_value in header] [renew token and send back new]\n\
				4. /registerUpload/<string:username>/<string:dmName> [send 'modelfile' : file] [get acknoledgement back]\n\
				"}
	return jsonify(response)

@app.route('/authenticate/<string:username>')
def authenticate(username):
	response = {}

	if not hasattr(request.args , 'key'):
		response["status"] = "fail"
		response["response"] = "'key' not sent in header"
		return jsonify(response)


	userprofile = db["authentication"].find_one(filter={"username" : username}, projection={'_id':False,'key':True, 'username' : True , 'validtill' : True})
	if userprofile.count() == 0:
		response["status"] = "fail"
		response["response"] = "User not registered yet"
		return jsonify(response)

	

	if request.args.key == str(userprofile["key"]):
		delta = dt.datetime.now() - userprofile["validtill"]
		if not delta >= dt.timedelta():
			response["status"] = "fail"
			response["response"] = "try refreshing your token, it is expired"
			return jsonify(response)
		response["status"] = "success"
		response["response"] = {"username" : userprofile["username"] , "Authenticated" : True}
		return jsonify(response)
	else:
		response["status"] = "fail"
		response["response"] = {"username" : userprofile["username"] , "Authenticated" : False}
		return jsonify(response)


@app.route('/register/<string:username>')
def registerUser(username):
	response = {}
	userprofile = db["authentication"].find_one(filter={"username" : username} , projection = {'_id' : True , 'key' : False , 'username' : False , 'validtill' : False})
	if userprofile.count() is not 0:
		response["status"] = "fail"
		response["response"] = "User already registered"
		return jsonify(response)

	key = create_random_key()
	validtill = create_expiry_object()
	userprofile = { "username" : username , "key" : key , "validtill" : validtill}
	db["authentication"].insert_one(userprofile)
	db["history"].insert_one( {"username" : username , uploads = [] } ) 
	response["status"] = "success"
	response["response"] = {"message" : "Successfully registerd user, check the object in 'returnvalue' to get the key" , "returnvalue" : userprofile}
	return jsonify(response)


@app.route('/refreshtoken/<string:username>')
def refreshtoken(username):
	response = {}
	
	if not hasattr(request.args , 'key'):
		response["status"] = "fail"
		response["response"] = "'key' not sent in header"
		return jsonify(response)

	userprofile = db["authentication"].find_one(filter={"username" : username}, projection={'_id':False,'key':True, 'username' : True , 'validtill' : True})
	if userprofile.count() == 0:
		response["status"] = "fail"
		response["response"] = "User not registered yet"
		return jsonify(response)

	if request.args.key == str(userprofile["key"]):
		key = create_random_key()
		validtill = create_expiry_object()
		db["authentication"].update_one(filter = {"username"  : username} , update = { '$set' : {'key' : key , 'validtill' : validtill} }, upsert = False)
		userprofile = { "username" : username , "key" : key , "validtill" : validtill}
		response["status"] = "success"
		response["response"] = {"message" : "Successfully updated key, check the object in 'returnvalue' to get the key" , "returnvalue" : userprofile}
	else:
		response["status"] = "fail"
		response["response"] = "wrong old key, provide correct old key to refresh token"

	
@app.route('/registerUpload/<string:username>/<string:dmName>' , methods = ['POST'])
def upload(username, dmName):
	pass
	#f = request.files['modelfile']
	#db["history"].update_one(filter = {"username" : username} , update = {'$push' : { dmName : f}} , upsert = True)

	# NITIN : TODO : check how to save blobs to mongo






'''
Program Flow
'''
if __name__ == '__main__':
	if sys.argv[1] == "RUN":
		app.run(host = sys.argv[2],port = sys.argv[3],debug = True)
	elif sys.argv[1] == "SETUP":
		setupandexit()