from flask import Blueprint

files = Blueprint('files', __name__)

from .views import *