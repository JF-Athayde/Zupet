from Dogram import database, app
from Dogram.models import User, Post, favorites, seguidores, Comment
from werkzeug.security import generate_password_hash

with app.app_context():
  database.create_all()
print('Data base Criada!')


with app.app_context():
    database.create_all()

    user1 = User(username="boby_dog", email="boby@example.com", password=generate_password_hash("123456"), story=True, profile_pic="profile1.jpg")
    user2 = User(username="luna_cat", email="luna@example.com", password=generate_password_hash("abcdef"), story=True, profile_pic="profile2.jpg")
    user3 = User(username="kiara", email="kiara@porco.com", password=generate_password_hash("Kiara10"), story=True, profile_pic="profile3.jpg")
    user4 = User(username="max_dog", email="max@dog.com", password=generate_password_hash("maximiliano10"), story=True, profile_pic="profile4.jpg")

    database.session.add_all([user1, user2, user3, user4])
    database.session.commit()

    post1 = Post(caption="Correndo no parque hoje! 🌳🐶", image_path="cachorro_safado.jpg", user_id=user1.id)
    post2 = Post(caption="Soneca depois do almoço 😴", image_path="gatinho_dormindo.jpg", user_id=user2.id)
    post3 = Post(caption="Kiara olhando para cima como uma roupa de tubarão.", image_path="post_kiara.jpg", user_id=user3.id)

    database.session.add_all([post1, post2, post3])
    database.session.commit()

    print("Banco de dados populado com sucesso!")
