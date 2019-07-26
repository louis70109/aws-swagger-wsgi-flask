from flask import request
from flask_restful import reqparse
from werkzeug.exceptions import Unauthorized
from flask_restful_swagger_2 import Resource, swagger, Schema


class BasicTodosModel(Schema):
    type = 'object'
    properties = {
        'title': {
            'type': 'string'
        },
        'desc': {
            'type': 'string'
        }
    }
    required = ['title', 'desc']


class QueryTodos(Schema):
    type = 'object'
    properties = {
        'result': {
            'type': 'array',
            'items': BasicTodosModel
        }
    }


class CreateTodos(Schema):
    type = 'object'
    properties = {
        'result': BasicTodosModel
    }


class TodosController(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login_request_parser = reqparse.RequestParser()
        self.login_request_parser.add_argument(
            'title', required=True, help='title can not be blank!', location='json')
        self.login_request_parser.add_argument(
            'desc', required=True, help='desc can not be blank!', location='json')

    @swagger.doc({
        'tags': ['Todos'],
        'description': 'Query todos',
        'responses': {
            '200': {
                'description': 'get todos',
                'schema': QueryTodos,
                'headers': {
                    'X-APP-KEY': {
                        'type': 'string',
                        'description': 'Validate app'
                    }
                },
                'examples': {
                    'application/json': {
                        'result': [{
                            'title': 'title1',
                            'desc': 'lorem 1',
                            'id': 1
                        }, {
                            'title': 'title2',
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
                    'title': 'title1',
                    'desc': 'lorem 1'
                }, {
                    'title': 'title2',
                    'desc': 'lorem 2'
                }]}, 200
        raise Unauthorized('X-APP-KEY not found')

    @swagger.doc({
        'tags': ['Todos'],
        'description': 'Create todos',
        'responses': {
            '200': {
                'description': 'create todo success',
                'schema': CreateTodos,
                'headers': {
                    'X-APP-KEY': {
                        'type': 'string',
                        'description': 'Validate app'
                    }
                },
                'examples': {
                    'application/json': {
                        'result': {
                            'title': 'title3',
                            'desc': 'lorem 3'
                        }
                    }
                }
            },
            '400': {
                'description': 'title & desc can not be blank',
                'examples': {
                    'application/json': {'message': {'title': 'title can not be blank!'}}
                }
            }
        }
    })
    def post(self):
        args = self.login_request_parser.parse_args()
        title = args['title']
        desc = args['desc']

        return {'result': {'title': title, 'desc': desc}}, 200
