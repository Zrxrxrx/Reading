from flask import Blueprint

rate_bp = Blueprint('rate', __name__)

from .rate import *
