from Dogram import database, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_usuarios(id_usuarios):
    return User.query.get(int(id_usuarios))

class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    profile_pic = database.Column(database.String, nullable=False, default='default.jpg')
    story = database.Column(database.Boolean, default=True, nullable=False)

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    caption = database.Column(database.String, nullable=False)
    image_path = database.Column(database.String, nullable=False)
    date_posted = database.Column(database.DateTime, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)

    user = database.relationship('User', backref='posts', lazy=True)
