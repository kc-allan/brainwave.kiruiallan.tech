from flask import Blueprint

groups = Blueprint('groups', __name__, url_prefix='/groups')

from .views import *