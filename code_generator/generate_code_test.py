import json

import os

from utilities.config_util import ConfigUtil
from utilities import port_scanner
from code_generator.template_utils import *


def get_server_info():
    # display_ip = "34.223.218.62" # Local env 127.0.0.0 Prev 18.216.141.169
    # server_ip = "0.0.0.0" # Local env - 127.0.0.0
    # port = port_scanner.runPortScan(2000, 6000)

    config = ConfigUtil()
    display_ip = config.get('IP', 'display_ip')
    server_ip = config.get('IP', 'server_ip')
    from_port = config.getInt('Port', 'from_port')
    to_port = config.getInt('Port', 'to_port')

    port = port_scanner.runPortScan(from_port, to_port)
    return display_ip, server_ip, port


"""This method parses json input and replaces the
respective values in the template and generates the js file """
def generate_model(language, template_location, output_path, json_data, dm_name):
    # read the template file as text
    with open(template_location, "r") as template_file:
        model_template = template_file.read()

    # extract model data
    model_data = {}
    for model_name in json_data:
        for element in json_data.get(model_name).get("elements"):
            elem_name = element.get("elementName")
            element_attrs = element.get("Attributes").get("Simple")
            attribute_list = [{"name": attribute["name"],
                               "type": attribute["details"]["type"]}
                              for attribute in element_attrs]
            model_data[elem_name] = attribute_list

    model_showing_data = {}

    # tender template for each model
    for elem_name in model_data:
        '''RUOBO: Method template currently not used'''
        final_str = ""
        data = {"model": elem_name,
                "name": elem_name,
                "methods": final_str}
        attribute_list = model_data[elem_name]
        attribute_names = [attrs["name"] for attrs in attribute_list]

        content = model_template
        content = replace_words(content, data)
        content = replace_strlist(content, "attributes", attribute_names)

        content, func_info_list = extract_funcs_info(content, attribute_list)
        model_showing_data[elem_name] = {"attribute_list": attribute_list,
                                         "func_info_list": func_info_list}

        language_suffix = LANGUAGE_SUFFIX[language]
        output_location = output_path + elem_name + language_suffix
        with open(output_location, "w") as output_file:
            output_file.write(content)
    return model_showing_data



""" This method creates the adapter js file"""
def generate_adapter(language, template_location, output_path, server_ip, port, dm_name):
    language_suffix = LANGUAGE_SUFFIX[language]
    output_location = output_path + "Adapter" + language_suffix

    with open(template_location, "r") as template_file:
        adapter_template = template_file.read()

    data = {"server_ip": server_ip,
            "port": port}
    content = replace_words(adapter_template, data)

    with open(output_location, "w") as output_file:
        output_file.write(content)


def generate_javascript(json_data, server_ip, port, dm_name):
    template_path = TEMPLATE_PATH["JavaScript"]
    output_path = "generated_code/default/" + dm_name + "/JavaScript/"

    adapter_template_location = template_path + "Adapter"
    model_template_location = template_path + "Model"

    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    generate_adapter("JavaScript", adapter_template_location, output_path, server_ip, port, dm_name)
    model_showing_data = generate_model("JavaScript", model_template_location, output_path, json_data, dm_name)
    return model_showing_data

def generate_java(json_data, server_ip, port, dm_name):
    template_path = TEMPLATE_PATH["Java"]
    output_path = "generated_code/default/" + dm_name + "/Java/"

    adapter_template_location = template_path + "Adapter.java"
    model_template_location = template_path + "ModelClass.java"

    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    generate_adapter("Java", adapter_template_location, output_path, server_ip, port, dm_name)
    model_showing_data = generate_model("Java", model_template_location, output_path, json_data, dm_name)
    return model_showing_data

""" This method creates the server js file"""
def generate_server(server_filename, server_ip, port, dm_name):
    server_template_file = open("code_templates/"+server_filename, "r").read()

    data = {"server_ip": server_ip,
            "port": port,
            "dbname": dm_name}
    content = replace_words(server_template_file, data)
    server_code = open("generated_code/default/" + dm_name + "/Server.js", "w")
    server_code.write(content)
    server_code.close()


def generate_all(db_name):
    # reading json data
    file_path = "generated_code/default/"+db_name+"/"

    with open(file_path + db_name + ".json") as json_input:
        json_data = json.load(json_input)
        display_ip, server_ip, port = get_server_info()

        element_names = {}
        for model_name in json_data:
            for element in json_data.get(model_name).get("elements"):
                elem_name = element.get("elementName")
                element_attrs = element.get("Attributes").get("Simple")
                element_names[elem_name] = [attribute["name"] for attribute in element_attrs]

        showing_data = {}

        showing_data["JavaScript"] = generate_javascript(json_data, str(server_ip), str(port), str(db_name))
        showing_data["Java"] = generate_java(json_data, str(server_ip), str(port), str(db_name))

        generate_server("Server", str(server_ip), str(port), str(db_name))

        return element_names, display_ip + ":" +str(port)

generate_all("generalization")