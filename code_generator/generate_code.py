import sys

sys.path.append('../')
from config import config
from utilities.config_util import ConfigUtil
from utilities import port_scanner, edm_utils
from code_generator.template_utils import *
from database_manager.setup import DBUtilities
from utilities.file_op import fileOps

from uml_parser.JSONParser import JSONParser
from uml_parser.UMLViewer import *
from code_generator.ApiGenerator import ApiGenerator


def get_server_info():
    # display_ip = "34.223.218.62" # Local env 127.0.0.0 Prev 18.216.141.169
    # server_ip = "0.0.0.0" # Local env - 127.0.0.0
    # port = port_scanner.runPortScan(2000, 6000)

    config_util = ConfigUtil()
    display_ip = config_util.get('IP', 'display_ip')
    server_ip = config_util.get('IP', 'server_ip')
    from_port = config_util.getInt('Port', 'from_port')
    to_port = config_util.getInt('Port', 'to_port')

    port = port_scanner.runPortScan(from_port, to_port)
    return str(display_ip), str(server_ip), str(port)


def configure_db(db_name):
    dbutils = DBUtilities()
    dbutils.setup(configDictionary={"host": "127.0.0.1", "port": 27017})
    dbutils.createWithUser(db_name)


def generate_model(language, template_model, output_dir, to_file):
    """
    Creates the Model code file with a specific language
    :param language: the language name. eg: 'JavaScript'
    :param template_model: template model for a class, see class TemplateModel
    :param output_dir: the root output path
    :param to_file: whether to rewrite the file
    :return: data used for code display in web page
    """
    template = ModelTemplate(language, template_model.dm_name, template_model, output_dir)

    data = {"model": template_model.name,
            "name": template_model.name}
    strlists = {"attributes": template_model.attribute_names}
    template.render(tofile=to_file, reset=False, replace_words=data, replace_strlists=strlists)

    code_display_data = template.get_display_data()
    return code_display_data


def generate_adapter(language, server_ip, port, dm_name, output_dir, to_file):
    """
    Creates the adapter code file with a specific language
    :param language: the language name. eg: 'JavaScript'
    :param server_ip: the ip of the REST api server.
    :param port: the port of the REST api server.
    :param dm_name: the domain model name
    :param output_dir: the output path
    :param to_file: whether to rewrite the file
    :return: data used for code display in web page
    """
    template = AdapterTemplate(language, dm_name, output_dir)

    data = {"server_ip": server_ip,
            "port": port,
            "dm_name": dm_name}
    template.render(tofile=to_file, reset=False, replace_words=data)

    code_display_data = template.get_display_data()
    return code_display_data


""" This method creates the server file"""


def generate_server(server_ip, port, output_path, dm_name, json_data):
    """
    Creates the server code file for the REST services
    :param server_ip: the ip of the REST api server.
    :param port: the port of the REST api server.
    :param output_path: the output path
    :param dm_name: the domain model name
    :json_data: the domain model json structure
    """
    server_file = open("code_templates/" + "Server", "r")

    db_template_path = config.get('Output', 'instance_db_template') + "/"

    class_file = open(db_template_path+ "class_template", "r")
    db_schema_file = open(db_template_path+ "db_schema_template", "r")
    db_schema_array_file = open(db_template_path+ "db_schema_array_template", "r")
    db_schema_nested_file = open(db_template_path+ "db_schema_nested_template", "r")
    db_schema_nested_array_file = open(db_template_path+ "db_schema_nested_array_template", "r")
    db_connection_file = open(db_template_path+ "db_connection_template", "r")
    db_ops_file = open(db_template_path+ "db_ops_template", "r")
    db_schema_validation_file = open(db_template_path+ "db_schema_validation_template", "r")
    authen_file = open("code_templates/"+ "authen_template", "r")
    behavior_file = open("code_templates/"+ "behavior", "r")
    package_json_file = open("code_templates/"+ "package.json", "r")
    type_converter_file = open(db_template_path+ "typeConverter", "r")

    server_template = server_file.read()
    class_template = class_file.read()
    db_schema_template = db_schema_file.read()
    db_schema_array_template = db_schema_array_file.read()
    db_schema_nested_template = db_schema_nested_file.read()
    db_schema_nested_array_template = db_schema_nested_array_file.read()
    db_connection_template = db_connection_file.read()
    db_ops_template = db_ops_file.read()
    db_schema_validation_template = db_schema_validation_file.read()
    authen_template = authen_file.read()
    behavior_template = behavior_file.read()
    package_json_template = package_json_file.read()
    type_converter_template = type_converter_file.read()

    output_path = output_path + "/Server/"
    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    log_path = output_path + "/log/"
    if not os.path.isdir(log_path):
        os.makedirs(log_path)

    elements = None
    for model_name in json_data:
        elements = json_data[model_name].get("elements")
    # deliver template for each model
    elem_names = [str(element["elementName"]) for element in elements]
    data = {"server_ip": server_ip,
            "port": port,
            "db_name": dm_name,
            "collection_names": str(elem_names)}
    content = replace_words(server_template, data)
    server_code = fileOps.safe_open_w(output_path + "Server" + ".js")
    server_code.write(content)
    server_code.close()

    package_json = fileOps.safe_open_w(output_path + "package" + ".json")
    package_json.write(package_json_template)
    package_json.close()

    # generate entities
    jp = JSONParser(json_data, dm_name)

    def add_simple_attribute_schema(entity_name, attribute_names, attribute_schema, jp=jp):
        for attribute in jp.findEntityAttributes(entity_name):
            attribute_names.add(attribute['name'].encode('utf-8'))

            data = {
                "attribute": attribute['name'],
                "type": attribute['details']['type']
            }

            if "details" in attribute and attribute["details"].get("isArray", 'false') == 'true':
                content = replace_words(db_schema_array_template, data)
            else:
                content = replace_words(db_schema_template, data)
            attribute_schema.append(content)

    # For handling nested object
    def add_complex_attribute_schema(entity_name, attribute_names, attribute_schema, jp=jp):
        # Bo: TODO: the current format of complex attributes is different 
        #           between the stardard parser and the XLST parser.
        #           This piece of code supports XLST paser only
        #           For the standard parser, it just ignore the complex attributes via try...except
        try:
            for attribute in jp.findEntityNestedObjects(entity_name):
                object_name = attribute['elementName'].encode('utf-8')
                attribute_names.add(object_name)

                inner_jp = JSONParser(attribute)

                inner_attribute_names = set()
                inner_attribute_schema = []

                add_simple_attribute_schema(object_name, inner_attribute_names, inner_attribute_schema, inner_jp)
                add_complex_attribute_schema(object_name, inner_attribute_names, inner_attribute_schema, inner_jp)

                data = {
                    "nested_object_name": attribute['elementName'],
                    "nested_attributes": str(list(inner_attribute_names)),
                    "nested_object_schema": ',\n'.join(inner_attribute_schema)
                }

                if "details" in attribute and attribute["details"].get("isArray", 'false') == 'true':
                    content = replace_words(db_schema_nested_array_template, data)
                else:
                    content = replace_words(db_schema_nested_template, data)

                attribute_schema.append(content)
        except Exception as e:
            print "In standard parser, the complex attributes are not handled"
            pass

    # End for handling nested object

    for entity_id, entity_name in jp.entities().items():
        attribute_names = set()
        attribute_schema = []

        add_simple_attribute_schema(entity_name, attribute_names, attribute_schema, jp)
        add_complex_attribute_schema(entity_name, attribute_names, attribute_schema, jp)

        data = {
            "collection_name": entity_name
        }
        validator = replace_words(db_schema_validation_template, data)

        data = {
            "collection_name": entity_name,
            "attribute_names": str(list(attribute_names)),
            "attribute_schema": ',\n'.join(attribute_schema),
            "validator": validator
        }
        content = replace_words(class_template, data)
        output_location = output_path + entity_name + ".js"
        with fileOps.safe_open_w(output_location) as output_file:
            output_file.write(content)

    # generate behaviors
    for element in elements:
        for behavior in element["Behaviors"]:
            output_location = output_path + "Behaviors/" + str(behavior['name']) + ".js"
            data = {"entity": str(element["elementName"]),
                    "behavior": str(behavior['name'])
                    }
            content = replace_words(behavior_template, data)
            with fileOps.safe_open_w(output_location) as output_file:
                output_file.write(content)

    # generate server db connection file
    output_location = output_path + "db_connection" + ".js"
    configure_db(dm_name)
    db_user, db_password = edm_utils.generate_user_credentials(dm_name)
    data = {"db_user": db_user,
            "db_password": db_password,
            "db_name": dm_name}
    with fileOps.safe_open_w(output_location) as output_file:
        content = replace_words(db_connection_template, data)
        output_file.write(content)

    # generate server db dbOps file
    output_location = output_path + "dbOps" + ".js"
    with fileOps.safe_open_w(output_location) as output_file:
        output_file.write(db_ops_template)

    # generate server authentication file
    output_location = output_path + "authen" + ".js"
    with fileOps.safe_open_w(output_location) as output_file:
        output_file.write(authen_template)

    # generate type converter file
    output_location = output_path + "typeConverter" + ".js"
    with fileOps.safe_open_w(output_location) as output_file:
        output_file.write(type_converter_template)

    server_file.close()
    class_file.close()
    db_schema_file.close()
    db_schema_array_file.close()
    db_schema_nested_file.close()
    db_schema_nested_array_file.close()
    db_connection_file.close()
    db_ops_file.close()
    db_schema_validation_file.close()
    authen_file.close()
    behavior_file.close()
    type_converter_file.close()


""" This method creates the api reference page """


def generate_api_reference(server_ip, port, output_path, dm_name, json_data):
    gen = ApiGenerator()
    gen.set_basic_path(server_ip + ":" + port, dm_name)
    # gen.set_access_key('1234567890')
    # gen.set_user_name('danny')
    # parameter
    jp = JSONParser(json_data, dm_name)

    for entity_id, entity_name in jp.entities().items():
        gen.add_entity(entity_name, jp)

    gen.generate_file(output_path)


def generate_diagram(json_data, dm_name, output_path):
    jp = JSONParser(json_data, dm_name)
    viewer = UMLViewer()

    for entity_id, entity_name in jp.entities().items():
        viewer.add_entity(entity_name)

        for attribute in jp.findEntityAttributes(entity_name):
            viewer.add_attribute(entity_name, attribute['name'], attribute['details']['type'])

        for behavior in jp.findEntityBehaviors(entity_name):
            viewer.add_behavior(entity_name, behavior['name'])

    for entity_name, associations in jp.associations().items():
        for association in associations:
            start_entity = jp.findEntityNameById(association['start'])
            end_entity = jp.findEntityNameById(association['end'])
            asso = UMLAssociation(start_entity, end_entity, association['relationType'])
            if 'multiplicity' in association.keys():
                asso.set_multiplicity(association['multiplicity'])
            viewer.add_association(asso)

    viewer.generate_diagram(output_path)


def generate_all(dm_name, output_dir, to_file=True):
    """
    generate a set of code files from JSON
    :param dm_name: name of the domain model
    :param output_dir: the directory for code generation
    :param to_file: whether to rewrite the file
    :return: data used for code display in web page

    NOTE don't consider the case that a class model called "Adapter"
    """
    file_location = output_dir + "/" + dm_name + ".json"
    with open(file_location) as json_input:
        json_data = json.load(json_input)
        # print json.dumps(json_data, indent=2)
        display_ip, server_ip, port = get_server_info()
        print(display_ip + ":" + port)

        model_display_data = {}

        # generate adapter code files
        model_display_data["Adapter"] = {
            language: generate_adapter(language, server_ip, port, dm_name, output_dir, to_file)
            for language in TEMPLATE_LANGUAGES}

        # read all the class models from json_data
        template_models = TemplateModel.extract_models(json_data)
        # generate class model code files
        for template_model in template_models:
            model_display_data[template_model.name] = {
                language: generate_model(language, template_model, output_dir, to_file)
                for language in TEMPLATE_LANGUAGES}

        # generate server code files
        generate_server(str(server_ip), str(port), output_dir, dm_name, json_data)

        generate_api_reference(str(server_ip), str(port), output_dir + '/Server', dm_name, json_data)

        # generate UML diagram
        generate_diagram(json_data, dm_name, output_dir)

        # TODO
        # write model_display_data and display_ip to file

        return model_display_data, display_ip + ":" + str(port)
        # return model_display_data


def write_description_to_file(dm_name, output_dir, meta_data):
    file_location = output_dir + "/" + dm_name + "Modeldata" + ".json"
    md = json.dumps(meta_data)
    with fileOps.safe_open_w(file_location) as json_input:
        json_input.write(md)
    json_input.close()


def read_description_from_file(dm_name, file_path):
    file_location = file_path + "/" + dm_name + "Modeldata" + ".json"
    with open(file_location, 'r') as json_input:
        meta_data = json.load(json_input)
    return meta_data
