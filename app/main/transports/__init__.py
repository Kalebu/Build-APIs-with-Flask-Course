from flask import Blueprint, request
from main.models import db, Transports, TrasportsSchema, serializeTransportSchema
from flask_restx import Resource, Api

transport_bp = Blueprint(
    "transport_bp",
    __name__,
    url_prefix='/'
)

transport_api = Api(transport_bp)


@transport_api.route('transport-locations')
class Transportlocations(Resource):
    def get(self):
        all_transports = Transports.query.all()
        transport_schema = TrasportsSchema(many=True)
        f_transports = transport_schema.dump(all_transports)
        return {
            "Transports": f_transports
        }

    def post(self):
        transport_data = request.get_json()
        if transport_data:
            try:
                transport_schema = serializeTransportSchema()
                my_transport = transport_schema.load(transport_data)
                db.session.add(my_transport)
                db.session.commit()
                return {
                    'response': {
                        'transport_id': my_transport.id,
                        'message': "Transport registered successfully"
                    }
                }
            except Exception as bug:
                print(bug)
                return {
                    'response': 'Transport registration failed'
                }
        return {
            'response': 'Transport data should not be empty'
        }

    def put(self):
        update_data = request.get_json()
        if update_data and update_data.get('id'):
            _id = update_data.get('id')
            try:
                target_transport = Transports.query.filter_by(id=_id).first()
                if not target_transport:
                    return {
                        'response': "Transport ID Does not exist"
                    }
                if update_data.get('transport_type'):
                    target_transport.transport_type = update_data.get(
                        'transport_type')

                if update_data.get('rent_fee'):
                    target_transport.rent_fee = update_data.get(
                        'rent_fee')

                if update_data.get('location'):
                    target_transport.location = update_data.get(
                        'location')

                if update_data.get('phone'):
                    target_transport.phone = update_data.get('phone')

                db.session.add(target_transport)
                db.session.commit()
                return {
                    'response': f"Transport with ID {_id} updated successufully"
                }
            except Exception as bug:
                print(bug)
                return {
                    'response': f'Failed updating Transport with ID {_id} '
                }

        return {
            'response': "Please structure well your update request body"
        }

    def delete(self):
        transport_data = request.get_json()
        if transport_data and transport_data.get('id'):
            _id = transport_data.get('id')
            try:
                target_transport = Transports.query.filter_by(id=_id).first()
                if not target_transport:
                    return {
                        'response': f'Transport with Id of {_id} does not exist'
                    }
                db.session.delete(target_transport)
                db.session.commit()
                return {
                    'response': f'Transport with ID of {_id} deleted successfully'
                }
            except Exception as bug:
                print(bug)
                return {
                    'response': f'Failed to delete Transport with Id of {_id}'
                }
        return {
            'response': "Please specify ID of transport you would like delete"
        }
