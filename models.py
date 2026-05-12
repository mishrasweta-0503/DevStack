
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy() #creating the database object, but we don't link it to an app yet. 
#This allows us to import db into other files without creating a circular loop.

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True) #primary key column, automatically generated IDs
    username = db.Column(db.String(50), index = True, unique = True) #user's username
    email = db.Column(db.String(80), index = True, unique = True) #user's email
    password_hash = db.Column(db.String(256), index = True, unique = False)
    resources = db.relationship('Resource',backref='user',lazy='dynamic')

class Resource(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), index = True, unique = False) 
    url = db.Column(db.String(80), index = True, unique = False)
    description = db.Column(db.String(80), index = True, unique = False)
    category = db.Column(db.String(80),index = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #a resource must point to a user(owner)