from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
from app.models import User
import psycopg2

conn = psycopg2.connect(dbname='postgres', user='postgres',
                        password='bibaboba', host='localhost',
                        port='5432')


class LoginForm(FlaskForm):
    login = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


class RegistrationForm(FlaskForm):
    fio = StringField('Фамилия Имя Отчество')
    phone = StringField('Номер')
    gender = RadioField('Пол', choices=[('М', 'Мужчина'), ('Ж', 'Женщина')])
    dr = DateField('День рождения', format='%d-%m-%Y')
    login = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Register'))

    def validate_email(self, login):
        cursor = conn.cursor()
        cursor.execute('select login from Uzer where login = %s',
                       [login])
        cursor.fetchone()
        user = cursor.fetchone()
        if user is not None:
            raise ValidationError(_('Please use a different email address.'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))
