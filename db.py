from Dogram import database, app
from Dogram.models import User, Post

with app.app_context():
  database.create_all()