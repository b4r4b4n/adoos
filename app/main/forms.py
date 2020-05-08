from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import _, lazy_gettext as _l
from app.models import User
from app.dbconn import conn

conn = conn()


class EditProfileForm(FlaskForm):
    fio = StringField('Фамилия Имя Отчество')
    login = StringField(_l('Login'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'),
                             validators=[Length(min=0, max=140)])
    phone = StringField('Номер')
    avatar = StringField('Аватар')
    gender = SelectField('Пол', choices=[('Мale', 'Male'),
                                         ('Female', 'Female'),
                                         ('Transexual Male', 'Transexsual Male'),
                                         (' Transexsual Female', 'Transexsual Female'),
                                         ('Metrosexual Male', 'Metrosexual Male'),
                                         ('Metrosexual Female', 'Metrosexual Female'),
                                         ('Male, but curious what being a Female like',
                                          'Male, but curious what being a Female like'),
                                         ('Female, but curious what being a Male like',
                                          'Female, but curious what being a Male like'),
                                         ('Hermaphrodite with Predominant Male leanings',
                                          'Hermaphrodite with Predominant Male leanings'),
                                         ('Hermaphrodite with Predominant Female leanings',
                                          'Hermaphrodite with Predominant Female leanings'),
                                         ('Hermaphrodite with no strong gender leanings',
                                          'Hermaphrodite with no strong gender leanings'),
                                         ('Conjoined Twin - Male', 'Conjoined Twin - Male'),
                                         ('Conjoined Twin - Female', 'Conjoined Twin - Female'),
                                         ('Born without genitals - identify as a Male',
                                          'Born without genitals - identify as a Male'),
                                         ('Born without genitals - identify as a Female',
                                          'Born without genitals - identify as a Female'),
                                         ('Born without genitals - proud of it', 'Born without genitals - proud of it'),
                                         ('Artificial intelligence with no gender',
                                          'Artificial intelligence with no gender'),
                                         ('Artificial intelligence - identifies as Male',
                                          'Artificial intelligence -identifies as Male'),
                                         ('Artificial intelligence - identifies as Female',
                                          'Artificial intelligence -identifies as Female'),
                                         ('Household pet that walked across the keyboard - Male',
                                          'Household pet that walked across the keyboard - Male'),
                                         ('Household pet that walked across the keyboard - Female',
                                          'Household pet that walked across the keyboard - Female'),
                                         ('Household pet that walked across the keyboard - Other',
                                          'Household pet that walked across the keyboard - Other'),
                                         ('Attack helicopter', 'Attack helicopter')
                                         ])
    cursor = conn.cursor()
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))


class PostForm(FlaskForm):
    post = TextAreaField(validators=[Length(min=1, max=140)])
    submit = SubmitField(_l('Отправить'))


class ComForm(FlaskForm):
    com = TextAreaField(u'Комментарий', validators=[Length(min=1, max=140)])
    submit = SubmitField(_l('Отправить'))


class EditCom(FlaskForm):
    editcom = TextAreaField(u'Редактировать', validators=[Length(min=1, max=140)])
    submit = SubmitField(_l('Отправить'))


class EditPostForm(FlaskForm):
    editpost = TextAreaField(validators=[Length(min=1, max=140)])
    submit = SubmitField(_l('Редактировать'))


