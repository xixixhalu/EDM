import sys
sys.path.append('../')
from utilities.file_op import fileOps
import json

from JSONParser import *

class JSONParser:

    def __init__(self, json_dm, dmname):

        self.__entity = {}
        self.__attribute = {}
        self.__behavior = {}
        self.__association = {}

        elements = json_dm[dmname]['elements']
        for entity in elements:
            # map id with name
            self.__entity[entity['elementId']] = entity['elementName']

            # process attributes
            self.__attribute[entity['elementName']] = entity['Attributes']['Simple']
            
            # process behaviors
            self.__behavior[entity['elementName']] = entity['Behaviors']

            # process associations
            self.__association[entity['elementName']] = entity['Relations']['To']

    @classmethod
    def fromFile(cls, path, dmname):
        file_path = path + "/" + dmname + '.json'
        with safe_open_r(self.__path) as f:
            json_dm = json.loads(f)
        return cls(json_dm)

    def entities(self):
        return self.__entity

    def attributes(self):
        return self.__attribute

    def behaviors(self):
        return self.__behavior

    def associations(self):
        return self.__association

    def findEntityNameById(self, entityId):
        if entityId in self.__entity:
            return self.__entity[entityId]
        else:
            return []

    def findEntityAttributes(self, entityName):
        if entityName in self.__attribute:
            return self.__attribute[entityName]
        else:
            return []

    def findEntityBehaviors(self, entityName):
        if entityName in self.__behavior:
            return self.__behavior[entityName]
        else:
            return []

    def findEntityAssociations(self, entityName):
        if entityName in self.__association:
            return self.__association[entityName]
        else:
            return []
