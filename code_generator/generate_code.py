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


def generate_model(language, template_model):
    """
    Creates the Model code file with a specific language
    :param language: the language name. eg: 'JavaScript'
    :param template_model: template model for a class, see class TemplateModel
    :return: data used for code display in web page
    """
    template = template_model.get_template(language)

    data = {"model": template_model.name,
            "name": template_model.name}
    strlists = {"attributes": template_model.attribute_names}
    template.render(tofile=True, reset=False, replace_words=data, replace_strlists=strlists)

    code_display_data = template.get_display_data()
    return code_display_data


def generate_adapter(language, server_ip, port, dm_name):
    """
    Creates the adapter code file with a specific language
    :param language: the language name. eg: 'JavaScript'
    :param server_ip: the ip of the REST api server.
    :param port: the port of the REST api server.
    :param dm_name: the domain model name
    :return: data used for code display in web page
    """
    template = AdapterTemplate(language, dm_name)

    data = {"server_ip": server_ip,
            "port": port}
    template.render(tofile=True, reset=False, replace_words=data)

    code_display_data = template.get_display_data()
    return code_display_data


# TODO need integration with new Server templates
def generate_server(server_ip, port, dm_name):
    """
    Creates the server code file for the REST services
    :param server_ip: the ip of the REST api server.
    :param port: the port of the REST api server.
    :param dm_name: the domain model name
    """
    configure_db(dm_name)
    db_user, db_password = edm_utils.generate_user_credentials(dm_name)

    template = ServerTemplate(dm_name)
    data = {"server_ip": server_ip,
            "port": port,
            "dbname": dm_name, 
            "db_user": db_user, 
            "db_password": db_password}
    template.render(tofile=True, reset=False, replace_words=data)


def generate_all(dm_name):
    """
    generate a set of code files from JSON
    :param dm_name: name of the domain model
    :return: data used for code display in web page

    NOTE don't consider the case that a class model called "Adapter"
    """
    file_location = "generated_code/default/" + dm_name + "/" + dm_name + ".json"
    with open(file_location) as json_input:
        json_data = json.load(json_input)
        display_ip, server_ip, port = get_server_info()
        print(display_ip + ":" + port)

        model_display_data = {}
        # generate adapter code files
        model_display_data["Adapter"] = {language: generate_adapter(language, server_ip, port, dm_name)
                                         for language in TEMPLATE_LANGUAGES}

        # read all the class models from json_data
        template_models = TemplateModel.extract_models(json_data)
        # generate class model code files
        for template_model in template_models:
            model_display_data[template_model.name] = {language: generate_model(language, template_model)
                                                       for language in TEMPLATE_LANGUAGES}

        # generate server code file
        generate_server(server_ip, port, dm_name)

        return model_display_data
