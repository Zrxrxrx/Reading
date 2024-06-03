from flask import Blueprint
bookapi = Blueprint('book', __name__)

from .actions import *
from .review import *
from .recommend import *