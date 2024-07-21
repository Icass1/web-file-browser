
from flask import Blueprint, request, jsonify, current_app, redirect, Response
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_jwt_extended import create_access_token
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.exc import IntegrityError

from .models import User
from .utils.createId import create_id

import os
import time

api = Blueprint('api', __name__, url_prefix="/api")

db: SQLAlchemy = current_app.config["db"]
login_manager: LoginManager = current_app.config["login_manager"]

@api.route('/get-directory/')
@login_required
def get_home():
    return get_directory("")

@api.route('/get-directory/<path:path>')
@login_required
def get_directory(path):
    path = os.path.join(os.environ["BASE_DIRECTORY"], current_user.scope, path)  
    items = os.listdir(path)

    contents = []

    for item in items:
        item_path = os.path.join(path, item)
        
        # Check if the item is a file or directory
        if os.path.isfile(item_path):
            item_type = "file"
            size = os.path.getsize(item_path)
        else:
            item_type = "directory"
            size = "-"
        
        # Get the date modified
        date_modified = time.ctime(os.path.getmtime(item_path))
        
        contents.append({
            "filename": item,
            "type": item_type,
            "size": size,
            "date_modified": date_modified,
        })

    return jsonify(contents)