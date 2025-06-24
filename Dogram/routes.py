from flask import *
from Dogram import app, database, bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from Dogram.form import *
from Dogram.models import *
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect, CSRFError
import os
import requests

csrf = CSRFProtect(app)

@app.route("/")
def homepage():
    profiles = User.query.filter_by(story=True).all()
    posts = Post.query.order_by(Post.date_posted.desc()).all()

    liked_post_ids = []
    if current_user.is_authenticated:
        liked_post_ids = [post.id for post in current_user.favorites]

    return render_template("homepage.html", profiles=profiles, posts=posts, liked_post_ids=liked_post_ids)


@app.route("/publicar", methods=["GET", "POST"])
def publicar():
    if not current_user.is_authenticated:
        flash("Você precisa estar logado para publicar um post.", "warning")
        return redirect(url_for("login"))

    form = FormPublicarPost()
    if form.validate_on_submit():
        arquivo = form.endereco_imagem.data
        nome_seguro = secure_filename(arquivo.filename)

        pasta_upload = os.path.join(app.root_path, 'static', 'assets', 'posts')
        os.makedirs(pasta_upload, exist_ok=True)

        caminho_arquivo = os.path.join(pasta_upload, nome_seguro)
        arquivo.save(caminho_arquivo)

        caminho_relativo = f"{nome_seguro}"
        print(caminho_relativo)
        post = Post(
            caption=form.descricao.data,
            image_path=caminho_relativo,
            user=current_user
        )

        database.session.add(post)
        database.session.commit()

        flash("Post publicado com sucesso!", "success")
        return redirect(url_for('homepage'))

    return render_template("publish.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    formLogin = FormLogin()
    if formLogin.validate_on_submit():
        usuario = User.query.filter_by(email=formLogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.password, formLogin.password.data):
            login_user(usuario)
            return redirect(url_for("homepage"))
        
        formLogin.email.errors.append("Login inexistente ou senha incorreta.")
    return render_template("login.html", form=formLogin)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    formCriarConta = FormCriarConta()
    
    if formCriarConta.validate_on_submit():

        usuario_existente = User.query.filter(
            (User.email == formCriarConta.email.data) | 
            (User.username == formCriarConta.username.data)
        ).first()
        if usuario_existente:
            flash("Este email ou nome de usuário já está em uso. Tente outro.", "danger")
            return render_template("signup.html", form=formCriarConta)
        senha_hash = bcrypt.generate_password_hash(formCriarConta.password.data).decode('utf-8')
        usuario = User(
            username=formCriarConta.username.data,
            password=senha_hash,
            email=formCriarConta.email.data,
            story=True
        )
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("homepage"))
    
    print(formCriarConta.errors)
    return render_template("signup.html", form=formCriarConta)

@app.route("/perfil/<string:username>")
def perfil(username):
    usuario = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user=usuario).order_by(Post.date_posted.desc()).all()
    return render_template("profile.html", usuario=usuario, posts=posts)

@csrf.exempt
@app.route("/curtir/<int:post_id>", methods=["POST"])
@login_required
def curtir(post_id):
    post = Post.query.get_or_404(post_id)

    if post in current_user.favorites:
        return {"success": False, "message": "Você já curtiu este post.", "likes": post.likes}

    post.likes += 1
    current_user.favorites.append(post)

    database.session.commit()

    return {"success": True, "likes": post.likes}

@csrf.exempt
@app.route("/seguir/<int:user_id>", methods=["POST"])
@login_required
def seguir(user_id):
    usuario_a_seguir = User.query.get_or_404(user_id)

    if usuario_a_seguir == current_user:
        return {"error": "Você não pode seguir a si mesmo."}, 400

    if not current_user.seguindo.filter_by(id=usuario_a_seguir.id).first():
        current_user.seguindo.append(usuario_a_seguir)
        seguindo = True
    else:
        current_user.seguindo.remove(usuario_a_seguir)
        seguindo = False

    database.session.commit()
    total_seguidores = usuario_a_seguir.seguidores.count()

    return {
        "success": True,
        "seguindo": seguindo,
        "total_seguidores": total_seguidores
    }

@app.route("/favoritos")
@login_required
def favoritos():
    favorite_posts = current_user.favorites.order_by(Post.date_posted.desc()).all()
    return render_template("likes.html", posts=favorite_posts)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))
