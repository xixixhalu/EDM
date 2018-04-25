#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
from utilities import exceptions as e
from utilities import edm_utils
from uml_parser.domain_model import DomainModel
from uml_parser import datatypes as dt
import xml.etree.ElementTree as ET

output_filename = ""


class Analyzer:

    def xmiPrefixAppender(self, key, xmiPrefix):
        return '{' + xmiPrefix + '}' + key

    def DM_File_Analyze(self,PROJECT_DIR, config, filename):
        if not os.path.exists(PROJECT_DIR):
            raise e.SimpleException("Project Home Directory not created, run project initialize first.")

        global output_filename
        output_filename = filename
        DM_File_type = config['DM_Input_type']
        if DM_File_type == "Simple_XML":       
            retObj = self.SimpleXMLUtil(PROJECT_DIR + "/" + filename+".xml", filename)
            if retObj is None:
                raise e.SimpleException("xml file not provided in the directory, check if file with extension .xml is uploaded")
            return retObj


    def SimpleXMLUtil(self,dmoFile, _dmoName):
        global output_filename
        # NITIN : TODO : check how to handle namepspaces dynamically later
        namespaces = {"xmi_namespace": "http://schema.omg.org/spec/XMI/2.1"}
        myDMO = ET.parse(dmoFile)
        root = myDMO.getroot()

        documentation=root.find('xmi_namespace:Documentation', namespaces)
        exporter=documentation.get('exporter')
        
        # ZHIYUN: call corresponding parser for xml file
        if exporter=="Enterprise Architect": return self.EA_XMLUtil(root,namespaces,_dmoName)
        elif exporter=="Visual Paradigm": return self.VP_XMLUtil(root,namespaces,_dmoName) 
        else: raise e.SimpleException("parser for your xml exporter is not provided")


    def EA_XMLUtil(self,root,namespaces,_dmoName):
        # NITIN : TODO : Change parsing after correcting assumptions about the XML structure
        definition = root.find('xmi_namespace:Extension', namespaces)   
        elements = definition.find("elements")
        if elements is not None : elements = elements.findall("element")

        dmo = DomainModel(_dmoName)
        

        # ZHIYUN: adding elements into model
        elem={}
        for element in elements:
            # ZHIYUN : extract element if it's a definition of a class
            if element.get(self.xmiPrefixAppender('type', namespaces["xmi_namespace"] )) == "uml:Class":
                elemId = element.get(self.xmiPrefixAppender('idref', namespaces["xmi_namespace"] ))
                elemName = element.get('name').strip()
                dmo.declareElement( elemName , elemId)
                elem[elemId]=elemName
      

        # ZHIYUN: adding attributes to element
        for element in elements:
            if element.get(self.xmiPrefixAppender('type', namespaces["xmi_namespace"] )) == "uml:Class":
                elemName = element.get('name').strip()
                elemAttributes = element.find('attributes')
                if elemAttributes is not None:
                    for elemAttribute in elemAttributes:
                        elemAttributeName = elemAttribute.get('name')
                        elemAttributeType = elemAttribute.find('properties').get('type')

                        # ZHIYUN: add complex attributes
                        if elemAttributeType in elem.values():
                            AttributeTypeSetter=dt.ComplexType(elemAttributeType)
                            dmo.defineComplexAttribute(elemName,elemAttributeName, elemAttributeType, AttributeTypeSetter) 
                      
                        #s ZHIYUN: add simple attributes
                        else:
                            elemAttributeTypeSetter=dt.SimpleType(elemAttributeType)
                            dmo.defineSimpleAttribute(elemName, elemAttributeName, elemAttributeTypeSetter)
                            
                        # NITIN : TODO : extract other features like upper and lower bounds, scope,

                # NITIN : TODO : Check if the element has any operations defined and aadd them, implement operations on domain model




        # ZHIYUN: iterate all upper value of relation                
	connectors=definition.find('connectors').findall('connector')
        upperValues={}
        for connector in connectors:
            relationId=connector.get(self.xmiPrefixAppender('idref', namespaces["xmi_namespace"] ))
            startUpperValue=connector.find('source').find('type').get('multiplicity')
            endUpperValue=connector.find('target').find('type').get('multiplicity')
            upperValues[relationId]=[startUpperValue,endUpperValue]


        # ZHIYUN: adding relations to elemnents
        for element in elements:
            if element.get(self.xmiPrefixAppender('type', namespaces["xmi_namespace"] )) == "uml:Class":
                elemRelations = element.find('links')
                if elemRelations is None : continue
                for elemRelation in elemRelations: 
                    # ZHIYUN: ignore relations to class not existing in the domain
                    if not (elem.has_key(str(elemRelation.get('start'))) and elem.has_key(str(elemRelation.get('end')))): continue;


                    relationId = elemRelation.get(self.xmiPrefixAppender('id',namespaces["xmi_namespace"]))

                    if(elemRelation.tag=='Generalization'):
                        dmo.defineRelation(relationId, str(elemRelation.get('start')), str(elemRelation.get('end')), str(elemRelation.tag))
                    else:
                        # ZHIYUN: add upper value to relation
                        startUpperValue='unknown'  
                        endUpperValue='unknown'
                        if upperValues.has_key(relationId): 
                            startUpperValue=upperValues[relationId][0]
                            endUpperValue=upperValues[relationId][1]
                        dmo.defineRelation(relationId, str(elemRelation.get('start')), str(elemRelation.get('end')) , str(elemRelation.tag), startUpperValue, endUpperValue)

        file_path = "generated_code/default/" + _dmoName + "/"
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        edm_utils.copyDirLink('code_templates/node_modules', file_path+'node_modules')
        json_file = open(file_path + output_filename + ".json", "w")


        json_file.write(dmo.toJson())
        json_file.close()

        return dmo.toJson()




    def VP_XMLUtil(self,root,namespaces,_dmoName):
        elements = root.findall("packagedElement")
        dmo = DomainModel(_dmoName)


        # ZHIYUN: store all mapping of attribute id to its name
        elemType={}
        for element in elements:
            if element.get(self.xmiPrefixAppender('type', namespaces["xmi_namespace"] )) == "uml:DataType":
                typeId=element.get(self.xmiPrefixAppender('id', namespaces["xmi_namespace"] ))
                elemType[typeId]=element.get("name")
        
        # ZHIYUN: adding elements into model
        elem={}
        for element in elements:
            if element.get(self.xmiPrefixAppender('type', namespaces["xmi_namespace"] )) == "uml:Class":
                elemId = element.get(self.xmiPrefixAppender('id', namespaces["xmi_namespace"] ))
                elemName = element.get('name').strip()
                dmo.declareElement(elemName , elemId)
                elem[elemId]=elemName
 
                
        # ZHIYUN: adding attributes to element
        for element in elements:
            if element.get(self.xmiPrefixAppender('type', namespaces["xmi_namespace"] )) == "uml:Class":
                elemName = element.get('name').strip()
                elemAttributes = element.findall('ownedAttribute')
                if elemAttributes is not None:
                    for elemAttribute in elemAttributes:
                        AttributeName = elemAttribute.get('name')
                        AttributeId = elemAttribute.get('type')
                        
                        # ZHIYUN: add simple attributes
                        if elemType.has_key(AttributeId):
                            AttributeType = elemType[AttributeId]      
                            AttributeTypeSetter=dt.SimpleType(AttributeType) 
                            dmo.defineSimpleAttribute(elemName, AttributeName, AttributeTypeSetter)

                        # ZHIYUN: add complex attribute
                        elif elem.has_key(AttributeId):
                            AttributeElemName = elem[AttributeId]
                            AttributeTypeSetter=dt.ComplexType(AttributeElemName)
                            dmo.defineComplexAttribute(elemName,AttributeName, AttributeElemName, AttributeTypeSetter)

        # ZHIYUN: adding relations to elemnents 
                
        # ZHIYUN: add generalization relations
        for element in elements:
            if element.get(self.xmiPrefixAppender('type', namespaces["xmi_namespace"] )) == "uml:Class":
                elemId = element.get(self.xmiPrefixAppender('id', namespaces["xmi_namespace"] ))
                elemRelations = element.findall('generalization')
                if elemRelations is None : continue
                for elemRelation in elemRelations:
                    relationId = elemRelation.get(self.xmiPrefixAppender('id',namespaces["xmi_namespace"]))                  
                   

                    dmo.defineRelation(relationId, str(elemId), str(elemRelation.get('general')) , str("Generalization"))


        # ZHIYUN: add other relations
        for element in elements:
            if element.get(self.xmiPrefixAppender('type', namespaces["xmi_namespace"] )) == "uml:Association":
                relationId = element.get(self.xmiPrefixAppender('id', namespaces["xmi_namespace"]))
                ownedEnds=element.findall('ownedEnd')
                start=ownedEnds[1]
                end=ownedEnds[0]

                # ZHIYUN: add upper value of start and end class to relation
                startUpperVaule="unknown"
                endUpperValue='unknown'
                if(start.find('upperValue') is not None): startUpperVaule=start.find('upperValue').get('value')
                if(end.find('upperValue') is not None): endUpperValue=end.find('upperValue').get('value')
                # ZHIYUN: add relations      
                if start.get('aggregation')=="shared":                 
                    dmo.defineRelation(relationId, str(start.get('type')), str(end.get('type')),str("Aggregation"), startUpperVaule,endUpperValue)
                elif start.get('aggregation')=="composite":
                    dmo.defineRelation(relationId,  str(start.get('type')), str(end.get('type')) , str("Composition"),startUpperVaule,endUpperValue)
                else:
                    dmo.defineRelation(relationId,  str(start.get('type')), str(end.get('type')) , str("Association"),startUpperVaule,endUpperValue)


  
        file_path = "generated_code/default/" + _dmoName + "/"
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        edm_utils.copyDirLink('code_templates/node_modules', file_path+'node_modules')
        json_file = open(file_path + output_filename + ".json", "w")
        
        json_file.write(dmo.toJson())
        json_file.close()

        return dmo.toJson()


# ZHIYUN: test code
#if __name__=='__main__':
 #   ana = analyzer()
  #  ana.DM_File_Analyze('Input', {'DM_Input_type': "Simple_XML"}, 'one_to_many')
         
