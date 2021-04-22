import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
