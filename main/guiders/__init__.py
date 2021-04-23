from flask import Blueprint, request
from flask_restx import Resource, Api
from marshmallow import ValidationError
from main.models import db, Guiders, GuidersSchema, serializeGuidersSchema

guiders_bp = Blueprint(
    "guiders_bp",
    __name__,
    url_prefix='/'
)

guiders_api = Api(guiders_bp)


@guiders_api.route('guiders')
class guiders(Resource):
    def get(self):
        all_guiders = Guiders.query.all()
        guider_schema = GuidersSchema(many=True)
        f_guiders = guider_schema.dump(all_guiders)
        return f_guiders

    def post(self):
        guiders_data = request.get_json()
        if guiders_data:
            try:
                s_guider_schema = serializeGuidersSchema()
                guider = s_guider_schema.load(guiders_data)
                db.session.add(guider)
                db.session.commit()

                return {
                    'response': "Guider added successfully"
                }
            except ValidationError as bug:
                print(bug)
                return {
                    'response': str(bug)
                }
        return {
            'response': "Guiders data should not be empty"
        }

    def put(self):
        update_data = request.get_json()
        if update_data and update_data.get('id'):
            _id = update_data.get('id')
            try:
                target_guider = Guiders.query.filter_by(id=_id).first()
                if not target_guider:
                    return {
                        'response': "Guider ID you specified does not Exist"
                    }

                if update_data.get('name'):
                    target_guider.name = update_data.get('name')
                if update_data.get('location'):
                    target_guider.location = update_data.get('location')
                if update_data.get('phone'):
                    target_guider.phone = update_data.get('phone')
                if update_data.get('description'):
                    target_guider.description = update_data.get('description')
                if update_data.get('charging_fee'):
                    target_guider.charging_fee = update_data.get(
                        'charging_fee')

                db.session.add(target_guider)
                db.session.commit()
                return {
                    'response': f"Guider with ID {_id} updated successfully"
                }
            except Exception as bug:
                print(bug)
                return {
                    'response': f'Failed updating user with id {_id}'
                }
        return {
            'response': "To update guiders data you need to specify"
        }

    def delete(self):
        guider_data = request.get_json()
        if guider_data and guider_data.get('id'):
            _id = guider_data.get('id')
            try:
                guider = Guiders.query.filter_by(id=_id).first()
                if not guider:
                    return {
                        'response': f'Guider with ID {_id} does not exist'
                    }
                db.session.delete(guider)
                db.session.commit()
                return {
                    'response': f'Guider with an ID of {_id} Deleted successfully'
                }
            except Exception as bug:
                print(bug)
                return {
                    'response': f'Failed deleting guider with an ID of {_id}'
                }
        return {
            'response': "This is delete guiders"
        }
