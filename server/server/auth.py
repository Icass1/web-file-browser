from flask import Blueprint, request, jsonify, current_app, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_jwt_extended import create_access_token
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.exc import IntegrityError

from .models import User
from .utils.createId import create_id

auth = Blueprint('auth', __name__, url_prefix="/auth")

db: SQLAlchemy = current_app.config["db"]
login_manager: LoginManager = current_app.config["login_manager"]

@login_manager.user_loader
def load_user(user_id):
    
    return db.session.get(User, user_id)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    print(data)

    id =        create_id()
    username =  data['username']
    password =  data['password']
    scope =     ''

    user = User(id=id, username=username, scope=scope)
    user.set_password(password=password)

    db.session.add(user)
    try: db.session.commit()
    except IntegrityError as e:
        print("IntegrityError", e.args, e.params)
        return jsonify(message=e.args), 400
    except Exception as e:
        print("Exception", e, type(e))
        return jsonify(message="Error adding user to database"), 400

    return jsonify(message="User created successfully"), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user: User | any = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        login_user(user)
        next_url = request.args.get("next")
        if next_url:
            return redirect(next_url)
        return jsonify(message="User logged in successfully"), 201

    print(user)

    return jsonify(message="Invalid credentials"), 401

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify(message="Logout successfully"), 200

