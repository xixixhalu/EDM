import sys
import json
sys.path.append('../')
from utilities.file_op import fileOps

class ApiGenerator:
    def __init__(self):
        self.__outjson = {}
        self.__dmname = ''
        self.__host = ''
        self.__accessKey = ''
        self.__user = ''

    '''
    Sample
    host: localhost:2000
    dmname: Generalization
    '''
    def set_basic_path(self, host, dmname):
        self.__host = host
        self.__dmname = dmname
        self.__json = self.__create_basic_template()

    def set_access_key(self, key):
        self.__accessKey = key

    def set_user_name(self, user):
        self.__user = user

    def add_entity(self, entity_name, attributes):
        self.__json['tags'].append({
            'name': entity_name,
            'description': 'Everything about ' + entity_name
        })
        self.__parse_entity(entity_name, attributes)

    def generate_file(self, path):
        with fileOps.safe_open_w(path + '/' + 'api.json') as o:
        # with open(path + '/' + 'openAPI.json', 'w') as o:
            json.dump(self.__json, o, indent=2)

    def __create_basic_template(self):
        api = {
	        'swagger': '2.0',	
        }
        api['info'] = {
            'version': '1.0.0',
            'title': self.__dmname + ' API Reference'
	    }
        api['schemes'] = ['http', 'https']
        api['host'] = self.__host
        api['basePath'] = '/' + self.__dmname
        api['tags'] = []
        # api details
        api['paths'] = {}
        # definition
        api['definitions'] = {}
        # definition
        api['parameters'] = {}

        return api

    '''
    use for building sample data structure
    '''
    def __define_object(self, object_name, obj):
        self.__json['definitions'][object_name] = obj

    # '''
    # use for building parameter data structure
    # '''
    # def __define_query(self, object_name, obj):
    #     self.__json['parameters'][object_name] = obj   

    def __parse_entity(self, entity_name, attributes):
        obj = ApiTemplate.initObject()
        if len(attributes) == 0:
            ApiTemplate.setAttribute(obj, ApiTemplate.entityPlaceholder())
            attribute_undefined = True
        else:
            for attribute in attributes:
                ApiTemplate.setAttribute(obj, attribute)
            attribute_undefined = False

        self.__define_object(entity_name, obj)
        self.__set_entity_apis(entity_name, attributes, attribute_undefined=attribute_undefined)


    def __set_entity_apis(self, entity_name, attributes, attribute_undefined=False):
        
        # Predefine path for _id
        path = {
            'name' : '_id',
            'details' : {
                'type' : 'objectId',
                'required' : True,
                'description' : '12-byte ObjectId value'
            }
        }
        # create data payload structure (sample)

        # ---- CREATE ----
        description = 'JSON body can be either an object or an array of objects'
        params = self.__gen_parameter(body=['#/definitions/' + entity_name], description=description)
        self.__add_entity_api(entity_name, 'Create One or Create Many', 'post', params, format='json')

        # ---- READ ----
        description = 'Optional'
        if not attribute_undefined:
            params = self.__gen_parameter(queries=attributes, description=description)
        else:
            params = []
        self.__add_entity_api(entity_name, 'Read All or Read Many By Attributes', 'get', params, format='json')

        description = ''
        params = self.__gen_parameter(path=[path], description=description)
        self.__add_entity_api(entity_name, 'Read One by Id', 'get', params, path=path)
 
        # ---- DELETE ----
        description = 'Optional'
        if not attribute_undefined:
            params = self.__gen_parameter(formData=attributes, description=description)
            self.__add_entity_api(entity_name, 'Detelte By Attributes', 'delete', params)

        description = ''
        params = self.__gen_parameter(path=[path], description=description)
        self.__add_entity_api(entity_name, 'Delete by Id', 'delete', params, path=path)

        # ---- UPDATE ----
        if not attribute_undefined:
            description = 'Optional'
            params = self.__gen_parameter(path=[path], formData=attributes, description=description)
            self.__add_entity_api(entity_name, 'Modify Entity', 'patch', params, path=path)

            for attr in attributes:
                attr['details']['required'] = True
            params = self.__gen_parameter(path=[path], formData=attributes, description=description)
            self.__add_entity_api(entity_name, 'Replace Entity', 'put', params, path=path)

        else:
            description = 'Optional'
            params = self.__gen_parameter(path=[path], body=['#/definitions/' + entity_name], description=description)
            self.__add_entity_api(entity_name, 'Modify Entity', 'patch', params, path=path, format='json')

        

    '''
    add_entity_api(Generalization, create, post, ...)
    '''

    def __gen_parameter(self, body=None, formData=None, path=None, queries=None, description=''):

        # def refAttribute(attribute=None, attrQueryMethod='body', required=True):
        #     param = {
        #         'in': attrQueryMethod,
        #         'name': 'body',
        #         'description': description,
        #         'required': required,
        #         'schema': {
        #             '$ref': attribute
        #         }
        #     }
        #     return param

        # def simpleAttribute(attribute=None, attrQueryMethod='query'):
        #     param = {
        #         'in': attrQueryMethod,
        #         'name': attribute.get('name', ''),
        #         'type': ApiTemplate.typeConvert(attribute['details'].get('type', 'string')),
        #         'description': attribute['details'].get('description', ''),
        #         'required': attribute['details'].get('required', False)
        #     }
        #     return param

        # def complexAttribute(attribute=None, attrQueryMethod='formData'):
        #     if len()
        #     param = {
        #         'in': attrQueryMethod,
        #         'name': 'body',
        #         'description': description,
        #         'required': False,
        #         'schema': {
        #             '$ref': ref
        #         }
        #     }
        #     return param
            # else:
            #     return simpleAttribute(attribute, attrQueryMethod)

        # type: ref, query, path, header, 'formData', body
        params = ApiTemplate.initQuery()

        if path:
            for attr in path:
                ApiTemplate.setParameter(params, attr, 'path', description=description)
        if body:
            for attr in body:
                ApiTemplate.setParameter(params, attr, 'body', description=description)
        if queries:
            for attr in queries:
                ApiTemplate.setParameter(params, attr, 'query', description=description)
        if formData:
            for attr in formData:
                ApiTemplate.setParameter(params, attr, 'formData', description=description)

        return params


    def __add_entity_api(self, entity_name, description, http_method, params, path=None, format='x-www-form-urlencoded'):
        if path:
            api_path = '/' + entity_name + '/{' + path['name'] + '}'
        else:
            api_path = '/' + entity_name + '/'

        if not self.__json['paths'].get(api_path):
            self.__json['paths'][api_path] = {}
        self.__json['paths'][api_path][http_method] = {
            'tags': [entity_name],
            'summary': description + ' for ' + entity_name,
            'consumes': ['application/' + format],
            'produces': ['application/json'],
            'responses': {
                '200': {
                    'description': entity_name + ': ' + description + ' successfully'
                }
            },
            'parameters': params
        }   


class ApiTemplate:

    # Define data model
    @staticmethod
    def entityPlaceholder():
        # create empty body for empty attrbutes case
        entityProperty = {
            'name': 'entityAttribute',
            'details': {
                'description': 'Can be any value - string, number, integer, boolean, array or object.',
                'type': 'unknown'
            }
        }
        return entityProperty

    @staticmethod
    def initObject():
        result = {
            'type': 'object',
            'properties' : {}
        }
        return result

    @staticmethod
    def setAttribute(obj, attribute):
        obj['properties'][attribute.get('name', 'unknown')] = {
            'type': ApiTemplate.typeConvert(attribute['details'].get('type')),
            'format': attribute['details'].get('type'),
            'example': ApiTemplate.typeExample(attribute['details'].get('type')),
            'description': attribute['details'].get('description', '')
        }

    @staticmethod
    def array(array, attributes, required=False):
        result = {}
        result[obj.get('name')] = {
            'type': ApiTemplate.typeConvert(obj['details'].get('type')),
            'description': obj['details'].get('description', ''),
            'required': obj['details'].get('required', required),
            'example': ApiTemplate.typeExample(ApiTemplate.typeConvert(attribute['details'].get('type'))),
            'schema': attributes
        }
        return result

    # End of define data model


    # Define parameter

    @staticmethod
    def initQuery():
        result = []
        return result

    @staticmethod
    def setParameter(qry, parameter, attrQueryMethod='query', required=False, description=''):
        if attrQueryMethod == 'body':
            param = {
                'in': attrQueryMethod,
                'name': 'body',
                'description': description,
                'required': required,
                'schema': {
                    '$ref': parameter
                }
            }
        else:
            param = {
                'in': attrQueryMethod,
                'name': parameter.get('name', 'unknown'),
                'description': parameter['details'].get('description', parameter['details'].get('type')),
                'required': parameter['details'].get('required', required),
                'schema': {
                    # 'example': ApiTemplate.typeExample(parameter['details'].get('type')),
                    'type': ApiTemplate.typeConvert(parameter['details'].get('type')),
                    'format': parameter['details'].get('type')
                }
            }
            if param['required']:
                param['schema']['example'] = ApiTemplate.typeExample(parameter['details'].get('type'))
        qry.append(param)
        


    # End of define parameter


    # Other definition helper

    @staticmethod
    def typeConvert(attr_type):
        type_switcher = {
            "string": "string",
            "date": "string",
            "datetime": "string",
            "time": "string",
            "byte": "string",
            "binary": "string",
            "decimal": "number",
            "float": "number",
            "double": "number",
            "int": "integer",
            "int32": "integer",
            "int64": "integer",
            "boolean": "boolean",
            "objectId": "string",
            "array": "array",
            "object": "object"
        }
        if not attr_type in type_switcher:
            result =  "string"
        else:
            result = type_switcher[attr_type]
        return result

    @staticmethod
    def typeExample(attr_type, formatExample={}):
        type_switcher = {
            "string": "attribute value",
            "date": "2018-12-25T00:00:00Z",
            "datetime": "2018-12-25T00:00:00Z",
            "time": "2018-12-25T00:00:00Z",
            "byte": "string",
            "binary": "string",
            "decimal": "3.1415926535",
            "float": "3.14",
            "double": "3.14159265",
            "int": "2",
            "int32": "32",
            "int64": "64",
            "boolean": True,
            "objectId": "5bda90261089fd3358f2e526",
            "array": [formatExample],
            "object": formatExample
        }
        if not attr_type in type_switcher:
            result =  "attribute value"
        else:
            result = type_switcher[attr_type]
        return result


if __name__ == '__main__':
    gen = ApiGenerator()
    gen.set_basic_path('localhost:2000', 'one_to_one')
    gen.set_access_key('1234567890')
    gen.set_user_name('danny')
    # parameter
    attr1 = [{
                'name': 'class1Attribute1',
                'details': {
                    'maxOccurs': 1,
                    'type': 'string',
                    'minOccurs': 1
                }
            },
            {
                'name': 'class1Attribute2',
                'details': {
                    'maxOccurs': 1,
                    'type': 'integer',
                    'minOccurs': 1
                }
            }]
    gen.add_entity('class1', attr1)
    attr2 = [{
                'name': 'class2Attribute1',
                'details': {
                    'maxOccurs': 1,
                    'type': 'integer',
                    'minOccurs': 1
                }
            }]
    gen.add_entity('class2', attr2)
    attr3 = []
    gen.add_entity('class3', attr3)
    gen.generate_file('./')