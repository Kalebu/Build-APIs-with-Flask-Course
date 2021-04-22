from flask import Blueprint, request
from flask_restx import Resource, Api
from marshmallow import ValidationError
from main.models import (
    db,
    placeToVisitSchema,
    placesToVisit,
    serializePlacesSchema)

hosters_bp = Blueprint(
    "hosters_bp",
    __name__,
    url_prefix='/'
)

hosters_api = Api(hosters_bp)


@hosters_api.route('hosters')
class hosters(Resource):
    def get(self):
        places_to_visit = placesToVisit.query.all()
        places_schema = placeToVisitSchema(many=True)
        f_places_to_visit = places_schema.dump(places_to_visit)
        return {
            'PlacesToVisit': f_places_to_visit
        }

    def post(self):
        hosters_data = request.get_json()
        if hosters_data:
            try:
                places_schema = serializePlacesSchema()
                place_to_visit = places_schema.load(hosters_data)
                db.session.add(place_to_visit)
                db.session.commit()
                return {
                    'response': "Hoster registered successfully"
                }
            except ValidationError as bug:
                print(bug)
                return {
                    'response': 'Failed adding hosters data'
                }
        return {
            'response': "Hoster data should not be empty"
        }

    def put(self):
        update_data = request.get_json()
        if update_data and update_data.get('id'):
            _id = update_data.get('id')
            try:
                place_to_visit = placesToVisit.query.filter_by(id=_id).first()
                if not place_to_visit:
                    return {
                        'response': "The place to visit ID you specified does not exist"
                    }

                if update_data.get('name'):
                    place_to_visit.name = update_data.get('name')
                if update_data.get('hoster_name'):
                    place_to_visit.hoster_name = update_data.get(
                        'hoster_name')
                if update_data.get('location'):
                    place_to_visit.location = update_data.get(
                        'location')
                if update_data.get('phone'):
                    place_to_visit.phone = update_data.get('phone')
                if update_data.get('fee'):
                    place_to_visit.fee = update_data.get('fee')
                if update_data.get('description'):
                    place_to_visit.description = update_data.get(
                        'description')
                db.session.add(place_to_visit)
                db.session.commit()
                return {
                    'response': f'Place to Visit with Id {_id} updated successfully'
                }
            except Exception as bug:
                print(bug)
                return {
                    'response': f'Failed updating place to visit with ID {_id}'
                }

        return {
            'response': "You need to specify ID of place you would like to update"
        }

    def delete(self):
        place_data = request.get_json()
        if place_data and place_data.get('id'):
            try:
                _id = place_data.get('id')
                place_to_visit = placesToVisit.query.filter_by(id=_id).first()
                if not place_to_visit:
                    return {
                        'response': f"The Id {_id} Does not Exist"
                    }
                db.session.delete(place_to_visit)
                db.session.commit()
                return {
                    'response': f"Place with an ID of {_id} has been deleted"
                }
            except Exception as bug:
                print(bug)
                return {
                    'response': f"Failed to Delete place with an ID of {_id}"
                }
        return {
            'response': "Please specify the ID of place you would like to delete"
        }
