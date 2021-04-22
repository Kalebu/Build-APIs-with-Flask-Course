from flask import Blueprint, request
from main.models import db
from flask_restx import Resource, Api

guiders_bp = Blueprint(
    "guiders_bp",
    __name__,
    url_prefix='/'
)

guiders_api = Api(guiders_bp)


@guiders_api.route('guiders')
class guiders(Resource):
    def get(self):
        return {
            'response': "This guiders bp"
        }

    def post(self):
        return {
            'response': "This post guiders"
        }

    def put(self):
        return {
            'response': "This is put guiders"
        }

    def delete(self):
        return {
            'response': "This is delete guiders"
        }
