from code_generator.generate_code import *
from jinja2 import Template, Environment, FileSystemLoader

dis, model_display_data = generate_all("generalization")

template = Template('''
var codeDisplayData = {{model_display_data|tojson|safe}}

''')


s = template.render(model_display_data=model_display_data)

print s