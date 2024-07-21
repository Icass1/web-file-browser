
from requests import get
import os

from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_login import LoginManager, login_required, current_user

IS_DEV = os.environ["FLASK_ENV"] == "development"
WEBPACK_DEV_SERVER_HOST = "http://localhost:3000"
app = Flask(__name__, instance_path=os.path.join(os.path.dirname(__file__), "instance"))

app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///database.db'

db = SQLAlchemy(app)
app.config["db"] = db


login_manager = LoginManager()
login_manager.init_app(app)
app.config["login_manager"] = login_manager

jwt = JWTManager(app)



def proxy(host, path):
    response = get(f"{host}/{path}")
    excluded_headers = [
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection",
    ]
    headers = {
        name: value
        for name, value in response.raw.headers.items()
        if name.lower() not in excluded_headers
    }
    return (response.content, response.status_code, headers)

def return_file(path):
    if IS_DEV:
        return proxy(WEBPACK_DEV_SERVER_HOST, path)
    return app.send_static_file(path)

@app.route("/<path:path>")
@app.route("/", defaults={"path": "index.html"})
@app.route("/static/js/<path:path>")
def get_app(path):
    # print("get_app")
    return return_file(request.path)

@app.route("/files/<path:path>")
@login_required
def get_files(path):
    # print("get_files")
    return return_file(request.path)

with app.app_context():
    from . import models
    from .auth import auth
    from .api import api

    db.create_all()
    app.register_blueprint(auth)
    app.register_blueprint(api)
