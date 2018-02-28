TEMPLATE_PREFIX = "$"

def list2template_str(name_list):
    result_str = ""
    for name in name_list:
        print name
        result_str += "\"" + name + "\" ,\n"
    result_str = result_str[:-2]
    return result_str


def generate_code(template_content, replacements):
    content = template_content
    for key in replacements:
        replacement = replacements[key]
        if isinstance(replacement,list):
            replacement = list2template_str(replacement)
        content = content.replace(TEMPLATE_PREFIX+key, replacement)
    return content

# for test
def generate_template(ori_filename, simple_variables, replacements, output_filename):
    file_content = open(ori_filename, "r").read()
    for variable_name in simple_variables:
        file_content = file_content.replace(variable_name, TEMPLATE_PREFIX+variable_name)
    for ori_name in replacements:
        replacement = replacements[ori_name]
        file_content = file_content.replace(ori_name, replacement)
    output_file = open(output_filename, "w")
    output_file.write(file_content)
    output_file.close()