from flask_wtf import FlaskForm
from wtforms.fields import FileField
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class FileForm(FlaskForm):
    name = StringField('Название книги', validators=[DataRequired()])
    author = StringField('Автор', validators=[DataRequired()])
    cover = FileField('Обложка')
    file = FileField('Файл')

class NoteForm(FlaskForm):
    note = StringField('Содержание комментария')