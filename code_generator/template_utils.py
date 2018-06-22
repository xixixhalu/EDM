import re
import json
import os

TEMPLATE_PREFIX = "$"
TEMPLATE_FUNC_MARK = "\$FUNC"
TEMPLATE_FUNC_END_MARK = "\$ENDFUNC"

TEMPLATE_LANGUAGES = ["JavaScript", "Java", "Swift"]

TEMPLATE_PATH = {"Java": "code_templates/java/",
                 "JavaScript": "code_templates/javascript/",
                 "Swift": "code_templates/swift/"}
LANGUAGE_SUFFIX = {"Java": ".java",
                   "JavaScript": ".js",
                   "Swift": ".swift"}

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

def template_output_path(dm_name, language=None, username="default"):
    if language:
        return "generated_code/%s/%s/%s/" % (username, dm_name, language)
    return "generated_code/%s/%s/" % (username, dm_name)


def remove_indent(func_str):
    """
    remove the indents for a string block
    eg. func_str: "
        func a {
            i=1
        }"
    return: "
    func a {
        i=1
    }"
    """
    func_strs = func_str.split("\n")
    indent = 1000
    for line in func_strs:
        if len(line) == 0:
            continue
        match_obj = re.match(" +", line)
        if not match_obj:
            return func_str
        if match_obj.span()[1] < indent:
            indent = match_obj.span()[1]

    func_strs = [func_str[indent:] for func_str in func_strs]
    return "\n".join(func_strs)


class TemplateModel(dict):
    """
    This class is used to store a model's data which is needed in creating model code file

    should only be created by TemplateModel.extract_models()

    current structure:
    {
        "dm_name": String,
        "name": String,
        "attributes": [{"name": String, "type": String}, ...],
        "methods": [String, ...]
    }
    """
    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)

    def __getattr__(self, item):
        return self.get(item, None)

    def __setattr__(self, attr, value):
        self[attr] = value

    @property
    def attribute_names(self):
        return [attr["name"] for attr in self.attributes]

    @staticmethod
    def extract_models(json_data):
        template_models = []
        dm_name = json_data.keys()[0]
        elements = json_data[dm_name].get("elements")
        for element in elements:
            elem_name = element.get("elementName")

            element_attrs = element.get("Attributes").get("Simple")
            attribute_list = [{"name": attribute["name"],
                               "type": attribute["details"]["type"]}
                              for attribute in element_attrs]

            # NOTE haven't test "Operations" part
            method_names = element["Operations"]
            data = {"dm_name": dm_name,
                    "name": elem_name,
                    "attributes": attribute_list,
                    "methods": method_names
                    }
            template_models.append(TemplateModel(**data))
        return template_models

    def get_template(self, language):
        return ModelTemplate(language, self.dm_name, self)

    def output(self):
        for language in TEMPLATE_LANGUAGES:
            self.get_template(language).output()


class TemplateMethod:
    """
    This class is used to store a method's info which is needed in code display data

    should only be created by Template.extract_methods()
    """
    def __init__(self, language, name, annotation, content, model=None):
        self.name = name
        self.content = remove_indent(content)
        self.language = language
        self.annotation = annotation
        self.model = model

    LANGUAGE_CALLFORM = {"Java": "%s.%s(%s);",
                         "JavaScript": "%s.%s(%s, success(function), error(function))",
                         "Swift": "%s.%s(%s)"}

    @staticmethod
    def get_example_callform(example, language, model_name, method_name):
        if isinstance(example, list) and len(example) > 0:
            example_str = ""
            for sub_example in example:
                example_str += sub_example + ", "
            example = example_str[:-2]
        return (TemplateMethod.LANGUAGE_CALLFORM[language] % (model_name, method_name, example)).encode("utf-8")

    @staticmethod
    # XXX need simplify
    def get_examples(func_name, attribute_list):
        if len(attribute_list) == 0:
            return []
        examples = []
        attr1_name = attribute_list[0]["name"].encode("utf-8")
        attr1_type = attribute_list[0]["type"].encode("utf-8")
        if func_name == "createOne":
            example_one = {attr1_name: "some value (" + attr1_type + ")"}
            examples = [str(example_one)]
        elif func_name == "createMany":
            example_many = [{attr1_name: "some value (" + attr1_type + ")"},
                            {attr1_name: "some other value (" + attr1_type + ")"}]
            examples = [str(example_many)]
        elif func_name == "readOne":
            example_id = {"_id": "specific id (String)"}
            example_attr = {attr1_name: "some value (" + attr1_type + ")"}
            examples = [str(example_id), str(example_attr)]
        elif func_name == "readMany":
            example_attr = {attr1_name: "some value (" + attr1_type + ")"}
            examples = [str(example_attr)]
        elif func_name == "update":
            example_update1 = ["{'_id': 'specific id (String)'}(search data)",
                               "{'%s': 'some value (%s)'}(update data)" % (attr1_name, attr1_type)]
            example_update2 = ["{'%s': 'some value (%s)'}(search data)" % (attr1_name, attr1_type),
                               "{'%s': 'some other value (%s)'}(update data)" % (attr1_name, attr1_type)]
            examples = [example_update1, example_update2]
        elif func_name == "delete":
            example_id = {"_id": "specific id (String)"}
            example_attr = {attr1_name: "some value (" + attr1_type + ")"}
            examples = [str(example_id), str(example_attr)]
        return examples

    def get_example(self, callform=False):
        if not self.model:
            return []
        examples = TemplateMethod.get_examples(self.name, self.model.attributes)
        if callform:
            return [TemplateMethod.get_example_callform(example, self.language, self.model.name, self.name)
                    for example in examples]
        return examples

    def get_method_info(self):
        example_callforms = self.get_example(True)
        return {"name": self.name,
                "annotation": self.annotation,
                "body": self.content,
                "examples": example_callforms}


class Template:
    """
    General template class

    """
    def __init__(self, language, template_type, dm_name=None, name=None, template_location=None, content=None):
        self.language = language
        self.type = template_type
        self.dm_name = dm_name
        self.name = name
        self.methods = None

        if content:
            self.content = self.raw_content = content
        else:
            template_location = template_location or (TEMPLATE_PATH[language] + template_type + LANGUAGE_SUFFIX[language])
            with open(template_location, "r") as template_file:
                self.content = self.raw_content = template_file.read()

    def __str__(self):
        return self.content

    @property
    def output_path(self):
        return template_output_path(self.dm_name, self.language)

    @property
    def output_location(self):
        return self.output_path + self.name + LANGUAGE_SUFFIX[self.language]

    def remove_func_marks(self):
        """
        remove "$FUNC" and "$ENDFUNC" marks
        """
        self.content = re.sub(TEMPLATE_FUNC_MARK + " (\S+)\s*(\{.*?\})?", "", self.content, 0, re.S)
        self.content = re.sub(TEMPLATE_FUNC_END_MARK + "\s?", "", self.content)

    def extract_methods(self):
        """
        extract methods info surrounded by "$FUNC" and "$ENDFUNC" and remove the marks
        """
        language = self.language
        pattern = TEMPLATE_FUNC_MARK + ''' (\S+)\s*\n(\{.*?\}\n)?(.*?)\n\s*''' + TEMPLATE_FUNC_END_MARK
        methods = []
        method_contents = re.findall(pattern, self.content, re.S)
        for method_name, method_annotation, method_body in method_contents:
            method_annotation = method_annotation[1:-2] if len(method_annotation) > 2 else ""

            methods.append(TemplateMethod(language, name=method_name,
                                          annotation=method_annotation, content=method_body))
        self.remove_func_marks()
        self.methods = methods
        return methods

    def replace_words(self, replacements):
        for key, replacement in replacements.items():
            self.content = self.content.replace(TEMPLATE_PREFIX + key, replacement)

    def replace_strlists(self, replacements):
        for key, name_list in replacements.items():
            list_str = json.dumps(name_list)
            list_str = list_str[1:-1]
            self.content = self.content.replace(TEMPLATE_PREFIX + key, list_str)

    def output(self):
        if not os.path.isdir(self.output_path):
            os.makedirs(self.output_path)
        with open(self.output_location, "w") as output_file:
            output_file.write(self.content)

    def render(self, tofile=True, reset=False, replace_words=None, replace_strlists=None):
        if replace_words:
            self.replace_words(replace_words)
        if replace_strlists:
            self.replace_strlists(replace_strlists)
        if tofile:
            self.output()
        if reset:
            content = self.content
            self.content = self.raw_content
            return content
        return self.content


class ModelTemplate(Template):
    """
    Template class for Model code file

    just implement the code display data for class model and handle "$method" mark
    """
    def __init__(self, language, dm_name, model):
        Template.__init__(self, language, "Model", dm_name, model.name)
        self.model = model
        self.replace_methods()
        self.raw_content = self.content

    # XXX need test and extend
    def replace_methods(self):
        """
        find "$method" mark in template and replace with methods code according to model's info
        """
        method_names = self.model.methods
        template = Template(self.language, "Method")
        method_content = [template.render(False, True, replace_words={"method": method_name, "parameters": ""})
                          for method_name in method_names]
        method_content = "".join(method_content)
        self.replace_words({"methods": method_content})

    def extract_methods(self):
        Template.extract_methods(self)
        for method in self.methods:
            method.model = self.model

    def get_display_data(self):
        func_info_list = [method.get_method_info() for method in self.methods]
        return {"func_info_list": func_info_list,
                "attribute_list": [],
                "file_uri": self.output_location}

    def render(self, tofile=True, reset=False, replace_words=None, replace_strlists=None):
        Template.render(self, False, False, replace_words, replace_strlists)
        self.extract_methods()
        Template.render(self, tofile, reset)


class AdapterTemplate(Template):
    """
    Template class for Adapter code file

    not much different from basic template but just implement the code display data for Adapter
    """
    def __init__(self, language, dm_name):
        Template.__init__(self, language, "Adapter", dm_name, "Adapter")

    def get_display_data(self):
        func_info_list = [method.get_method_info() for method in self.methods]
        return {"func_info_list": func_info_list,
                "attribute_list": [],
                "file_uri": self.output_location}

    def render(self, tofile=True, reset=False, replace_words=None, replace_strlists=None):
        Template.render(self, False, False, replace_words, replace_strlists)
        self.extract_methods()
        Template.render(self, tofile, reset)


# Legacy class
class ServerTemplate(Template):
    """
    Template class for Server code file

    not much different from basic template but just specify file path
    """
    def __init__(self, dm_name):
        template_location = "code_templates/Server"
        Template.__init__(self, "JavaScript", "Server", dm_name, "Server", template_location=template_location)

    @property
    def output_path(self):
        return template_output_path(self.dm_name)
