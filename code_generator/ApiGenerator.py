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
        self.__set_entity_apis(entity_name, attributes)

    def generate_file(self, path):
        with fileOps.safe_open_w(path + '/' + 'api.json') as o:
        # with open(path + '/' + 'openAPI.json', 'w') as o:
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

    def __set_entity_apis(self, entity_name, attributes):
        # create data payload structure (sample)

        # CREATE
        params = []
        self.__gen_parameter(params, attributes=attributes)
        self.__add_entity_api(entity_name, 'CreateOne or CreateMany', 'post', params)

        # same path can only have one API sample
        # params = []
        # self.__gen_parameter(params, attributes=attributes, data_num=3)
        # self.__add_entity_api(entity_name, 'CreateMany', 'post', params)

        # # READ
        # params = []
        # path = {}
        # path['name'] = 'Id'
        # path['details'] = {}
        # path['details']['type'] = 'string'
        # path['details']['required'] = True
        # self.__gen_parameter(params, path=path)
        # self.__add_entity_api(entity_name, 'ReadOnebyId', 'get', params, path=path)

        # params = []
        # queries = []
        # query = {}
        # query['name'] = attributes[0]['name']
        # query['details'] = {}
        # query['details']['type'] = 'string'
        # queries.append(query)
        # self.__gen_parameter(params, queries=queries)
        # self.__add_entity_api(entity_name, 'ReadAll or ReadManyByAttributes', 'get', params)

        # # DELETE
        # params = []
        # self.__gen_parameter(params, attributes=attributes)
        # self.__add_entity_api(entity_name, 'DeletebyId or DeleteByAttributes', 'delete', params)

        # params = []
        # path = {}
        # path['name'] = 'Id'
        # path['details'] = {}
        # path['details']['type'] = 'string'
        # path['details']['required'] = True
        # self.__gen_parameter(params, path=path)
        # self.__add_entity_api(entity_name, 'DeletebyIdviaLink', 'delete', params, path=path)


    '''
    add_entity_api(Generalization, create, post, ...)
    '''
    def __add_entity_api(self, entity_name, description, http_method, params, path=None):
        if path:
            api_path = '/' + entity_name + '/{' + path['name'] + '}'
        else:
            api_path = '/' + entity_name + '/'
        

        if not self.__json['paths'].get(api_path):
            self.__json['paths'][api_path] = {}
        self.__json['paths'][api_path][http_method] = {
            'tags': [entity_name],
            'summary': description + ' for ' + entity_name,
            'consumes': ['application/json', 'application/x-www-form-urlencoded'],
            'produces': ['application/json'],
            'responses': {
                '200': {
                    'description': entity_name + ': ' + description + ' successfully'
                }
            },
            'parameters': params
        }   


    # def __gen_properties(self, entity_name, id_num=0, data_num=0, old_data=0, new_data=0):
    #     properties = {}
    #     if id == 1:
    #         properties['_id'] = {
    #             'type': 'string',
    #             'example': '5b2a10190d7dceabda2fe3bb'
    #         }
    #     sample_data = {
    #         'name': 'test1'
    #     }
    #     if data_num > 1:
    #         sample_list = []
    #         for i in xrange(1, data_num + 1):
    #             sample_list.append({'name': 'test' + str(i)})

    #         properties['data'] = {
    #             'type': 'string',
    #             'example': str(sample_list).encode('string-escape')
    #         }
    #     elif data_num == 1:
    #         properties['data'] = {
    #             'type': 'string',
    #             'example': str(sample_data).encode('string-escape')
    #         }
    #     if old_data == 1:
    #         properties['oldData'] = {
    #             'type': 'string',
    #             'example': str(sample_data).encode('string-escape')
    #         }
    #     if new_data == 1:
    #         properties['newData'] = {
    #             'type': 'string',
    #             'example': str(sample_data).encode('string-escape')
    #         }
    #     properties['collection'] = {
    #         'type': 'string',
    #         'example': entity_name
    #     }

    def __gen_parameter(self, params, attributes=None, path=None, queries=None, data_num=1):
        # type: query, path, header, 'formData', body
        if path:
            param = {
                'in': 'path',
                'name': path.get('name', ''),
                'type': path['details'].get('type', 'string'),
                'description': path['details'].get('description', ''),
                'required': path['details'].get('required', False)
            }
            params.append(param)
        if queries:
            for query in queries:
                param = {
                    'in': 'query',
                    'name': query.get('name', ''),
                    'type': query['details'].get('type', 'string'),
                    'description': query['details'].get('description', ''),
                    'required': query['details'].get('required', False)
                }
                params.append(param)
        if attributes:
            for attr in attributes:
                # print(attr)
                param = {
                    'in': 'formData',
                    'name': attr.get('name'),
                    'type': attr['details'].get('type', 'string'),
                    'description': attr['details'].get('description', '')
                    # 'required': True,
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
    gen.generate_file('./')