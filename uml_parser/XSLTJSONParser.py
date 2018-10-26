import sys
sys.path.append('../')
from utilities.file_op import fileOps
from config import config
import os
import lxml.etree as eTree
import xml.etree.ElementTree as ET
import json
import glob


class XSLTJSONParser:

    @staticmethod
    def process(PROJECT_DIR, _dmoName):

        xml_path = PROJECT_DIR + "/" + _dmoName +".xml"
        template_file = config.get('Output', 'default_xslt_template')

        rst = XSLTJSONParser.parse_xml(xml_path, template_file)

        # Wrap the json project for further processing
        json_dmo = {}
        json_dmo[_dmoName] = {}
        json_dmo[_dmoName]["elements"] = rst

        with fileOps.safe_open_w(PROJECT_DIR + "/" + _dmoName + ".json") as o:
            o.write(json.dumps(json_dmo, indent=2));

        return rst

    
    @staticmethod
    def parse_xml(xml_path, xslt_path):
        try: 
            xml_file = eTree.parse(xml_path)
            xslt_file = eTree.parse(xslt_path)
            transform = eTree.XSLT(xslt_file)
            json_str = transform(xml_file)
        except Exception as e:
            print e
        print str(json_str)
        return json.loads(str(json_str))


    # bash test
    @staticmethod
    def bash_test(input_path, output_path):
        
        xslt_path = "../code_templates/XSLTJSON/BUILD.XML.DICT.xml"

        file_list = glob.glob(input_path + "*.xml")

        success_size = 0
        error_size = 0
        error_files = []

        for file in file_list:

            print "Proceessing" + file + "..."
            pre_path, file_name = os.path.split(file)

            try:
                rst = XSLTJSONParser.parse_xml(file, xslt_path)
                
                with fileOps.safe_open_w(output_path + file_name + ".json") as o:
                    # o.write(rst);
                    o.write(str(rst))

                success_size += 1
            except Exception as e:
                print "Error in " + file
                print e
                error_files.append(file_name)
                error_size += 1
                continue

        print "Total size: " + str(len(file_list))
        print "Total success: " + str(success_size)
        print "Total error: " + str(error_size)
        print "Total error files: " + str(error_files)


    # Find all Types
    @staticmethod
    def find_types(input_path):

        # ['MatchList', 'Text', 'Decimal', 'Object', 'Dollar', 'Dollar4', 
        # 'Datetime', 'Rate6', 'Rate', 'Boolean', 'Rate3', 'Rate2', 'Time', 
        # 'Date', 'Integer', 'DateTime', 'TextBox', 'ObjectList']


        file_list = glob.glob(input_path + "*.xml")

        type_set = set()

        for file in file_list:
            # print "Proceessing" + file + "..."

            try: 
                dmo = ET.parse(file)
                root = dmo.getroot()
                tags = root.findall("Tag");

                for tag in tags:
                    tag_type = tag.get('Type')
                    # if tag_type is not None:
                    if tag_type == 'ObjectList':
                        print file
                        type_set.add(tag_type.strip())
            except Exception as e:
                print "Error in " + file
                print e
                continue

        print str(type_set)



# Bo: test code
if __name__=='__main__':

    input_path = ""
    output_path = ""
        
    XSLTJSONParser.bash_test(input_path, output_path)

    # XSLTJSONParser.find_types(input_path)