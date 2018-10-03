import sys
import json
sys.path.append('../')
# from utilities.file_op import fileOps
from ApiGenerator import *

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

    def add_entity(self, entity_name):
        self.__json['tags'].append({
            'name': entity_name,
            'description': 'Everything about' + entity_name
        })
        self.__set_entity_apis(entity_name)

    def generate_file(self, path):
        # with fileOps.safe_open_w(path + 'openAPI.json', 'w') as o:
        with open(path + 'openAPI.json', 'w') as o:
            json.dump(self.__json, o)

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
        return api

    def __set_entity_apis(self, entity_name):
        # create data payload structure
        self.__define_object('SingleData', self.__gen_properties(entity_name, data_num=1)) 
        self.__define_object('SingleId', self.__gen_properties(entity_name, id_num=1))
        self.__define_object('MultiData', self.__gen_properties(entity_name, data_num=2))
        self.__define_object('UpdateById', self.__gen_properties(entity_name, id_num=1, new_data=1))
        self.__define_object('UpdateByData', self.__gen_properties(entity_name, old_data=1, new_data=1))

        params = []
        self.__gen_parameter(params, 'Create with single data', 'SingleData')
        self.__add_entity_api(entity_name, 'create', 'post', params)

        params = []
        self.__gen_parameter(params, 'Create with multiple data', 'MultiData')
        self.__add_entity_api(entity_name, 'createMany', 'post', params)

        params = []
        # self.__gen_parameter(params, 'Read by data', 'SingleData') # can't apply multiple request body
        self.__gen_parameter(params, 'Read by id', 'SingleId')
        self.__add_entity_api(entity_name, 'readOne', 'post', params)

        params = []
        self.__gen_parameter(params, 'Read all by data', 'SingleData')
        self.__add_entity_api(entity_name, 'readAll', 'post', params)

        params = []
        self.__gen_parameter(params, 'Detele by data', 'SingleData')
        # self.__gen_parameter(params, 'Delete by id', 'SingleId')
        self.__add_entity_api(entity_name, 'delete', 'delete', params)

        params = []
        # self.__gen_parameter(params, 'Update data by data id', 'UpdateById')
        self.__gen_parameter(params, 'Update data by old data', 'UpdateByData')
        self.__add_entity_api(entity_name, 'update', 'put', params)
    
    '''
    add_entity_api(Generalization, create, post, ...)
    '''
    def __add_entity_api(self, entity_name, action, http_method, params):
        api_path = '/' + entity_name + '/' + action
        self.__json['paths'][api_path] = {}
        self.__json['paths'][api_path][http_method] = {
            'tags': [entity_name],
            'summary': action + ' elements for ' + entity_name,
            'consumes': ['application/json'],
            'produces': ['application/json'],
            'responses': {
                '200': {
                    'description': entity_name + ': ' + action + ' successfully'
                }
            },
            'parameters': params
        }

    def __gen_properties(self, entity_name, id_num=0, data_num=0, old_data=0, new_data=0):
        properties = {}
        if id == 1:
            properties['_id'] = {
                'type': 'string',
                'example': '5b2a10190d7dceabda2fe3bb'
            }
        sample_data = {
            'name': 'test1'
        }
        if data_num > 1:
            sample_list = []
            for i in xrange(1, data_num + 1):
                sample_list.append({'name': 'test' + str(i)})

            properties['data'] = {
                'type': 'string',
                'example': str(sample_list).encode('string-escape')
            }
        elif data_num == 1:
            properties['data'] = {
                'type': 'string',
                'example': str(sample_data).encode('string-escape')
            }
        if old_data == 1:
            properties['oldData'] = {
                'type': 'string',
                'example': str(sample_data).encode('string-escape')
            }
        if new_data == 1:
            properties['newData'] = {
                'type': 'string',
                'example': str(sample_data).encode('string-escape')
            }
        properties['collection'] = {
            'type': 'string',
            'example': entity_name
        }
        properties['username'] = {
            'type': 'string',
            'example': self.__user
        }
        properties['key'] = {
            'type': 'string',
            'example': self.__accessKey
        }
        return properties

    def __gen_parameter(self, params, description, object_name):
        param = {
            'in': 'body',
            'name': 'body',
            'description': description,
            'required': True,
            'schema': {
                '$ref': '#/definitions/' + object_name
            }
        }
        params.append(param)

    '''
    use for building sample data structure
    '''
    def __define_object(self, object_name, properties):
        self.__json['definitions'][object_name] = {
            'type': 'object',
	        'properties': properties
        }

if __name__ == '__main__':
    gen = ApiGenerator()
    gen.set_basic_path('localhost:2000', 'one_to_one')
    gen.set_access_key('1234567890')
    gen.set_user_name('danny')
    gen.add_entity('class1')
    gen.add_entity('class2')
    gen.generate_file('./')