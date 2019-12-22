from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from flask_babel import _
from app.auth import bp
from werkzeug.security import generate_password_hash, check_password_hash
from app.auth.forms import LoginForm, RegistrationForm
from app.models import load_user
from app.dbconn import conn

conn = conn()


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
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
        login_user(user, remember=form.remember_me.data, force=True)
        return redirect('main.user', id=current_user.id)
    return render_template('auth/login.html', title=_('Sign In'), form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    cursor = conn.cursor()
    if form.validate_on_submit():
        cursor.execute(
            'insert into Uzer (fio,phone,gender,dyennarodjenya,login,password,avatar) values(%s,%s,%s,%s,%s,%s,%s)',
            [form.fio.data, form.phone.data, form.gender.data, form.dr.data, form.login.data,
             generate_password_hash(form.password.data),'https://sun9-31.userapi.com/c622218/v622218469/3809c/DVjj0zqmizo.jpg'])
        conn.commit()
        flash(_('Учетная запись для {} создана успешно!'.format(form.fio.data)))
        flash(_('Login: {}'.format(form.login.data)))
        flash(_('Password: {}'.format(form.password.data)))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title=_('Register'),
                           form=form)