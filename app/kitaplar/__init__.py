from flask import Blueprint

bp = Blueprint('kitaplar', __name__)

from app.kitaplar import routes