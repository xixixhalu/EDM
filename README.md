# EDMToolkit

**_Please remember to branch off and merge later, do not commit on master_**

## Basic Structure
-*main* : Contains the blueprint with main view functions and the Flask login manager object.

-*authentication* : Contains the authentication service that authorizes access to the REST API using a key associated with every user.

-*code_templates* : Contains the javascript templates for the Adapter, Method, Model and Server.

-*database_manager* : Creates the required database and collections in Mongo DB. Also creates a singleton PyMongo object for other modules to import.

-*generated\_code* : Contains the json file obtained after parsing the XML file and extracting necessary information. It also contains the js files generated from code_templates after the ```Submit``` button is clicked. These files are created at the following location -> generated_code/default/<domain_module_name>/.

-*input* : The input xml file gets stored here.

-*static* : Contains the scripts and CSS for the application. The JS folder contains the generated code.

-*templates* : This directory contains the Flask jinja templates.

-*to_delete* : This is a temporary directory to be deleted after complete testing. Unaccessed code is placed here.

-*uml_parser* : This is a parser module for the uploaded files.

-*utilities* : 
  - port_scanner : Contains the port scanner utility that looks for ports available on a machine, given the port range as input.
  - exceptions : Custom excetions can be added here.
  - edm_utils : Contains general custom utilities for the project.
  - config_util : This is a config utility to read properties from config.properties.
    Usage:
```python
      from utilities.config_util import ConfigUtil
      config = ConfigUtil()
      propertyVal = config.get(<section_name>, <property_name>)
```

## Naming convention:
- Please name all directories in small case. Seperate spaces with underscores.
	E.g. Generated code -> generated_code

- Please name all files in small case. Seperate spaces with underscores.
	E.g. launchServer.sh -> launch_server.sh

- Please name all classes in camel case.
	E.g. domain_model -> DomainModel

- Please name all methods in camel case with the FIRST letter small.
	E.g. ParseSimpleXML() -> parseSimpleXML()

## How to run:
- Clone the repository
- Navigate inside EDMToolkit
- **Before every execution, please run `sh clean_pycs.sh` on the root folder to clean all binaries**
- run the `sh trigger_script.sh <name_of_python_file_to_run>`. For example I run `sh trigger_script.sh tester.py` to run some tests on the code.
- Make sure that all the code in directories have a `__init.py__` file associated to make it an importable library.
- Update the following in config.properties based on your machine:
	- host : Your hostname (Set to 127.0.0.1 for running on your local machine).
	- port :  Port you want the application to run on.
	- display_ip : Your display IP (Set to 127.0.0.1 for running on your local machine).
	- server_ip : Your server IP(Set to 127.0.0.1 for running on your local machine or 0.0.0.0 for AWS instance).
	- from_port : Port number for port scanner to start with (E.g. 2000)
	- to_port : Port number for port scanner to end with (E.g. 6000)
- The `startup.py` file represents the entry point of the application. Run this file as `python startup.py`

