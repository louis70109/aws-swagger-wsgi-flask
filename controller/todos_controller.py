from flask import request
from flask_restful import reqparse
from werkzeug.exceptions import Unauthorized
from flask_restful_swagger_2 import Resource, swagger, Schema


class TodosModel(Schema):
    type = 'object'
    properties = {
        'name': {
            'type': 'string'
        },
        'desc': {
            'type': 'string'
        }
    }
    required = ['name']
    required = ['desc']


class TodosController(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login_request_parser = reqparse.RequestParser()
        self.login_request_parser.add_argument(
            'name', required=True, help='name can not be blank!', location='json')
        self.login_request_parser.add_argument(
            'desc', required=True, help='desc can not be blank!', location='json')

    @swagger.doc({
        'tags': ['Todos'],
        'description': 'Query todos',
        'responses': {
            '200': {
                'description': 'get todos',
                'headers': {
                    'X-APP-KEY': {
                        'type': 'string',
                        'description': 'Validate app'
                    }
                },
                'examples': {
                    'application/json': {
                        'result': [{
                            'name': 'name1',
                            'desc': 'lorem 1',
                            'id': 1
                        }, {
                            'name': 'name2',
                            'desc': 'lorem 2',
                            'id': 2
                        }]
                    }
                }
            },
            '204': {
                'description': 'X-APP-KEY not found',
                'examples': {
                    'application/json': {'message': 'X-APP-KEY not found'}
                }
            }
        }
    })
    def get(self):
        app = request.headers.get('X-APP-KEY')
        if app is not None:
            return {
                'result': [{
                    'name': 'name1',
                    'desc': 'lorem 1',
                    'id': 1
                }, {
                    'name': 'name2',
                    'desc': 'lorem 2',
                    'id': 2
                }]}, 200
        raise Unauthorized('X-APP-KEY not found')

    @swagger.doc({
        'tags': ['Todos'],
        'description': 'Create todos',
        'responses': {
            '200': {
                'description': 'create todo success',
                'schema': TodosModel,
                'headers': {
                    'X-APP-KEY': {
                        'type': 'string',
                        'description': 'Validate app'
                    }
                },
                'examples': {
                    'application/json': {
                        'result': {
                            'id': 3,
                            'name': 'name3',
                            'desc': 'lorem 3'
                        }
                    }
                }
            },
            '400': {
                'description': 'name & desc can not be blank',
                'examples': {
                    'application/json': {'message': {'name': 'name can not be blank!'}}
                }
            }
        }
    })
    def post(self):
        args = self.login_request_parser.parse_args()
        name = args['name']
        desc = args['desc']

        return {'result': {'name': name, 'desc': desc}}, 200
