import sys
sys.path.append('../')
from utilities.file_op import fileOps
import json

from JSONParser import *

class JSONParser:

    def __init__(self, json_dm, dmname=None):

        self.__entity = {}
        self.__attribute = {}
        self.__nested_object = {}
        self.__behavior = {}
        self.__association = {}

        if dmname is not None:
            elements = json_dm[dmname]['elements']
        else:
            elements = [json_dm]

        
        for entity in elements:
            try:
                # map id with name
                self.__entity[entity['elementId']] = entity['elementName']
            except Exception as e:
                pass

            try:
                # process attributes
                self.__attribute[entity['elementName']] = entity['Attributes']['Simple']
            except Exception as e:
                pass

            try:
                # process nested_object
                self.__nested_object[entity['elementName']] = entity['Attributes']['Complex']
            except Exception as e:
                pass
            
            try:
            # process behaviors
                self.__behavior[entity['elementName']] = entity['Behaviors']
            except Exception as e:
                pass

            try:
                # process associations
                self.__association[entity['elementName']] = entity['Relations']['To']
            except Exception as e:
                pass


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

    def nested_objects(self):
        return self.__nested_object

    def behaviors(self):
        return self.__behavior

    def associations(self):
        return self.__association

    def findEntityNameById(self, entityId):
        if self.__entity and entityId in self.__entity:
            return self.__entity[entityId]
        else:
            return []

    def findEntityAttributes(self, entityName):
        if self.__attribute and entityName in self.__attribute:
            return self.__attribute[entityName]
        else:
            return []

    def findEntityNestedObjects(self, entityName):
        if self.__nested_object and entityName in self.__nested_object:
            return self.__nested_object[entityName]
        else:
            return []

    def findEntityBehaviors(self, entityName):
        if self.__behavior and entityName in self.__behavior:
            return self.__behavior[entityName]
        else:
            return []

    def findEntityAssociations(self, entityName):
        if self.__association and entityName in self.__association:
            return self.__association[entityName]
        else:
            return []
