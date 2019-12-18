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
    gender = RadioField('Пол', choices=[('М', 'Мужчина'), ('Ж', 'Женщина')])
    cursor = conn.cursor()
    cursor.execute('select idvuz,namevuz from vuz order by idvuz asc')
    VUZ = cursor.fetchall()
    SelVUZ = SelectField('ВУЗ', choices=VUZ, coerce=int)
    SelFack = SelectField('Факультет', choices=[], coerce=int)
    SelKaf = SelectField('Кафедра', choices=[], coerce=int)
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


