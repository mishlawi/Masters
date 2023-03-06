from flask import Flask
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)


class Info(Resource):
    @staticmethod
    def get():
        f = open('./API/bettingAPI.json')
        data = json.load(f)
        return data, 200

class Exchange(Resource):
    @staticmethod
    def get():
        f = open('./API/cambioAPI.json')
        data = json.load(f)
        return data, 200


api.add_resource(Info, '/info')
api.add_resource(Exchange, '/exchange')

if __name__ == '__main__':
    app.run()
