from flask import Blueprint

bp = Blueprint('satis', __name__)

from app.satis import routes