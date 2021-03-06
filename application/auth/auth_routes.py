from flask import current_app as app,request
from flask import render_template,jsonify
from ..models import db, User
import simplejson
import json
from flask_restful import Api,Resource,reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

parser = reqparse.RequestParser()
parser.add_argument('email',help='This field can not be blank',required=True)
parser.add_argument('password',help='This field can not be blank',required=True)
parse = reqparse.RequestParser()
parse.add_argument('name',help='This field can not be blank',required=True)
parse.add_argument('password',help='This field can not be blank',required=True)
parse.add_argument('email',help='This field can not be blank',required=True)

class UserRegistration(Resource):
    def post(self):
        data = parse.parse_args()
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user is None:
            user = User(
                name = data['name'],
                email = data['email']
            )
            user.set_password(data['password'])
            db.session.add(user)
            db.session.commit()
            access_token = create_access_token(identity = data['email'])
            refresh_token = create_refresh_token(identity = data['email'])
            return {
                'message': 'User {} was created'.format(data['email']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        return {'status': 'Alrady user register'},400

class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        user = User.query.filter_by(email=data['email']).first()
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity = data['email'])
            refresh_token = create_refresh_token(identity = data['email'])
            return {
                'message': 'User {} was created'.format(data['email']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        return {'message': 'Wrong credentials'},400
      
class UserLogoutAccess(Resource):
    def post(self):
        
        return {'message': 'User logout'}
      
      
class UserLogoutRefresh(Resource):
    def post(self):
        return {'message': 'User logout'}
      
      
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}
      
      
class AllUsers(Resource):
    def get(self):
        return {'message': 'List of users'}

    def delete(self):
        return {'message': 'Delete all users'}