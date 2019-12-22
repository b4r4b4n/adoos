from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from flask_babel import _
from app.main.forms import EditProfileForm, PostForm, ComForm, EditPostForm, EditCom
from app.models import User, Post
from app.main import bp
from flask_paginate import Pagination, get_page_args
from datetime import datetime
from app.dbconn import conn

conn = conn()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        conn.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('main.index'))
    return render_template('index.html', title=_('Home'), form=form)


@bp.route('/edit_post/<id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    form = EditPostForm()
    cursor = conn.cursor()
    cursor.execute('select * from Uzer where login = %s',
                   [current_user.login])
    user = cursor.fetchone()
    cursor.execute('SELECT * FROM POST WHERE idpost = %s', [id])
    text = cursor.fetchone()
    conn.commit()
    #vremya = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if form.validate_on_submit():
        if user is None:
            return redirect(url_for('main.user', id=user[4]))
        else:
            cursor.execute('UPDATE POST SET tekst = %s WHERE idpost = %s', [form.editpost.data, id])
            conn.commit()
            return redirect(url_for('main.user', id=text[4]))
    elif request.method == 'GET':
        form.editpost.data = text[0]
    return render_template('edit_post.html', title=_('Редактирование') ,form=form)


@bp.route('/edit_com/<id>', methods=['GET', 'POST'])
@login_required
def edit_com(id):
    form = EditCom()
    cursor = conn.cursor()
    cursor.execute('select * from Uzer where login = %s',
                   [current_user.login])
    user = cursor.fetchone()
    cursor.execute('SELECT * FROM com WHERE idcom = %s', [id])
    text = cursor.fetchone()
    conn.commit()
    #vremya = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if form.validate_on_submit():
        if user is None:
            return redirect(url_for('main.user', id=user[4]))
        else:
            cursor.execute('UPDATE COM SET tekst = %s WHERE idcom = %s', [form.editcom.data,  id])
            conn.commit()
            return redirect(url_for('main.user', id=text[5]))
    elif request.method == 'GET':
        form.editcom.data = text[0]
    return render_template('edit_post.html', title=_('Редактирование') ,form=form)


@bp.route('/user/id<id>', methods=['GET', 'POST'])
@login_required
def user(id):
    cursor = conn.cursor()
    cursor.execute('select * from Uzer where iduser = %s',
                   [id])
    user = cursor.fetchone()
    conn.commit()
    if user is None:
        return redirect(url_for('main.index'))
    if current_user.id != user[4]:
        cursor.execute('select * from addfriend where id2user = %s and id1user = %s',
                       [current_user.id,user[4]])
        frend = cursor.fetchone()
        conn.commit()
        if frend is None:
            followed = False
        else:
            followed = True
    cursor.execute('select count(*) from addfriend where id1user = %s',
                   [user[4]])
    followers = cursor.fetchone()
    followers = int(followers[0])
    cursor.execute('select count(*) from addfriend where id2user = %s',
                   [user[4]])
    following = cursor.fetchone()
    following = int(following[0])
    conn.commit()
    form = PostForm()
    if form.validate_on_submit():
        vremya = datetime.now().strftime("%Y-%m-%d %X")
        if id == current_user.id:
            cursor.execute('INSERT INTO post(tekst,datapost,idavtor,idrecepient) VALUES (%s,%s,%s,%s)',
                           [form.post.data,vremya,current_user.id,current_user.id])
            conn.commit()
        else:
            cursor.execute('INSERT INTO post(tekst,datapost,idavtor,idrecepient) VALUES (%s,%s,%s,%s)',
                           [form.post.data, vremya, current_user.id, user[4]])
            conn.commit()
        return redirect(url_for('main.user', id=user[4]))
    cursor.execute(
        'SELECT * FROM POST inner join uzer on uzer.iduser = post.idavtor WHERE idrecepient = %s order by datapost DESC',
        [user[4]])
    posts = cursor.fetchall()
    conn.commit()
    cursor.execute(
        'SELECT * FROM POST inner join com on post.idpost=com.idpost inner join uzer on uzer.iduser = com.idavtor WHERE post.idrecepient = %s order by datacom ASC',
        [user[4]])
    coms = cursor.fetchall()
    conn.commit()
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    cursor.execute(
        'SELECT count(*) FROM POST WHERE idrecepient = %s',
        [user[4]])
    total = cursor.fetchone()
    conn.commit()
    pagination_posts = posts[offset: offset + per_page]
    pagination = Pagination(page=page, total=total[0], record_name='posts', css_framework='bootstrap4', per_page=10)
    return render_template('user.html', form=form, user=user, fio=user[0], logen=user[5], about_me=user[7], followed=followed,
                           following=following, followers=followers, posts=pagination_posts, avatar=user[8], coms=coms, id=user[4], pagination=pagination)


@bp.route('/user/<login>/popup')
@login_required
def user_popup(login):
    cursor = conn.cursor()
    cursor.execute('select * from Uzer where login = %s',
                   [login])
    user = cursor.fetchone()
    conn.commit()
    if user is None:
        flash(_('User %(username)s not found.', username=login))
        return redirect(url_for('main.index'))
    if current_user.id != user[4]:
        cursor.execute('select * from addfriend where id2user = %s and id1user = %s',
                       [current_user.id,user[4]])
        frend = cursor.fetchone()
        conn.commit()
        if frend is None:
            followed = False
        else:
            followed = True
    cursor.execute('select * from vo where iduser = %s',
                   [user[4]])
    vo = cursor.fetchone()
    conn.commit()
    if vo is not None:
        cursor.execute(
            'SELECT * FROM vo natural join kafedra natural join facultet natural join vuz where iduser = %s', [user[4]])
        vishobr = cursor.fetchone()
        conn.commit()
    else:
        return redirect(url_for('main.user', id=user[4]))
    cursor.execute('select count(*) from addfriend where id1user = %s',
                   [user[4]])
    followers = cursor.fetchone()
    followers = int(followers[0])
    cursor.execute('select count(*) from addfriend where id2user = %s',
                   [user[4]])
    following = cursor.fetchone()
    following = int(following[0])
    conn.commit()
    return render_template('user_popup.html', user=user, fio=user[0], logen=user[5], about_me=user[7], followed=followed,
                           following=following, followers=followers, avatar=user[8], phone=user[1], gender=user[2],
                           dr=user[3], vuz=vishobr[8], kafedra=vishobr[6], facultet=vishobr[7], iduser=user[4])


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.login)
    cursor = conn.cursor()
    vuz = form.SelVUZ.data
    cursor.execute('select idFack,nameFack from facultet where idvuz = %s', [vuz])
    fack = cursor.fetchall()
    conn.commit()
    kolvofack = len(fack)
    form.SelFack.choices = fack
    Fack = form.SelFack.data
    cursor.execute('select idKafedra,nameKafedra from kafedra where idfack = %s', [Fack])
    kaf = cursor.fetchall()
    conn.commit()
    form.SelKaf.choices = kaf
    Kaf = form.SelKaf.data
    if form.validate_on_submit():
        cursor = conn.cursor()
        current_user.fio = form.fio.data
        current_user.phone = form.phone.data
        current_user.gender = form.gender.data
        current_user.about_me = form.about_me.data
        current_user.avatar = form.avatar.data
        cursor.execute('update Uzer set fio = %s, login = %s, phone = %s, gender = %s, about_me = %s, avatar = %s where login = %s',
                       [current_user.fio,form.login.data,current_user.phone,current_user.gender,current_user.about_me,current_user.avatar,current_user.login])
        conn.commit()
        cursor.execute('SELECT iduser FROM VO WHERE iduser = %s', [current_user.id])
        iduser = cursor.fetchone()
        conn.commit()
        if iduser is None:
            cursor.execute('INSERT INTO VO(iduser,idvuz,idfack,idkafedra) VALUES(%s,%s,%s,%s)', [current_user.id,vuz,Fack,Kaf])
            conn.commit()
        else:
            cursor.execute('UPDATE VO SET idvuz = %s,idfack = %s, idkafedra = %s WHERE iduser = %s',
                           [vuz, Fack, Kaf,current_user.id])
            conn.commit()
        current_user.login = form.login.data
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.fio.data = current_user.fio
        form.login.data = current_user.login
        form.phone.data = current_user.phone
        form.gender.data = current_user.gender
        form.about_me.data = current_user.about_me
        form.avatar.data = current_user.avatar
        cursor.execute('SELECT idvuz from VO where iduser = %s', [current_user.id])
        nomervuza = cursor.fetchone()
        cursor.execute('SELECT idvuz from VUZ where idvuz = %s', [nomervuza])
        vuzik = cursor.fetchone()
        conn.commit()
        form.SelVUZ.default = [('2', 'Горный')]
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form, vuz=vuz, kolvofack=kolvofack, Kaf=Kaf, fack=fack)


@bp.route('/follow/<id>')
@login_required
def follow(id):
    cursor = conn.cursor()
    cursor.execute('select * from Uzer where iduser = %s',
                   [id])
    user = cursor.fetchone()
    conn.commit()
    if user is None:
        flash(_('User %(username)s not found.', username=user[5]))
        return redirect(url_for('main.index'))
    if current_user.login == user[5]:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('main.user', id=user[4]))
    cursor = conn.cursor()
    cursor.execute(
        'insert into addfriend (dataadd,id1user,id2user) values(clock_timestamp(),%s,%s)',
        (user[4], current_user.id))
    cursor.close()
    conn.commit()
    flash(_('You are following %(username)s!', username=user[5]))
    return redirect(url_for('main.user', id=user[4]))


@bp.route('/unfollow/<id>')
@login_required
def unfollow(id):
    cursor = conn.cursor()
    cursor.execute('select * from Uzer where iduser = %s',
                   [id])
    user = cursor.fetchone()
    conn.commit()
    if user is None:
        flash(_('User %(username)s not found.', username=user[5]))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('main.user', id=user[4]))
    cursor.execute(
        'DELETE FROM addfriend WHERE id2user = %s and id1user = %s',
        [current_user.id,user[4]])
    conn.commit()
    flash(_('You are not following %(username)s.', username=user[5]))
    return redirect(url_for('main.user', id=user[4]))


@bp.route('/deletepost/<id>')
@login_required
def deletepost(id):
    cursor = conn.cursor()
    cursor.execute('select * from Uzer where login = %s',
                   [current_user.login])
    user = cursor.fetchone()
    cursor.execute(
        'SELECT idrecepient from post where (idavtor = %s and idpost = %s) or (idrecepient = %s and idpost = %s)',
        [current_user.id, id, current_user.id, id])
    biba = cursor.fetchone()
    cursor.execute(
        'SELECT * from com where idpost = %s',
        [id])
    bibaboba = cursor.fetchone()
    conn.commit()
    if user[5] == current_user.login:
        if bibaboba is None:
            cursor.execute(
                'DELETE FROM post WHERE (idavtor = %s and idpost = %s) or (idrecepient = %s and idpost = %s)',
                [current_user.id, id, current_user.id, id])
            conn.commit()
        else:
            cursor.execute('DELETE FROM COM WHERE idpost=%s',[id])
            conn.commit()
            cursor.execute(
                'DELETE FROM post WHERE (idavtor = %s and idpost = %s) or (idrecepient = %s and idpost = %s)',
                [current_user.id, id, current_user.id, id])
            conn.commit()
        return redirect(url_for('main.user', id=biba[0]))
    return redirect(url_for('main.user', id=biba[0]))


@bp.route('/comment/<id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    cursor = conn.cursor()
    cursor.execute('select * from Uzer where login = %s',
                   [current_user.login])
    user = cursor.fetchone()
    cursor.execute('select idrecepient from post where idpost = %s',
                   [id])
    usten = cursor.fetchone()
    cursor.execute('select * from uzer where iduser = %s',
                   [usten])
    ust = cursor.fetchone()
    conn.commit()
    forma = ComForm()
    if forma.validate_on_submit():
        vremy = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if user is None:
            return redirect(url_for('main.index'))
        else:
            cursor.execute('INSERT INTO com(tekst,datacom,idavtor,idpost,idrecepient) VALUES (%s,%s,%s,%s,%s)',
                           [forma.com.data, vremy, current_user.id, id, ust[4]])
            conn.commit()
        return redirect(url_for('main.user', id=ust[4]))
    return render_template('sendcom.html', forma=forma)

@bp.route('/deletecom/<id>')
@login_required
def deletecom(id):
    cursor = conn.cursor()
    cursor.execute('select * from Uzer where login = %s',
                   [current_user.login])
    user = cursor.fetchone()
    cursor.execute(
        'SELECT idrecepient from com where (idavtor = %s and idcom = %s) or (idrecepient = %s and idcom = %s)',
        [current_user.id, id, current_user.id, id])
    biba = cursor.fetchone()
    conn.commit()
    if user[5] == current_user.login:
        cursor.execute(
            'DELETE FROM com WHERE (idavtor = %s and idcom = %s) or (idrecepient = %s and idcom = %s)',
            [current_user.id, id, current_user.id, id])
        conn.commit()
        cursor.close()
        return redirect(url_for('main.user', id=biba[0]))
    return redirect(url_for('main.user', id=biba[0]))


@bp.route('/following/<id>', methods=['GET', 'POST'])
@login_required
def folowww(id):
    cursor = conn.cursor()
    cursor.execute('select * from Uzer where iduser = %s',
                   [id])
    user = cursor.fetchone()
    cursor.execute(
        'SELECT * FROM addfriend inner join uzer on addfriend.id1user=uzer.iduser and addfriend.id2user = %s',
        [id])
    frendi = cursor.fetchall()
    conn.commit()
    friendempty = False
    if len(frendi) == 0:
        friendempty = True
    idfoll = id
    return render_template('unfoloww.html', title=_('Пiдписки'), frendi=frendi, friendempty=friendempty, idfoll=idfoll,
                           login=user[5], id=user[4])


@bp.route('/followers/<id>', methods=['GET', 'POST'])
@login_required
def foloww(id):
    cursor = conn.cursor()
    cursor.execute('select * from Uzer where iduser = %s',
                   [id])
    user = cursor.fetchone()
    cursor.execute(
        'SELECT * FROM addfriend inner join uzer on addfriend.id2user=uzer.iduser and addfriend.id1user = %s',
        [id])
    frendi = cursor.fetchall()
    conn.commit()
    friendempty = False
    if len(frendi) == 0:
        friendempty = True
    idfoll = id
    return render_template('foloww.html', title=_('Пiдписники'), frendi=frendi, friendempty=friendempty, idfoll=idfoll,
                           login=user[5], id=user[4])