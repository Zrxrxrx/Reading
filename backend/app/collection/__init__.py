from flask import Blueprint
collection_bp = Blueprint('collection', __name__)

from .collection import *
from .comment import *
from .read import *