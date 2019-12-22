from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, RadioField, SelectField,IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
from app.models import User
from app.dbconn import conn

conn = conn()


class LoginForm(FlaskForm):
    login = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


class RegistrationForm(FlaskForm):
    fio = StringField('Фамилия Имя Отчество')
    phone = IntegerField('Номер')
    gender = SelectField('Пол', choices=[('Мale', 'Male'),
                                         ('Female', 'Female'),
                                         ('Transexual Male', 'Transexsual Male'),
                                         (' Transexsual Female', 'Transexsual Female'),
                                         ('Metrosexual Male', 'Metrosexual Male'),
                                         ('Metrosexual Female', 'Metrosexual Female'),
                                         ('Male, but curious what being a Female like', 'Male, but curious what being a Female like'),
                                         ('Female, but curious what being a Male like', 'Female, but curious what being a Male like'),
                                         ('Hermaphrodite with Predominant Male leanings', 'Hermaphrodite with Predominant Male leanings'),
                                         ('Hermaphrodite with Predominant Female leanings', 'Hermaphrodite with Predominant Female leanings'),
                                         ('Hermaphrodite with no strong gender leanings', 'Hermaphrodite with no strong gender leanings'),
                                         ('Conjoined Twin - Male', 'Conjoined Twin - Male'),
                                         ('Conjoined Twin - Female', 'Conjoined Twin - Female'),
                                         ('Born without genitals - identify as a Male', 'Born without genitals - identify as a Male'),
                                         ('Born without genitals - identify as a Female', 'Born without genitals - identify as a Female'),
                                         ('Born without genitals - proud of it', 'Born without genitals - proud of it'),
                                         ('Artificial intelligence with no gender', 'Artificial intelligence with no gender'),
                                         ('Artificial intelligence - identifies as Male', 'Artificial intelligence -identifies as Male'),
                                         ('Artificial intelligence - identifies as Female', 'Artificial intelligence -identifies as Female'),
                                         ('Household pet that walked across the keyboard - Male', 'Household pet that walked across the keyboard - Male'),
                                         ('Household pet that walked across the keyboard - Female', 'Household pet that walked across the keyboard - Female'),
                                         ('Household pet that walked across the keyboard - Other', 'Household pet that walked across the keyboard - Other'),
                                         ('Attack helicopter', 'Attack helicopter')
                                         ])
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