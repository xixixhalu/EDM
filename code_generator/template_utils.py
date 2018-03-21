import re

TEMPLATE_PREFIX = "$"
TEMPLATE_FUNC_MARK = "\$FUNC"
TEMPLATE_FUNC_END_MARK = "\$ENDFUNC"

TEMPLATE_LANGUAGES = ["JavaScript", "Java"]

TEMPLATE_PATH = {"Java": "code_templates/java/",
                 "JavaScript": "code_templates/javascript/"}
LANGUAGE_SUFFIX = {"Java": ".java",
                   "JavaScript": ".js"}

# not used yet
JAVA_TYPE_MAP = {"Integer": "int"}
JAVASCRIPT_TYPE_MAP = {}
LANGUAGE_TYPE_MAP = {"Java": JAVA_TYPE_MAP,
                     "JavaScript": JAVASCRIPT_TYPE_MAP}


def template_output_path(dm_name, language, username = "default"):
    return "generated_code/%s/%s/%s/" % (username, dm_name, language)


# XXX need simplify
def get_examples(func_name, attribute_list):
    if len(attribute_list) == 0:
        return []
    examples = []
    attr1_name = attribute_list[0]["name"].encode("utf-8")
    attr1_type = attribute_list[0]["type"].encode("utf-8")
    if func_name == "create":
        example_one = {attr1_name: "some value (" + attr1_type + ")"}
        example_many = [{attr1_name: "some value (" + attr1_type + ")"},
                        {attr1_name: "some other value (" + attr1_type + ")"}]
        examples = [str(example_one), str(example_many)]
    elif func_name == "read" or func_name == "readOne":
        example_id = {"_id": "specific id (String)"}
        example_attr = {attr1_name: "some value (" + attr1_type + ")"}
        examples = [str(example_id), str(example_attr)]
    elif func_name == "readMany":
        example_attr = {attr1_name: "some value (" + attr1_type + ")"}
        examples = [str(example_attr)]
    elif func_name == "update":
        example_update1 = {"oldData": {"_id": "specific id (String)"},
                           "newData": {attr1_name: "some value (" + attr1_type + ")"}}
        example_update2 = {"oldData": {attr1_name: "some value (" + attr1_type + ")"},
                           "newData": {attr1_name: "some other value (" + attr1_type + ")"}}
        examples = [str(example_update1), str(example_update2)]
    elif func_name == "delete":
        example_id = {"_id": "specific id (String)"}
        example_attr = {attr1_name: "some value (" + attr1_type + ")"}
        examples = [str(example_id), str(example_attr)]
    return examples


def extract_funcs_info(template_content, attribute_list):
    pattern = TEMPLATE_FUNC_MARK + ''' (\S+)\s*(\{.*?\})?(.*?)''' + TEMPLATE_FUNC_END_MARK
    content = template_content
    func_info_list = []
    func_content_list = re.findall(pattern, content, re.S)
    for func_name, func_annotation, func_body in func_content_list:
        if len(func_annotation) > 1:
            func_annotation = func_annotation[1:-1]

        func_info_list.append({"name": func_name,
                               "annotation": func_annotation,
                               "body": func_body,
                               "examples": get_examples(func_name, attribute_list)})
    content = re.sub(TEMPLATE_FUNC_MARK + " (\S+)\s*(\{.*?\})?", "", content, 0, re.S)
    content = re.sub(TEMPLATE_FUNC_END_MARK + "\s?", "", content)
    return content, func_info_list


def list2template_str(name_list):
    result_str = ""
    for name in name_list:
        print name
        result_str += "\"" + name + "\", "
    result_str = result_str[:-2]
    return result_str


def replace_strlist(template_content, keyword, name_list):
    list_str = ""
    for name in name_list:
        print name
        list_str += "\"" + name + "\", "
    list_str = list_str[:-2]
    content = template_content.replace(TEMPLATE_PREFIX + keyword, list_str)
    return content


def replace_words(template_content, replacements):
    content = template_content
    for key in replacements:
        replacement = replacements[key]
        content = content.replace(TEMPLATE_PREFIX + key, replacement)
    return content




# for test
'''def generate_template(ori_filename, simple_variables, replacements, output_filename):
    file_content = open(ori_filename, "r").read()
    for variable_name in simple_variables:
        file_content = file_content.replace(variable_name, TEMPLATE_PREFIX + variable_name)
    for ori_name in replacements:
        replacement = replacements[ori_name]
        file_content = file_content.replace(ori_name, replacement)
    output_file = open(output_filename, "w")
    output_file.write(file_content)
    output_file.close()'''

'''
def extract_model_data(json_data):
    model_data = {}
    for model_name in json_data:
        for element in json_data.get(model_name).get("elements"):
            elem_name = element.get("elementName")
            element_attrs = element.get("Attributes").get("Simple")
            attribute_list = [{"name": attribute["name"],
                               "type": attribute["details"]["type"]}
                              for attribute in element_attrs]
            model_data[elem_name] = attribute_list
        #for operation in json_data.get(model_name).get("Operations"):
            #operation_name = operation["name"]
    return model_data
'''