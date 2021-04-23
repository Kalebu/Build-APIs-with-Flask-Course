from flask import current_app as app
from flask import Blueprint, request
from flask_restx import Resource, Api
from main.models import UserSchema, db, Users
from marshmallow import ValidationError
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

users_bp = Blueprint(
    "users_bp",
    __name__,
    url_prefix='/'
)

serializer = Serializer('Hhdshuusys&', 600)
users_api = Api(users_bp)


@users_api.route('users')
class UsersEndpoint(Resource):
    def get(self):
        return {
            'response': "No users in system"
        }

    def post(self):
        # registering
        user_data = request.get_json()
        if user_data:
            try:
                user_schema = UserSchema()
                user = user_schema.load(user_data)
                db.session.add(user)
                db.session.commit()
                return {
                    'response': "User Registered successfully"
                }
            except ValidationError as bug:
                print(bug)
                return {
                    'response': str(bug)
                }
        return {
            'response': "User data should be empty"
        }


@users_api.route('login')
class login(Resource):
    def post(self):
        user_data = request.get_json()
        if user_data:
            try:
                print(Users)
                target_user = Users.query.filter_by(
                    username=user_data.get('username')).first()
                if not target_user or not target_user.verify(user_data.get('password')):
                    return {
                        'response': 'Invalid username/password try again'
                    }
                user_body = {'user_id': target_user.id}
                token = serializer.dumps(user_body).decode('utf-8')
                target_user.token = token
                db.session.add(target_user)
                db.session.commit()
                return {
                    "Token": token
                }
            except Exception as bug:
                print(bug)
                return {
                    'response': 'Failed generating auth token '
                }
        return {
            'response': "Please make sure you include username and password"
        }
