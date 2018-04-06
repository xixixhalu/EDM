# -*- coding: utf-8 -*-

from utilities import exceptions as e
from uml_parser import datatypes as dt
import json

class DomainModel:
	

	def __init__(self, _dmoName):
		# NITIN : NOTE : Directory holds the id to object reference for the elements
		self.ElementDirectory = {}
        # NITIN : NOTE : Directory holds the name to id reference for the elements
 		self.ElementReference = {}
 		# NITIN : NOTE : Set holds id of relations in the domain model
 		self.Relations = set()
 		# NITIN : NOTE : Name of the domain model
 		self.dmoName = _dmoName

 	# NITIN : Element must be declared before being used
	def declareElement(self , _ElementName, _id):
		# NITIN : NOTE : create a unique id for each element, used for associations
                _ElementName=_ElementName.lower().replace(" ","_")
		newElement = self.Element(_ElementName , _id)
		self.ElementDirectory[_id] = newElement
		self.ElementReference[_ElementName] = _id
              

	# NITIN : NOTE : Define simple atrribute on a declared element
	def defineSimpleAttribute(self , _ElementName , _AttributeName , _AttributeType): 
                _ElementName=_ElementName.lower().replace(" ","_")
		try:
			assert self.isElementDeclared(_ElementName)
		except:
			raise e.SimpleException("No such element declared, check for declaration of element :" + _ElementName)
		
		id = self.ElementReference[_ElementName]
		self.ElementDirectory[id].addSimpleAttribute(_AttributeName, _AttributeType)

	# NITIN : NOTE : Define a attribute of the type of another element
	def defineComplexAttribute(self, _ElementName , _AttributeName , _AttributeElementName , _AttributeType):
                _ElementName=_ElementName.lower().replace(" ","_")
                _AttributeElementName=_AttributeElementName.lower().replace(" ","_")
		try:
			assert self.isElementDeclared(_ElementName)
		except:
			raise e.SimpleException("No such element declared, check for declaration of element :" + _ElementName)

		if not self.isElementDeclared(_AttributeElementName) : 
                    raise e.SimpleException("Attempt to create attribute of type " + _AttributeElementType + " which is not declared .")
               
		id = self.ElementReference[_ElementName]
		self.ElementDirectory[id].addComplexAttribute(_AttributeName, _AttributeElementName, _AttributeType)

	# NITIN : NOTE : Define relations between element
	def defineRelation(self, _id, _start, _end, RelationType = "Association"):
		if _id in self.Relations : return

		# NITIN : TODO : handle exceptions without stopping execution of program
		if not self.ElementDirectory.has_key(_start) : raise e.SimpleException("Starting Element of relation not defined, startId : " + _start)
		if not self.ElementDirectory.has_key(_end) : raise e.SimpleException("Ending Element of relation not defined, startId : " + _end)

		if RelationType == "Association":
			relation = dt.Association(_id, _start, _end)
		elif RelationType == "Aggregation":
			relation = dt.Aggregation(_id, _start, _end)
                        
                        #add start node to end node as an attribute
                        elemName = str(self.ElementDirectory[_start].ElementName)
                        elemAttributeTypeSetter = dt.SimpleType("string")
                        elemAttributeName=str(self.ElementDirectory[_end].ElementName)+"_id"
                        self.defineSimpleAttribute(elemName, elemAttributeName, elemAttributeTypeSetter)
		elif RelationType == "Generalization":
			relation = dt.Generalization(_id, _start, _end)
                elif RelationType == "Composition":
                        relation = dt.Composition(_id, _start, _end)
		else:
			raise e.SimpleException("Type of relation not defined : " + RelationType)


		self.Relations.add(_id)
		self.ElementDirectory[_start].relationsFromThisElement.append(relation)
		self.ElementDirectory[_end].relationsToThisElement.append(relation)


	# NITIN : NOTE : Make an element an extension of another element, basically imports all the base element's attributes and functions
	def extendElement(self, _ElementName, _ExtensionType):
                _ElementName=_ElementName.lower().replace(" ","_")
		if not isinstance(_ExtensionType, dt.ExtensionType): raise e.SimpleException("_AttributeType has to be ExtensionType.")
                
		id = self.ElementReference[_ElementName]
		self.ElementReference[id].extendElement(_ExtensionType)

	# NITIN : NOTE : Utility function to check if element is declared
	def isElementDeclared(self, _ElementName):
		return self.ElementReference.has_key(_ElementName)

	# NITIN : NOTE : Utility function to display state of domain model
	def toString(self):
		returnString = ""
		returnString += "Elements and their descriptions  :\n\n"
		for key,value in self.ElementReference.iteritems():
			returnString += key + " : \n" + str(self.ElementDirectory[value].tostring()) + "\n"
		return returnString

	def toJson(self):
		return_obj = {}
		return_obj[self.dmoName] = {"elements" : []}
		for id,element in self.ElementDirectory.iteritems():
			return_obj[self.dmoName]["elements"].append(element.toJson())
		return json.dumps(return_obj)


	class Element:
		
		def __init__(self, _ElementName , _id):
			self.id = _id
			# NITIN : NOTE : Keep tab if the element is an extension of another element
			self.isExtension = False
			self.ElementName = _ElementName
			# NITIN : NOTE : maps attribute name to a SimpleType Object
			self.SimpleAttributes = {}
			# NITIN : NOTE : maps attribute name to a tupl (ElementName, ComplexType Object)
			self.ComplexAttributes = {}
			# NITIN : TODO : add fucntionality to add custom functions on Domain Models
			self.Functions = {}
			# NITIN : NOTE : add relationships
			self.relationsToThisElement = []
			self.relationsFromThisElement = [] 
		
		def addSimpleAttribute(self, _AttributeName , _AttributeType):
			if not isinstance(_AttributeType,dt.SimpleType) : raise e.SimpleException("Trying to add a non SimpleType attribute in the function addSimpleAttribute .") 
			self.SimpleAttributes[_AttributeName] = _AttributeType
		
		def addComplexAttribute(self, _AttributeName , _AttributeElementName , _AttributeType):
			if not isinstance(_AttributeType, dt.ComplexType) : raise e.SimpleException("Trying to add a non ComplexType attribute in the function addComplexAttribute .")
			self.ComplexAttributes[_AttributeName] = (_AttributeElementName, _AttributeType)

		def extendElement(self, _ExtensionType):
			self.isExtension = True
			self.ExtensionType = _ExtensionType

		# NITIN : NOTE : Utility function to display state of Element	
		def tostring(self):
			returnString = ""
			returnString += "Simple attributes : "
			for key,value in self.SimpleAttributes.iteritems():
				returnString += key + ","
			returnString += "\nComplex attributes : "
			for key,value in self.SimpleAttributes.iteritems():
				returnString += key + ","
			returnString += "\nRelations from this element :" + str(self.relationsFromThisElement)
			returnString += "\nRelations to this element :" + str(self.relationsToThisElement)
			returnString += "\n"

			return returnString

		def toJson(self):
			return_obj = {}
			return_obj["elementName"] = str(self.ElementName)
			return_obj["elementId"] = str(self.id)
			return_obj["isExtension"] = self.isExtension
			if self.isExtension:
				return_obj["extensionType"] = str(self.ExtensionType)
			return_obj["Attributes"] = {}
			return_obj["Attributes"]["Simple"] = []
			return_obj["Attributes"]["Complex"] = []
			return_obj["Operations"] = []
			return_obj["Relations"] = {}
			return_obj["Relations"]["From"] = []
			return_obj["Relations"]["To"] = []

			for key,value in self.SimpleAttributes.iteritems():
				attrObj = {}
				attrObj["name"] = key
				attrObj["details"] = value.toJson()
				return_obj["Attributes"]["Simple"].append(attrObj)

			for key,value in self.ComplexAttributes.iteritems():
				attrObj = {}
				attrObj["name"] = key
				attrObj["referenceType"] = value[0]
				attrObj["details"] = value[1].toJson()
				return_obj["Attributes"]["Complex"].append(attrObj)

			for relation in self.relationsFromThisElement:
				return_obj["Relations"]["From"].append(relation.toJson())

			for relation in self.relationsToThisElement:
				return_obj["Relations"]["To"].append(relation.toJson())

			# NITIN : TODO : write implementation to add the operation in this element to json

			return return_obj











