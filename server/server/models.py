
from flask import current_app
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import bcrypt

db = current_app.config["db"]

class User(UserMixin, db.Model):
    id =               db.Column(db.String(30), primary_key=True, unique=True)
    username =         db.Column(db.String(80), unique=True, nullable=False)
    password_hash =    db.Column(db.String(128), unique=True, nullable=False)
    salt =             db.Column(db.String(29))
    scope =            db.Column(db.String(255), default="")
    admin =            db.Column(db.Boolean, default=False)
    shares =           db.Column(db.String(20000), default="[]")

    def set_password(self, password):
        # Generate a random salt and hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.password_hash = hashed_password
        self.salt = salt

    def check_password(self, password):
        if bcrypt.checkpw(password.encode('utf-8'), self.password_hash):
            db.session.commit()
            return True
        else: 
            return False


class Shares(db.Model):
    id =               db.Column(db.String(30), primary_key=True, unique=True)
    url_path =         db.Column(db.String(255), nullable=False)
    local_path =       db.Column(db.String(255), nullable=False)
    password =         db.Column(db.String(255))
    times_accessed =   db.Column(db.Integer, default=0)
    times_downloaded = db.Column(db.Integer, default=0)
    editable =         db.Column(db.Boolean, default=False)
    expiration_date =  db.Column(db.Date, nullable=False)
