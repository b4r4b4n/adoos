from flask import render_template, redirect, url_for, flash, request,session
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_babel import _
from app.auth import bp
from werkzeug.security import generate_password_hash, check_password_hash
from app.auth.forms import LoginForm, RegistrationForm, \
    ResetPasswordRequestForm, ResetPasswordForm
from app.models import load_user
from app.auth.email import send_password_reset_email
import psycopg2

conn = psycopg2.connect(dbname='postgres', user='postgres',
                        password='bibaboba', host='localhost',
                        port='5432')


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
        parol = form.password.data
        if user is None or not check_password_hash(user[0], parol):
            flash(_('Invalid username or password'))
            return redirect(url_for('auth.login'))
        user = load_user(user[2])
        login_user(user, remember=form.remember_me.data, force=True)
        return redirect('index')
    return render_template('auth/login.html', title=_('Sign In'), form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        cursor = conn.cursor()
        cursor.execute(
            'insert into Uzer (fio,phone,gender,dyennarodjenya,login,password) values(%s,%s,%s,%s,%s,%s)',
            (form.fio.data, form.phone.data, form.gender.data, form.dr.data, form.login.data,
             generate_password_hash(form.password.data)))
        conn.commit()
        cursor.close()
        flash(_('Учетная запись для {} создана успешно!'.format(form.fio.data)))
        flash(_('Login: {}'.format(form.login.data)))
        flash(_('Password: {}'.format(form.password.data)))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title=_('Register'),
                           form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title=_('Reset Password'), form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
