from genderTracker.config import uri
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['genderTracker_NEW_USER_SECRET'] = os.environ.get('genderTracker_NEW_USER_SECRET', None)

db = SQLAlchemy(app)
