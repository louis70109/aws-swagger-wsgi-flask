from flask import request
from flask_restful import Resource, reqparse
from werkzeug.exceptions import Unauthorized


class TodosController(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login_request_parser = reqparse.RequestParser()
        self.login_request_parser.add_argument(
            'title', required=True, help='title can not be blank!', location='json')
        self.login_request_parser.add_argument(
            'desc', required=True, help='desc can not be blank!', location='json')

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

    def post(self):
        args = self.login_request_parser.parse_args()
        title = args['title']
        desc = args['desc']

        return {'result': {'title': title, 'desc': desc}}, 200
