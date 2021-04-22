import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///twende.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)


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


@app.route('/register-transport', methods=['POST'])
def register_transports():
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


@app.route('/get-all-transports', methods=['GET'])
def get_all_transports():
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


if __name__ == '__main__':
    app.run(debug=True)
