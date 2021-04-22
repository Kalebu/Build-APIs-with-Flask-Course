from flask import Blueprint, request
from main.models import db, Transports
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
        cleaned_transports = []
        for _tansport in all_transports:
            transport_dict = {
                "id": _tansport.id,
                "location": _tansport.location,
                "rent_fee": _tansport.rent_fee,
                "transport_type": _tansport.transport_type,
                "phone": _tansport.phone,
                "registered_on": _tansport.date_created.isoformat()
            }
            cleaned_transports.append(transport_dict)
        return {
            "Transports": cleaned_transports
        }

    def post(self):
        transport_data = request.get_json()
        try:
            my_transport = Transports(
                transport_type=transport_data.get('transport_type'),
                rent_fee=transport_data.get('rent_fee'),
                location=transport_data.get('location'),
                phone=transport_data.get('phone')
            )
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

    def put(self):
        return {
            'response': "This is transport put method"
        }

    def delete(self):
        return {
            'response': "This is transport delete method"
        }
