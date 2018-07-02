from utilities.config_util import ConfigUtil
from utilities import port_scanner, edm_utils
from code_generator.template_utils import *
from database_manager.setup import DBUtilities


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
    return str(display_ip), str(server_ip), str(port)


def configure_db(db_name):
    dbutils = DBUtilities()
    dbutils.setup(configDictionary={"host":"127.0.0.1","port":27017})
    dbutils.createWithUser(db_name)


def generate_model(language, template_model, output_dir, to_file):
    """
    Creates the Model code file with a specific language
    :param language: the language name. eg: 'JavaScript'
    :param template_model: template model for a class, see class TemplateModel
    :param output_dir: the output path
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
            "port": port}
    template.render(tofile=to_file, reset=False, replace_words=data)

    code_display_data = template.get_display_data()
    return code_display_data


""" This method creates the server js file"""
def generate_server(server_ip, port, output_path, dm_name, json_data):
    """
    Creates the server code file for the REST services
    :param server_ip: the ip of the REST api server.
    :param port: the port of the REST api server.
    :param output_path: the output path
    :param dm_name: the domain model name
    :json_data: the domain model json structure
    """

    server_template = open("code_templates/" + "Server", "r").read()
    class_template = open("code_templates/"+ "class_template", "r").read()
    db_connection_template = open("code_templates/"+ "db_connection_template", "r").read()
    db_ops_template = open("code_templates/"+ "db_ops_template", "r").read()
    authen_template = open("code_templates/"+ "authen_template", "r").read()

    output_path = output_path + "/Server/"
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    
    elements = None
    for model_name in json_data:
        elements = json_data[model_name].get("elements")
    # deliver template for each model
    elem_names = [str(element["elementName"]) for element in elements]
    data = {"server_ip": server_ip,
            "port": port,
            "db_name": dm_name,
            "collection_names" : str(elem_names)}
    content = replace_words(server_template, data)
    server_code = open(output_path + "Server" + ".js", "w")
    server_code.write(content)
    server_code.close()

    for elem_name in elem_names :
        output_location = output_path + elem_name + ".js"
        with open(output_location, "w") as output_file:
            output_file.write(class_template)

    # generate server db connection file
    output_location = output_path + "db_connection" + ".js"
    configure_db(dm_name)
    db_user, db_password = edm_utils.generate_user_credentials(dm_name)
    data = {"db_user": db_user, 
            "db_password": db_password,
            "db_name" : dm_name}
    with open(output_location, "w") as output_file:
        content = replace_words(db_connection_template, data)
        output_file.write(content)

    # generate server db dbOps file
    output_location = output_path + "dbOps" + ".js"
    with open(output_location, "w") as output_file:
        output_file.write(db_ops_template)

    # generate server authentication file
    output_location = output_path + "authen" + ".js"
    with open(output_location, "w") as output_file:
        output_file.write(authen_template)

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
        #print json.dumps(json_data, indent=2)
        display_ip, server_ip, port = get_server_info()
        print(display_ip + ":" + port)

        model_display_data = {}

        # generate adapter code files
        model_display_data["Adapter"] = {language: generate_adapter(language, server_ip, port, dm_name, output_dir, to_file)
                                         for language in TEMPLATE_LANGUAGES}

        # read all the class models from json_data
        template_models = TemplateModel.extract_models(json_data)
        # generate class model code files
        for template_model in template_models:
            model_display_data[template_model.name] = {language: generate_model(language, template_model, output_dir, to_file)
                                                       for language in TEMPLATE_LANGUAGES}


        # generate server code files
        generate_server(str(server_ip), str(port), output_dir, dm_name, json_data)

        return model_display_data, display_ip + ":" + str(port)
        #return model_display_data