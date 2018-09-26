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



# NITIN : TODO : Implement restrictions implementations for the SimpleTypes ... from xsd ... refer(https://www.w3schools.com/xml/schema_dtypes_string.asp)



# NITIN : NOTE : all relations
class BaseRelation:
	def __init__(self, _id,_startId,_endId, _RationalType):
		self.id = _id
		self.startId = _startId
		self.endId = _endId
		self.type=_RationalType
                

class SimpleRelation(BaseRelation):
	def __init__(self, _id,_startId,_endId, _RationalType):
		BaseRelation.__init__(self, _id,_startId,_endId, _RationalType);
	def toJson(self,_target):
		retObj = {}
		retObj["relationType"] = self.type
		retObj["start"] = self.startId
		retObj["end"] = self.endId
                
		return retObj

	
class ComplexRelation(BaseRelation):
    def __init__(self, _id, _startId,_endId,_RationalType,_startUpperValue,_endUpperValue):
        BaseRelation.__init__(self, _id, _startId,_endId,_RationalType);
		# ZHIYUN: upper value of start and end class of relation
        self.startUpperValue=_startUpperValue
        self.endUpperValue=_endUpperValue
    def toJson(self,_target):
        retObj = {}
        retObj["relationType"] = self.type
        retObj["start"] = self.startId
        retObj["end"] = self.endId
        # ZHIYUN: transaltion upper value to relation type 
        if(self.startUpperValue=='*'and self.endUpperValue=='*'):
            retObj["multiplicity"]="many_to_many"
        elif(self.startUpperValue=='1'and self.endUpperValue=='1'):
            retObj["multiplicity"]="one_to_one"
        elif(self.startUpperValue=='1' and self.endUpperValue=='*'):
            if(_target=='from'):
                retObj["multiplicity"]="one_to_many"
            else:
                retObj["multiplicity"]="many_to_one"
        elif(self.startUpperValue=='*' and self.endUpperValue=='1'):
            if(_target=='from'):
                retObj["multiplicity"]="many_to_one"
            else:
                retObj["multiplicity"]="one_to_many"
        else:
            retObj["multiplicity"]="unknown"
        return retObj

class Generalization(SimpleRelation):
	def __init__(self, _id,_startId,_endId, _RationalType):
		SimpleRelation.__init__(self, _id,_startId,_endId, _RationalType)
	

class Aggregation(ComplexRelation):
	def __init__(self, _id, _startId,_endId,_RationalType,_startUpperValue,_endUpperValue):
		ComplexRelation.__init__(self, _id, _startId,_endId,_RationalType,_startUpperValue,_endUpperValue)
		
class Association(ComplexRelation):
	def __init__(self, _id,_startId,_endId,_RationalType,_startUpperValue,_endUpperValue):
		ComplexRelation.__init__(self, _id,_startId,_endId,_RationalType,_startUpperValue,_endUpperValue)

class Composition(ComplexRelation):
	def __init__(self, _id, _startId,_endId,_RationalType,_startUpperValue,_endUpperValue):
		ComplexRelation.__init__(self, _id, _startId,_endId,_RationalType,_startUpperValue,_endUpperValue)
	




