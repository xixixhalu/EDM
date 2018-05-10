from code_generator.generate_code import *
import jinja2

model_display_data = generate_all("generalization")

template = jinja2.Template('''
var codeDisplayData = {{model_display_data|tojson|safe}}

''')

s = template.render(model_display_data=model_display_data)

print s
