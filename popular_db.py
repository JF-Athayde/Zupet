from Dogram import app, database
from Dogram.models import User, Post
from werkzeug.security import generate_password_hash

with app.app_context():
    database.create_all()

    user1 = User(username="boby_dog", email="boby@example.com", password=generate_password_hash("123456"), story=True)
    user2 = User(username="luna_cat", email="luna@example.com", password=generate_password_hash("abcdef"), story=True)
    user3 = User(username="kiara", email="kiara@porco.com", password=generate_password_hash("Kiara10"), story=True)

    database.session.add_all([user1, user2, user3])
    database.session.commit()

    post1 = Post(caption="Correndo no parque hoje! 🌳🐶", image_path="cachorro_safado.jpg", id_usuario=user1.id)
    post2 = Post(caption="Soneca depois do almoço 😴", image_path="gatinho_dormindo.jpg", id_usuario=user2.id)
    post3 = Post(caption="Kiara olhando para cima como uma roupa de tubarão.", image_path="post_kiara.jpg", id_usuario=user3.id)

    database.session.add_all([post1, post2, post3])
    database.session.commit()

    print("Banco de dados populado com sucesso!")
