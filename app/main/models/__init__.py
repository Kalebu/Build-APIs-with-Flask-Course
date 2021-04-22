import datetime
from flask.globals import request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, post_load

db = SQLAlchemy()
ma = Marshmallow()


class Transports(db.Model):  # table
    # columns
    id = db.Column(db.Integer, primary_key=True)
    transport_type = db.Column(db.String(128), nullable=False)
    rent_fee = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self) -> str:
        return f'<Transport {self.id}> : {self.rent_fee}'


class TrasportsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        transports = Transports
        fields = ['id', 'transport_type', "rent_fee",
                  "location", "phone", "date_created"]
        load_instance = True


class serializeTransportSchema(ma.SQLAlchemyAutoSchema):
    transport_type = fields.String(required=True)
    rent_fee = fields.Float(required=True)
    location = fields.String(required=True)
    phone = fields.String(required=True)

    @post_load
    def create_transport(self, transport_data, **kwargs):
        return Transports(**transport_data)


class Guiders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(128), nullable=False)
    charging_fee = db.Column(db.Float, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(250), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __repr__(self) -> str:
        return f'<Guider {self.id}>: {self.name}'


class GuidersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        guiders = Guiders
        fields = ['id', 'name', 'location',
                  'charging_fee', 'phone', 'description']
        load_instance = True


class serializeGuidersSchema(ma.SQLAlchemyAutoSchema):
    name = fields.String(required=True)
    location = fields.String(required=True)
    charging_fee = fields.Float(required=True)
    phone = fields.String(required=True)
    description = fields.String(required=False)

    @post_load
    def create_guider(self, guider_data, **kwargs):
        return Guiders(**guider_data)


class placesToVisit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    hoster_name = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(128), nullable=False)
    fee = db.Column(db.Float, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self) -> str:
        return f'< Place to Visit {self.id}> : {self.places}'


class placeToVisitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        place_to_visits = placesToVisit
        fields = ['id', 'name', 'hoster_name',
                  'location', 'fee', 'phone', 'description']
        load_instance = True


class serializePlacesSchema(ma.SQLAlchemyAutoSchema):
    name = fields.String(required=True)
    hoster_name = fields.String(required=True)
    location = fields.String(required=True)
    fee = fields.Float(required=True)
    phone = fields.String(required=True)
    description = fields.String(required=False)

    @post_load
    def create_place_to_visit(self, places_data, **kwargs):
        return placesToVisit(**places_data)
