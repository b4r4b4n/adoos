from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
import random
import re
from flask_babel import _
from app.main.forms import EditProfileForm, PostForm, ComForm, EditPostForm, EditCom
from app.models import User, Post
from app.main import bp
from flask_paginate import Pagination, get_page_args
from datetime import datetime
from app.dbconn import conn
from config import Config

conn = conn()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    cursor = conn.cursor()
    argg = request.args
    if argg and argg.get('page') is None:
        gender = argg.get('gender')
        category = argg.get('category')
        discount = argg.get('discount')
        minprice = argg.get('minprice')
        maxprice = argg.get('maxprice')
        brand = argg.get('brand')
        store = argg.get('store')
        if minprice > maxprice:
            buf = maxprice
            maxprice = minprice
            minprice = buf
        if gender:
            if gender == 'women':
                cursor.execute('SELECT * FROM ITEMS WHERE gender = %s or gender = %s', ['W','U'])
                genderY = cursor.fetchall()
            elif gender == 'men':
                cursor.execute('SELECT * FROM ITEMS WHERE gender = %s or gender = %s', ['M', 'U'])
                genderY = cursor.fetchall()
            elif gender == 'all':
                cursor.execute('SELECT * FROM ITEMS WHERE gender = %s', ['U'])
                genderY = cursor.fetchall()
    cursor.execute('select * from ITEMS')
    items = cursor.fetchall()
    ult = convert_to_list(items)
    conn.commit()
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    cursor.execute(
        'SELECT count(*) FROM ITEMS')
    total = cursor.fetchone()
    cursor.execute(
        'SELECT distinct(Brand) FROM ITEMS ORDER BY Brand ASC')
    brands = cursor.fetchall()
    cursor.execute(
        'SELECT distinct(site) FROM ITEMS ORDER BY site ASC')
    sites = cursor.fetchall()
    cursor.execute('SELECT MAX(saleprice) FROM ITEMS;')
    maxcost = cursor.fetchone()
    pagination_posts = ult[offset: offset + per_page]
    pagination = Pagination(page=page, total=total[0], record_name='items', per_page=per_page)
    chkindex = True
    return render_template('main.html', items=pagination_posts, pagination=pagination, paga=page, chkindex=chkindex, brands=brands, sites=sites, maxcost=maxcost)


@bp.route('/item/<id>', methods=['GET', 'POST'])
def item_fw(id):
    cursor = conn.cursor()
    cursor.execute('select * from ITEMS where id = %s',
                   [id])
    tkitem = cursor.fetchone()
    descr = re.sub(r'[\r]','',tkitem[12])
    description = [x for x in descr.strip().split('\n') if x]
    item = list(tkitem)
    item[10] = re.sub(r'[{}]', '', item[10]).split(',')
    full = [it.replace('737x737', '1474x1474') for it in item[10]]
    review = [it.replace('737x737', '120x120') for it in item[10]]
    conn.commit()
    cursor.execute('SELECT * FROM ITEMS WHERE TYPEITEM=%s AND NOT ID=%s', [item[9], id])
    types = cursor.fetchall()
    type = convert_to_list(types)
    cursor.execute('SELECT count(*) FROM ITEMS WHERE TYPEITEM=%s AND NOT ID=%s', [item[9], id])
    skilko = cursor.fetchone()
    if skilko[0] < 4:
        relateditems = type
    elif skilko[0] >= 4:
        relateditems = random.sample(type, 4)
    kolvo = len(item[10])
    return render_template('submainitem.html', title=item[5], item=item, kolvo=kolvo, review=review, full=full,
                           related=relateditems, description=description)



def convert_to_list(type):
    ult = [list(item) for item in type]
    for ul in ult:
        try:
            index = int(ult.index(ul))
            ult[index][10] = re.sub(r'[{}]', '', ul[10]).split(',')
        except:
            continue
    return ult


@bp.route('/shop/<gender>/<type>', methods=['GET', 'POST'])
def shopw(gender,type):
    cursor = conn.cursor()
    if gender == 'women':
        gend = 'W'
    elif gender == 'men':
        gend = 'M'
    if type:
        cursor.execute('select * from ITEMS WHERE (gender = %s or gender = %s) and typeitem = %s', ['U', gend, type])
    else:
        cursor.execute('select * from ITEMS WHERE gender = %s or gender = %s', ['U', gend])
    items = cursor.fetchall()
    ult = convert_to_list(items)
    conn.commit()
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    if type:
        cursor.execute(
            'SELECT count(*) FROM ITEMS WHERE (gender = %s or gender = %s) and typeitem = %s', ['U',gend,type])
    else:
        cursor.execute('select count(*) from ITEMS WHERE gender = %s or gender = %s', ['U', gend])
    total = cursor.fetchone()
    pagination_posts = ult[offset: offset + per_page]
    pagination = Pagination(page=page, total=total[0], record_name='items', per_page=per_page)
    return render_template('main.html', items=pagination_posts, pagination=pagination, paga=page)


@bp.route('/shop/<gender>', methods=['GET', 'POST'])
def shopg(gender):
    if gender == 'women':
        gend = 'W'
    elif gender == 'men':
        gend = 'M'
    cursor = conn.cursor()
    cursor.execute('select * from ITEMS WHERE gender = %s or gender = %s', ['U', gend])
    items = cursor.fetchall()
    ult = convert_to_list(items)
    conn.commit()
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    cursor.execute(
        'SELECT count(*) FROM ITEMS WHERE gender = %s or gender = %s', ['U', gend])
    total = cursor.fetchone()
    pagination_posts = ult[offset: offset + per_page]
    pagination = Pagination(page=page, total=total[0], record_name='items', per_page=per_page)
    return render_template('main.html', items=pagination_posts, pagination=pagination, paga=page)


@bp.route('/search', methods=['GET', 'POST'])
def search():
    arg = request.args['q']
    if arg == '':
        return redirect(url_for('main.index'))
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ITEMS WHERE to_tsvector(BRAND) || to_tsvector(nameitem) || to_tsvector(typeitem) @@ plainto_tsquery(%s)', [arg])
    items = cursor.fetchall()
    ult = convert_to_list(items)
    conn.commit()
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    cursor.execute(
        'SELECT count(*) FROM ITEMS WHERE to_tsvector(BRAND) || to_tsvector(nameitem) || to_tsvector(typeitem) @@ plainto_tsquery(%s)', [arg])
    total = cursor.fetchone()
    pagination_posts = ult[offset: offset + per_page]
    pagination = Pagination(page=page, total=total[0], record_name='items', per_page=per_page)
    checksrch = True
    return render_template('main.html', items=pagination_posts, pagination=pagination, paga=page, arg=arg, checksrch=checksrch )


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
        cursor.execute(
            'update Uzer set fio = %s, login = %s, phone = %s, gender = %s, about_me = %s, avatar = %s where login = %s',
            [current_user.fio, form.login.data, current_user.phone, current_user.gender, current_user.about_me,
             current_user.avatar, current_user.login])
        conn.commit()
        cursor.execute('SELECT iduser FROM VO WHERE iduser = %s', [current_user.id])
        iduser = cursor.fetchone()
        conn.commit()
        if iduser is None:
            cursor.execute('INSERT INTO VO(iduser,idvuz,idfack,idkafedra) VALUES(%s,%s,%s,%s)',
                           [current_user.id, vuz, Fack, Kaf])
            conn.commit()
        else:
            cursor.execute('UPDATE VO SET idvuz = %s,idfack = %s, idkafedra = %s WHERE iduser = %s',
                           [vuz, Fack, Kaf, current_user.id])
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
        cursor.execute('SELECT idvuz,idfack,idkafedra from VO where iduser = %s', [current_user.id])
        numb = cursor.fetchone()
        if numb is not None:
            form.SelVUZ.data = numb[0]
            form.SelFack.data = numb[1]
            form.SelKaf.data = numb[2]
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
        [current_user.id, user[4]])
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
    if user[5] == current_user.login:
        if current_user.login == 'tehno-09@mail.ru':
            cursor.execute(
                'SELECT idrecepient from post where idpost=%s',
                [id])
            biba = cursor.fetchone()
            conn.commit()
            cursor.execute(
                'SELECT * from com where idpost = %s',
                [id])
            bibaboba = cursor.fetchone()
            conn.commit()
            if bibaboba is None:
                cursor.execute(
                    'DELETE FROM post WHERE idpost=%s',
                    [id])
                conn.commit()
            else:
                cursor.execute('DELETE FROM COM WHERE idpost=%s', [id])
                conn.commit()
                cursor.execute(
                    'DELETE FROM post WHERE idpost = %s',
                    [id])
                conn.commit()
                cursor.close()
            return redirect(url_for('main.user', id=biba[0]))
        else:
            cursor.execute(
                'SELECT idrecepient from post where (idavtor = %s and idpost = %s) or (idrecepient = %s and idpost = %s)',
                [current_user.id, id, current_user.id, id])
            biba = cursor.fetchone()
            cursor.execute(
                'SELECT * from com where idpost = %s',
                [id])
            bibaboba = cursor.fetchone()
            conn.commit()
            if bibaboba is None:
                cursor.execute(
                    'DELETE FROM post WHERE (idavtor = %s and idpost = %s) or (idrecepient = %s and idpost = %s)',
                    [current_user.id, id, current_user.id, id])
                conn.commit()
            else:
                cursor.execute('DELETE FROM COM WHERE idpost=%s', [id])
                conn.commit()
                cursor.execute(
                    'DELETE FROM post WHERE (idavtor = %s and idpost = %s) or (idrecepient = %s and idpost = %s)',
                    [current_user.id, id, current_user.id, id])
                conn.commit()
            return redirect(url_for('main.user', id=biba[0]))
    return redirect(url_for('main.user', id=current_user.id))


@bp.route('/comment/<id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    cursor = conn.cursor()
    cursor.execute('select * from Uzer where login = %s',
                   [current_user.login])
    user = cursor.fetchone()
    cursor.execute('select idrecepient,idavtor from post where idpost = %s',
                   [id])
    usten = cursor.fetchone()
    conn.commit()
    forma = ComForm()
    if forma.validate_on_submit():
        vremy = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if user is None:
            return redirect(url_for('main.index'))
        else:
            cursor.execute(
                'INSERT INTO com(tekst,datacom,idavtor,idpost,idrecepient,idrecepientpost) VALUES (%s,%s,%s,%s,%s,%s)',
                [forma.com.data, vremy, current_user.id, id, usten[0], usten[1]])
            conn.commit()
        return redirect(url_for('main.user', id=usten[0]))
    return render_template('sendcom.html', forma=forma)


@bp.route('/deletecom/<id>')
@login_required
def deletecom(id):
    cursor = conn.cursor()
    cursor.execute('select * from Uzer where login = %s',
                   [current_user.login])
    user = cursor.fetchone()
    if user[5] == current_user.login:
        if current_user.login == 'tehno-09@mail.ru':
            cursor.execute(
                'SELECT idrecepient from com where idcom=%s',
                [id])
            biba = cursor.fetchone()
            conn.commit()
            cursor.execute(
                'DELETE FROM com WHERE idcom=%s',
                [id])
            conn.commit()
            cursor.close()
            return redirect(url_for('main.user', id=biba[0]))
        else:
            cursor.execute(
                'SELECT idrecepient from com where (idavtor = %s and idcom = %s) or (idrecepient = %s and idcom = %s)',
                [current_user.id, id, current_user.id, id])
            biba = cursor.fetchone()
            conn.commit()
            cursor.execute(
                'DELETE FROM com WHERE (idavtor = %s and idcom = %s) or (idrecepient = %s and idcom = %s)',
                [current_user.id, id, current_user.id, id])
            conn.commit()
            cursor.close()
            return redirect(url_for('main.user', id=biba[0]))
    return redirect(url_for('main.user', id=current_user.id))


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


@bp.route('/delete_profile/<id>')
@login_required
def delete_profile(id):
    cursor = conn.cursor()
    cursor.execute('select * from Uzer where login = %s',
                   [current_user.login])
    user = cursor.fetchone()
    conn.commit()
    if user[5] == current_user.login and current_user.login == 'tehno-09@mail.ru':
        cursor.execute(
            'DELETE FROM addfriend WHERE id1user = %s or id2user = %s',
            [id, id])
        conn.commit()
        cursor.execute(
            'DELETE FROM com WHERE idavtor = %s or idrecepient = %s or idrecepientpost =%s',
            [id, id, id])
        conn.commit()
        cursor.execute(
            'DELETE FROM post WHERE idavtor = %s or idrecepient = %s',
            [id, id])
        conn.commit()
        cursor.execute(
            'DELETE FROM vo WHERE iduser = %s',
            [id])
        conn.commit()
        cursor.execute(
            'DELETE FROM uzer WHERE iduser = %s',
            [id])
        conn.commit()
        return redirect(url_for('main.user', id=id))
    return redirect(url_for('main.user', id=current_user.id))
