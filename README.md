# EDMToolkit

**_Please remember to branch off and merge later, do not commit on master_**

## Basic Structure
- *Authentication* : Contains the authentication service that authorizes access to the REST API using a key associated with every user
- *Backend* : All the functionalities that execute once the file has been uploaded to server
  - Parser : Parser module for the uploaded files
  - Errors : Custom error modules
  - Database Setup : Creates the required database and collections in Mongo DB
- *GeneratedCode* : Contains the json file obtained after parsing the XML file and extracting necessary information
- *Input* : The input xml file gets stored here
- *Utilities* : Contains the port scanner utility that looks for ports available on a machine, given the port range as input
- *code_templates* : Contains the javascript templates for the Adapter, Method, Model and Server
- *static* - Conatains the scripts and CSS for the application. The JS folder contains the generated code after the ```Submit``` button is clicked
- *templates* - This directory contains the Flask jinja templates

## How to run:
- Clone the repository
- Navigate inside EDMToolkit
- **Before every execution, please run `sh clean_pycs.sh` on the root folder to clean all binaries**
- run the `sh trigger_script.sh <name_of_python_file_to_run>`. For example I run `sh trigger_script.sh Backend/tester.py` to run some tests on the backend code.
- Make sure that all the code in the Backend has a `__init.py__` file associated to make it a importable library.
- The `FirstPage.py` file represents the entrypoint of the application. Run this file as `python FirstPage.py`

