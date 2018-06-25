import os
from pymongo import MongoClient
import json
from utilities import edm_utils, exceptions as e


class DBUtilities:
	
	# NITIN : NOTE : Usage is as follows : .setup(configDictionary={dict}) or .setup(configFile='/path/to/configFile'), priority given to configDictionary
	def setup(self, configDictionary=None, configFile=None):
		if configDictionary is not None:
			self.configurations = configDictionary
			if 'host' and 'port' not in configDictionary.keys() : raise e.SimpleException("configDictionary needs to contain host and port")
		elif configFile is not None:
			if os.path.exists(configFile):
				with open(configFile) as cfile:
					self.configurations = json.load(cfile)
					if 'host' and 'port' not in self.configurations.keys() : raise e.SimpleException("configDictionary needs to contain host and port")
		else:
			self.configurations = None

		try :
			if self.configurations is None:
				self.client = MongoClient()
			else:
				if self.configurations['port'] is not int:
					# NITIN : TODO : Handle error and continue to parse it anyway
					#raise e.SimpleException()
					self.configurations['port'] = int(self.configurations['port'])
				self.client = MongoClient(self.configurations['host'], self.configurations['port'])
		except Exception as ex:
			print str(ex)
			raise e.SimpleException('problem connecting to the db instance, try firing again!')


	def createRespectiveCollections(self, jsonDMO, domainModelName):
		if self.client is None:
			print "call setup() on the DBUtilities and pass config file to it"

		elements = jsonDMO[domainModelName]['elements']
		db = self.client.domainModelName
		for obj in elements:
			print str(obj['elementName'])
			db.create_collection(str(obj['elementName']))
		print db.collection_names()


	def createWithUser(self, domainModelName):
		db = self.client[domainModelName]
		db_user, db_password = edm_utils.generate_user_credentials(domainModelName)
	
		try:
			db.command("dropUser", db_user)
		except Exception as ex:
			pass
		db.command("createUser", db_user, pwd=db_password, roles=['readWrite'])
		print("Added user " + db_user + " to mongo db " + domainModelName)

	def createOrUpdateDB(self, jsonDMO):
		if self.client is None:
			print "call setup() on the DBUtilities and pass config file to it"
		# NITIN : TODO : implement the authentications, user management etc later
		# NITIN : NOTE : if domain model DNE create a database for it

		# NITIN : TODO : check if it can be updated in place without loosing data
		if type(jsonDMO) is not dict:
			jsonDMO = json.loads(jsonDMO)
		domainModelName = str(jsonDMO.keys()[0])
		if domainModelName in map(lambda a : str(a), self.client.database_names()):
			self.client.drop_database(domainModelName)
			
		# NITIN : TODO : call the collections creations services here, the database is created when collections are created
		self.createRespectiveCollections(jsonDMO,domainModelName)


	def getDBConnectionObject(self, domainModelName):
		if self.client is None:
			print "call setup() on the DBUtilities and pass config file to it"

		if domainModelName not in map(lambda a: str(a), self.client.database_names()):
			return None
		return self.client.get_database(domainModelName)


	def shutdown(self):
		if self.client is None:
			print "call setup() on the DBUtilities and pass config to it"

		self.client.close()
