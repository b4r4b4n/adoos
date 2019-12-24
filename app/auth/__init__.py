from flask import Blueprint  # создание чертежа для папки auth

bp = Blueprint('auth', __name__)

from app.auth import routes
