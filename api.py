from flask import Flask
from flask_cors import CORS
from flask_restful_swagger_2 import Api

from controller.todos_controller import TodosController
app = Flask(__name__)
CORS(app)

security = {
    "appKey": {
        'in': 'header',
        'type': 'apiKey',
        'name': 'X-APP-KEY'
    }
}

api = Api(app,
          schemes=['http'],
          #   schemes=['https'],
          #   base_path='/dev',
          security_definitions=security,
          security=[{'appKey': []}],
          api_version='0.01',
          api_spec_url='/api/swagger')
api.add_resource(TodosController, '/todos')

if __name__ == '__main__':
    app.run(debug=True)
