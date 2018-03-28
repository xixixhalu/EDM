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



def generate_model(language, json_data, dm_name):
    """
    This method parses json input and replaces the
    respective values in the template and generates the target model file

    :param language: the language name. eg: 'JavaScript'
    :param json_data: a dict contains json data from xml_parser.
    :param dm_name: the domain model name

    :return code_display_data: a dict contains data will be used in code display page
    """

    template_location = TEMPLATE_PATH[language] + "Model" + LANGUAGE_SUFFIX[language]
    output_path = template_output_path(dm_name, language)

    with open(template_location, "r") as template_file:
        model_template = template_file.read()

    method_template_location = TEMPLATE_PATH[language] + "Method" + LANGUAGE_SUFFIX[language]
    with open(method_template_location, "r") as template_file:
        method_template = template_file.read()

    elements = None
    for model_name in json_data:
        elements = json_data[model_name].get("elements")

    # deliver template for each model
    code_display_data = {}
    for element in elements:
        # read info form json data
        elem_name = element.get("elementName")

        element_attrs = element.get("Attributes").get("Simple")
        attribute_list = [{"name": attribute["name"],
                           "type": attribute["details"]["type"]}
                          for attribute in element_attrs]
        attribute_names = [attrs["name"] for attrs in attribute_list]

        content = model_template

        # add methods
        # XXX need test and more functions
        method_names = element["Operations"]
        method_content = ""
        for method_name in method_names:
            method_content += replace_words(method_template, {"method": method_name,
                                                              "parameters": ""})
        content = replace_words(content, {"methods": method_content})

        # replace variables
        data = {"model": elem_name,
                "name": elem_name}
        content = replace_words(content, data)
        content = replace_strlist(content, "attributes", attribute_names)

        # extract func info and remove func marks
        content, func_info_list = extract_funcs_info(content, attribute_list)
        code_display_data[elem_name] = {"attribute_list": attribute_list,
                                        "func_info_list": func_info_list}

        # create final file
        output_location = output_path + elem_name + LANGUAGE_SUFFIX[language]
        with open(output_location, "w") as output_file:
            output_file.write(content)

    return code_display_data



def generate_adapter(language, server_ip, port, dm_name):
    """
    This method creates the adapter script file from the template

    :param language: the language name. eg: 'JavaScript'
    :param server_ip: the ip of the restful api server.
    :param port: the port of the restful api server.
    :param dm_name: the domain model name
    """
    template_location = TEMPLATE_PATH[language] + "Adapter" + LANGUAGE_SUFFIX[language]
    output_path = template_output_path(dm_name, language)
    output_location = output_path + "Adapter" + LANGUAGE_SUFFIX[language]

    with open(template_location, "r") as template_file:
        adapter_template = template_file.read()

    data = {"server_ip": server_ip,
            "port": port}
    content = replace_words(adapter_template, data)

    content, func_info_list = extract_funcs_info(content, [])

    with open(output_location, "w") as output_file:
        output_file.write(content)
    return func_info_list


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

        # create files for each language
        model_display_data = {"Adapter":{}}
        temp_display_data = {}
        for language in TEMPLATE_LANGUAGES:
            output_path = template_output_path(db_name, language)
            if not os.path.isdir(output_path):
                os.makedirs(output_path)
            model_display_data["Adapter"][language] = {}
            model_display_data["Adapter"][language]["func_info_list"] = generate_adapter(language, str(server_ip), str(port), str(db_name))
            temp_display_data[language] = generate_model(language, json_data, str(db_name))

        # TODO need update
        generate_server("Server", str(server_ip), str(port), str(db_name))

        # structure adjustment for model_display_data
        # temporary solution, may change later
        # [language][model] ==> [model][language]

        for language in temp_display_data:
            for model in temp_display_data[language]:
                model_display_data.setdefault(model, {})[language] = {
                    "func_info_list": temp_display_data[language][model]["func_info_list"],
                    "attribute_list": temp_display_data[language][model]["attribute_list"]
                }

        for model in model_display_data:
            if model != "Adapter":
                model_display_data[model]["attribute_list"] = temp_display_data["JavaScript"][model]["attribute_list"]

        return display_ip + ":" + str(port), model_display_data
