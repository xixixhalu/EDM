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
        
        if exporter=="Enterprise Architect": return self.EA_XMLUtil(root,namespaces,_dmoName)
        elif exporter=="Visual Paradigm": return self.VP_XMLUtil(root,namespaces,_dmoName) 
        else: raise e.SimpleException("parser for your xml exporter is not provided")


    def EA_XMLUtil(self,root,namespaces,_dmoName):
        # NITIN : TODO : Change parsing after correcting assumptions about the XML structure
        definition = root.find('xmi_namespace:Extension', namespaces)   
        elements = definition.find("elements")
        if elements is not None : elements = elements.findall("element")

        dmo = DomainModel(_dmoName)


        # NITIN : NOTE : Adding elements and their attributes/operations into model
        for element in elements:
            # NITIN : NOTE : If element is a definition of a class, then extract it's name, definition, attributes, relations
            if element.get(self.xmiPrefixAppender('type', namespaces["xmi_namespace"] )) == "uml:Class":
                elemId = element.get(self.xmiPrefixAppender('idref', namespaces["xmi_namespace"] ))
                elemName = element.get('name').strip()
                dmo.declareElement( elemName , elemId)
                
                # NITIN : NOTE : Check if the element has any attributes defined and aadd them
                elemAttributes = element.find('attributes')
                if elemAttributes is not None:
                    for elemAttribute in elemAttributes:
                        elemAttributeName = elemAttribute.get('name')
                        elemAttributeType = elemAttribute.find('properties').get('type')
                        # NITIN : TODO : implementation only for simple attributes, check how complex attributes are represented in xml
                        if elemAttributeType == "int" : elemAttributeTypeSetter = dt.Integer()
                        if elemAttributeType == "string" : elemAttributeTypeSetter = dt.String()
                        # NITIN : TODO : implement checker for other data datatypes like float etc.
                        dmo.defineSimpleAttribute(elemName, elemAttributeName, elemAttributeTypeSetter)
                        # NITIN : TODO : extract other features like upper and lower bounds, scope,

                # NITIN : TODO : Check if the element has any operations defined and aadd them, implement operations on domain model

                
        # NITIN : NOTE : Adding relations on elemnets into model
        for element in elements:
            if element.get(self.xmiPrefixAppender('type', namespaces["xmi_namespace"] )) == "uml:Class":

                elemRelations = element.find('links')
                if elemRelations is None : continue
                for elemRelation in elemRelations:
                    relationId = elemRelation.get(self.xmiPrefixAppender('id',namespaces["xmi_namespace"]))
                    dmo.defineRelation(relationId, str(elemRelation.get('start')), str(elemRelation.get('end')) , str(elemRelation.tag))

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

        elemType={}
        for element in elements:
            if element.get(self.xmiPrefixAppender('type', namespaces["xmi_namespace"] )) == "uml:DataType":
                typeId=element.get(self.xmiPrefixAppender('id', namespaces["xmi_namespace"] ))
                elemType[typeId]=element.get("name")


        for element in elements:
            if element.get(self.xmiPrefixAppender('type', namespaces["xmi_namespace"] )) == "uml:Class":
                elemId = element.get(self.xmiPrefixAppender('id', namespaces["xmi_namespace"] ))
                elemName = element.get('name').strip()
                dmo.declareElement(elemName , elemId)
                print(elemName,elemId)
                
                elemAttributes = element.findall('ownedAttribute')
                if elemAttributes is not None:
                    for elemAttribute in elemAttributes:
                        elemAttributeName = elemAttribute.get('name')
                        elemAttributeId = elemAttribute.get('type')
                        elemAttributeType = elemType[elemAttributeId]
                        print(elemAttributeName,elemAttributeType)
                        
                        if elemAttributeType == "int" : elemAttributeTypeSetter = dt.Integer()
                        if elemAttributeType == "string" : elemAttributeTypeSetter = dt.String()
                       
                        dmo.defineSimpleAttribute(elemName, elemAttributeName, elemAttributeTypeSetter)
                        
        #generalization
        for element in elements:
            if element.get(self.xmiPrefixAppender('type', namespaces["xmi_namespace"] )) == "uml:Class":
                elemId = element.get(self.xmiPrefixAppender('id', namespaces["xmi_namespace"] ))
                elemRelations = element.findall('generalization')
                if elemRelations is None : continue
                for elemRelation in elemRelations:
                    relationId = elemRelation.get(self.xmiPrefixAppender('id',namespaces["xmi_namespace"]))                  
                    dmo.defineRelation(relationId, str(elemId), str(elemRelation.get('general')) , str("Generalization"))


        #association/aggregation
        for element in elements:
            if element.get(self.xmiPrefixAppender('type', namespaces["xmi_namespace"] )) == "uml:Association":
                relationId = element.get(self.xmiPrefixAppender('id', namespaces["xmi_namespace"]))
                ownedEnds=element.findall('ownedEnd')
                if ownedEnds[1].get('aggregation')=="shared":                 
                    dmo.defineRelation(relationId, str(ownedEnds[1].get('type')), str(ownedEnds[0].get('type')) , str("Aggregation"))
                    print(relationId, str(ownedEnds[1].get('type')), str(ownedEnds[0].get('type')) , str("Aggregation"))
                else:
                    dmo.defineRelation(relationId, str(ownedEnds[1].get('type')), str(ownedEnds[0].get('type')) , str("Association"))
                    print(relationId, str(ownedEnds[1].get('type')), str(ownedEnds[0].get('type')) , str("Association"))

        json_file = open("generated_code/default/"+output_filename+".json", "w")
        json_file.write(dmo.toJson())
        json_file.close()

        return dmo.toJson()



#if __name__=='__main__':
 #   ana = analyzer()
  #  ana.DM_File_Analyze('Input', {'DM_Input_type': "Simple_XML"}, 'Generalization_vp')
         
