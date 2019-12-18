import base64
from datetime import datetime, timedelta
from hashlib import md5
import json
import os
from time import time
from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import redis
import rq
from app import login
import psycopg2

conn = psycopg2.connect(dbname='postgres', user='postgres',
                        password='bibaboba', host='localhost',
                        port='5432')


class User(UserMixin):
    def __init__(self, fio, id, password_hash, phone, gender, dyennarodjenya, login, about_me,avatar):
        self.id = id
        self.fio = fio
        self.password_hash = password_hash
        self.phone = phone
        self.gender = gender
        self.dyennarodjenya = dyennarodjenya
        self.login = login
        self.about_me = about_me
        self.avatar = avatar

    def __repr__(self):
        return '<User {}>'.format(self.fio)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')


@login.user_loader
def load_user(iduser):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Uzer WHERE iduser = %s', [iduser])
    uuid = cursor.fetchone()
    user = User(id=iduser, fio=uuid[0], password_hash=uuid[6], phone=uuid[1], gender=uuid[2], dyennarodjenya=uuid[3],
                login=uuid[5], about_me=uuid[7], avatar=uuid[8])
    if user is not None:
        return user
    else:
        return None


class Post():
    __searchable__ = ['body']

    def __init__(self, tekst, datapost, idpost, idavtora, idrecepient, loginavtora):
        self.tekst = tekst
        self.datapost = datapost
        self.idpost = idpost
        self.idavtora = idavtora
        self.idrecepient = idrecepient
        self.loginavtora = loginavtora

    def __repr__(self):
        return '<Post {}>'.format(self.body)
