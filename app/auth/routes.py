from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from flask_babel import _
from app.auth import bp
from werkzeug.security import generate_password_hash, check_password_hash
from app.auth.forms import LoginForm, RegistrationForm
from app.models import load_user
from app.dbconn import conn

conn = conn()  # подключение к БД


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # проверка пользователя на авторизированость
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():  # проверка на нажатие пользователем кнопки Submit
        cursor = conn.cursor()
        cursor.execute('select password,login,iduser from Uzer where login = %s',
                       [form.login.data])
        user = cursor.fetchone()
        conn.commit()
        parol = form.password.data
        if user is None or not check_password_hash(user[0], parol):
            flash(_('Invalid username or password'))
            return redirect(url_for('auth.login'))
        user = load_user(user[2])
        login_user(user, remember=form.remember_me.data, force=True)  # создание пользователя как обьекта
        return redirect(url_for('main.user', id=current_user.id))
    return render_template('auth/login.html', title=_('Sign In'), form=form)


@bp.route('/logout')
def logout():  # логаут
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():  # регистрация
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()  # инициализация форм указанных в forms.py
    cursor = conn.cursor()
    if form.validate_on_submit():
        fio = form.familiya.data + ' ' + form.imya.data + ' ' + form.otchestvo.data
        cursor.execute(
            'insert into Uzer (fio,phone,gender,dyennarodjenya,login,password,avatar) values(%s,%s,%s,%s,%s,%s,%s)',
            [fio, form.phone.data, form.gender.data, form.dr.data, form.login.data,
             generate_password_hash(form.password.data),'https://sun9-31.userapi.com/c622218/v622218469/3809c/DVjj0zqmizo.jpg'])
        conn.commit()   # добавление данных введенных при регистрации в БД
        flash(_('Учетная запись для %(fio)s создана успешно!', fio=fio))
        flash(_('Login: %(login)s', login=form.login.data))
        flash(_('Password: %(passw)s', passw=form.password.data))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title=_('Register'),
                           form=form)