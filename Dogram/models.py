from Dogram import database, login_manager
from flask_login import UserMixin
from datetime import datetime

# Tabela de favoritos (usuários que curtiram posts)
favorites = database.Table('favorites',
    database.Column('user_id', database.Integer, database.ForeignKey('user.id'), primary_key=True),
    database.Column('post_id', database.Integer, database.ForeignKey('post.id'), primary_key=True)
)

# Tabela de seguidores (seguindo/seguidores)
seguidores = database.Table('seguidores',
    database.Column('seguidor_id', database.Integer, database.ForeignKey('user.id'), primary_key=True),
    database.Column('seguido_id', database.Integer, database.ForeignKey('user.id'), primary_key=True)
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    profile_pic = database.Column(database.String, nullable=False, default='default.jpg')
    story = database.Column(database.Boolean)

    # Curtidas (favoritos)
    favorites = database.relationship(
        'Post', secondary=favorites,
        backref='favorited_by', lazy='dynamic'
    )

    # Relacionamento de seguidores
    seguindo = database.relationship(
        'User', secondary=seguidores,
        primaryjoin=(seguidores.c.seguidor_id == id),
        secondaryjoin=(seguidores.c.seguido_id == id),
        backref=database.backref('seguidores', lazy='dynamic'),
        lazy='dynamic'
    )

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    caption = database.Column(database.String, nullable=False)
    image_path = database.Column(database.String, nullable=False)
    date_posted = database.Column(database.DateTime, default=datetime.utcnow)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    likes = database.Column(database.Integer, nullable=False, default=0)

    # Usuário que criou o post
    user = database.relationship('User', backref='posts', lazy=True)
