# Code Generator

A brief intro for the part of generating code files from the JSON data(output of the parser).

## Related structures/files

* /code_templates/ : Contains templates for code generating

+ /generated_code/ : All the generated codes will be saved to there
  - generated_code/ user name / model name / language name / ...

* /to_delete/template_tester.py : I used this file to test. Can just delete.

## Basic usage

Use
``generate_all(dm_name)``
to create all the files for a domain model.

<br>

Inside, we use our Template classes to handle the code generation.

Create template:

```
template = Template(language, template_type [,...])
```

If not specify *content* or *template_location*,
will read template file according to *language* and *template_type* as template's content.

<br>

Then render template content:
```
template.render(...)
```
Currently mainly just to replace words and strlists.

## Notes

1. Sometimes the functions involve encoding change for strings.
Current code usually just make everything str. Can be potential problems.

2. Due to the time limit and the abilities, some functions or structures can be inefficient or messy.
(eg. replace_words() uses str.replace() a lot).

3. Have not test the template files (and the output code files) carefully.
 May have bugs.

---

<p align="right">Ruobo</p>
<p align="right">2018.5.10</p>

