from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FloatField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange
from flask_wtf.file import FileField, FileAllowed
from Dogram.models import User, Post

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    botao_confirm = SubmitField("Fazer login")

class FormCriarConta(FlaskForm):
    username = StringField("Usuário", validators=[DataRequired(message="O nome de usuário é obrigatório.")])
    email = StringField("E-mail", validators=[DataRequired(message="O e-mail é obrigatório."), Email(message="E-mail inválido.")])
    password = PasswordField("Senha", validators=[
        DataRequired(message="A senha é obrigatória."),
        Length(min=6, message="A senha deve ter pelo menos 6 caracteres.")
    ])
    confirm_password = PasswordField("Confirmar Senha", validators=[
        DataRequired(message="A confirmação de senha é obrigatória."),
        EqualTo('password', message="As senhas não coincidem.")
    ])
    submit = SubmitField("Criar Conta")

class FormPublicarPost(FlaskForm):
    endereco_imagem = FileField("Endereço da imagem", validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Apenas imagens')])
    descricao = TextAreaField("Descrição", validators=[Length(max=600)])

    botao_confirm = SubmitField("Publicar")