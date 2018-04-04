from utilities import exceptions as e


# NITIN : NOTE : all elements types

class BaseType:
	def __init__(self, _type, _minOccurs=1, _maxOccurs = 1):
                self.type=_type
		self.minOccurs = 1
		self.maxOccurs = 1


class SimpleType(BaseType):
	def __init__(self, _type, _minOccurs=1, _maxOccurs = 1):
		BaseType.__init__(self, _type, _minOccurs,_maxOccurs)
        def toJson(self):
		retObj = {}
                retObj["type"]=self.type
		retObj["minOccurs"] = self.minOccurs
		retObj["maxOccurs"] = self.maxOccurs
		return retObj


class ComplexType(BaseType):
	def __init__(self , _type, _minOccurs=1, _maxOccurs = 1):
		BaseType.__init__(self, _type, _minOccurs,_maxOccurs)
	def toJson(self):
		retObj = {}
                retObj["type"]=self.type.lower().replace(" ","_")
		retObj["minOccurs"] = self.minOccurs
		retObj["maxOccurs"] = self.maxOccurs
		return retObj

# NITIN : extends a base element
class ExtensionType(BaseType):
	def __init__(self, _BaseElementName):
		BaseType.__init__(self)
		self.BaseElementName = _BaseElementName

#class Integer(SimpleType):
#	def __init__(self,_minOccurs=1, _maxOccurs = 1):
#		SimpleType.__init__(self,_minOccurs,_maxOccurs)
#	def toJson(self):
#		retObj = {}
#		retObj["minOccurs"] = self.minOccurs
#		retObj["maxOccurs"] = self.maxOccurs
#		retObj["type"] = "Integer"
#		return retObj

# NITIN : TODO : Enumerate all the simple datatypes...int,string,float
# NITIN : TODO : Implement restrictions implementations for the SimpleTypes ... from xsd ... refer(https://www.w3schools.com/xml/schema_dtypes_string.asp)



# NITIN : NOTE : all relations

class BaseRelation:
	def __init__(self, _id, _startId, _endId):
		self.id = _id
		self.startId = _startId
		self.endId = _endId


class Aggregation(BaseRelation):
	def __init__(self, _id, _startId, _endId):
		BaseRelation.__init__(self, _id, _startId, _endId)
	def toJson(self):
		retObj = {}
		retObj["relationType"] = "Aggregation"
		retObj["start"] = self.startId
		retObj["end"] = self.endId
		return retObj

class Association(BaseRelation):
	def __init__(self, _id, _startId, _endId):
		BaseRelation.__init__(self, _id, _startId,_endId)
	def toJson(self):
		retObj = {}
		retObj["relationType"] = "Association"
		retObj["start"] = self.startId
		retObj["end"] = self.endId
		return retObj

class Generalization(BaseRelation):
	def __init__(self, _id, _startId , _endId):
		BaseRelation.__init__(self, _id, _startId, _endId)
	def toJson(self):
		retObj = {}
		retObj["relationType"] = "Generalization"
		retObj["start"] = self.startId
		retObj["end"] = self.endId
		return retObj

class Composition(BaseRelation):
	def __init__(self, _id, _startId , _endId):
		BaseRelation.__init__(self, _id, _startId, _endId)
	def toJson(self):
		retObj = {}
		retObj["relationType"] = "Composition"
		retObj["start"] = self.startId
		retObj["end"] = self.endId
		return retObj




