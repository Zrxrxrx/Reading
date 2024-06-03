from flask import Blueprint

user_bp = Blueprint('user', __name__)

from .profile import *
from .editPassword import *
from .collections import *
