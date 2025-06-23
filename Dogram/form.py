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
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired(), Length(min=0, max=20)])
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=6, max=20)])
    confirmar_senha = PasswordField("Confirmação de senha", validators=[DataRequired(), Length(min=6, max=20), EqualTo("password")])
    botao_confirm = SubmitField("Criar conta")

    def validate_email(self, email):
        usuario = User.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("Email já cadastrado")

class FormPublicarPost(FlaskForm):
    endereco_imagem = FileField("Endereço da imagem", validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Apenas imagens')])
    descricao = TextAreaField("Descrição", validators=[Length(max=600)])

    botao_confirm = SubmitField("Publicar")