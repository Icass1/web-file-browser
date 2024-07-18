

from flask import current_app

db = current_app.config["database"]

class User(db.Model):
    id =                db.Column(db.String(30), primary_key=True, unique=True)
    username =          db.Column(db.String(80), unique=True, nullable=False)
    password =          db.Column(db.String(80), unique=True, nullable=False)
    scope =             db.Column(db.String(255))
    admin =             db.Column(db.Boolean, default=False)
    shares =            db.Column(db.String(20000), default="[]")

class Shares(db.Model):
    id =               db.Column(db.String(30), primary_key=True, unique=True)
    url_path =         db.Column(db.String(255), nullable=False)
    local_path =       db.Column(db.String(255), nullable=False)
    password =         db.Column(db.String(255))
    times_accessed =   db.Column(db.Integer, default=0)
    times_downloaded = db.Column(db.Integer, default=0)
    editable =         db.Column(db.Boolean, default=False)
    expiration_date =  db.Column(db.Date, nullable=False)
