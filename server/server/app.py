
from requests import get
import os

from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

IS_DEV = os.environ["FLASK_ENV"] == "development"
WEBPACK_DEV_SERVER_HOST = "http://localhost:3000"
app = Flask(__name__, instance_path=os.path.join(os.path.dirname(__file__), "instance"))

app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///database.db'

db = SQLAlchemy(app)
app.config["database"] = db

jwt = JWTManager(app)




def proxy(host, path):
    response = get(f"{host}{path}")
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

@app.route("/<path:path>")
@app.route("/", defaults={"path": "index.html"})
@app.route("/static/js/<path:path>")
def get_app(path):
    if IS_DEV:
        return proxy(WEBPACK_DEV_SERVER_HOST, request.path)
    return app.send_static_file(path)

with app.app_context():
    from . import models
    from .auth import auth

    db.create_all()
    app.register_blueprint(auth, url_prefix="/auth")
