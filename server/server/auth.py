from flask import Blueprint, request, jsonify, current_app
from .models import User
from flask_jwt_extended import create_access_token
import bcrypt

import os
import base64

auth = Blueprint('auth', __name__)

db = current_app.config["database"]

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    print(data)

    # hashed_password = bcrypt.hashpw(bytes(data['password'], "utf-8"), base64.b64encode(os.urandom(16))).decode('utf-8')
    # user = User(username=data['username'], email=data['email'], password=hashed_password)
    # db.session.add(user)
    # db.session.commit()
    return jsonify(message="User created successfully"), 201




@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.checkpw(user.password, data['password']):
        access_token = create_access_token(identity={'username': user.username, 'email': user.email})
        return jsonify(access_token=access_token), 200
    return jsonify(message="Invalid Credentials"), 401