from flask import Blueprint, request
from main.models import db
from flask_restx import Resource, Api

hosters_bp = Blueprint(
    "hosters_bp",
    __name__,
    url_prefix='/'
)

hosters_api = Api(hosters_bp)


@hosters_api.route('hosters')
class hosters(Resource):
    def get(self):
        return {
            'response': "This get hosters bp"
        }

    def post(self):
        return {
            'response': "This is post hosters bp"
        }

    def put(self):
        return {
            'response': "This is  hosters bp"
        }

    def delete(self):
        return {
            'response': "This is delete hosters bp"
        }
