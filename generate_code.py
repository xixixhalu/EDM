import json
from utilities.config_util import ConfigUtil
from utilities import port_scanner

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
def generate_model(json_data, template_filename, dm_name):

    element_names = {}
    # read the template file as text
    model_template_file = open("code_templates/" + template_filename, "r").read()

    for model_name in json_data:
        for element in json_data.get(model_name).get("elements"):
            template_file_elem = model_template_file
            elem_name = element.get("elementName")

            #  create a js file with name as elem_name
            file_name = elem_name + ".js"
            js_file = open("generated_code/default/" + dm_name + "/" + file_name, "w")

            # replace all $model with elem_name
            template_file_elem = template_file_elem.replace("$model", elem_name)
            template_file_elem = template_file_elem.replace("$name", "\"" + elem_name + "\"")

            # Reading attributes from json
            attribute_list = []
            attribute_str = ""
            for attribute in element.get("Attributes").get("Simple"):
                attribute_name = attribute.get("name")
                attribute_list.append(attribute_name)
                attribute_str += "\"" + attribute_name + "\" ,\n"
            attribute_str = attribute_str[:-2]

            element_names[elem_name] = attribute_list
            # replace $attributes with the attribute list
            template_file_elem = template_file_elem.replace("$attributes", attribute_str)

            #  TODO: Handling complex attributes

            # Adding methods
            template_method_file = open("code_templates/Method", "r").read()
            template_method_file = template_method_file.replace("$model", elem_name)
            final_str = ""
            for operation in element.get("Operations"):
                # replace $method with the method name
                all_methods = template_method_file.replace("$method", operation.get("name"))

                #  TODO: Handling method parameters
                all_methods = all_methods.replace("$parameters", " ")
                final_str += all_methods

            # write to file
            js_file.write(template_file_elem.replace("// $methods", final_str))

            #  closing resources
            js_file.close()

    return element_names


""" This method creates the adapter js file"""
def generate_adapter(adapter_filename, server_ip, port, dm_name):
    adapter_template_file = open("code_templates/"+adapter_filename, "r").read()
    adapter_template_file = adapter_template_file.replace("$server_ip", "\""+server_ip+"\"")
    adapter_template_file = adapter_template_file.replace("$port", "\""+port+"\"")
    adapter_code = open("generated_code/default/" + dm_name + "/Adapter.js", "w")
    adapter_code.write(adapter_template_file)
    adapter_code.close()


""" This method creates the server js file"""
def generate_server(server_filename, server_ip, port, dm_name):
    server_template_file = open("code_templates/"+server_filename, "r").read()
    server_template_file = server_template_file.replace("$server_ip", "\""+server_ip+"\"")
    server_template_file = server_template_file.replace("$port", "\""+port+"\"")
    server_template_file = server_template_file.replace("$dbname", "\""+dm_name+"\"")
    server_code = open("generated_code/default/" + dm_name + "/Server.js", "w")
    server_code.write(server_template_file)
    server_code.close()


def generate_all(db_name):
    # reading json data
    file_path = "generated_code/default/"+db_name+"/"
    with open(file_path + db_name + ".json") as json_input:
        data = json.load(json_input)
        display_ip, server_ip, port = get_server_info()
        element_names = generate_model(data, "Model", str(db_name))
        generate_adapter("Adapter", str(server_ip), str(port), str(db_name))
        generate_server("Server", str(server_ip), str(port), str(db_name))
        return element_names, display_ip + ":" +str(port)



