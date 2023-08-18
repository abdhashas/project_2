from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)

api = Api(app)


class Hello(Resource):
    def get(self):
        return {'greeting': "hello mother fucker"}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, location='values', type=str)
        parser.add_argument('l_name', required=True, location='values', type=str)
        args = parser.parse_args()
        return {
            'name': args['name'],
            'l_name': args['l_name'],
        }, 200


api.add_resource(Hello, '/h')

if __name__ == "__main__":
    app.run(debug=True)
