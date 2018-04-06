import ConfigParser
import os

class ConfigUtil():

   def get(self, section, property):
	config = ConfigParser.ConfigParser()
	cwd = os.getcwd()
	config.read(cwd + "/config.properties")
	return config.get(section, property)

   def getInt(self, section, property):
	return int(self.get(section, property))
